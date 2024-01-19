from abc import ABC
from typing import Generator, Literal, Iterable, Optional, Iterator
import logging
from itertools import product
from functools import cached_property, lru_cache
from reprlib import repr
from collections import namedtuple

import pymc as pm
from Bio import SeqIO
import pandas as pd
from pandas.api.types import CategoricalDtype
import numpy as np
import xarray as xr
import arviz as az
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.model_selection import GroupKFold
from adjustText import adjust_text

from scipy import odr
from scipy.stats import pearsonr

"""
1 letter amino acid codes, sorted by biophysical property.
"""
aminoAcidsByProperty = (
    # Hydrophobic
    "W",
    "Y",
    "F",
    "M",
    "L",
    "I",
    "V",
    "A",
    # Special
    "P",
    "G",
    "C",
    # Polar uncharged
    "Q",
    "N",
    "T",
    "S",
    # Charged (-)
    "E",
    "D",
    # Charged (+)
    "H",
    "K",
    "R",
)

"""
1 letter amino acid codes, sorted alphabetically.
"""
aminoAcids = (
    "A",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "K",
    "L",
    "M",
    "N",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "V",
    "W",
    "Y",
)

"""
1 letter amino acid codes, sorted alphabetically, including a gap character.
"""
aminoAcidsAndGap = (
    "-",
    "A",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "K",
    "L",
    "M",
    "N",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "V",
    "W",
    "Y",
)


normal_lcdf = pm.distributions.dist_math.normal_lcdf
uncensored_censored_tuple = namedtuple(
    "UncensoredCensoredTuple", ("uncensored", "censored", "combined")
)
train_test_tuple = namedtuple("TrainTestTuple", ("train", "test"))


def string_to_series(string: str) -> pd.Series:
    """
    Expand characters in a string to individual items in a series.
    """
    return pd.Series(list(string))


def expand_sequences(series: pd.Series) -> pd.DataFrame:
    """
    Expand Series containing sequences into DataFrame.

    Notes:
        Any elements in series that cannot be expanded will be dropped.

    Args:
        series (pd.Series)

    Returns:
        pd.DataFrame: Columns are sequence positions, indexes match
            series.index.
    """
    df = series.apply(string_to_series)
    df.columns = list(range(df.shape[1]))
    df.columns += 1
    return df[df.notnull().all(axis=1)]


def df_from_fasta(path: str, positions: Optional[list[int]] = None) -> pd.DataFrame:
    """
    Read a fasta file.

    Args:
        path: Path to fasta file.
        positions: Optional 1-indexed list of positions to include.

    Returns:
        DataFrame. Indexes are record IDs in upper case, columns are positions.
    """
    with open(path, "r") as handle:
        data = {record.id: record.seq for record in SeqIO.parse(handle, "fasta")}

    df = pd.DataFrame.from_dict(data, orient="index")
    df.columns = list(range(1, df.shape[1] + 1))

    if positions is not None:
        df = df[list(positions)]

    return df


class AminoAcidPair(ABC):
    """
    Abstract base class for a pair of amino acids.
    """

    _known_amino_acids = set(aminoAcidsAndGap)

    def __init__(self, a: str, b: str) -> None:
        for item in a, b:
            if item not in self._known_amino_acids:
                raise ValueError(f"unrecognized amino acid: {item}")

    def __str__(self) -> str:
        return "".join(self.pair)

    def __eq__(self, other: "AminoAcidPair") -> bool:
        return self.pair == other.pair

    def __getitem__(self, item: int) -> str:
        return self.pair[item]

    def __hash__(self) -> int:
        return hash(self.pair)


@lru_cache
class SymmetricAminoAcidPair(AminoAcidPair):
    """
    A pair of amino acids. Symmetric means that it doesn't matter which order a and b are
    supplied in. I.e. NK == KN.
    """

    def __init__(self, a: str, b: str) -> None:
        super().__init__(a, b)
        self.pair = tuple(sorted((a, b)))

    def __repr__(self) -> str:
        return f"SymmetricAminoAcidPair({self.pair})"


@lru_cache
class AsymmetricAminoAcidPair(AminoAcidPair):
    """
    A pair of amino acids. Asymmetric means that the order of a and b matters, so NK !=
    KN.
    """

    def __init__(self, a: str, b: str) -> None:
        super().__init__(a, b)
        self.pair = a, b

    def __repr__(self) -> str:
        return f"AsymmetricAminoAcidPair({self.pair})"


class SeqDf:
    def __init__(self, df: pd.DataFrame) -> None:
        """
        DataFrame containing amino acid sequences.

        Args:
            df: Columns are amino acid positions, rows are antigens or sera, cells
                contain amino acids.
        """
        if unknown_aa := set(np.unique(df.values)) - set(aminoAcidsAndGap):
            raise ValueError(f"unrecognised amino acid(s): {', '.join(unknown_aa)}")

        self.df = df

        # Categorical DataFrame and codes
        self.df_cat = df.astype(CategoricalDtype(list(aminoAcidsAndGap), ordered=False))
        self.df_codes = pd.DataFrame(
            {position: self.df_cat[position].cat.codes for position in self.df_cat}
        )

    def __repr__(self) -> None:
        return "SeqDf(df=\n{})".format(repr(self.df))

    def __str__(self) -> None:
        return str(self.df)

    @classmethod
    def from_fasta(cls, path: str, positions: Optional[list[int]] = None) -> "SeqDf":
        """Make a SeqDf from a fasta file.

        Args:
            path: Path to fasta file.
            positions: Optional 1-indexed positions to include.

        Returns:
            SeqDf
        """
        return cls(df_from_fasta(path=path, positions=positions))

    @classmethod
    def from_series(cls, series: pd.Series) -> "SeqDf":
        """Make SeqDf from a series.

        Args:
            series (pd.Series): Each element in series is a string. See
                mapdeduce.helper.expand_sequences for more details.

        Returns:
            (SeqDf)
        """
        return cls(expand_sequences(series))

    def remove_invariant(self) -> "SeqDf":
        """
        Remove positions (columns) that contain only one amino acid.
        """
        mask = self.df.apply(lambda x: pd.unique(x).shape[0] > 1)
        n = (~mask).sum()
        logging.info(f"removed {n} invariant sequence positions")
        new = self.df.loc[:, self.df.columns[mask]]
        return SeqDf(new)

    def keep_positions(self, positions: list[int]) -> "SeqDf":
        """
        Keep only a subset of positions.
        """
        return SeqDf(self.df.loc[:, positions])

    def amino_acid_changes_sequence_pairs(
        self, sequence_pairs: Iterable[Iterable[str]], symmetric: bool
    ) -> set[AminoAcidPair]:
        """
        All amino acid changes that occur between sequence_pairs of sequences.

        Args:
            sequence_pairs: Pairs of sequence names.
            symmetric: If True, AB considered the same as BA. SymmetricAminoAcidPair
                instances are returned.
        """
        aa_idx = np.argwhere(self.amino_acid_matrix(sequence_pairs).values)
        Aa = SymmetricAminoAcidPair if symmetric else AsymmetricAminoAcidPair
        return set(Aa(aminoAcidsAndGap[i], aminoAcidsAndGap[j]) for i, j in aa_idx)

    def amino_acid_matrix(
        self,
        sequence_pairs: Iterable[tuple[str, str]],
        positions: Optional[list[int]] = None,
        names: tuple[str, str] = ("antigen", "serum"),
    ) -> pd.DataFrame:
        """
        Generate an amino acid matrix based on the given sequence pairs.

        Args:
            sequence_pairs (Iterable[tuple[str, str]]): A collection of sequence pairs,
                where each pair consists of an antigen sequence and a serum sequence.
            positions (Optional[list[int]], optional): A list of positions to consider in
                the matrix. If None, all positions in the sequence pairs will be
                considered. Defaults to None.
            names (tuple[str, str], optional): A tuple of names for the antigen and serum
                sequences. Defaults to ("antigen", "serum").

        Returns:
            pd.DataFrame: A DataFrame representing the amino acid matrix, where each row
            and column corresponds to an amino acid and the values indicate whether the
            amino acids at the corresponding positions in the sequence pairs are found in
            the data.
        """

        aa = np.full((21, 21), False)

        positions = list(self.df_codes) if positions is None else positions
        df_codes = self.df_codes[positions]

        for pair in sequence_pairs:
            if len(pair) != 2:
                raise ValueError(f"sequence_pairs must contain pairs, found: {pair}")

            idx = df_codes.loc[list(pair)].values
            # (2x faster not to call np.unique(idx))
            aa[idx[0], idx[1]] = True

        return pd.DataFrame(
            aa,
            index=pd.Index(aminoAcidsAndGap, name=f"{names[0]}_aa"),
            columns=pd.Index(aminoAcidsAndGap, name=f"{names[1]}_aa"),
        )

    def position_aa_combinations(
        self, symmetric_aa: bool, sequence_pairs: Iterator[tuple[str, str]]
    ) -> Generator[tuple[int, tuple[str, str]], None, None]:
        """
        Generate combinations of amino acid pairs for each position in the dataset.

        Args:
            symmetric_aa (bool): Flag indicating whether to use symmetric amino acid pairs.
            sequence_pairs (Iterator[tuple[str, str]]): Iterator of sequence pairs.

        Yields:
            tuple[int, tuple[str, str]]: A tuple containing the position and amino acid
            pair.
        """
        Aa = SymmetricAminoAcidPair if symmetric_aa else AsymmetricAminoAcidPair
        for position in self.df:
            aa_mat = self.amino_acid_matrix(
                sequence_pairs=sequence_pairs, positions=[position]
            )
            for a, b in self.amino_acid_matrix_to_pairs(aa_mat):
                yield position, str(Aa(a, b))

    @staticmethod
    def amino_acid_matrix_to_pairs(aa_mat: pd.DataFrame) -> Iterator[tuple[str, str]]:
        """
        Converts an amino acid matrix into pairs of amino acids.

        Args:
            aa_mat (pd.DataFrame): The amino acid matrix.

        Returns:
            Iterator[tuple[str, str]]: An iterator of pairs of amino acids.

        """
        row_aa_idx, col_aa_idx = np.where(aa_mat)
        return zip(aa_mat.index[row_aa_idx], aa_mat.index[col_aa_idx])


def plot_forest_sorted(
    data: az.InferenceData | xr.DataArray, var_name: str, dim: str = None, **kwds
):
    """
    Plot parameters of an inference data object sorted by their median value.

    Args:
        data: Any object that can be converted to arviz.InferenceData.
        var_name: The variable to plot.
        **kwds: Passed to arviz.plot_forest
    """
    post = az.extract(data)
    median = post[var_name].median(dim="sample")
    sorted_param = post[var_name].sortby(median)

    non_sample_dims = set(post[var_name].dims) - {"sample"}
    if len(non_sample_dims) == 1:
        (dim,) = non_sample_dims
    else:
        raise ValueError("multiple dims present, pass a dim for labelling")

    az.plot_forest(
        data,
        var_names=var_name,
        coords={dim: sorted_param[dim]},
        combined=True,
        **kwds,
    )


def plot_aa_matrix(
    idata: az.InferenceData,
    ax: Optional[mpl.axes.Axes] = None,
    force_upper_left: bool = False,
    vmin: float = -3.0,
    vmax: float = 3.0,
) -> tuple[mpl.axes.Axes, mpl.cm.ScalarMappable]:
    """
    Show the amino acid parameters as a matrix.

    Args:
        idata: Inference data containing b_aa variable.
        ax: Plot on this axes.
        force_upper_left: Push all the coloured squares in to the upper left corner of
            the plot. (Implementation note: this would happen by default if amino acids
            were sorted by their position in the aminoAcidsByProperty tuple, rather than
            alphabetically when amino acid pairs get defined in TiterRegression.aa_uniq.)
        v{min,max}: Set the boundary of the colormap.
    """
    aas = list(reversed(aminoAcidsByProperty))
    aas.append("-")

    post = az.extract(idata)
    b_aa_med = post["b_aa"].mean("sample").to_dataframe().squeeze()

    norm = mpl.colors.Normalize(vmin, vmax)
    mappable = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.RdBu)

    ax = plt.gca() if ax is None else ax

    seen = set()

    rect_kwds = dict(width=1.0, height=1.0, clip_on=False)

    for aa_pair, _b_aa in b_aa_med.items():
        j, i = aas.index(aa_pair[0]), aas.index(aa_pair[1])

        if force_upper_left:
            i, j = sorted((i, j))
            if (i, j) in seen:
                raise ValueError(
                    "forcing values in upper left would over write (maybe you are using "
                    "force_upper_left with asymmetric amino acids)"
                )

        congruence = j == i
        ax.add_artist(
            mpl.patches.Rectangle(
                (i, j),
                facecolor=mpl.cm.RdBu(norm(_b_aa)),
                lw=0.5 if congruence else 0,
                zorder=15 if congruence else 10,
                edgecolor="black",
                **rect_kwds,
            )
        )
        seen.add((i, j))

    for ij in product(range(len(aas)), range(len(aas))):
        if ij not in seen:
            ax.add_artist(
                mpl.patches.Rectangle(ij, facecolor="lightgrey", zorder=5, **rect_kwds)
            )

    lim = 0, len(aas)
    ticks = np.arange(0.5, len(aas) + 0.5)
    ax.set(
        xlim=lim,
        ylim=lim,
        aspect=1,
        xticks=ticks,
        yticks=ticks,
        xticklabels=aas,
        yticklabels=aas,
    )
    ax.grid(False, "major", "both")

    kwds = dict(c="white", zorder=12)
    for x in 3, 5, 9, 12, 17, 20:
        ax.axvline(x, **kwds)
        ax.axhline(x, **kwds)

    return ax, mappable


class CrossValidationFoldResult:
    def __init__(
        self,
        idata: az.InferenceData,
        y_true: np.ndarray,
        train: uncensored_censored_tuple,
        test: uncensored_censored_tuple,
    ) -> None:
        """
        The results of a single train/test cross validation fold.

        Args:
            idata: The inference data object. Should have a `posterior_predictive`
                attribute.
            y_true: Measured responses of the test set.
            train: Tuple of masks used to define training data.
            test: Tuple of masks used to define testing data.
        """
        self.idata = idata
        self.y_pred = (
            idata.posterior_predictive["obs_u"].mean(dim="draw").mean(dim="chain")
        )
        self.y_true = y_true
        self.err = (self.y_pred - self.y_true).values
        self.err_abs = np.absolute(self.err)
        self.err_sqr = self.err**2
        self.mean_err_sqr = np.mean(self.err_sqr)
        self.mean_err_abs = np.mean(self.err_abs)
        self.train = train
        self.test = test

    def __repr__(self) -> str:
        return f"CrossValidationFoldResult({self.idata})"

    def __str__(self) -> str:
        return (
            f"mean squared error: {self.mean_err_sqr}\n"
            f"mean absolute error: {self.mean_err_abs}"
        )

    def plot_predicted_titers(
        self, ax=None, jitter: float = 0.2, ylabel: str = "Predicted log titer"
    ) -> None:
        """
        Plot predicted vs true log titer values.

        Args:
            ax: Matplotlib ax.
            jitter: Size of jitter to add to x-axis values.
            ylabel: Y-axis label.
        """
        ax = plt.gca() if ax is None else ax
        jitter = np.random.uniform(-jitter / 2, jitter / 2, len(self.y_true))
        ax.scatter(
            self.y_true + jitter,
            self.y_pred,
            lw=0.5,
            clip_on=False,
            s=15,
            edgecolor="white",
        )
        ax.set(
            aspect=1,
            xlabel="True log titer",
            ylabel=ylabel,
            xticks=np.arange(0, 10, 2),
            yticks=np.arange(0, 10, 2),
        )
        ax.axline((0, 0), slope=1, c="lightgrey", zorder=0)


class CrossValidationResults:
    def __init__(self, results: Iterable[CrossValidationFoldResult]) -> None:
        self.results = tuple(results)

    @property
    def df_error(self) -> pd.DataFrame:
        """
        DataFrame containing absolute error, squared error, raw error for each predicted
        titer in each fold.
        """
        return pd.concat(
            [
                pd.DataFrame(
                    {
                        "absolute_error": self.results[i].err_abs,
                        "squared_error": self.results[i].err_sqr,
                        "raw_error": self.results[i].err,
                    }
                ).assign(fold=i)
                for i in range(len(self.results))
            ]
        )

    def plot_predicted_titers(
        self, figsize: tuple[float, float] = (15.0, 10.0)
    ) -> np.ndarray:
        _, axes = plt.subplots(
            ncols=len(self.results), sharex=True, sharey=True, figsize=figsize
        )
        for result, ax in zip(self.results, axes):
            result.plot_predicted_titers(ax=ax, ylabel="Predicted log titer")
            ax.text(
                0,
                1,
                f"Mean abs. err={result.mean_err_abs:.2f}",
                transform=ax.transAxes,
                va="top",
                fontsize=8,
            )
            ax.label_outer()
        return axes


class TiterRegression:
    def __init__(
        self,
        sequences: pd.DataFrame | SeqDf,
        titers: pd.Series,
        constrain_aa_effects: bool,
        symmetric_aas: bool,
        covariates: Optional[pd.DataFrame] = None,
    ) -> None:
        """
        A class that holds data and constructs a Bayesian model for conducting a titer
        regression.

        Args:
            sequences: DataFrame containing sequences for all antigens and sera. Columns
                are sequence positions, rows are names of antigens and sera. The
                'sequence' of a serum is the sequence of the antigen used to raise that
                serum.
            titers: Series that has a multilevel index of (antigen, serum) and values are
                titers.
            constrain_aa_effects: Force the effects of substitutions to be negative and
                congruences to be positive. A substitution is an amino acid pair where
                the amino acids do not match (e.g. "NK" and "HS"). A congruence is a pair
                where the amino acids do match (e.g. "NN", "SS").
            symmetric_aas: If False, then estimate separate effects for "NK" and "KN".
            covariates: Optional DataFrame containing additional covariates to include in
                the regression for each (antigen, serum) pair. Rows correspond to
                (antigen, serum) pairs. Columns contain the covariates. Must be the same
                length as titers and have an identical index.

        Attributes:
            n_titers: (int) number of titrations, (i.e. 'pairs' of antigens and sera).
            n_positions: (int) number of positions to estimate effects for. Only
                positions that are variable in `sequences` are considered.
            titers: (n_titers,) pd.Series of the raw titer values. Multilevel index of
                (antigen, serum).
            Y: (n_titers,) array of log2(titer/10) titer values. <10 is represented as -1,
                although threshold values are handled by the model as < 0 on the log
                scale.
            aa_uniq: tuple[str] of all unique pairs of amino acids (including pairs where
                the amino acids match such as 'NN') between sera and antigens in sequences.
            aa: (n_titers, n_pos) array containing the index of the substitution for this
                serum-antigen combination at this position.
            ags,srs: (n_titers,) pd.Categorical of the antigens or sera used in each
                titration.
            c: (n_titers,) boolean array. True in this array means the titer is 'censored'
                (i.e. thresholded).
            n: (n_titers,) boolean array. False corresponds to regular/numeric titers.
        """
        self.constrain_aa_effects = constrain_aa_effects
        self.symmetric_aas = symmetric_aas

        self.seqdf = (
            sequences.remove_invariant()
            if isinstance(sequences, SeqDf)
            else SeqDf(sequences).remove_invariant()
        )

        self.titers = pd.Series(titers, dtype=str)

        # Check have all sequences for antigens and sera in titers
        antigens = self.titers.index.get_level_values("antigen")
        sera = self.titers.index.get_level_values("serum")
        for virus in list(antigens) + list(sera):
            if virus not in self.seqdf.df.index:
                raise ValueError(f"{virus} not in sequences")

        self.Y = np.array([Titer(t).log_value for t in self.titers])

        # Titer table contains <10 and <20 values
        self.c = self.titers.str.contains("<").values  # 'c'ensored
        self.u = ~self.c  # 'u'ncensored

        # all amino acid changes in the alignment
        self.aa_uniq = tuple(
            sorted(
                str(aa)
                for aa in self.seqdf.amino_acid_changes_sequence_pairs(
                    self.titers.index, symmetric=symmetric_aas
                )
            )
        )

        # List where 0 indicates a substitution and 1 indicates a congruence
        self.aa_sign = np.array(
            [-1.0 if aa[0] != aa[1] else 1.0 for aa in self.aa_uniq]
        )

        # aa will be an array that for each pair at each position indexes into the aa
        # parameter vector
        self.n_titers = self.titers.shape[0]
        self.n_positions = self.seqdf.df.shape[1]

        self.aa = np.empty((self.n_titers, self.n_positions), dtype=np.int32)
        for i, (ag, sr) in enumerate(self.titers.index):
            if not symmetric_aas:
                aa_pairs = self.seqdf.df.loc[[ag, sr]].apply("".join)
            else:
                aa_pairs = self.seqdf.df.loc[[ag, sr]].apply(sorted).apply("".join)

            for j, aa_pair in enumerate(aa_pairs):
                try:
                    self.aa[i, j] = self.aa_uniq.index(aa_pair)
                except ValueError as err:
                    print(aa_pair)
                    raise err

        # Keep track of the order of antigens and sera
        self.ags, self.srs = [
            pd.Categorical(self.titers.index.get_level_values(level))
            for level in ("antigen", "serum")
        ]

        # Covariates
        if covariates is not None:
            if len(self.titers) != len(covariates):
                raise ValueError("covariates and titers have different length")

            if not (self.titers.index == covariates.index).all():
                raise ValueError("covariates and titers must have identical indexes")
            else:
                self.covs = covariates.values
                self.cov_names = list(covariates.columns)
        else:
            self.covs = None

    def __repr__(self):
        return (
            f"TiterRegression(sequences={self.seqdf}, titers={self.titers}, "
            f"constrain_aa_effects={self.constrain_aa_effects} ",
            f"symmetric_aas={self.symmetric_aas} ",
            f"covariates={self.covs})",
        )

    @classmethod
    def from_chart(cls, chart: "maps.Chart", positions: list[int]) -> "TiterRegression":
        """
        Make a TiterRegresion instance from a maps.Chart object.

        Args:
            chart:
            positions: Only include these positions in the regression.
        """
        ag_seqs = {ag.name: list(ag.sequence) for ag in chart.antigens}
        sr_seqs = {sr.name: list(sr.sequence) for sr in chart.sera}

        df_seq = pd.DataFrame.from_dict({**ag_seqs, **sr_seqs}, orient="index")
        df_seq.columns += 1

        df_seq = df_seq[positions]

        return cls(sequences=df_seq, titers=chart.table_long)

    @property
    def coords(self) -> dict[str, Iterable[str | int]]:
        """
        Model coordinates.
        """
        coords = {
            "aa": self.aa_uniq,
            "pos": self.seqdf.df.columns,
            "ag": self.ags.categories,
            "sr": self.srs.categories,
        }

        if self.covs is not None:
            coords["covs"] = self.cov_names

        return coords

    def compute_titer(
        self,
        b_pos: "pytensor.tensor.TensorVariable",
        b_aa: "pytensor.tensor.TensorVariable",
        b_ag: "pytensor.tensor.TensorVariable",
        b_sr: "pytensor.tensor.TensorVariable",
        b_cov: "pytensor.tensor.TensorVariable",
        b_const: "pytensor.tensor.TensorVariable",
        suffix: Literal["u", "c"],
        mask: Optional[np.ndarray] = None,
    ):
        """
        Compute titers.

        Args:
            suffix: "u" uncensored, or "c" censored titers.
            mask: (n_titers,) boolean array. Include only these antigen-serum pairs.
        """
        if mask is None:
            mask = np.repeat(True, self.n_titers)

        aa = pm.MutableData(f"aa_{suffix}", self.aa[mask])
        ags = pm.MutableData(f"ags_{suffix}", self.ags.codes[mask])
        srs = pm.MutableData(f"srs_{suffix}", self.srs.codes[mask])

        if self.covs is None:
            return b_aa[aa] @ b_pos + b_ag[ags] + b_sr[srs] + b_const

        else:
            covs = pm.MutableData(f"covs_{suffix}", self.covs[mask])
            return b_aa[aa] @ b_pos + b_ag[ags] + b_sr[srs] + covs @ b_cov + b_const

    def make_variables(self) -> dict[str, "pytensor.tensor.TensorVariable"]:
        # Positions
        # 0-1 values that 'turn on/off' the effect of amino acid pairs
        b_pos_raw = noncentered_normal(
            "b_pos_raw", hyper_mu=-2.0, hyper_sigma=1.0, dims="pos"
        )
        b_pos = pm.Deterministic("b_pos", pm.math.invlogit(b_pos_raw), dims="pos")

        # Amino acids
        if self.constrain_aa_effects:
            # Positive effects for congruences
            # Negative effects for substitutions
            raw_b_aa = noncentered_normal("_raw_b_aa", dims="aa", lognormal=True)
            b_aa = pm.Deterministic("b_aa", self.aa_sign * raw_b_aa, dims="aa")
        else:
            b_aa = noncentered_normal("b_aa", dims="aa")

        # Per-antigen / per-serum effects
        b_ag = noncentered_normal("b_ag", dims="ag")
        b_sr = noncentered_normal("b_sr", dims="sr")

        # Covariates
        b_cov = (
            pm.Normal("b_cov", 0.0, 1.0, dims="covs") if self.covs is not None else None
        )

        # Intercept and error
        b_const = pm.Normal("b_const", 0.0, 1.0)

        return dict(
            b_pos=b_pos,
            b_aa=b_aa,
            b_ag=b_ag,
            b_sr=b_sr,
            b_cov=b_cov,
            b_const=b_const,
        )

    @cached_property
    def model(self) -> pm.Model:
        with pm.Model(coords=self.coords) as model:
            variables = self.make_variables()
            sigma = pm.Exponential("sd", 1.0)

            # Censored data (less than titers)
            Y_c = pm.MutableData("Y_c", self.Y[self.c])
            mu_c = self.compute_titer(suffix="c", mask=self.c, **variables)

            # using pm.Censored here causes loss to be nan when calling pm.fit
            pm.Potential("obs_c", normal_lcdf(mu=mu_c, sigma=sigma, x=Y_c))

            # Uncensored data (numeric titers)
            Y_u = pm.MutableData("Y_u", self.Y[self.u])
            mu_u = self.compute_titer(suffix="u", mask=self.u, **variables)
            pm.Normal("obs_u", mu=mu_u, sigma=sigma, observed=Y_u)

        return model

    @cached_property
    def uncensored_model(self) -> pm.Model:
        """
        Treat all data as uncensored.

        This was implemented in order to generate a posterior preditive for the censored
        data. For censored data the posterior predictive is computed as if the data
        were uncensored. I.e., it's only the likelihood (that uses the censored response)
        that requires special handling.
        """
        with pm.Model(coords=self.coords) as model:
            variables = self.make_variables()
            sigma = pm.Exponential("sd", 1)
            mu = self.compute_titer(suffix="u", mask=None, **variables)
            Y_u = pm.MutableData("Y_u", self.Y)
            pm.Normal("obs_u", mu=mu, sigma=sigma, observed=Y_u)

        return model

    def set_data(self, mask: np.ndarray, suffix: Literal["u", "c"]) -> None:
        """
        Set data in a pymc model context.

        Args:
            mask: (n_titers,) boolean array with True for titers to include.
            suffix: "u" for uncensored data or "c" for censored data.
        """
        data = {
            f"aa_{suffix}": self.aa[mask],
            f"ags_{suffix}": self.ags.codes[mask],
            f"srs_{suffix}": self.srs.codes[mask],
            f"Y_{suffix}": self.Y[mask],
        }

        if self.covs is not None:
            data[f"covs_{suffix}"] = self.covs[mask]

        pm.set_data(data)

    @staticmethod
    def data_shape(model: pm.Model) -> dict[str, tuple]:
        """The shape of data currently set on the model."""
        shapes = {}
        for suffix in "u", "c":
            for variable in "aa", "ags", "srs", "Y":
                key = f"{variable}_{suffix}"
                try:
                    shapes[key] = model[key].eval().shape
                except KeyError:
                    continue
        return shapes

    @staticmethod
    def log_data_shape(model: pm.Model) -> None:
        """Report the shape of data currently set on a model."""
        logging.info(f"current data shapes: {TiterRegression.data_shape(model)}")

    def fit(self, netcdf_path: Optional[str] = None, **kwds) -> az.InferenceData:
        """
        Fit the model using variational inference.

        Args:
            netcdf_path: Path to save inference data NetCDF object. Attempt to load a
                file with this name before sampling.
            **kwds: Passed to pymc.fit
        """
        try:
            return az.from_netcdf(netcdf_path)
        except (FileNotFoundError, TypeError):
            with self.model:
                callbacks = [
                    pm.callbacks.CheckParametersConvergence(
                        diff="absolute", tolerance=0.01
                    )
                ]
                mean_field = pm.fit(
                    n=kwds.pop("n", 100_000), callbacks=callbacks, **kwds
                )

            idata = mean_field.sample(1_000)
            idata.attrs["mean_field_hist"] = mean_field.hist
            if netcdf_path is not None:
                az.to_netcdf(idata, netcdf_path)
            return idata

    def sample(self, netcdf_path: Optional[str] = None, **kwds) -> az.InferenceData:
        """
        Sample from the model posterior.

        Args:
            netcdf_path: Path to save inference data NetCDF object. Attempt to load a
                file with this name before sampling.
            **kwds: Passed to pymc.sample.
        """
        try:
            return az.from_netcdf(netcdf_path)
        except (FileNotFoundError, TypeError):
            with self.model:
                idata = pm.sample(**kwds)
            if netcdf_path is not None:
                az.to_netcdf(idata, netcdf_path)
            return idata

    def grouped_cross_validation(
        self,
        n_splits: int,
        variational_inference: bool = False,
        netcdf_prefix: Optional[str] = None,
        vi_kwds: Optional[dict] = None,
        sample_kwds: Optional[dict] = None,
    ) -> Generator[CrossValidationFoldResult, None, None]:
        """
        Run cross validation.

        Args:
            n_splits: Number of train/test folds to generate.
            variational_inference: Fit using variational inference rather than sampling
                from a posterior.
            netcdf_prefix: Save an InferenceData object for each fold to disk with this
                prefix. Prefixes have "-fold{i}.nc" appended where 'i' indexes the fold.
                If files already exist then load them instead of sampling.
            vi_kwds: Keyword arguments passed to pymc.fit if variational inference is
                being used.
            sample_kwds: Keyword arguments passed to pymc.sample if variational inference
                is not being used.
        """
        folds = self.grouped_train_test_sets(n_splits=n_splits)

        vi_kwds = {} if vi_kwds is None else vi_kwds
        sample_kwds = {} if sample_kwds is None else sample_kwds

        for i, (train, test) in enumerate(folds):
            netcdf_path = f"{netcdf_prefix}-fold{i}.nc"
            with self.model:
                logging.info(
                    "setting training data "
                    f"#uncensored={sum(train.uncensored)} "
                    f"#censored={sum(train.censored)}"
                )
                self.set_data(train.censored, suffix="c")
                self.set_data(train.uncensored, suffix="u")
                TiterRegression.log_data_shape(self.model)
                idata = (
                    self.fit(netcdf_path=netcdf_path, **vi_kwds)
                    if variational_inference
                    else self.sample(netcdf_path=netcdf_path, **sample_kwds)
                )

            # Generate posterior predictive samples on the test data
            with self.uncensored_model:
                logging.info(
                    "setting testing data (all test data treated as uncensored) "
                    f"#combined={sum(test.combined)} "
                )
                # self.set_data(np.zeros_like(test.combined, dtype=bool), suffix="c")
                self.set_data(test.combined, suffix="u")
                TiterRegression.log_data_shape(self.uncensored_model)
                idata.extend(pm.sample_posterior_predictive(idata, progressbar=False))

            yield CrossValidationFoldResult(
                idata, y_true=self.Y[test.combined], train=train, test=test
            )

    def make_train_test_sets(
        self, random_seed: int, test_proportion: float = 0.1
    ) -> None:
        """
        Attach boolean arrays to self that define train and test sets for censored and
        uncensored data.

        Args:
            random_seed:
            test_proportion: Proportion of titers used for the test set.

        Attributes:
            mask_test,mask_train: Boolean ndarrays. All titers are either in mask_test or
                mask_train.
            mask_train_c,mask_train_u: Boolean ndarrays. Censored (c) and uncensored (u)
                titers for the training set. All titers in the training set are in one of
                these arrays.
            mask_test_c,mask_test_u: Boolean ndarrays. Censored (c) and uncensored (u)
                titers for the test set. All titers in the test set are in one of these
                arrays.
        """
        if not 0 < test_proportion < 1:
            raise ValueError("test_proportion should be between 0-1.")

        np.random.seed(random_seed)

        n_test = int(np.round(test_proportion * self.n_titers))
        idx_test = np.random.choice(
            np.arange(self.n_titers), replace=False, size=n_test
        )
        self.mask_test = np.repeat(False, self.n_titers)
        self.mask_test[idx_test] = True
        self.mask_train = ~self.mask_test

        self.mask_train_u, self.mask_train_c, *_ = self.make_censored_uncensored_masks(
            self.mask_train
        )

        self.mask_test_u, self.mask_test_c, *_ = self.make_censored_uncensored_masks(
            self.mask_test
        )

    def grouped_train_test_sets(
        self, n_splits: int
    ) -> Generator[
        train_test_tuple[uncensored_censored_tuple, uncensored_censored_tuple],
        None,
        None,
    ]:
        """
        Generate train and test sets of uncensored and censored arrays. The titers are
        grouped by the serum/antigen pair used such that all titers from a single
        serum/antigen pair will appear in the same train or test split. I.e. testing will
        never involve testing a titer that has also appeared in the training set.

        Arrays are boolean masks the same length as the number of titers in the dataset.

        sklearn.model_selection.GroupKFold is used which is deterministic and therefore
        does not require setting a random seed to generate repeatable folds.

        Args:
            n_splits: Number of folds.

        Returns:
            4-tuple containing masks of:
                - uncensored training
                - censored training
                - uncensored testing
                - censored testing
        """
        gkf = GroupKFold(n_splits=n_splits)
        for train, test in gkf.split(range(self.n_titers), groups=self.titers.index):
            mask_train = self.indexes_to_mask(train)
            mask_test = self.indexes_to_mask(test)
            yield train_test_tuple(
                train=self.make_censored_uncensored_masks(mask_train),
                test=self.make_censored_uncensored_masks(mask_test),
            )

    def make_censored_uncensored_masks(
        self, mask: np.ndarray
    ) -> uncensored_censored_tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Given a boolean mask return the same mask but decomposed into censored and
        uncensored titers.

        Args:
            mask: 1D array containing True and False.

        Returns:
            3-tuple of boolean masks:
                - uncensored
                - censored
                - combination (the logical 'or' of censored and uncensored, also equal to
                  the input mask)
        """
        if len(mask) != self.n_titers:
            raise ValueError(
                f"mask length different to n. titers ({len(mask)} vs {self.n_titers})"
            )
        if any(set(mask) - {True, False}):
            raise ValueError("mask must only contain True and False")
        if mask.ndim != 1:
            raise ValueError("mask must be 1D")

        uncensored = np.logical_and(self.u, mask)
        censored = np.logical_and(self.c, mask)
        combined = np.logical_or(uncensored, censored)

        assert all(combined == mask)

        return uncensored_censored_tuple(
            uncensored=uncensored, censored=censored, combined=combined
        )

    def indexes_to_mask(self, indexes: np.ndarray) -> np.ndarray:
        """
        Convert an array containing integer indexes to boolean masks.

        If indexes contains [2, 4, 6] and there are 9 titers in the dataset, this would
        return: [False, False, True, False, True, False, True, False, False, False].

        Args:
            indexes: Array of integers.
        """
        mask = np.full(self.n_titers, False)
        mask[indexes] = True
        return mask

    def combined_position_aa_effects(self, idata: az.InferenceData) -> xr.DataArray:
        """
        DataArray containing all amino acid x position effects. Amino acid effects just
        report the effects of an amino acid pair (e.g. 'NK'). Position effects just
        report the effects of a position (e.g. 145). This array contains the product of
        amino acid and position effects (e.g. 'NK145') for all combinations of amino
        acids found at positions in the dataset.

        Args:
            idata: InferenceData object containing posterior samples. (Must contain
                b_aa and b_pos with 'aa' and 'pos' coords.)
        """
        pos_aa_combined = sorted(
            set(
                self.seqdf.position_aa_combinations(
                    symmetric_aa=self.symmetric_aas, sequence_pairs=self.titers.index
                )
            )
        )
        positions, aa_pairs = zip(*pos_aa_combined)
        b_pos = idata.posterior.sel(pos=list(positions))["b_pos"]
        b_aa = idata.posterior.sel(aa=list(aa_pairs))["b_aa"]

        if b_pos.dims[:-1] != b_aa.dims[:-1]:
            raise ValueError("b_pos and b_aa have different leading dims")

        return xr.DataArray(
            b_pos.values * b_aa.values,
            dims=(*b_pos.dims[:-1], "aa_pos"),
            name="b_aa_pos",
            coords=dict(
                aa_pos=[
                    f"{aa}{pos}"
                    for aa, pos in zip(b_aa.indexes["aa"], b_pos.indexes["pos"])
                ]
            ),
        )


def geom_mean(a, b):
    """The geometric mean of a and b."""
    return np.sqrt(a * b)


def noncentered_normal(
    name: str,
    dims: str,
    hyper_mu: float = 0.0,
    hyper_sigma: float = 0.5,
    hyper_lam: float = 2.0,
    lognormal: bool = False,
) -> "pytensor.tensor.TensorVariable":
    """
    Non-center parameterised hierarchical normal distribution. Equivalent to:

        mu = Normal(`name`_mu, hyper_mu, hyper_sigma)
        sigma = Exponential(`name`_sigma, hyper_lam)
        Normal(name, mu, sigma, dims=dims)

    Args:
        name: Variable name.
        dims: Dimensions of the model for the variable.
        hyper_{mu,sigma,lam}: Hyperpriors.
        lognormal: Make this a lognormal variable.
    """
    mu = pm.Normal(f"{name}_mu", mu=hyper_mu, sigma=hyper_sigma)
    sigma = pm.Exponential(f"{name}_sd", lam=hyper_lam)
    z = pm.Normal(f"_{name}_z", mu=0.0, sigma=1.0, dims=dims)
    return (
        pm.Deterministic(name, np.exp(z * sigma + mu), dims=dims)
        if lognormal
        else pm.Deterministic(name, z * sigma + mu, dims=dims)
    )


class Titer:
    """
    A titer from a 2-fold dilution series using a 1:10 starting dilution.
    """

    def __init__(self, titer):
        self.titer = str(titer).replace(" ", "")
        if self.titer[0] == ">":
            raise NotImplementedError("gt titers not implemented")
        self.is_threshold = self.titer[0] == "<"
        self.is_inbetween = "/" in self.titer

    def __str__(self) -> str:
        return self.titer

    @property
    def log_value(self) -> float:
        if self.is_inbetween:
            a, b = self.titer.split("/")
            return (Titer(a).log_value + Titer(b).log_value) / 2
        elif self.is_threshold:
            return Titer(self.titer[1:]).log_value - 1
        else:
            return np.log2(float(self.titer) / 10)


def aa_pairs_with_reversed(aa_pairs: Iterable[str]) -> set[tuple[str, str]]:
    """
    Select pairs of amino acid pairs where the reversed amino acid pair is also
    present. In this example "AN" is returned, with "NA" because both "AN" and "NA" are
    in the input:

    >>> aa_pairs_with_reversed(["QR", "AN", "TS", "ST", "KN", "NA"])
    {("AN", "NA"), ("ST", "TS")}

    Args:
        aa_pairs: Amino acid pairs.
    """
    return set(
        tuple(sorted((pair, f"{pair[1]}{pair[0]}")))
        for pair in aa_pairs
        if f"{pair[1]}{pair[0]}" in aa_pairs and pair[0] != pair[1]
    )


def plot_reversed_amino_acid_effects_scatter(
    idata: az.InferenceData,
    ax: Optional[mpl.axes.Axes] = None,
    label_threshold: float = 1.0,
    text_kwds: Optional[dict] = None,
) -> mpl.axes.Axes:
    """
    Plot the effects of amino acid pairs and their reverse. E.g. the effect of "NK" and
    "KN" are plotted as a single point where the x-axis value represents the "KN" value
    and the y-axis value is the "NK" value.

    The regression line that is plotted is an orthogonal least squares fit (Deming
    regression). The parameters that are reported are the slope and intercept of this
    model (m and c), an a Pearson correlation coefficient (r), and p-value.

    Args:
        idata: Inference data object.
        ax: Matplotlib ax.
        label_threshold: Label amino acid pairs whose absolute difference in x and y
            values is greater than this value.
    """
    text_kwds = dict() if text_kwds is None else text_kwds
    ax = plt.gca() if ax is None else ax
    post = az.extract(idata)
    hdi = az.hdi(idata)

    kwds = dict(c="black")
    line_kwds = dict(alpha=0.5, linewidth=0.35)

    pairs_of_pairs = aa_pairs_with_reversed(post.coords["aa"].values)

    xy = np.array(
        [
            post["b_aa"].sel(aa=[pair_a, pair_b]).mean(dim="sample").values
            for pair_a, pair_b in pairs_of_pairs
        ]
    )

    labels = []
    for i, (pair_a, pair_b) in enumerate(pairs_of_pairs):
        x, y = xy[i]
        x_hdi, y_hdi = hdi["b_aa"].sel(aa=[pair_a, pair_b])

        ax.scatter(x, y, s=5, **kwds)
        ax.plot((x, x), y_hdi, **kwds, **line_kwds)
        ax.plot(x_hdi, (y, y), **kwds, **line_kwds)

        if abs(x - y) > label_threshold:
            labels.append(ax.text(x, y, f"{pair_a}/{pair_b}", **text_kwds))

    adjust_text(labels, x=xy[:, 0], y=xy[:, 1])

    ax.axline((0, 0), (1, 1), c="grey", lw=0.5)
    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(base=2))
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(base=2))
    ax.set(aspect=1, xlabel="ab", ylabel="ba")

    # Deming regression
    dr = reversed_amino_acid_effects_orthogonal_least_squares_regression(idata)
    text = f"r={dr['r']:.2f}\nm={dr['m']:.2f}\nc={dr['c']:.2f}\np={dr['p']:.2f}"
    ax.text(1, 1, text, transform=ax.transAxes, va="top", fontsize=8)
    ax.axline((0, dr["c"]), slope=dr["m"], c="black")

    return ax


def reversed_amino_acid_effects_orthogonal_least_squares_regression(
    idata: az.InferenceData,
) -> dict[str, float]:
    """
    Orthogonal Least squares regression on the amino acid pairs that are estimated both
    ways round. (E.g. there are estiamtes for "NK" aswell as "KN").

    Args:
        idata: Inference data object.

    Returns:
        dict containing:
            m: Model slope.
            c: Model intercept.
            r: Pearson correlation coefficient.
            p: p-value of the Pearson correlation coefficient.

        r and p are independent of the regression. See:
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html
    """
    post = az.extract(idata)
    arr = np.array(
        [
            post["b_aa"].sel(aa=[pair_a, pair_b]).mean(dim="sample").values
            for pair_a, pair_b in aa_pairs_with_reversed(post.coords["aa"].values)
        ]
    )

    def f(p, x):
        return p[0] * x + p[1]

    od_reg = odr.ODR(odr.Data(arr[:, 0], arr[:, 1]), odr.Model(f), beta0=[1.0, 0.0])
    out = od_reg.run()

    pearsonr_result = pearsonr(arr[:, 0], arr[:, 1])
    return dict(
        m=out.beta[0],
        c=out.beta[1],
        r=pearsonr_result.statistic,
        p=pearsonr_result.pvalue,
    )
