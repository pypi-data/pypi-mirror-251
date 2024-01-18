from __future__ import annotations

import datetime
import functools
import inspect
import warnings
from collections.abc import Callable, Hashable, Mapping
from numbers import Integral, Number
from typing import Any, ClassVar, Iterable, Literal

import dask.array as da
import dask.dataframe.methods as methods
import numpy as np
import pandas as pd
from dask import compute, delayed
from dask.array import Array
from dask.base import DaskMethodsMixin, is_dask_collection, named_schedulers
from dask.core import flatten
from dask.dataframe.accessor import CachedAccessor
from dask.dataframe.core import (
    _concat,
    _convert_to_numeric,
    _Frame,
    _sqrt_and_convert_to_timedelta,
    check_divisions,
    has_parallel_type,
    is_arraylike,
    is_dataframe_like,
    is_index_like,
    is_series_like,
    meta_warning,
    new_dd_object,
)
from dask.dataframe.dispatch import is_categorical_dtype, make_meta, meta_nonempty
from dask.dataframe.multi import warn_dtype_mismatch
from dask.dataframe.utils import (
    AttributeNotImplementedError,
    has_known_categories,
    index_summary,
    meta_frame_constructor,
    meta_series_constructor,
)
from dask.delayed import delayed
from dask.utils import (
    IndexCallable,
    M,
    get_meta_library,
    memory_repr,
    put_lines,
    random_state_data,
    typename,
)
from fsspec.utils import stringify_path
from pandas import CategoricalDtype
from pandas.api.types import is_bool_dtype, is_datetime64_any_dtype, is_numeric_dtype
from pandas.api.types import is_scalar as pd_is_scalar
from pandas.api.types import is_timedelta64_dtype
from tlz import first

from dask_expr import _expr as expr
from dask_expr._align import AlignPartitions
from dask_expr._categorical import CategoricalAccessor, Categorize, GetCategories
from dask_expr._concat import Concat
from dask_expr._datetime import DatetimeAccessor
from dask_expr._describe import DescribeNonNumeric, DescribeNumeric
from dask_expr._expr import (
    BFill,
    Diff,
    Eval,
    FFill,
    FillnaCheck,
    Query,
    Shift,
    ToDatetime,
    ToNumeric,
    ToTimedelta,
    no_default,
)
from dask_expr._merge import JoinRecursive, Merge
from dask_expr._quantile import SeriesQuantile
from dask_expr._quantiles import RepartitionQuantiles
from dask_expr._reductions import (
    Corr,
    Cov,
    DropDuplicates,
    IndexCount,
    IsMonotonicDecreasing,
    IsMonotonicIncreasing,
    Len,
    MemoryUsageFrame,
    MemoryUsageIndex,
    Moment,
    NLargest,
    NSmallest,
    PivotTable,
    Unique,
    ValueCounts,
)
from dask_expr._repartition import Repartition, RepartitionFreq
from dask_expr._shuffle import (
    RearrangeByColumn,
    SetIndex,
    SetIndexBlockwise,
    SortValues,
)
from dask_expr._str_accessor import StringAccessor
from dask_expr._util import (
    RaiseAttributeError,
    _BackendData,
    _convert_to_list,
    _get_shuffle_preferring_order,
    _is_any_real_numeric_dtype,
    _maybe_from_pandas,
    _raise_if_object_series,
    _tokenize_deterministic,
    _validate_axis,
    is_scalar,
)
from dask_expr.io import FromPandasDivisions, FromScalars

#
# Utilities to wrap Expr API
# (Helps limit boiler-plate code in collection APIs)
#


def _wrap_expr_api(*args, wrap_api=None, **kwargs):
    # Use Expr API, but convert to/from Expr objects
    assert wrap_api is not None
    result = wrap_api(
        *[arg.expr if isinstance(arg, FrameBase) else arg for arg in args],
        **kwargs,
    )
    if isinstance(result, expr.Expr):
        return new_collection(result)
    return result


def _wrap_expr_op(self, other, op=None):
    # Wrap expr operator
    assert op is not None
    if isinstance(other, FrameBase):
        other = other.expr
    elif isinstance(other, da.Array):
        other = from_dask_array(
            other, index=self.index.to_dask_dataframe(), columns=self.columns
        )
        if self.ndim == 1:
            other = other[self.columns[0]]

    if (
        not isinstance(other, expr.Expr)
        and is_dataframe_like(other)
        or is_series_like(other)
    ):
        other = self._create_alignable_frame(other).expr

    if not isinstance(other, expr.Expr):
        return new_collection(getattr(self.expr, op)(other))
    elif (
        expr.are_co_aligned(self.expr, other, allow_broadcast=False)
        or other.npartitions == self.npartitions == 1
        and (self.ndim > other.ndim or self.ndim == 0)
    ):
        return new_collection(getattr(self.expr, op)(other))
    else:
        return new_collection(
            getattr(AlignPartitions(self.expr, other), op)(
                AlignPartitions(other, self.expr)
            )
        )


def _wrap_expr_method_operator(name, class_):
    """
    Add method operators to Series or DataFrame like DataFrame.add.
    _wrap_expr_method_operator("add", DataFrame)
    """
    if class_ == DataFrame:

        def method(self, other, axis="columns", level=None, fill_value=None):
            if level is not None:
                raise NotImplementedError("level must be None")

            axis = _validate_axis(axis)

            if (
                is_dataframe_like(other)
                or is_series_like(other)
                and axis in (0, "index")
            ) and not is_dask_collection(other):
                other = self._create_alignable_frame(other)

            if axis in (1, "columns"):
                if isinstance(other, Series):
                    msg = f"Unable to {name} dd.Series with axis=1"
                    raise ValueError(msg)

            frame = self
            if isinstance(other, FrameBase) and not expr.are_co_aligned(
                self.expr, other.expr, allow_broadcast=False
            ):
                divs = expr.calc_divisions_for_align(self.expr, other.expr)
                frame, other = expr.maybe_align_partitions(
                    self.expr, other.expr, divisions=divs
                )

            return new_collection(
                expr.MethodOperator(
                    name=name,
                    left=frame,
                    right=other,
                    axis=axis,
                    level=level,
                    fill_value=fill_value,
                )
            )

    elif class_ == Series:

        def method(self, other, level=None, fill_value=None, axis=0):
            if level is not None:
                raise NotImplementedError("level must be None")

            axis = _validate_axis(axis)

            if is_series_like(other) and not is_dask_collection(other):
                other = self._create_alignable_frame(other)

            frame = self
            if isinstance(other, FrameBase) and not expr.are_co_aligned(
                self.expr, other.expr, allow_broadcast=False
            ):
                divs = expr.calc_divisions_for_align(self.expr, other.expr)
                frame, other = expr.maybe_align_partitions(
                    self.expr, other.expr, divisions=divs
                )

            return new_collection(
                expr.MethodOperator(
                    name=name,
                    left=frame,
                    right=other,
                    axis=axis,
                    fill_value=fill_value,
                    level=level,
                )
            )

    else:
        raise NotImplementedError(f"Cannot create method operator for {class_=}")

    method.__name__ = name
    return method


def _wrap_unary_expr_op(self, op=None):
    # Wrap expr operator
    assert op is not None
    return new_collection(getattr(self.expr, op)())


#
# Collection classes
#


class FrameBase(DaskMethodsMixin):
    """Base class for Expr-backed Collections"""

    __dask_scheduler__ = staticmethod(
        named_schedulers.get("threads", named_schedulers["sync"])
    )
    __dask_optimize__ = staticmethod(lambda dsk, keys, **kwargs: dsk)

    def __init__(self, expr):
        self._expr = expr

    @property
    def expr(self) -> expr.Expr:
        return self._expr

    @property
    def _meta(self):
        return self.expr._meta

    @functools.cached_property
    def _meta_nonempty(self):
        return meta_nonempty(self._meta)

    @property
    def divisions(self):
        return self.expr.divisions

    @property
    def dtypes(self):
        return self.expr._meta.dtypes

    @property
    def size(self):
        return new_collection(self.expr.size)

    @property
    def columns(self):
        return self._meta.columns

    @columns.setter
    def columns(self, columns):
        if len(columns) != len(self.columns):
            # surface pandas error
            self._expr._meta.columns = columns
        self._expr = expr.ColumnsSetter(self, columns)

    def clear_divisions(self):
        return new_collection(expr.ClearDivisions(self))

    def __len__(self):
        return new_collection(Len(self)).compute()

    @property
    def nbytes(self):
        raise NotImplementedError("nbytes is not implemented on DataFrame")

    def __reduce__(self):
        return new_collection, (self._expr,)

    def __getitem__(self, other):
        if isinstance(other, FrameBase):
            return new_collection(self.expr.__getitem__(other.expr))
        elif isinstance(other, slice):
            from pandas.api.types import is_float_dtype

            is_integer_slice = any(
                isinstance(i, Integral) for i in (other.start, other.step, other.stop)
            )
            if (
                self.ndim == 2
                and is_integer_slice
                and not is_float_dtype(self.index.dtype)
            ):
                return self.iloc[other]
            else:
                return self.loc[other]
        if isinstance(other, np.ndarray) or is_series_like(other):
            other = list(other)
        return new_collection(self.expr.__getitem__(other))

    def __bool__(self):
        raise ValueError(
            f"The truth value of a {self.__class__.__name__} is ambiguous. "
            "Use a.any() or a.all()."
        )

    def __array__(self, dtype=None, **kwargs):
        return np.array(self.compute())

    def persist(self, fuse=True, **kwargs):
        out = self.optimize(fuse=fuse)
        return DaskMethodsMixin.persist(out, **kwargs)

    def compute(self, fuse=True, **kwargs):
        out = self
        if not isinstance(out, Scalar):
            out = out.repartition(npartitions=1)
        out = out.optimize(fuse=fuse)
        return DaskMethodsMixin.compute(out, **kwargs)

    @property
    def dask(self):
        return self.__dask_graph__()

    def __dask_graph__(self):
        out = self.expr
        out = out.lower_completely()
        return out.__dask_graph__()

    def __dask_keys__(self):
        out = self.expr
        out = out.lower_completely()
        return out.__dask_keys__()

    def simplify(self):
        return new_collection(self.expr.simplify())

    def lower_once(self):
        return new_collection(self.expr.lower_once())

    def optimize(self, fuse: bool = True):
        return new_collection(self.expr.optimize(fuse=fuse))

    @property
    def dask(self):
        return self.__dask_graph__()

    def __dask_postcompute__(self):
        state = new_collection(self.expr.lower_completely())
        if type(self) != type(state):
            return state.__dask_postcompute__()
        return _concat, ()

    def __dask_postpersist__(self):
        state = new_collection(self.expr.lower_completely())
        return from_graph, (state._meta, state.divisions, state._name)

    def __getattr__(self, key):
        try:
            # Prioritize `FrameBase` attributes
            return object.__getattribute__(self, key)
        except AttributeError as err:
            try:
                # Fall back to `expr` API
                # (Making sure to convert to/from Expr)
                val = getattr(self.expr, key)
                if callable(val):
                    return functools.partial(_wrap_expr_api, wrap_api=val)
                return val
            except AttributeError:
                # Raise original error
                raise err

    def visualize(self, tasks: bool = False, **kwargs):
        """Visualize the expression or task graph

        Parameters
        ----------
        tasks:
            Whether to visualize the task graph. By default
            the expression graph will be visualized instead.
        """
        if tasks:
            return super().visualize(**kwargs)
        return self.expr.visualize(**kwargs)

    @property
    def index(self):
        return new_collection(self.expr.index)

    @index.setter
    def index(self, value):
        assert expr.are_co_aligned(
            self.expr, value.expr
        ), "value needs to be aligned with the index"
        _expr = expr.AssignIndex(self, value)
        self._expr = _expr

    def reset_index(self, drop=False):
        return new_collection(expr.ResetIndex(self, drop))

    def head(self, n=5, npartitions=1, compute=True):
        out = new_collection(expr.Head(self, n=n, npartitions=npartitions))
        if compute:
            out = out.compute()
        return out

    def tail(self, n=5, compute=True):
        out = new_collection(expr.Tail(self, n=n))
        if compute:
            out = out.compute()
        return out

    def copy(self, deep=False):
        """Return a copy of this object"""
        if deep is not False:
            raise ValueError(
                "The `deep` value must be False. This is strictly a shallow copy "
                "of the underlying computational graph."
            )
        return new_collection(self.expr)

    def isin(self, values):
        if isinstance(self, DataFrame):
            # DataFrame.isin does weird alignment stuff
            bad_types = (FrameBase, pd.Series, pd.DataFrame)
        else:
            bad_types = (FrameBase,)
        if isinstance(values, bad_types):
            raise NotImplementedError("Passing a %r to `isin`" % typename(type(values)))

        # We wrap values in a delayed for two reasons:
        # - avoid serializing data in every task
        # - avoid cost of traversal of large list in optimizations
        if isinstance(values, list):
            # Motivated by https://github.com/dask/dask/issues/9411.  This appears to be
            # caused by https://github.com/dask/distributed/issues/6368, and further
            # exacerbated by the fact that the list contains duplicates.  This is a patch until
            # we can create a better fix for Serialization.
            try:
                values = list(set(values))
            except TypeError:
                pass
            if not any(is_dask_collection(v) for v in values):
                try:
                    values = np.fromiter(values, dtype=object)
                except ValueError:
                    # Numpy 1.23 supports creating arrays of iterables, while lower
                    # version 1.21.x and 1.22.x do not
                    pass
        from dask_expr.io._delayed import _DelayedExpr

        return new_collection(
            expr.Isin(
                self,
                values=_DelayedExpr(
                    delayed(values, name="delayed-" + _tokenize_deterministic(values))
                ),
            )
        )

    def _partitions(self, index):
        # Used by `partitions` for partition-wise slicing

        # Convert index to list
        if isinstance(index, int):
            index = [index]
        index = np.arange(self.npartitions, dtype=object)[index].tolist()

        # Check that selection makes sense
        assert set(index).issubset(range(self.npartitions))

        # Return selected partitions
        return new_collection(expr.Partitions(self, index))

    @property
    def partitions(self):
        """Partition-wise slicing of a collection

        Examples
        --------
        >>> df.partitions[0]
        >>> df.partitions[:3]
        >>> df.partitions[::10]
        """
        return IndexCallable(self._partitions)

    def get_partition(self, n):
        if not 0 <= n < self.npartitions:
            msg = f"n must be 0 <= n < {self.npartitions}"
            raise ValueError(msg)
        return self.partitions[n]

    def shuffle(
        self,
        index: str | list,
        ignore_index: bool = False,
        npartitions: int | None = None,
        shuffle_method: str | None = None,
        **options,
    ):
        """Shuffle a collection by column names

        Parameters
        ----------
        index:
            Column names to shuffle by.
        ignore_index: optional
            Whether to ignore the index. Default is ``False``.
        npartitions: optional
            Number of output partitions. The partition count will
            be preserved by default.
        shuffle_method: optional
            Desired shuffle method. Default chosen at optimization time.
        **options: optional
            Algorithm-specific options.
        """

        # Preserve partition count by default
        npartitions = npartitions or self.npartitions

        if isinstance(index, FrameBase):
            if not expr.are_co_aligned(self.expr, index.expr):
                raise TypeError(
                    "index must be aligned with the DataFrame to use as shuffle index."
                )
        elif pd.api.types.is_list_like(index) and not is_dask_collection(index):
            index = list(index)

        # Returned shuffled result
        return new_collection(
            RearrangeByColumn(
                self,
                index,
                npartitions,
                ignore_index,
                shuffle_method,
                options,
            )
        )

    def resample(self, rule, closed=None, label=None):
        from dask_expr._resample import Resampler

        return Resampler(self, rule, **{"closed": closed, "label": label})

    def rolling(self, window, **kwargs):
        from dask_expr._rolling import Rolling

        return Rolling(self, window, **kwargs)

    def map_partitions(
        self,
        func,
        *args,
        meta=no_default,
        enforce_metadata=True,
        transform_divisions=True,
        clear_divisions=False,
        align_dataframes=False,
        parent_meta=None,
        **kwargs,
    ):
        """Apply a Python function to each partition

        Parameters
        ----------
        func : function
            Function applied to each partition.
        args, kwargs :
            Arguments and keywords to pass to the function. Arguments and
            keywords may contain ``FrameBase`` or regular python objects.
            DataFrame-like args (both dask and pandas) must have the same
            number of partitions as ``self` or comprise a single partition.
            Key-word arguments, Single-partition arguments, and general
            python-object arguments will be broadcasted to all partitions.
        enforce_metadata : bool, default True
            Whether to enforce at runtime that the structure of the DataFrame
            produced by ``func`` actually matches the structure of ``meta``.
            This will rename and reorder columns for each partition, and will
            raise an error if this doesn't work, but it won't raise if dtypes
            don't match.
        transform_divisions : bool, default True
            Whether to apply the function onto the divisions and apply those
            transformed divisions to the output.
        clear_divisions : bool, default False
            Whether divisions should be cleared. If True, `transform_divisions`
            will be ignored.
        meta : Any, optional
            DataFrame object representing the schema of the expected result.
        """

        return map_partitions(
            func,
            self,
            *args,
            meta=meta,
            enforce_metadata=enforce_metadata,
            transform_divisions=transform_divisions,
            clear_divisions=clear_divisions,
            align_dataframes=align_dataframes,
            parent_meta=parent_meta,
            **kwargs,
        )

    def map_overlap(
        self,
        func,
        before,
        after,
        *args,
        meta=no_default,
        enforce_metadata=True,
        transform_divisions=True,
        clear_divisions=False,
        align_dataframes=False,
        **kwargs,
    ):
        return map_overlap(
            func,
            self,
            before,
            after,
            *args,
            meta=meta,
            enforce_metadata=enforce_metadata,
            transform_divisions=transform_divisions,
            clear_divisions=clear_divisions,
            align_dataframes=align_dataframes,
            **kwargs,
        )

    def repartition(
        self,
        divisions: tuple | None = None,
        npartitions: int | None = None,
        partition_size: str = None,
        freq=None,
        force: bool = False,
    ):
        """Repartition a collection

        Exactly one of `divisions`, `npartitions` or `partition_size` should be
        specified. A ``ValueError`` will be raised when that is not the case.

        Parameters
        ----------
        divisions : list, optional
            The "dividing lines" used to split the dataframe into partitions.
            For ``divisions=[0, 10, 50, 100]``, there would be three output partitions,
            where the new index contained [0, 10), [10, 50), and [50, 100), respectively.
            See https://docs.dask.org/en/latest/dataframe-design.html#partitions.
        npartitions : int, Callable, optional
            Approximate number of partitions of output. The number of
            partitions used may be slightly lower than npartitions depending
            on data distribution, but will never be higher.
            The Callable gets the number of partitions of the input as an argument
            and should return an int.
        partition_size : str, optional
            Max number of bytes of memory for each partition. Use numbers or strings
            like 5MB. If specified npartitions and divisions will be ignored. Note that
            the size reflects the number of bytes used as computed by
            pandas.DataFrame.memory_usage, which will not necessarily match the size
            when storing to disk.
        force : bool, default False
            Allows the expansion of the existing divisions.
            If False then the new divisions' lower and upper bounds must be
            the same as the old divisions'.
        freq : str, pd.Timedelta
            A period on which to partition timeseries data like ``'7D'`` or
            ``'12h'`` or ``pd.Timedelta(hours=12)``.  Assumes a datetime index.
        """

        if (
            sum(
                [
                    divisions is not None,
                    npartitions is not None,
                    partition_size is not None,
                    freq is not None,
                ]
            )
            != 1
        ):
            raise ValueError(
                "Please provide exactly one of the ``npartitions=`` or "
                "``divisions=`` keyword arguments."
            )
        if divisions is not None:
            check_divisions(divisions)
        if freq is not None:
            if not isinstance(self.divisions[0], pd.Timestamp):
                raise TypeError("Can only repartition on frequency for timeseries")
            return new_collection(RepartitionFreq(self, freq))
        else:
            return new_collection(
                Repartition(self, npartitions, divisions, force, partition_size, freq)
            )

    def to_dask_dataframe(self, optimize: bool = True, **optimize_kwargs) -> _Frame:
        """Convert to a dask-dataframe collection

        Parameters
        ----------
        optimize
            Whether to optimize the underlying `Expr` object before conversion.
        **optimize_kwargs
            Key-word arguments to pass through to `optimize`.
        """
        df = self.optimize(**optimize_kwargs) if optimize else self
        return new_dd_object(df.dask, df._name, df._meta, df.divisions)

    def to_dask_array(
        self, lengths=None, meta=None, optimize: bool = True, **optimize_kwargs
    ) -> Array:
        return self.to_dask_dataframe(optimize, **optimize_kwargs).to_dask_array(
            lengths=lengths, meta=meta
        )

    @property
    def values(self):
        return self.to_dask_array()

    def __divmod__(self, other):
        result = self.expr.__divmod__(other)
        return new_collection(result[0]), new_collection(result[1])

    def __rdivmod__(self, other):
        result = self.expr.__rdivmod__(other)
        return new_collection(result[0]), new_collection(result[1])

    def __abs__(self):
        return self.abs()

    def sum(
        self,
        axis=None,
        skipna=True,
        numeric_only=False,
        min_count=0,
        split_every=False,
        **kwargs,
    ):
        axis = self._validate_axis(axis)
        if axis == 1:
            return self.map_partitions(
                M.sum,
                skipna=skipna,
                numeric_only=numeric_only,
                axis=axis,
                min_count=min_count,
            )

        result = new_collection(self.expr.sum(skipna, numeric_only, split_every))
        return self._apply_min_count(result, min_count)

    def _apply_min_count(self, result, min_count):
        if min_count:
            cond = self.notnull().sum() >= min_count
            cond_meta = cond._meta
            if not is_series_like(cond_meta):
                result = result.to_series()
                cond = cond.to_series()

            result = result.where(cond, other=np.nan)
            if not is_series_like(cond_meta):
                return result.min()
            else:
                return result
        else:
            return result

    def prod(
        self,
        axis=None,
        skipna=True,
        numeric_only=False,
        min_count=0,
        split_every=False,
        **kwargs,
    ):
        axis = self._validate_axis(axis)
        if axis == 1:
            return self.map_partitions(
                M.prod,
                skipna=skipna,
                numeric_only=numeric_only,
                axis=axis,
                min_count=min_count,
            )
        result = new_collection(self.expr.prod(skipna, numeric_only, split_every))
        return self._apply_min_count(result, min_count)

    product = prod

    def var(
        self,
        axis=0,
        skipna=True,
        ddof=1,
        numeric_only=False,
        split_every=False,
        **kwargs,
    ):
        _raise_if_object_series(self, "var")
        axis = self._validate_axis(axis)
        self._meta.var(axis=axis, skipna=skipna, numeric_only=numeric_only)
        frame = self
        if is_dataframe_like(self._meta) and numeric_only:
            frame = frame[list(self._meta.var(numeric_only=True).index)]
        return new_collection(
            frame.expr.var(axis, skipna, ddof, numeric_only, split_every=split_every)
        )

    def std(
        self,
        axis=0,
        skipna=True,
        ddof=1,
        numeric_only=False,
        split_every=False,
        **kwargs,
    ):
        _raise_if_object_series(self, "std")
        axis = self._validate_axis(axis)
        numeric_dd = self
        meta = meta_nonempty(self._meta).std(
            axis=axis, skipna=skipna, ddof=ddof, numeric_only=numeric_only
        )
        needs_time_conversion, time_cols = False, None
        if is_dataframe_like(self._meta):
            if axis == 0:
                numeric_dd = numeric_dd[list(meta.index)]
            else:
                numeric_dd = numeric_dd.copy()

            if numeric_only is True:
                _meta = numeric_dd._meta.select_dtypes(include=[np.number])
            else:
                _meta = numeric_dd._meta
            time_cols = _meta.select_dtypes(include=["datetime", "timedelta"]).columns
            if len(time_cols) > 0:
                if axis == 1 and len(time_cols) != len(self.columns):
                    numeric_dd = from_pandas(
                        meta_frame_constructor(self)(
                            {"_": meta_series_constructor(self)([np.nan])},
                            index=self.index,
                        ),
                        npartitions=self.npartitions,
                    )
                else:
                    needs_time_conversion = True
                    for col in time_cols:
                        numeric_dd[col] = _convert_to_numeric(numeric_dd[col], skipna)
        else:
            needs_time_conversion = is_datetime64_any_dtype(self._meta)
            if needs_time_conversion:
                numeric_dd = _convert_to_numeric(self, skipna)

        if axis == 1:
            return numeric_dd.map_partitions(
                M.std if not needs_time_conversion else _sqrt_and_convert_to_timedelta,
                meta=meta,
                axis=axis,
                skipna=skipna,
                ddof=ddof,
                enforce_metadata=False,
                numeric_only=numeric_only,
            )

        result = numeric_dd.var(
            skipna=skipna, ddof=ddof, numeric_only=numeric_only, split_every=split_every
        )

        if needs_time_conversion:
            sqrt_func_kwargs = {
                "is_df_like": is_dataframe_like(self._meta),
                "time_cols": time_cols,
                "axis": axis,
                "dtype": getattr(meta, "dtype", None),
            }
            sqrt_func = _sqrt_and_convert_to_timedelta
        else:
            sqrt_func_kwargs = {}
            sqrt_func = np.sqrt

        result = result.map_partitions(
            sqrt_func,
            meta=meta,
            enforce_metadata=False,
            parent_meta=self._meta,
            **sqrt_func_kwargs,
        )
        return result

    def enforce_runtime_divisions(self):
        """Enforce the current divisions at runtime"""
        if not self.known_divisions:
            raise ValueError("No known divisions to enforce!")
        return new_collection(expr.EnforceRuntimeDivisions(self))

    def skew(
        self,
        axis=0,
        bias=True,
        nan_policy="propagate",
        numeric_only=False,
    ):
        """
        .. note::

           This implementation follows the dask.array.stats implementation
           of skewness and calculates skewness without taking into account
           a bias term for finite sample size, which corresponds to the
           default settings of the scipy.stats skewness calculation. However,
           Pandas corrects for this, so the values differ by a factor of
           (n * (n - 1)) ** 0.5 / (n - 2), where n is the number of samples.

           Further, this method currently does not support filtering out NaN
           values, which is again a difference to Pandas.
        """
        _raise_if_object_series(self, "skew")
        if axis is None:
            raise ValueError("`axis=None` isn't currently supported for `skew`")
        axis = self._validate_axis(axis)

        if is_dataframe_like(self):
            # Let pandas raise errors if necessary
            meta = self._meta_nonempty.skew(axis=axis, numeric_only=numeric_only)
        else:
            meta = self._meta_nonempty.skew()

        if axis == 1:
            return self.map_partitions(
                M.skew,
                meta=meta,
                axis=axis,
                enforce_metadata=False,
            )

        if not bias:
            raise NotImplementedError("bias=False is not implemented.")
        if nan_policy != "propagate":
            raise NotImplementedError(
                "`nan_policy` other than 'propagate' have not been implemented."
            )

        frame = self
        if frame.ndim > 1:
            frame = frame.select_dtypes(
                include=["number", "bool"], exclude=[np.timedelta64]
            )
        m2 = new_collection(Moment(frame, order=2))
        m3 = new_collection(Moment(frame, order=3))
        result = m3 / m2**1.5
        if result.ndim == 1:
            result = result.fillna(0.0)
        return result

    def kurtosis(
        self,
        axis=0,
        fisher=True,
        bias=True,
        nan_policy="propagate",
        numeric_only=False,
    ):
        """
        .. note::

           This implementation follows the dask.array.stats implementation
           of kurtosis and calculates kurtosis without taking into account
           a bias term for finite sample size, which corresponds to the
           default settings of the scipy.stats kurtosis calculation. This differs
           from pandas.

           Further, this method currently does not support filtering out NaN
           values, which is again a difference to Pandas.
        """
        _raise_if_object_series(self, "kurtosis")
        if axis is None:
            raise ValueError("`axis=None` isn't currently supported for `skew`")
        axis = self._validate_axis(axis)

        if is_dataframe_like(self):
            # Let pandas raise errors if necessary
            meta = self._meta_nonempty.kurtosis(axis=axis, numeric_only=numeric_only)
        else:
            meta = self._meta_nonempty.kurtosis()

        if axis == 1:
            return map_partitions(
                M.kurtosis,
                self,
                meta=meta,
                token=self._token_prefix + "kurtosis",
                axis=axis,
                enforce_metadata=False,
            )

        if not bias:
            raise NotImplementedError("bias=False is not implemented.")
        if nan_policy != "propagate":
            raise NotImplementedError(
                "`nan_policy` other than 'propagate' have not been implemented."
            )

        frame = self
        if frame.ndim > 1:
            frame = frame.select_dtypes(
                include=["number", "bool"], exclude=[np.timedelta64]
            )
        m2 = new_collection(Moment(frame, order=2))
        m4 = new_collection(Moment(frame, order=4))
        result = m4 / m2**2.0
        if result.ndim == 1:
            result = result.fillna(0.0)
        if fisher:
            return result - 3
        else:
            return result

    kurt = kurtosis

    def sem(
        self, axis=None, skipna=True, ddof=1, split_every=False, numeric_only=False
    ):
        axis = self._validate_axis(axis)
        _raise_if_object_series(self, "sem")
        if axis == 1:
            return self.map_partitions(
                M.sem,
                axis=axis,
                skipna=skipna,
                ddof=ddof,
                numeric_only=numeric_only,
            )
        meta = self._meta.sem(skipna=skipna, ddof=ddof, numeric_only=numeric_only)
        frame = self
        if self.ndim == 2:
            frame = self[list(meta.index)]

        v = frame.var(skipna=skipna, ddof=ddof, split_every=split_every)
        n = frame.count(split_every=split_every)
        result = map_partitions(
            np.sqrt,
            v / n,
            meta=meta,
            enforce_metadata=False,
            parent_meta=self._meta,
        )
        return result

    def _prepare_cov_corr(self, min_periods, numeric_only):
        if min_periods is None:
            min_periods = 2
        elif min_periods < 2:
            raise ValueError("min_periods must be >= 2")

        self._meta.cov(numeric_only=numeric_only, min_periods=min_periods)

        frame = self
        if numeric_only:
            numerics = self._meta._get_numeric_data()
            if len(numerics.columns) != len(self.columns):
                frame = frame[list(numerics.columns)]
        return frame, min_periods

    def _cov(
        self, min_periods=None, numeric_only=False, split_every=False, scalar=False
    ):
        frame, min_periods = self._prepare_cov_corr(min_periods, numeric_only)
        return new_collection(Cov(frame, min_periods, split_every, scalar))

    def _corr(
        self,
        method="pearson",
        min_periods=None,
        numeric_only=False,
        split_every=False,
        scalar=False,
    ):
        if method != "pearson":
            raise NotImplementedError("Only Pearson correlation has been implemented")
        frame, min_periods = self._prepare_cov_corr(min_periods, numeric_only)
        return new_collection(Corr(frame, min_periods, split_every, scalar))

    def mean(
        self, axis=0, skipna=True, numeric_only=False, split_every=False, **kwargs
    ):
        _raise_if_object_series(self, "mean")
        axis = self._validate_axis(axis)
        if axis == 1:
            return self.map_partitions(
                M.mean, skipna=skipna, numeric_only=numeric_only, axis=axis
            )
        return new_collection(
            self.expr.mean(skipna, numeric_only, split_every=split_every, axis=axis)
        )

    def max(self, axis=0, skipna=True, numeric_only=False, split_every=False, **kwargs):
        axis = self._validate_axis(axis)
        if axis == 1:
            return self.map_partitions(
                M.max, skipna=skipna, numeric_only=numeric_only, axis=axis
            )
        return new_collection(self.expr.max(skipna, numeric_only, split_every, axis))

    def any(self, axis=0, skipna=True, split_every=False, **kwargs):
        axis = self._validate_axis(axis)
        if axis == 1:
            return self.map_partitions(M.any, skipna=skipna, axis=axis)
        return new_collection(self.expr.any(skipna, split_every))

    def all(self, axis=0, skipna=True, split_every=False, **kwargs):
        axis = self._validate_axis(axis)
        if axis == 1:
            return self.map_partitions(M.all, skipna=skipna, axis=axis)
        return new_collection(self.expr.all(skipna, split_every))

    def idxmin(self, axis=0, skipna=True, numeric_only=False, split_every=False):
        axis = self._validate_axis(axis)
        if axis == 1:
            return self.map_partitions(
                M.idxmin, skipna=skipna, numeric_only=numeric_only, axis=axis
            )
        return new_collection(self.expr.idxmin(skipna, numeric_only, split_every))

    def idxmax(self, axis=0, skipna=True, numeric_only=False, split_every=False):
        axis = self._validate_axis(axis)
        if axis == 1:
            return self.map_partitions(
                M.idxmax, skipna=skipna, numeric_only=numeric_only, axis=axis
            )
        return new_collection(self.expr.idxmax(skipna, numeric_only, split_every))

    def min(self, axis=0, skipna=True, numeric_only=False, split_every=False, **kwargs):
        axis = self._validate_axis(axis)
        if axis == 1:
            return self.map_partitions(
                M.min, skipna=skipna, numeric_only=numeric_only, axis=axis
            )
        return new_collection(self.expr.min(skipna, numeric_only, split_every, axis))

    def count(self, axis=0, numeric_only=False, split_every=False):
        axis = self._validate_axis(axis)
        if axis == 1:
            return self.map_partitions(M.count, numeric_only=numeric_only, axis=axis)
        return new_collection(self.expr.count(numeric_only, split_every))

    def abs(self):
        # Raise pandas errors
        _raise_if_object_series(self, "abs")
        meta_nonempty(self._meta).abs()
        return new_collection(self.expr.abs())

    def astype(self, dtypes):
        return new_collection(self.expr.astype(dtypes))

    def combine_first(self, other):
        other = self._create_alignable_frame(other, "outer").expr
        return new_collection(self.expr.combine_first(other))

    def to_timestamp(self, freq=None, how="start"):
        return new_collection(self.expr.to_timestamp(freq, how))

    def isna(self):
        return new_collection(self.expr.isna())

    def random_split(self, frac, random_state=None, shuffle=False):
        """Pseudorandomly split dataframe into different pieces row-wise

        Parameters
        ----------
        frac : list
            List of floats that should sum to one.
        random_state : int or np.random.RandomState
            If int or None create a new RandomState with this as the seed.
            Otherwise draw from the passed RandomState.
        shuffle : bool, default False
            If set to True, the dataframe is shuffled (within partition)
            before the split.

        Examples
        --------

        50/50 split

        >>> a, b = df.random_split([0.5, 0.5])  # doctest: +SKIP

        80/10/10 split, consistent random_state

        >>> a, b, c = df.random_split([0.8, 0.1, 0.1], random_state=123)  # doctest: +SKIP

        See Also
        --------
        dask.DataFrame.sample
        """
        if not np.allclose(sum(frac), 1):
            raise ValueError("frac should sum to 1")
        frame = expr.Split(self, frac, random_state, shuffle)

        out = []
        for i in range(len(frac)):
            out.append(new_collection(expr.SplitTake(frame, i)))
        return out

    def isnull(self):
        return new_collection(self.expr.isnull())

    def round(self, decimals=0):
        return new_collection(self.expr.round(decimals))

    def where(self, cond, other=np.nan):
        cond = self._create_alignable_frame(cond)
        other = self._create_alignable_frame(other)
        cond = cond.expr if isinstance(cond, FrameBase) else cond
        other = other.expr if isinstance(other, FrameBase) else other
        return new_collection(self.expr.where(cond, other))

    def mask(self, cond, other=np.nan):
        cond = self._create_alignable_frame(cond)
        other = self._create_alignable_frame(other)
        cond = cond.expr if isinstance(cond, FrameBase) else cond
        other = other.expr if isinstance(other, FrameBase) else other
        return new_collection(self.expr.mask(cond, other))

    def replace(self, to_replace=None, value=no_default, regex=False):
        return new_collection(self.expr.replace(to_replace, value, regex))

    def ffill(self, axis=0, limit=None):
        axis = _validate_axis(axis)
        if axis == 1:
            return self.map_partitions(M.ffill, axis=axis, limit=limit)
        frame = self
        if limit is None:
            frame = FillnaCheck(self, "ffill", lambda x: 0)
        return new_collection(FFill(frame, limit))

    def bfill(self, axis=0, limit=None):
        axis = _validate_axis(axis)
        if axis == 1:
            return self.map_partitions(M.bfill, axis=axis, limit=limit)
        frame = self
        if limit is None:
            frame = FillnaCheck(self, "bfill", lambda x: x.npartitions - 1)
        return new_collection(BFill(frame, limit))

    def fillna(self, value=None, axis=None):
        axis = self._validate_axis(axis)
        if axis == 1:
            return self.map_partitions(M.fillna, value, axis=axis)
        if isinstance(value, FrameBase):
            value = value.expr
        return new_collection(self.expr.fillna(value))

    def shift(self, periods=1, freq=None, axis=0):
        if not isinstance(periods, Integral):
            raise TypeError("periods must be an integer")

        axis = _validate_axis(axis)
        if axis == 0:
            return new_collection(Shift(self, periods, freq))

        return self.map_partitions(
            func=Shift.func,
            enforce_metadata=False,
            transform_divisions=False,
            periods=periods,
            axis=axis,
            freq=freq,
        )

    def diff(self, periods=1, axis=0):
        axis = _validate_axis(axis)
        if axis == 0:
            return new_collection(Diff(self, periods))
        return self.map_partitions(
            func=Diff.func,
            enforce_metadata=False,
            transform_divisions=False,
            clear_divisions=False,
            periods=periods,
            axis=axis,
        )

    def rename_axis(
        self, mapper=no_default, index=no_default, columns=no_default, axis=0
    ):
        return new_collection(self.expr.rename_axis(mapper, index, columns, axis))

    def _create_alignable_frame(self, other, join="outer"):
        if not is_dask_collection(other) and (
            is_series_like(other) or is_dataframe_like(other)
        ):
            if join in ("inner", "left"):
                npartitions = 1
            else:
                # We have to trigger alignment, otherwise pandas will add
                # the same values to every partition
                npartitions = 2
            other = from_pandas(other, npartitions=npartitions)
        return other

    def align(self, other, join="outer", axis=None, fill_value=None):
        other = self._create_alignable_frame(other, join)
        return self.expr.align(other.expr, join, axis, fill_value)

    def nunique_approx(self, split_every=None):
        return new_collection(self.expr.nunique_approx(split_every=split_every))

    def cumsum(self, axis=0, skipna=True, **kwargs):
        if axis == 1:
            return self.map_partitions(M.cumsum, axis=axis, skipna=skipna)
        return new_collection(self.expr.cumsum(skipna=skipna))

    def cumprod(self, axis=0, skipna=True, **kwargs):
        if axis == 1:
            return self.map_partitions(M.cumprod, axis=axis, skipna=skipna)
        return new_collection(self.expr.cumprod(skipna=skipna))

    def cummax(self, axis=0, skipna=True):
        if axis == 1:
            return self.map_partitions(M.cummax, axis=axis, skipna=skipna)
        return new_collection(self.expr.cummax(skipna=skipna))

    def cummin(self, axis=0, skipna=True):
        if axis == 1:
            return self.map_partitions(M.cummin, axis=axis, skipna=skipna)
        return new_collection(self.expr.cummin(skipna=skipna))

    def memory_usage_per_partition(self, index=True, deep=False):
        return new_collection(self.expr.memory_usage_per_partition(index, deep))

    @property
    def loc(self):
        from dask_expr._indexing import LocIndexer

        return LocIndexer(self)

    def notnull(self):
        return new_collection(expr.NotNull(self))

    def isnull(self):
        return ~self.notnull()

    def compute_current_divisions(self, col=None, set_divisions=False):
        """Compute the current divisions of the DataFrame.

        This method triggers immediate computation. If you find yourself running this command
        repeatedly for the same dataframe, we recommend storing the result
        so you don't have to rerun it.

        If the column or index values overlap between partitions, raises ``ValueError``.
        To prevent this, make sure the data are sorted by the column or index.

        Parameters
        ----------
        col : string, optional
            Calculate the divisions for a non-index column by passing in the name of the column.
            If col is not specified, the index will be used to calculate divisions.
            In this case, if the divisions are already known, they will be returned
            immediately without computing.

        Examples
        --------
        >>> import dask
        >>> ddf = dask.datasets.timeseries(start="2021-01-01", end="2021-01-07", freq="1h").clear_divisions()
        >>> divisions = ddf.compute_current_divisions()
        >>> print(divisions)  # doctest: +NORMALIZE_WHITESPACE
        (Timestamp('2021-01-01 00:00:00'),
         Timestamp('2021-01-02 00:00:00'),
         Timestamp('2021-01-03 00:00:00'),
         Timestamp('2021-01-04 00:00:00'),
         Timestamp('2021-01-05 00:00:00'),
         Timestamp('2021-01-06 00:00:00'),
         Timestamp('2021-01-06 23:00:00'))

        >>> ddf.divisions = divisions
        >>> ddf.known_divisions
        True

        >>> ddf = ddf.reset_index().clear_divisions()
        >>> divisions = ddf.compute_current_divisions("timestamp")
        >>> print(divisions)  # doctest: +NORMALIZE_WHITESPACE
        (Timestamp('2021-01-01 00:00:00'),
         Timestamp('2021-01-02 00:00:00'),
         Timestamp('2021-01-03 00:00:00'),
         Timestamp('2021-01-04 00:00:00'),
         Timestamp('2021-01-05 00:00:00'),
         Timestamp('2021-01-06 00:00:00'),
         Timestamp('2021-01-06 23:00:00'))

        >>> ddf = ddf.set_index("timestamp", divisions=divisions, sorted=True)
        """
        if col is None and self.known_divisions:
            return self.divisions

        if col is not None and set_divisions:
            raise NotImplementedError(
                "Can't set divisions of non-index, call set_index instead."
            )

        if col is not None:
            frame = self[col]
        else:
            frame = self.index

        mins, maxes, lens = _compute_partition_stats(frame, allow_overlap=set_divisions)
        divisions = tuple(mins) + (maxes[-1],)
        if not set_divisions:
            return divisions
        if len(mins) == len(self.divisions) - 1:
            if not any(mins[i] >= maxes[i - 1] for i in range(1, len(mins))):
                return new_collection(expr.SetDivisions(self, divisions))

        return new_collection(expr.ResolveOverlappingDivisions(self, mins, maxes, lens))

    @classmethod
    def from_dict(
        cls, data, *, npartitions=1, orient="columns", dtype=None, columns=None
    ):
        return from_dict(data, npartitions, orient, dtype=dtype, columns=columns)

    def to_json(self, filename, *args, **kwargs):
        """See dd.to_json docstring for more information"""
        from dask.dataframe.io import to_json

        return to_json(self, filename, *args, **kwargs)

    def to_sql(
        self,
        name: str,
        uri: str,
        schema=None,
        if_exists: str = "fail",
        index: bool = True,
        index_label=None,
        chunksize=None,
        dtype=None,
        method=None,
        compute=True,
        parallel=False,
        engine_kwargs=None,
    ):
        from dask_expr.io.sql import to_sql

        return to_sql(
            self,
            name,
            uri,
            schema=schema,
            if_exists=if_exists,
            index=index,
            index_label=index_label,
            chunksize=chunksize,
            dtype=dtype,
            method=method,
            compute=compute,
            parallel=parallel,
            engine_kwargs=engine_kwargs,
        )

    def to_orc(self, path, *args, **kwargs):
        """See dd.to_orc docstring for more information"""
        from dask_expr.io.orc import to_orc

        return to_orc(self, path, *args, **kwargs)

    def to_csv(self, filename, **kwargs):
        """See dd.to_csv docstring for more information"""
        from dask_expr.io.csv import to_csv

        return to_csv(self, filename, **kwargs)

    def to_records(self, index=False, lengths=None):
        from dask_expr.io.records import to_records

        if lengths is True:
            lengths = tuple(self.map_partitions(len).compute())

        frame = self.to_dask_dataframe()
        records = to_records(frame)

        chunks = frame._validate_chunks(records, lengths)
        records._chunks = (chunks[0],)

        return records

    def to_bag(self, index=False, format="tuple"):
        """Create a Dask Bag from a Series"""
        from dask_expr.io.bag import to_bag

        return to_bag(self, index, format=format)

    def to_hdf(self, path_or_buf, key, mode="a", append=False, **kwargs):
        """See dd.to_hdf docstring for more information"""
        from dask_expr.io.hdf import to_hdf

        return to_hdf(self, path_or_buf, key, mode, append, **kwargs)

    def to_delayed(self, optimize_graph=True):
        """Convert into a list of ``dask.delayed`` objects, one per partition.

        Parameters
        ----------
        optimize_graph : bool, optional
            If True [default], the graph is optimized before converting into
            ``dask.delayed`` objects.

        Examples
        --------
        >>> partitions = df.to_delayed()  # doctest: +SKIP

        See Also
        --------
        dask.dataframe.from_delayed
        """
        return self.to_dask_dataframe().to_delayed(optimize_graph=optimize_graph)

    def to_backend(self, backend: str | None = None, **kwargs):
        """Move to a new DataFrame backend

        Parameters
        ----------
        backend : str, Optional
            The name of the new backend to move to. The default
            is the current "dataframe.backend" configuration.

        Returns
        -------
        DataFrame, Series or Index
        """
        from dask.dataframe.io import to_backend

        return to_backend(self.to_dask_dataframe(), backend=backend, **kwargs)

    def dot(self, other, meta=no_default):
        if not isinstance(other, FrameBase):
            raise TypeError("The second operand must be a dask dataframe")

        if isinstance(other, DataFrame):
            s = self.map_partitions(M.dot, other, meta=meta)
            return s.groupby(by=s.index).apply(
                lambda x: x.sum(skipna=False), meta=s._meta_nonempty
            )

        return self.map_partitions(_dot_series, other, meta=meta).sum(skipna=False)

    def pipe(self, func, *args, **kwargs):
        if isinstance(func, tuple):
            func, target = func
            if target in kwargs:
                raise ValueError(
                    "%s is both the pipe target and a keyword argument" % target
                )
            kwargs[target] = self
            return func(*args, **kwargs)
        else:
            return func(self, *args, **kwargs)


def _dot_series(*args, **kwargs):
    # .sum() is invoked on each partition before being applied to all
    # partitions. The return type is expected to be a series, not a numpy object
    return meta_series_constructor(args[0])(M.dot(*args, **kwargs))


# Add operator attributes
for op in [
    "__add__",
    "__radd__",
    "__sub__",
    "__rsub__",
    "__mul__",
    "__rmul__",
    "__mod__",
    "__rmod__",
    "__floordiv__",
    "__rfloordiv__",
    "__truediv__",
    "__rtruediv__",
    "__pow__",
    "__rpow__",
    "__lt__",
    "__rlt__",
    "__gt__",
    "__rgt__",
    "__le__",
    "__rle__",
    "__ge__",
    "__rge__",
    "__eq__",
    "__ne__",
    "__and__",
    "__rand__",
    "__or__",
    "__ror__",
    "__xor__",
    "__rxor__",
]:
    setattr(FrameBase, op, functools.partialmethod(_wrap_expr_op, op=op))

for op in [
    "__invert__",
    "__neg__",
    "__pos__",
]:
    setattr(FrameBase, op, functools.partialmethod(_wrap_unary_expr_op, op=op))


class DataFrame(FrameBase):
    """DataFrame-like Expr Collection"""

    _accessors: ClassVar[set[str]] = set()
    _partition_type = pd.DataFrame

    @property
    def shape(self):
        return self.size / max(len(self.columns), 1), len(self.columns)

    @property
    def empty(self):
        # __getattr__ will be called after we raise this, so we'll raise it again from there
        raise AttributeNotImplementedError(
            "Checking whether a Dask DataFrame has any rows may be expensive. "
            "However, checking the number of columns is fast. "
            "Depending on which of these results you need, use either "
            "`len(df.index) == 0` or `len(df.columns) == 0`"
        )

    def keys(self):
        return self.columns

    def items(self):
        for i, name in enumerate(self.columns):
            yield (name, self.iloc[:, i])

    @property
    def axes(self):
        return [self.index, self.columns]

    def __contains__(self, key):
        return key in self._meta

    def __iter__(self):
        return iter(self._meta)

    def iterrows(self):
        frame = self.optimize()
        for i in range(self.npartitions):
            df = frame.get_partition(i).compute()
            yield from df.iterrows()

    def itertuples(self, index=True, name="Pandas"):
        frame = self.optimize()
        for i in range(self.npartitions):
            df = frame.get_partition(i).compute()
            yield from df.itertuples(index=index, name=name)

    @property
    def _elemwise(self):
        return elemwise

    def __array_ufunc__(self, numpy_ufunc, method, *inputs, **kwargs):
        out = kwargs.get("out", ())
        for x in inputs + out:
            # ufuncs work with 0-dimensional NumPy ndarrays
            # so we don't want to raise NotImplemented
            if isinstance(x, np.ndarray) and x.shape == ():
                continue
            elif not isinstance(
                x, (Number, Scalar, FrameBase, Array, pd.DataFrame, pd.Series, pd.Index)
            ):
                return NotImplemented

        if method == "__call__":
            if numpy_ufunc.signature is not None:
                return NotImplemented
            if numpy_ufunc.nout > 1:
                # ufuncs with multiple output values
                # are not yet supported for frames
                return NotImplemented
            else:
                return elemwise(numpy_ufunc, *inputs, **kwargs)
        else:
            # ufunc methods are not yet supported for frames
            return NotImplemented

    def __array_wrap__(self, array, context=None):
        if isinstance(context, tuple) and len(context) > 0:
            if isinstance(context[1][0], np.ndarray) and context[1][0].shape == ():
                index = None
            else:
                index = context[1][0].index
        else:
            try:
                import inspect

                method_name = f"`{inspect.stack()[3][3]}`"
            except IndexError:
                method_name = "This method"

            raise NotImplementedError(
                f"{method_name} is not implemented for `dask.dataframe.DataFrame`."
            )

        return meta_frame_constructor(self)(array, index=index, columns=self.columns)

    def _ipython_key_completions_(self):
        return methods.tolist(self.columns)

    def assign(self, **pairs):
        result = self
        for k, v in pairs.items():
            v = _maybe_from_pandas([v])[0]
            if not isinstance(k, str):
                raise TypeError(f"Column name cannot be type {type(k)}")

            if callable(v):
                v = v(result)

            if isinstance(v, (Scalar, Series)):
                if isinstance(v, Series):
                    if not expr.are_co_aligned(
                        self.expr, v.expr, allow_broadcast=False
                    ):
                        result, v = self.expr._align_divisions(v.expr)

                result = new_collection(expr.Assign(result, k, v))
            elif not isinstance(v, FrameBase) and isinstance(v, Hashable):
                result = new_collection(expr.Assign(result, k, v))
            elif isinstance(v, Array):
                if len(v.shape) > 1:
                    raise ValueError("Array assignment only supports 1-D arrays")
                if v.npartitions != result.npartitions:
                    raise ValueError(
                        "Number of partitions do not match "
                        f"({v.npartitions} != {result.npartitions})"
                    )
                result = new_collection(
                    expr.Assign(
                        result,
                        k,
                        from_dask_array(
                            v, index=result.index.to_dask_dataframe(), meta=result._meta
                        ),
                    )
                )
            else:
                raise TypeError(f"Column assignment doesn't support type {type(v)}")

        return result

    def clip(self, lower=None, upper=None, axis=None, **kwargs):
        axis = self._validate_axis(axis)
        if axis == 1:
            return self.map_partitions(M.clip, lower, upper, axis=axis)
        return new_collection(self.expr.clip(lower, upper, axis))

    def merge(
        self,
        right,
        how="inner",
        on=None,
        left_on=None,
        right_on=None,
        left_index=False,
        right_index=False,
        suffixes=("_x", "_y"),
        indicator=False,
        shuffle_method=None,
        npartitions=None,
        broadcast=None,
    ):
        """Merge the DataFrame with another DataFrame

        Parameters
        ----------
        right: FrameBase or pandas DataFrame
        how : {'left', 'right', 'outer', 'inner'}, default: 'inner'
            How to handle the operation of the two objects:
            - left: use calling frame's index (or column if on is specified)
            - right: use other frame's index
            - outer: form union of calling frame's index (or column if on is
              specified) with other frame's index, and sort it
              lexicographically
            - inner: form intersection of calling frame's index (or column if
              on is specified) with other frame's index, preserving the order
              of the calling's one
        on : label or list
            Column or index level names to join on. These must be found in both
            DataFrames. If on is None and not merging on indexes then this
            defaults to the intersection of the columns in both DataFrames.
        left_on : label or list, or array-like
            Column to join on in the left DataFrame. Other than in pandas
            arrays and lists are only support if their length is 1.
        right_on : label or list, or array-like
            Column to join on in the right DataFrame. Other than in pandas
            arrays and lists are only support if their length is 1.
        left_index : boolean, default False
            Use the index from the left DataFrame as the join key.
        right_index : boolean, default False
            Use the index from the right DataFrame as the join key.
        suffixes : 2-length sequence (tuple, list, ...)
            Suffix to apply to overlapping column names in the left and
            right side, respectively
        indicator : boolean or string, default False
            Passed through to the backend DataFrame library.
        shuffle_method: optional
            Shuffle method to use if shuffling is necessary.
        npartitions : int, optional
            The number of output partitions
        broadcast : float, bool, optional
            Whether to use a broadcast-based join in lieu of a shuffle-based join for
            supported cases. By default, a simple heuristic will be used to select
            the underlying algorithm. If a floating-point value is specified, that
            number will be used as the broadcast_bias within the simple heuristic
            (a large number makes Dask more likely to choose the broacast_join code
            path). See broadcast_join for more information.
        """
        return merge(
            self,
            right,
            how,
            on,
            left_on,
            right_on,
            left_index,
            right_index,
            suffixes,
            indicator,
            shuffle_method,
            npartitions=npartitions,
            broadcast=broadcast,
        )

    def join(
        self,
        other,
        on=None,
        how="left",
        lsuffix="",
        rsuffix="",
        shuffle_method=None,
        npartitions=None,
    ):
        if not isinstance(other, list) and not is_dask_collection(other):
            other = from_pandas(other, npartitions=1)
        if (
            not isinstance(other, list)
            and not is_dataframe_like(other._meta)
            and hasattr(other._meta, "name")
        ):
            other = new_collection(expr.ToFrame(other))

        if not isinstance(other, FrameBase):
            if not isinstance(other, list) or not all(
                isinstance(o, FrameBase) for o in other
            ):
                raise ValueError("other must be DataFrame or list of DataFrames")
            if how not in ("outer", "left"):
                raise ValueError("merge_multi only supports left or outer joins")

            other = [
                from_pandas(o, npartitions=1) if not is_dask_collection(o) else o
                for o in other
            ]

            return new_collection(
                JoinRecursive([self.expr] + [o.expr for o in other], how=how)
            )

        return self.merge(
            right=other,
            left_index=on is None,
            right_index=True,
            left_on=on,
            how=how,
            suffixes=(lsuffix, rsuffix),
            shuffle_method=shuffle_method,
            npartitions=npartitions,
        )

    def groupby(
        self, by, group_keys=True, sort=None, observed=None, dropna=None, **kwargs
    ):
        from dask_expr._groupby import GroupBy

        if isinstance(by, FrameBase) and not isinstance(by, Series):
            raise ValueError(
                f"`by` must be a column name or list of columns, got {by}."
            )

        return GroupBy(
            self,
            by,
            group_keys=group_keys,
            sort=sort,
            observed=observed,
            dropna=dropna,
            **kwargs,
        )

    def __setitem__(self, key, value):
        if isinstance(key, (tuple, list)) and isinstance(value, DataFrame):
            out = self.assign(**{k: value[c] for k, c in zip(key, value.columns)})

        elif isinstance(key, pd.Index) and not isinstance(value, DataFrame):
            out = self.assign(**{k: value for k in list(key)})
        elif (
            is_dataframe_like(key)
            or is_series_like(key)
            or isinstance(key, (DataFrame, Series))
        ):
            out = self.where(~key, value)
        elif not isinstance(key, str):
            raise NotImplementedError(f"Item assignment with {type(key)} not supported")
        else:
            out = self.assign(**{key: value})
        self._expr = out._expr

    def __delitem__(self, key):
        columns = [c for c in self.columns if c != key]
        out = self[columns]
        self._expr = out._expr

    def __getattr__(self, key):
        try:
            # Prioritize `DataFrame` attributes
            return object.__getattribute__(self, key)
        except AttributeError as err:
            try:
                # Check if key is in columns if key
                # is not a normal attribute
                if key in self.expr._meta.columns:
                    return Series(self.expr[key])
                raise err
            except AttributeError:
                # Fall back to `BaseFrame.__getattr__`
                return super().__getattr__(key)

    def __dir__(self):
        o = set(dir(type(self)))
        o.update(self.__dict__)
        o.update(set(dir(expr.Expr)))
        o.update(c for c in self.columns if (isinstance(c, str) and c.isidentifier()))
        return list(o)

    def map(self, func, na_action=None, meta=None):
        if meta is None:
            meta = expr._emulate(M.map, self, func, na_action=na_action, udf=True)
            warnings.warn(meta_warning(meta))
        return new_collection(expr.Map(self, arg=func, na_action=na_action, meta=meta))

    def __repr__(self):
        return f"<dask_expr.expr.DataFrame: expr={self.expr}>"

    def nlargest(self, n=5, columns=None, split_every=None):
        return new_collection(
            NLargest(self, n=n, _columns=columns, split_every=split_every)
        )

    def nsmallest(self, n=5, columns=None, split_every=None):
        return new_collection(
            NSmallest(self, n=n, _columns=columns, split_every=split_every)
        )

    def memory_usage(self, deep=False, index=True):
        return new_collection(MemoryUsageFrame(self, deep=deep, _index=index))

    def combine(self, other, func, fill_value=None, overwrite=True):
        other = self._create_alignable_frame(other, "outer")
        left, right = self.expr._align_divisions(other.expr, axis=0)
        return new_collection(
            expr.CombineFrame(left, right, func, fill_value, overwrite)
        )

    def drop_duplicates(
        self,
        subset=None,
        ignore_index=False,
        split_every=None,
        split_out=True,
        shuffle_method=None,
        keep="first",
    ):
        shuffle_method = _get_shuffle_preferring_order(shuffle_method)
        if keep is False:
            raise NotImplementedError("drop_duplicates with keep=False")
        # Fail early if subset is not valid, e.g. missing columns
        subset = _convert_to_list(subset)
        meta_nonempty(self._meta).drop_duplicates(subset=subset, keep=keep)
        return new_collection(
            DropDuplicates(
                self,
                subset=subset,
                ignore_index=ignore_index,
                split_out=split_out,
                split_every=split_every,
                shuffle_method=shuffle_method,
                keep=keep,
            )
        )

    def apply(self, function, *args, meta=no_default, axis=0, **kwargs):
        axis = self._validate_axis(axis)
        if axis == 0:
            msg = (
                "Dask DataFrame.apply only supports axis=1\n"
                "  Try: df.apply(func, axis=1)"
            )
            raise NotImplementedError(msg)
        if meta is no_default:
            meta = expr._emulate(
                M.apply, self, function, args=args, udf=True, axis=axis, **kwargs
            )
            warnings.warn(meta_warning(meta))
        return new_collection(
            self.expr.apply(function, *args, meta=meta, axis=axis, **kwargs)
        )

    def dropna(self, how=no_default, subset=None, thresh=no_default):
        if how is not no_default and thresh is not no_default:
            raise TypeError(
                "You cannot set both the how and thresh arguments at the same time."
            )
        subset = _convert_to_list(subset)
        return new_collection(
            expr.DropnaFrame(self, how=how, subset=subset, thresh=thresh)
        )

    @classmethod
    def _validate_axis(cls, axis=0, numeric_axis: bool = True) -> None | Literal[0, 1]:
        if axis not in (0, 1, "index", "columns", None):
            raise ValueError(f"No axis named {axis}")
        if numeric_axis:
            num_axis: dict[str | None, Literal[0, 1]] = {"index": 0, "columns": 1}
            return num_axis.get(axis, axis)
        else:
            return axis

    def sample(self, n=None, frac=None, replace=False, random_state=None):
        if n is not None:
            msg = (
                "sample does not support the number of sampled items "
                "parameter, 'n'. Please use the 'frac' parameter instead."
            )
            if isinstance(n, Number) and 0 <= n <= 1:
                warnings.warn(msg)
                frac = n
            else:
                raise ValueError(msg)

        if frac is None:
            raise ValueError("frac must not be None")

        if random_state is None:
            random_state = np.random.RandomState()

        state_data = random_state_data(self.npartitions, random_state)
        return new_collection(
            expr.Sample(self, state_data=state_data, frac=frac, replace=replace)
        )

    def rename(self, index=None, columns=None):
        if index is not None:
            raise ValueError("Cannot rename index.")
        return new_collection(expr.RenameFrame(self, columns=columns))

    def squeeze(self, axis=None):
        if axis in [None, 1]:
            if len(self.columns) == 1:
                return self[self.columns[0]]
            else:
                return self

        elif axis == 0:
            raise NotImplementedError(
                f"{type(self)} does not support squeeze along axis 0"
            )

        else:
            raise ValueError(f"No axis {axis} for object type {type(self)}")

    def explode(self, column):
        column = _convert_to_list(column)
        return new_collection(expr.ExplodeFrame(self, column=column))

    def drop(self, labels=None, axis=0, columns=None, errors="raise"):
        if columns is None and labels is None:
            raise TypeError("must either specify 'columns' or 'labels'")

        axis = _validate_axis(axis)

        if axis == 1:
            columns = labels or columns
        elif axis == 0 and columns is None:
            raise NotImplementedError(
                "Drop currently only works for axis=1 or when columns is not None"
            )
        return new_collection(expr.Drop(self, columns=columns, errors=errors))

    def to_parquet(self, path, **kwargs):
        from dask_expr.io.parquet import to_parquet

        return to_parquet(self, path, **kwargs)

    def select_dtypes(self, include=None, exclude=None):
        columns = list(
            self._meta.select_dtypes(include=include, exclude=exclude).columns
        )
        return new_collection(self.expr[columns])

    def eval(self, expr, **kwargs):
        if "inplace" in kwargs:
            raise NotImplementedError("inplace is not supported for eval")
        return new_collection(Eval(self, _expr=expr, expr_kwargs=kwargs))

    def set_index(
        self,
        other,
        drop=True,
        sorted=False,
        npartitions: int | None = None,
        divisions=None,
        sort: bool = True,
        shuffle_method=None,
        upsample: float = 1.0,
        partition_size: float = 128e6,
        append: bool = False,
        **options,
    ):
        if isinstance(other, list) and len(other) == 1:
            other = other[0]
        if isinstance(other, list):
            if any([isinstance(c, FrameBase) for c in other]):
                raise TypeError("List[FrameBase] not supported by set_index")
            else:
                raise NotImplementedError(
                    "Dask dataframe does not yet support multi-indexes.\n"
                    f"You tried to index with this index: {other}\n"
                    "Indexes must be single columns only."
                )
        if isinstance(other, DataFrame):
            raise NotImplementedError(
                "Dask dataframe does not yet support multi-indexes.\n"
                f"You tried to index with a frame with these columns: {list(other.columns)}\n"
                "Indexes must be single columns only."
            )
        if isinstance(other, Series):
            if other._name == self.index._name:
                return self
        elif other == self.index.name:
            return self

        if divisions is not None:
            check_divisions(divisions)

        if (sorted or not sort) and npartitions is not None:
            raise ValueError(
                "Specifying npartitions with sort=False or sorted=True is not "
                "supported. Call `repartition` afterwards."
            )

        if sorted:
            if divisions is not None and len(divisions) - 1 != self.npartitions:
                msg = (
                    "When doing `df.set_index(col, sorted=True, divisions=...)`, "
                    "divisions indicates known splits in the index column. In this "
                    "case divisions must be the same length as the existing "
                    "divisions in `df`\n\n"
                    "If the intent is to repartition into new divisions after "
                    "setting the index, you probably want:\n\n"
                    "`df.set_index(col, sorted=True).repartition(divisions=divisions)`"
                )
                raise ValueError(msg)
            result = new_collection(
                SetIndexBlockwise(
                    self, other, drop, new_divisions=divisions, append=append
                )
            )
            return result.compute_current_divisions(set_divisions=True)
        elif not sort:
            return new_collection(
                SetIndexBlockwise(self, other, drop, None, append=append)
            )

        return new_collection(
            SetIndex(
                self,
                other,
                drop,
                user_divisions=divisions,
                npartitions=npartitions,
                upsample=upsample,
                partition_size=partition_size,
                shuffle_method=shuffle_method,
                append=append,
                options=options,
            )
        )

    def sort_values(
        self,
        by: str | list[str],
        npartitions: int | None = None,
        ascending: bool | list[bool] = True,
        na_position: Literal["first"] | Literal["last"] = "last",
        partition_size: float = 128e6,
        sort_function: Callable[[pd.DataFrame], pd.DataFrame] | None = None,
        sort_function_kwargs: Mapping[str, Any] | None = None,
        upsample: float = 1.0,
        ignore_index: bool | None = False,
        shuffle_method: str | None = None,
        **options,
    ):
        """See DataFrame.sort_values for docstring"""
        if na_position not in ("first", "last"):
            raise ValueError("na_position must be either 'first' or 'last'")
        if not isinstance(by, list):
            by = [by]
        if any(not isinstance(b, str) for b in by):
            raise NotImplementedError(
                "Dataframes only support sorting by named columns which must be passed as a "
                "string or a list of strings.\n"
                "You passed %s" % str(by)
            )

        if not isinstance(ascending, bool) and self.npartitions > 1:
            # support [True] as input
            if (
                isinstance(ascending, list)
                and len(ascending) == 1
                and isinstance(ascending[0], bool)
            ):
                ascending = ascending[0]
            else:
                raise NotImplementedError(
                    f"Dask currently only supports a single boolean for ascending. You passed {str(ascending)}"
                )

        return new_collection(
            SortValues(
                self,
                by,
                ascending,
                na_position,
                npartitions,
                partition_size,
                sort_function,
                sort_function_kwargs,
                upsample,
                ignore_index,
                shuffle_method,
                options=options,
            )
        )

    def query(self, expr, **kwargs):
        return new_collection(Query(self, expr, kwargs))

    def mode(self, dropna=True, split_every=False, numeric_only=False):
        modes = []
        for _, col in self.items():
            if numeric_only and not pd.api.types.is_numeric_dtype(col.dtype):
                continue
            modes.append(col.mode(dropna=dropna, split_every=split_every))
        return concat(modes, axis=1)

    def add_prefix(self, prefix):
        return new_collection(expr.AddPrefix(self, prefix))

    def add_suffix(self, suffix):
        return new_collection(expr.AddSuffix(self, suffix))

    def pivot_table(self, index, columns, values, aggfunc="mean"):
        return pivot_table(self, index, columns, values, aggfunc)

    @property
    def iloc(self):
        from dask_expr._indexing import ILocIndexer

        return ILocIndexer(self)

    def _comparison_op(self, expr_cls, other, level, axis):
        if level is not None:
            raise NotImplementedError("level must be None")
        axis = self._validate_axis(axis)
        return new_collection(expr_cls(self, other, axis))

    def lt(self, other, level=None, axis=0):
        return self._comparison_op(expr.LTFrame, other, level, axis)

    def le(self, other, level=None, axis=0):
        return self._comparison_op(expr.LEFrame, other, level, axis)

    def gt(self, other, level=None, axis=0):
        return self._comparison_op(expr.GTFrame, other, level, axis)

    def ge(self, other, level=None, axis=0):
        return self._comparison_op(expr.GEFrame, other, level, axis)

    def ne(self, other, level=None, axis=0):
        return self._comparison_op(expr.NEFrame, other, level, axis)

    def eq(self, other, level=None, axis=0):
        return self._comparison_op(expr.EQFrame, other, level, axis)

    def categorize(self, columns=None, index=None, split_every=None, **kwargs):
        """Convert columns of the DataFrame to category dtype.

        .. warning:: This method eagerly computes the categories of the chosen columns.

        Parameters
        ----------
        columns : list, optional
            A list of column names to convert to categoricals. By default any
            column with an object dtype is converted to a categorical, and any
            unknown categoricals are made known.
        index : bool, optional
            Whether to categorize the index. By default, object indices are
            converted to categorical, and unknown categorical indices are made
            known. Set True to always categorize the index, False to never.
        split_every : int, optional
            Group partitions into groups of this size while performing a
            tree-reduction. If set to False, no tree-reduction will be used.
        kwargs
            Keyword arguments are passed on to compute.
        """
        df = self
        meta = df._meta
        if columns is None:
            columns = list(meta.select_dtypes(["object", "string", "category"]).columns)
        elif is_scalar(columns):
            columns = [columns]

        # Filter out known categorical columns
        columns = [
            c
            for c in columns
            if not (is_categorical_dtype(meta[c]) and has_known_categories(meta[c]))
        ]

        if index is not False:
            if is_categorical_dtype(meta.index):
                index = not has_known_categories(meta.index)
            elif index is None:
                index = str(meta.index.dtype) in ("object", "string")

        # Nothing to do
        if not len(columns) and index is False:
            return df

        from dask_expr._collection import new_collection

        # Eagerly compute the categories
        categories, index = new_collection(
            GetCategories(self, columns=columns, index=index, split_every=split_every)
        ).compute()

        # Some operations like get_dummies() rely on the order of categories
        categories = {k: v.sort_values() for k, v in categories.items()}

        # Categorize each partition
        return new_collection(Categorize(self, categories, index))

    def nunique(self, axis=0, dropna=True, split_every=False):
        if axis == 1:
            return new_collection(expr.NUniqueColumns(self, axis=axis, dropna=dropna))
        else:
            return concat(
                [
                    col.nunique(dropna=dropna, split_every=split_every).to_series(name)
                    for name, col in self.items()
                ]
            )

    def quantile(self, q=0.5, axis=0, numeric_only=False, method="default"):
        """Approximate row-wise and precise column-wise quantiles of DataFrame

        Parameters
        ----------
        q : list/array of floats, default 0.5 (50%)
            Iterable of numbers ranging from 0 to 1 for the desired quantiles
        axis : {0, 1, 'index', 'columns'} (default 0)
            0 or 'index' for row-wise, 1 or 'columns' for column-wise
        method : {'default', 'tdigest', 'dask'}, optional
            What method to use. By default will use dask's internal custom
            algorithm (``'dask'``).  If set to ``'tdigest'`` will use tdigest
            for floats and ints and fallback to the ``'dask'`` otherwise.
        """
        allowed_methods = ["default", "dask", "tdigest"]
        if method not in allowed_methods:
            raise ValueError("method can only be 'default', 'dask' or 'tdigest'")
        meta = make_meta(
            meta_nonempty(self._meta).quantile(
                q=q, numeric_only=numeric_only, axis=axis
            )
        )

        if axis == 1:
            if isinstance(q, list):
                # Not supported, the result will have current index as columns
                raise ValueError("'q' must be scalar when axis=1 is specified")

            return self.map_partitions(
                M.quantile,
                q,
                axis,
                enforce_metadata=False,
                meta=meta,
                numeric_only=numeric_only,
            )

        if numeric_only:
            frame = self.select_dtypes(
                "number", exclude=[np.timedelta64, np.datetime64]
            )
        else:
            frame = self

        collections = []
        for _, col in frame.items():
            collections.append(col.quantile(q=q, method=method))

        if len(collections) > 0 and isinstance(collections[0], Scalar):
            return _from_scalars(collections, meta, frame.expr.columns)

        return concat(collections, axis=1)

    def median(self, axis=0, numeric_only=False):
        if axis == 1 or self.npartitions == 1:
            return self.median_approximate(axis=axis, numeric_only=numeric_only)
        raise NotImplementedError(
            "Dask doesn't implement an exact median in all cases as this is hard to do in parallel. "
            "See the `median_approximate` method instead, which uses an approximate algorithm."
        )

    def median_approximate(self, axis=0, method="default", numeric_only=False):
        return self.quantile(
            axis=axis, method=method, numeric_only=numeric_only
        ).rename(None)

    def describe(
        self,
        split_every=False,
        percentiles=None,
        percentiles_method="default",
        include=None,
        exclude=None,
    ):
        # TODO: duplicated columns
        if include is None and exclude is None:
            _include = [np.number, np.timedelta64, np.datetime64]
            columns = self._meta.select_dtypes(include=_include).columns
            if len(columns) == 0:
                columns = self._meta.columns
        elif include == "all":
            if exclude is not None:
                raise ValueError("exclude must be None when include is 'all'")
            columns = self._meta.columns
        else:
            columns = self._meta.select_dtypes(include=include, exclude=exclude).columns

        stats = [
            self[col].describe(
                split_every=split_every,
                percentiles=percentiles,
                percentiles_method=percentiles_method,
            )
            for col in columns
        ]
        return concat(stats, axis=1)

    def pop(self, item):
        out = self[item]
        self._expr = expr.Drop(self, columns=[item])
        return out

    def info(self, buf=None, verbose=False, memory_usage=False):
        """
        Concise summary of a Dask DataFrame
        """
        if buf is None:
            import sys

            buf = sys.stdout
        lines = [str(type(self)).replace("._collection", "")]

        if len(self.columns) == 0:
            lines.append(f"{type(self.index._meta).__name__}: 0 entries")
            lines.append(f"Empty {type(self).__name__}")
            put_lines(buf, lines)
            return

        # Group and execute the required computations
        computations = {}
        if verbose:
            computations.update({"index": self.index, "count": self.count()})
        if memory_usage:
            computations["memory_usage"] = self.memory_usage(deep=True, index=True)

        computations = dict(zip(computations.keys(), compute(*computations.values())))

        if verbose:
            import textwrap

            index = computations["index"]
            counts = computations["count"]
            lines.append(index_summary(index))
            lines.append(f"Data columns (total {len(self.columns)} columns):")

            from pandas.io.formats.printing import pprint_thing

            space = max(len(pprint_thing(k)) for k in self.columns) + 1
            column_width = max(space, 7)

            header = (
                textwrap.dedent(
                    """\
             #   {{column:<{column_width}}} Non-Null Count  Dtype
            ---  {{underl:<{column_width}}} --------------  -----"""
                )
                .format(column_width=column_width)
                .format(column="Column", underl="------")
            )
            column_template = textwrap.dedent(
                """\
            {{i:^3}}  {{name:<{column_width}}} {{count}} non-null      {{dtype}}""".format(
                    column_width=column_width
                )
            )
            column_info = [
                column_template.format(
                    i=pprint_thing(i),
                    name=pprint_thing(name),
                    count=pprint_thing(count),
                    dtype=pprint_thing(dtype),
                )
                for i, (name, count, dtype) in enumerate(
                    # NOTE: Use `counts.values` for cudf support
                    zip(self.columns, counts.values, self.dtypes)
                )
            ]
            lines.extend(header.split("\n"))
        else:
            column_info = [index_summary(self.columns, name="Columns")]

        lines.extend(column_info)
        dtype_counts = [
            "%s(%d)" % k for k in sorted(self.dtypes.value_counts().items(), key=str)
        ]
        lines.append("dtypes: {}".format(", ".join(dtype_counts)))

        if memory_usage:
            memory_int = computations["memory_usage"].sum()
            lines.append(f"memory usage: {memory_repr(memory_int)}\n")

        put_lines(buf, lines)

    def cov(self, min_periods=None, numeric_only=False, split_every=False):
        return self._cov(min_periods, numeric_only, split_every)

    def corr(
        self,
        method="pearson",
        min_periods=None,
        numeric_only=False,
        split_every=False,
    ):
        return self._corr(method, min_periods, numeric_only, split_every)


class Series(FrameBase):
    """Series-like Expr Collection"""

    _accessors: ClassVar[set[str]] = set()
    _partition_type = pd.Series

    @property
    def shape(self):
        return (self.size,)

    @property
    def axes(self):
        return [self.index]

    @property
    def _elemwise(self):
        return elemwise

    def __dir__(self):
        o = set(dir(type(self)))
        o.update(self.__dict__)
        o.update(set(dir(expr.Expr)))
        for accessor in ["cat", "str"]:
            if not hasattr(self._meta, accessor):
                o.remove(accessor)
        return list(o)

    def __contains__(self, item):
        raise NotImplementedError(
            "Using 'in' to test for membership is not supported. Use the values instead"
        )

    def __iter__(self):
        frame = self.optimize()
        for i in range(self.npartitions):
            s = frame.get_partition(i).compute()
            yield from s

    def __getitem__(self, key):
        if isinstance(key, Series) or self.npartitions == 1:
            return super().__getitem__(key)
        return self.loc[key]

    @property
    def name(self):
        return self.expr._meta.name

    @name.setter
    def name(self, name):
        self._expr = self.rename(index=name)._expr

    @property
    def dtype(self):
        return self.expr._meta.dtype

    @property
    def nbytes(self):
        return new_collection(self.expr.nbytes)

    def keys(self):
        return self.index

    def __array_ufunc__(self, numpy_ufunc, method, *inputs, **kwargs):
        out = kwargs.get("out", ())
        for x in inputs + out:
            # ufuncs work with 0-dimensional NumPy ndarrays
            # so we don't want to raise NotImplemented
            if isinstance(x, np.ndarray) and x.shape == ():
                continue
            elif not isinstance(
                x, (Number, Scalar, FrameBase, Array, pd.DataFrame, pd.Series, pd.Index)
            ):
                return NotImplemented

        if method == "__call__":
            if numpy_ufunc.signature is not None:
                return NotImplemented
            if numpy_ufunc.nout > 1:
                # ufuncs with multiple output values
                # are not yet supported for frames
                return NotImplemented
            else:
                return elemwise(numpy_ufunc, *inputs, **kwargs)
        else:
            # ufunc methods are not yet supported for frames
            return NotImplemented

    def __array_wrap__(self, array, context=None):
        if isinstance(context, tuple) and len(context) > 0:
            if isinstance(context[1][0], np.ndarray) and context[1][0].shape == ():
                index = None
            else:
                index = context[1][0].index
        else:
            try:
                import inspect

                method_name = f"`{inspect.stack()[3][3]}`"
            except IndexError:
                method_name = "This method"
            raise NotImplementedError(
                f"{method_name} is not implemented for `dask.dataframe.Series`."
            )

        return meta_series_constructor(self)(array, index=index, name=self.name)

    def map(self, arg, na_action=None, meta=None):
        if isinstance(arg, Series):
            if not expr.are_co_aligned(self.expr, arg.expr):
                if not self.divisions == arg.divisions:
                    raise NotImplementedError(
                        "passing a Series as arg isn't implemented yet"
                    )
        if meta is None:
            meta = expr._emulate(M.map, self, arg, na_action=na_action, udf=True)
            warnings.warn(meta_warning(meta))
        return new_collection(expr.Map(self, arg=arg, na_action=na_action, meta=meta))

    def clip(self, lower=None, upper=None, axis=None, **kwargs):
        axis = self._validate_axis(axis)
        return new_collection(self.expr.clip(lower, upper, axis))

    def __repr__(self):
        return f"<dask_expr.expr.Series: expr={self.expr}>"

    def to_frame(self, name=no_default):
        return new_collection(expr.ToFrame(self, name=name))

    def _comparison_op(self, expr_cls, other, level, fill_value, axis):
        if level is not None:
            raise NotImplementedError("level must be None")
        self._validate_axis(axis)
        return new_collection(expr_cls(self, other, fill_value=fill_value))

    def lt(self, other, level=None, fill_value=None, axis=0):
        return self._comparison_op(expr.LTSeries, other, level, fill_value, axis)

    def le(self, other, level=None, fill_value=None, axis=0):
        return self._comparison_op(expr.LESeries, other, level, fill_value, axis)

    def gt(self, other, level=None, fill_value=None, axis=0):
        return self._comparison_op(expr.GTSeries, other, level, fill_value, axis)

    def ge(self, other, level=None, fill_value=None, axis=0):
        return self._comparison_op(expr.GESeries, other, level, fill_value, axis)

    def ne(self, other, level=None, fill_value=None, axis=0):
        return self._comparison_op(expr.NESeries, other, level, fill_value, axis)

    def eq(self, other, level=None, fill_value=None, axis=0):
        return self._comparison_op(expr.EQSeries, other, level, fill_value, axis)

    def value_counts(
        self,
        sort=None,
        ascending=False,
        dropna=True,
        normalize=False,
        split_every=None,
        split_out=no_default,
    ):
        if split_out is no_default:
            if isinstance(self.dtype, CategoricalDtype):
                # unobserved categories are a pain
                split_out = 1
            else:
                split_out = True
        length = None
        if (split_out > 1 or split_out is True) and normalize:
            frame = self if not dropna else self.dropna()
            length = Len(frame)

        return new_collection(
            ValueCounts(
                self, sort, ascending, dropna, normalize, split_every, split_out, length
            )
        )

    def mode(self, dropna=True, split_every=False):
        return new_collection(self.expr.mode(dropna, split_every))

    def nlargest(self, n=5, split_every=None):
        return new_collection(NLargest(self, n=n, split_every=split_every))

    def nsmallest(self, n=5, split_every=None):
        return new_collection(NSmallest(self, n=n, split_every=split_every))

    def memory_usage(self, deep=False, index=True):
        return new_collection(MemoryUsageFrame(self, deep=deep, _index=index))

    def unique(self, split_every=None, split_out=True, shuffle_method=None):
        shuffle_method = _get_shuffle_preferring_order(shuffle_method)
        return new_collection(Unique(self, split_every, split_out, shuffle_method))

    def nunique(self, dropna=True, split_every=False, split_out=True):
        uniqs = self.drop_duplicates(split_every=split_every, split_out=split_out)
        if dropna:
            # count mimics pandas behavior and excludes NA values
            if isinstance(uniqs, Index):
                uniqs = uniqs.to_series()
            return uniqs.count()
        else:
            return uniqs.size

    def drop_duplicates(
        self,
        ignore_index=False,
        split_every=None,
        split_out=True,
        shuffle_method=None,
        keep="first",
    ):
        shuffle_method = _get_shuffle_preferring_order(shuffle_method)
        if keep is False:
            raise NotImplementedError("drop_duplicates with keep=False")
        return new_collection(
            DropDuplicates(
                self,
                ignore_index=ignore_index,
                split_out=split_out,
                split_every=split_every,
                shuffle_method=shuffle_method,
                keep=keep,
            )
        )

    def apply(self, function, *args, meta=no_default, axis=0, **kwargs):
        self._validate_axis(axis)
        if meta is no_default:
            meta = expr._emulate(M.apply, self, function, args=args, udf=True, **kwargs)
            warnings.warn(meta_warning(meta))
        return new_collection(self.expr.apply(function, *args, meta=meta, **kwargs))

    @classmethod
    def _validate_axis(cls, axis=0, numeric_axis: bool = True) -> None | Literal[0, 1]:
        if axis not in (0, "index", None):
            raise ValueError(f"No axis named {axis} for Series")
        if numeric_axis:
            num_axis: dict[str | None, Literal[0, 1]] = {"index": 0}
            return num_axis.get(axis, axis)
        else:
            return axis

    def squeeze(self):
        return self

    def dropna(self):
        return new_collection(expr.DropnaSeries(self))

    def between(self, left, right, inclusive="both"):
        return new_collection(
            expr.Between(self, left=left, right=right, inclusive=inclusive)
        )

    def combine(self, other, func, fill_value=None):
        other = self._create_alignable_frame(other, "outer")
        left, right = self.expr._align_divisions(other.expr, axis=0)
        return new_collection(expr.CombineSeries(left, right, func, fill_value))

    def explode(self):
        return new_collection(expr.ExplodeSeries(self))

    def add_prefix(self, prefix):
        return new_collection(expr.AddPrefixSeries(self, prefix))

    def add_suffix(self, suffix):
        return new_collection(expr.AddSuffixSeries(self, suffix))

    cat = CachedAccessor("cat", CategoricalAccessor)
    dt = CachedAccessor("dt", DatetimeAccessor)
    str = CachedAccessor("str", StringAccessor)

    def _repartition_quantiles(self, npartitions, upsample=1.0, random_state=None):
        return new_collection(
            RepartitionQuantiles(self, npartitions, upsample, random_state)
        )

    def groupby(self, by, **kwargs):
        from dask_expr._groupby import SeriesGroupBy

        return SeriesGroupBy(self, by, **kwargs)

    def rename(self, index, sorted_index=False):
        return new_collection(expr.RenameSeries(self, index, sorted_index))

    def quantile(self, q=0.5, method="default"):
        """Approximate quantiles of Series

        Parameters
        ----------
        q : list/array of floats, default 0.5 (50%)
            Iterable of numbers ranging from 0 to 1 for the desired quantiles
        method : {'default', 'tdigest', 'dask'}, optional
            What method to use. By default will use dask's internal custom
            algorithm (``'dask'``).  If set to ``'tdigest'`` will use tdigest
            for floats and ints and fallback to the ``'dask'`` otherwise.
        """
        _raise_if_object_series(self, "quantile")
        allowed_methods = ["default", "dask", "tdigest"]
        if method not in allowed_methods:
            raise ValueError("method can only be 'default', 'dask' or 'tdigest'")
        return new_collection(SeriesQuantile(self, q, method))

    def median(self):
        if self.npartitions == 1:
            return self.median_approximate()
        raise NotImplementedError(
            "Dask doesn't implement an exact median in all cases as this is hard to do in parallel. "
            "See the `median_approximate` method instead, which uses an approximate algorithm."
        )

    def median_approximate(self, method="default"):
        return self.quantile(method=method)

    def cov(self, other, min_periods=None, split_every=False):
        if not isinstance(other, Series):
            raise TypeError("other must be a dask.dataframe.Series")
        df = concat([self, other], axis=1)
        return df._cov(min_periods, True, split_every, scalar=True)

    def corr(self, other, method="pearson", min_periods=None, split_every=False):
        if not isinstance(other, Series):
            raise TypeError("other must be a dask.dataframe.Series")
        df = concat([self, other], axis=1)
        return df._corr(method, min_periods, True, split_every, scalar=True)

    def autocorr(self, lag=1, split_every=False):
        if not isinstance(lag, Integral):
            raise TypeError("lag must be an integer")
        return self.corr(self if lag == 0 else self.shift(lag), split_every=split_every)

    def describe(
        self,
        split_every=False,
        percentiles=None,
        percentiles_method="default",
        include=None,
        exclude=None,
    ):
        if (
            is_numeric_dtype(self.dtype)
            and not is_bool_dtype(self.dtype)
            or is_timedelta64_dtype(self.dtype)
            or is_datetime64_any_dtype(self.dtype)
        ):
            return new_collection(
                DescribeNumeric(self, split_every, percentiles, percentiles_method)
            )
        else:
            return new_collection(
                DescribeNonNumeric(self, split_every, percentiles, percentiles_method)
            )

    @property
    def is_monotonic_increasing(self):
        return new_collection(IsMonotonicIncreasing(self))

    @property
    def is_monotonic_decreasing(self):
        return new_collection(IsMonotonicDecreasing(self))


for name in [
    "add",
    "sub",
    "mul",
    "div",
    "divide",
    "truediv",
    "floordiv",
    "mod",
    "pow",
    "radd",
    "rsub",
    "rmul",
    "rdiv",
    "rtruediv",
    "rfloordiv",
    "rmod",
    "rpow",
]:
    assert not hasattr(DataFrame, name), name
    setattr(DataFrame, name, _wrap_expr_method_operator(name, DataFrame))

    assert not hasattr(Series, name), name
    setattr(Series, name, _wrap_expr_method_operator(name, Series))


class Index(Series):
    """Index-like Expr Collection"""

    _accessors: ClassVar[set[str]] = set()
    _partition_type = pd.Index

    _dt_attributes = {
        "nanosecond",
        "microsecond",
        "millisecond",
        "dayofyear",
        "minute",
        "hour",
        "day",
        "dayofweek",
        "second",
        "week",
        "weekday",
        "weekofyear",
        "month",
        "quarter",
        "year",
    }

    _cat_attributes = {
        "known",
        "as_known",
        "as_unknown",
        "add_categories",
        "categories",
        "remove_categories",
        "reorder_categories",
        "as_ordered",
        "codes",
        "remove_unused_categories",
        "set_categories",
        "as_unordered",
        "ordered",
        "rename_categories",
    }

    def __getattr__(self, key):
        if (
            isinstance(self._meta.dtype, pd.CategoricalDtype)
            and key in self._cat_attributes
        ):
            return getattr(self.cat, key)
        elif key in self._dt_attributes:
            return getattr(self.dt, key)

        if hasattr(super(), key):  # Doesn't trigger super().__getattr__
            # Not a magic attribute. This is a real method or property of Series that
            # has been overridden by RaiseAttributeError().
            raise AttributeError(
                f"{self.__class__.__name__!r} object has no attribute {key!r}"
            )
        return super().__getattr__(key)

    def __repr__(self):
        return f"<dask_expr.expr.Index: expr={self.expr}>"

    def __array_wrap__(self, array, context=None):
        return pd.Index(array, name=self.name)

    def to_series(self, index=None, name=no_default):
        if index is not None:
            raise NotImplementedError
        return new_collection(expr.ToSeriesIndex(self, index=index, name=name))

    def to_frame(self, index=True, name=no_default):
        if not index:
            raise NotImplementedError
        return new_collection(expr.ToFrameIndex(self, index=index, name=name))

    def memory_usage(self, deep=False):
        return new_collection(MemoryUsageIndex(self, deep=deep))

    def shift(self, periods=1, freq=None):
        return new_collection(expr.ShiftIndex(self, periods, freq))

    def map(self, arg, na_action=None, meta=None, is_monotonic=False):
        if isinstance(arg, Series):
            if not expr.are_co_aligned(self.expr, arg.expr):
                if not self.divisions == arg.divisions:
                    raise NotImplementedError(
                        "passing a Series as arg isn't implemented yet"
                    )
        if meta is None:
            meta = expr._emulate(M.map, self, arg, na_action=na_action, udf=True)
            warnings.warn(meta_warning(meta))
        return new_collection(
            expr.Map(
                self, arg=arg, na_action=na_action, meta=meta, is_monotonic=is_monotonic
            )
        )

    def __dir__(self):
        o = set(dir(type(self)))
        o.update(self.__dict__)
        o.update(set(dir(expr.Expr)))
        o.update(self._dt_attributes)
        if isinstance(self.dtype, pd.CategoricalDtype):
            o.update(self._cat_attributes)
        return list(o)

    # Methods and properties of Series that are not implemented on Index

    def count(self, split_every=False):
        return new_collection(IndexCount(self, split_every))

    index = RaiseAttributeError()
    sum = RaiseAttributeError()
    prod = RaiseAttributeError()
    mean = RaiseAttributeError()
    std = RaiseAttributeError()
    var = RaiseAttributeError()
    idxmin = RaiseAttributeError()
    idxmax = RaiseAttributeError()


class Scalar(FrameBase):
    """Scalar Expr Collection"""

    def __repr__(self):
        return f"<dask_expr.expr.Scalar: expr={self.expr}>"

    def __bool__(self):
        raise TypeError(
            f"Trying to convert {self} to a boolean value. Because Dask objects are "
            "lazily evaluated, they cannot be converted to a boolean value or used "
            "in boolean conditions like if statements. Try calling .compute() to "
            "force computation prior to converting to a boolean value or using in "
            "a conditional statement."
        )

    def __dask_postcompute__(self):
        return first, ()

    def to_series(self, index=0) -> Series:
        return new_collection(expr.ScalarToSeries(self, index=index))

    def __array__(self):
        # array interface is required to support pandas instance + Scalar
        # Otherwise, above op results in pd.Series of Scalar (object dtype)
        return np.asarray(self.compute())


def new_collection(expr):
    """Create new collection from an expr"""

    meta = expr._meta
    expr._name  # Ensure backend is imported
    if is_dataframe_like(meta):
        return DataFrame(expr)
    elif is_series_like(meta):
        return Series(expr)
    elif is_index_like(meta):
        return Index(expr)
    else:
        return Scalar(expr)


def optimize(collection, fuse=True):
    return new_collection(expr.optimize(collection.expr, fuse=fuse))


def from_pandas(data, npartitions=None, sort=True, chunksize=None):
    if chunksize is not None and npartitions is not None:
        raise ValueError("Exactly one of npartitions and chunksize must be specified.")
    elif chunksize is None and npartitions is None:
        npartitions = 1

    if not has_parallel_type(data):
        raise TypeError("Input must be a pandas DataFrame or Series.")

    if data.index.isna().any() and not _is_any_real_numeric_dtype(data.index):
        raise NotImplementedError(
            "Index in passed data is non-numeric and contains nulls, which Dask does not entirely support.\n"
            "Consider passing `data.loc[~data.isna()]` instead."
        )

    if npartitions is not None and not isinstance(npartitions, int):
        raise TypeError(
            "Please provide npartitions as an int, or possibly as None if you specify chunksize."
        )
    elif chunksize is not None and not isinstance(chunksize, int):
        raise TypeError(
            "Please provide chunksize as an int, or possibly as None if you specify npartitions."
        )

    from dask_expr.io.io import FromPandas

    return new_collection(
        FromPandas(
            _BackendData(data.copy()),
            npartitions=npartitions,
            sort=sort,
            chunksize=chunksize,
        )
    )


def from_array(arr, chunksize=50_000, columns=None, meta=None):
    import dask.array as da

    if isinstance(arr, da.Array):
        return from_dask_array(arr, columns=columns, meta=meta)

    from dask_expr.io.io import FromArray

    return new_collection(
        FromArray(
            arr,
            chunksize=chunksize,
            original_columns=columns,
            meta=meta,
        )
    )


def from_graph(*args, **kwargs):
    from dask_expr.io.io import FromGraph

    return new_collection(FromGraph(*args, **kwargs))


def from_dict(
    data,
    npartitions,
    orient="columns",
    dtype=None,
    columns=None,
    constructor=pd.DataFrame,
):
    """
    Construct a Dask DataFrame from a Python Dictionary

    Parameters
    ----------
    data : dict
        Of the form {field : array-like} or {field : dict}.
    npartitions : int
        The number of partitions of the index to create. Note that depending on
        the size and index of the dataframe, the output may have fewer
        partitions than requested.
    orient : {'columns', 'index', 'tight'}, default 'columns'
        The "orientation" of the data. If the keys of the passed dict
        should be the columns of the resulting DataFrame, pass 'columns'
        (default). Otherwise if the keys should be rows, pass 'index'.
        If 'tight', assume a dict with keys
        ['index', 'columns', 'data', 'index_names', 'column_names'].
    dtype: bool
        Data type to force, otherwise infer.
    columns: string, optional
        Column labels to use when ``orient='index'``. Raises a ValueError
        if used with ``orient='columns'`` or ``orient='tight'``.
    constructor: class, default pd.DataFrame
        Class with which ``from_dict`` should be called with.

    Examples
    --------
    >>> import dask.dataframe as dd
    >>> ddf = dd.from_dict({"num1": [1, 2, 3, 4], "num2": [7, 8, 9, 10]}, npartitions=2)
    """

    collection_types = {type(v) for v in data.values() if is_dask_collection(v)}
    if collection_types:
        raise NotImplementedError(
            "from_dict doesn't currently support Dask collections as inputs. "
            f"Objects of type {collection_types} were given in the input dict."
        )

    return from_pandas(
        constructor.from_dict(data, orient, dtype, columns),
        npartitions,
    )


def from_dask_dataframe(ddf: _Frame, optimize: bool = True) -> FrameBase:
    """Create a dask-expr collection from a dask-dataframe collection

    Parameters
    ----------
    optimize
        Whether to optimize the graph before conversion.
    """
    graph = ddf.dask
    if optimize:
        graph = ddf.__dask_optimize__(graph, ddf.__dask_keys__())
    return from_graph(graph, ddf._meta, ddf.divisions, ddf._name)


def from_dask_array(x, columns=None, index=None, meta=None):
    from dask.dataframe.io import from_dask_array

    if isinstance(index, FrameBase):
        index = index.to_dask_dataframe()

    df = from_dask_array(x, columns=columns, index=index, meta=meta)
    return from_dask_dataframe(df, optimize=True)


def read_csv(
    path,
    *args,
    header="infer",
    usecols=None,
    dtype_backend=None,
    storage_options=None,
    **kwargs,
):
    from dask_expr.io.csv import ReadCSV

    if not isinstance(path, str):
        path = stringify_path(path)
    return new_collection(
        ReadCSV(
            path,
            columns=usecols,
            dtype_backend=dtype_backend,
            storage_options=storage_options,
            kwargs=kwargs,
            header=header,
        )
    )


def read_table(
    path,
    *args,
    header="infer",
    usecols=None,
    dtype_backend=None,
    storage_options=None,
    **kwargs,
):
    from dask_expr.io.csv import ReadTable

    if not isinstance(path, str):
        path = stringify_path(path)
    return new_collection(
        ReadTable(
            path,
            columns=usecols,
            dtype_backend=dtype_backend,
            storage_options=storage_options,
            kwargs=kwargs,
            header=header,
        )
    )


def read_parquet(
    path=None,
    columns=None,
    filters=None,
    categories=None,
    index=None,
    storage_options=None,
    dtype_backend=None,
    calculate_divisions=False,
    ignore_metadata_file=False,
    metadata_task_size=None,
    split_row_groups="infer",
    blocksize="default",
    aggregate_files=None,
    parquet_file_extension=(".parq", ".parquet", ".pq"),
    filesystem="fsspec",
    engine=None,
    **kwargs,
):
    from dask_expr.io.parquet import ReadParquet, _set_parquet_engine

    if not isinstance(path, str):
        path = stringify_path(path)

    kwargs["dtype_backend"] = dtype_backend

    if filters is not None:
        for filter in flatten(filters, container=list):
            col, op, val = filter
            if op == "in" and not isinstance(val, (set, list, tuple)):
                raise TypeError("Value of 'in' filter must be a list, set or tuple.")

    return new_collection(
        ReadParquet(
            path,
            columns=_convert_to_list(columns),
            filters=filters,
            categories=categories,
            index=index,
            storage_options=storage_options,
            calculate_divisions=calculate_divisions,
            ignore_metadata_file=ignore_metadata_file,
            metadata_task_size=metadata_task_size,
            split_row_groups=split_row_groups,
            blocksize=blocksize,
            aggregate_files=aggregate_files,
            parquet_file_extension=parquet_file_extension,
            filesystem=filesystem,
            engine=_set_parquet_engine(engine),
            kwargs=kwargs,
            _series=isinstance(columns, str),
        )
    )


def concat(
    dfs,
    axis=0,
    join="outer",
    ignore_unknown_divisions=False,
    ignore_order=False,
    interleave_partitions=False,
    **kwargs,
):
    if not isinstance(dfs, list):
        raise TypeError("dfs must be a list of DataFrames/Series objects")
    if len(dfs) == 0:
        raise ValueError("No objects to concatenate")
    if len(dfs) == 1:
        if axis == 1 and isinstance(dfs[0], Series):
            return dfs[0].to_frame()
        return dfs[0]

    if join not in ("inner", "outer"):
        raise ValueError("'join' must be 'inner' or 'outer'")

    dfs = [from_pandas(df) if not isinstance(df, FrameBase) else df for df in dfs]

    if axis == 1:
        dfs = [df for df in dfs if len(df.columns) > 0 or isinstance(df, Series)]

    return new_collection(
        Concat(
            join,
            ignore_order,
            kwargs,
            axis,
            ignore_unknown_divisions,
            interleave_partitions,
            *dfs,
        )
    )


def merge(
    left,
    right,
    how="inner",
    on=None,
    left_on=None,
    right_on=None,
    left_index=False,
    right_index=False,
    suffixes=("_x", "_y"),
    indicator=False,
    shuffle_method=None,
    npartitions=None,
    broadcast=None,
):
    for o in [on, left_on, right_on]:
        if isinstance(o, FrameBase):
            raise NotImplementedError()
    if not on and not left_on and not right_on and not left_index and not right_index:
        on = [c for c in left.columns if c in right.columns]
        if not on:
            left_index = right_index = True

    if on and not left_on and not right_on:
        left_on = right_on = on

    supported_how = ("left", "right", "outer", "inner")
    if how not in supported_how:
        raise ValueError(
            f"dask.dataframe.merge does not support how='{how}'."
            f"Options are: {supported_how}."
        )

    # Transform pandas objects into dask.dataframe objects
    if not is_dask_collection(left):
        if right_index and left_on:  # change to join on index
            left = left.set_index(left[left_on])
            left_on = None
            left_index = True
        left = from_pandas(left, npartitions=1)

    if not is_dask_collection(right):
        if left_index and right_on:  # change to join on index
            right = right.set_index(right[right_on])
            right_on = None
            right_index = True
        right = from_pandas(right, npartitions=1)

    assert is_dataframe_like(right._meta)
    if left_on and right_on:
        warn_dtype_mismatch(left, right, left_on, right_on)

    return new_collection(
        Merge(
            left,
            right,
            how=how,
            left_on=left_on,
            right_on=right_on,
            left_index=left_index,
            right_index=right_index,
            suffixes=suffixes,
            indicator=indicator,
            shuffle_method=shuffle_method,
            _npartitions=npartitions,
            broadcast=broadcast,
        )
    )


def merge_asof(
    left,
    right,
    on=None,
    left_on=None,
    right_on=None,
    left_index=False,
    right_index=False,
    by=None,
    left_by=None,
    right_by=None,
    suffixes=("_x", "_y"),
    tolerance=None,
    allow_exact_matches=True,
    direction="backward",
):
    if direction not in ["backward", "forward", "nearest"]:
        raise ValueError(
            "Invalid merge_asof direction. Choose from 'backward'"
            " 'forward', or 'nearest'"
        )

    kwargs = {
        "on": on,
        "left_on": left_on,
        "right_on": right_on,
        "left_index": left_index,
        "right_index": right_index,
        "by": by,
        "left_by": left_by,
        "right_by": right_by,
        "suffixes": suffixes,
        "tolerance": tolerance,
        "allow_exact_matches": allow_exact_matches,
        "direction": direction,
    }

    if left is None or right is None:
        raise ValueError("Cannot merge_asof on None")

    # if is_dataframe_like(left) and is_dataframe_like(right):
    if isinstance(left, pd.DataFrame) and isinstance(right, pd.DataFrame):
        return pd.merge_asof(left, right, **kwargs)

    if on is not None:
        if left_on is not None or right_on is not None:
            raise ValueError(
                "Can only pass argument 'on' OR 'left_on' and 'right_on', not a "
                "combination of both."
            )
        left_on = right_on = on
        kwargs["left_on"] = left_on
        kwargs["right_on"] = right_on
    del kwargs["on"]

    for o in [left_on, right_on]:
        if isinstance(o, _Frame):
            raise NotImplementedError(
                "Dask collections not currently allowed in merge columns"
            )

    if not is_dask_collection(left):
        left = from_pandas(left, npartitions=1)

    if not is_dask_collection(right):
        right = from_pandas(right, npartitions=1)

    if by is not None:
        if left_by is not None or right_by is not None:
            raise ValueError(
                "Can only pass argument 'by' OR 'left_by' and 'right_by', not a combination of both."
            )
        kwargs["left_by"] = kwargs["right_by"] = by
    del kwargs["by"]

    if left_by is None and right_by is not None:
        raise ValueError("Must specify both left_on and right_on if one is specified.")
    if left_by is not None and right_by is None:
        raise ValueError("Must specify both left_on and right_on if one is specified.")

    from dask_expr._merge_asof import MergeAsof

    return new_collection(MergeAsof(left, right, **kwargs))


def from_map(
    func,
    *iterables,
    args=None,
    meta=no_default,
    divisions=None,
    label=None,
    enforce_metadata=False,
    **kwargs,
):
    """Create a dask-expr collection from a custom function map

    NOTE: The underlying ``Expr`` object produced by this API
    will support column projection (via ``simplify``) if
    the ``func`` argument has "columns" in its signature.
    """
    from dask.dataframe.io.utils import DataFrameIOFunction

    from dask_expr.io import FromMap, FromMapProjectable

    if "token" in kwargs:
        # This option doesn't really make sense in dask-expr
        raise NotImplementedError("dask_expr does not support a token argument.")

    lengths = set()
    iterables = list(iterables)
    for i, iterable in enumerate(iterables):
        if not isinstance(iterable, Iterable):
            raise ValueError(
                f"All elements of `iterables` must be Iterable, got {type(iterable)}"
            )
        try:
            lengths.add(len(iterable))
        except (AttributeError, TypeError):
            iterables[i] = list(iterable)
            lengths.add(len(iterables[i]))
    if len(lengths) == 0:
        raise ValueError("`from_map` requires at least one Iterable input")
    elif len(lengths) > 1:
        raise ValueError("All `iterables` must have the same length")
    if lengths == {0}:
        raise ValueError("All `iterables` must have a non-zero length")

    # Check if `func` supports column projection
    allow_projection = False
    if "columns" in inspect.signature(func).parameters:
        allow_projection = True
    elif isinstance(func, DataFrameIOFunction):
        warnings.warn(
            "dask_expr does not support the DataFrameIOFunction "
            "protocol for column projection. To enable column "
            "projection, please ensure that the signature of `func` "
            "includes a `columns=` keyword argument instead."
        )
    else:
        allow_projection = False

    args = [] if args is None else args
    kwargs = {} if kwargs is None else kwargs
    if allow_projection:
        columns = kwargs.pop("columns", None)
        return new_collection(
            FromMapProjectable(
                func,
                iterables,
                columns,
                args,
                kwargs,
                meta,
                enforce_metadata,
                divisions,
                label,
            )
        )
    else:
        return new_collection(
            FromMap(
                func,
                iterables,
                args,
                kwargs,
                meta,
                enforce_metadata,
                divisions,
                label,
            )
        )


def repartition(df, divisions, force=False):
    if isinstance(df, FrameBase):
        return df.repartition(divisions=divisions, force=force)
    elif is_dataframe_like(df) or is_series_like(df):
        return new_collection(
            FromPandasDivisions(_BackendData(df), divisions=divisions)
        )
    else:
        raise NotImplementedError(f"repartition is not implemented for {type(df)}.")


def pivot_table(df, index, columns, values, aggfunc="mean"):
    if not is_scalar(index) or index not in df._meta.columns:
        raise ValueError("'index' must be the name of an existing column")
    if not is_scalar(columns) or columns not in df._meta.columns:
        raise ValueError("'columns' must be the name of an existing column")
    if not methods.is_categorical_dtype(df._meta[columns]):
        raise ValueError("'columns' must be category dtype")
    if not has_known_categories(df._meta[columns]):
        raise ValueError("'columns' must have known categories")

    if not (
        is_scalar(values)
        and values in df._meta.columns
        or not is_scalar(values)
        and all(is_scalar(x) and x in df._meta.columns for x in values)
    ):
        raise ValueError("'values' must refer to an existing column or columns")

    available_aggfuncs = ["mean", "sum", "count", "first", "last"]

    if not is_scalar(aggfunc) or aggfunc not in available_aggfuncs:
        raise ValueError(
            "aggfunc must be either " + ", ".join(f"'{x}'" for x in available_aggfuncs)
        )

    return new_collection(
        PivotTable(df, index=index, columns=columns, values=values, aggfunc=aggfunc)
    )


def to_numeric(arg, errors="raise", downcast=None, meta=None):
    """
    Return type depends on input. Delayed if scalar, otherwise same as input.
    For errors, only "raise" and "coerce" are allowed.
    """
    if errors not in ("raise", "coerce"):
        raise ValueError("invalid error value specified")

    if pd_is_scalar(arg):
        if meta is not None:
            raise KeyError("``meta`` is not allowed when input is a scalar.")
        return delayed(pd.to_numeric, pure=True)(arg, errors=errors, downcast=downcast)

    if is_arraylike(arg):
        return new_collection(
            ToNumeric(
                from_array(arg).astype(arg.dtype), errors=errors, downcast=downcast
            )
        ).to_dask_array(meta=meta)

    if is_series_like(arg):
        return new_collection(
            ToNumeric(frame=arg, errors=errors, downcast=downcast, meta=meta)
        )

    raise TypeError(
        "arg must be a list, tuple, dask.array.Array, or dask.dataframe.Series"
    )


def to_datetime(arg, meta=None, **kwargs):
    tz_kwarg = {"tz": "utc"} if kwargs.get("utc") else {}

    (arg,) = _maybe_from_pandas([arg])

    if meta is None:
        if isinstance(arg, Index):
            meta = get_meta_library(arg).DatetimeIndex([], **tz_kwarg)
            meta.name = arg.name
        elif not (is_dataframe_like(arg) or is_series_like(arg)):
            raise NotImplementedError(
                "dask.dataframe.to_datetime does not support "
                "non-index-able arguments (like scalars)"
            )
        else:
            meta = meta_series_constructor(arg)([pd.Timestamp("2000", **tz_kwarg)])
            meta.index = meta.index.astype(arg.index.dtype)
            meta.index.name = arg.index.name

    kwargs.pop("infer_datetime_format", None)

    return new_collection(ToDatetime(frame=arg, kwargs=kwargs, meta=meta))


def to_timedelta(arg, unit=None, errors="raise"):
    if not isinstance(arg, Series):
        raise TypeError("arg must be a Series")
    return new_collection(ToTimedelta(frame=arg, unit=unit, errors=errors))


def _from_scalars(scalars, meta, names):
    return new_collection(FromScalars(meta, names, *scalars))


def map_partitions(
    func,
    *args,
    meta=no_default,
    enforce_metadata=True,
    transform_divisions=True,
    clear_divisions=False,
    align_dataframes=False,
    parent_meta=None,
    **kwargs,
):
    if align_dataframes:
        # TODO: Handle alignment?
        # Perhaps we only handle the case that all `Expr` operands
        # have the same number of partitions or can be broadcasted
        # within `MapPartitions`. If so, the `map_partitions` API
        # will need to call `Repartition` on operands that are not
        # aligned with `self.expr`.
        raise NotImplementedError()
    new_expr = expr.MapPartitions(
        args[0],
        func,
        meta,
        enforce_metadata,
        transform_divisions,
        clear_divisions,
        align_dataframes,
        parent_meta,
        kwargs,
        *args[1:],
    )
    return new_collection(new_expr)


def map_overlap(
    func,
    df,
    before,
    after,
    *args,
    meta=no_default,
    enforce_metadata=True,
    transform_divisions=True,
    clear_divisions=False,
    align_dataframes=False,
    **kwargs,
):
    if isinstance(before, str):
        before = pd.to_timedelta(before)
    if isinstance(after, str):
        after = pd.to_timedelta(after)

    if isinstance(before, datetime.timedelta) or isinstance(after, datetime.timedelta):
        if isinstance(df, FrameBase):
            inferred_type = df.index._meta_nonempty.inferred_type
        else:
            inferred_type = df.index.inferred_type

        if not is_datetime64_any_dtype(inferred_type):
            raise TypeError(
                "Must have a `DatetimeIndex` when using string offset "
                "for `before` and `after`"
            )

    elif not (
        isinstance(before, Integral)
        and before >= 0
        and isinstance(after, Integral)
        and after >= 0
    ):
        raise ValueError("before and after must be positive integers")

    df = _maybe_from_pandas([df])[0]
    args = _maybe_from_pandas(args)

    if align_dataframes:
        dfs = [df] + args
        dfs = [df for df in dfs if isinstance(df, FrameBase)]
        if len(dfs) > 1 and not expr.are_co_aligned(*dfs, allow_broadcast=False):
            return new_collection(
                expr.MapOverlapAlign(
                    df,
                    func,
                    before,
                    after,
                    meta,
                    enforce_metadata,
                    transform_divisions,
                    clear_divisions,
                    align_dataframes,
                    kwargs,
                    *args,
                )
            )

    new_expr = expr.MapOverlap(
        df,
        func,
        before,
        after,
        meta,
        enforce_metadata,
        transform_divisions,
        clear_divisions,
        align_dataframes,
        kwargs,
        *args,
    )
    return new_collection(new_expr)


def isna(arg):
    if isinstance(arg, FrameBase):
        return arg.isna()
    else:
        return from_pandas(arg).isna()


def elemwise(op, *args, meta=no_default, out=None, transform_divisions=True, **kwargs):
    """Elementwise operation for Dask dataframes

    Parameters
    ----------
    op: callable
        Function to apply across input dataframes
    *args: DataFrames, Series, Scalars, Arrays,
        The arguments of the operation
    meta: pd.DataFrame, pd.Series (optional)
        Valid metadata for the operation.  Will evaluate on a small piece of
        data if not provided.
    transform_divisions: boolean
        If the input is a ``dask.dataframe.Index`` we normally will also apply
        the function onto the divisions and apply those transformed divisions
        to the output.  You can pass ``transform_divisions=False`` to override
        this behavior
    out : ``dask.array`` or ``None``
        If out is a dask.DataFrame, dask.Series or dask.Scalar then
        this overwrites the contents of it with the result
    **kwargs: scalars

    Examples
    --------
    >>> elemwise(operator.add, df.x, df.y)  # doctest: +SKIP
    """

    args = _maybe_from_pandas(args)

    # TODO: Add align partitions

    dfs = [df for df in args if isinstance(df, FrameBase)]
    if len(dfs) <= 1 or expr.are_co_aligned(*dfs, allow_broadcast=False):
        result = new_collection(
            expr.UFuncElemwise(dfs[0], op, meta, transform_divisions, kwargs, *args)
        )
    else:
        result = new_collection(expr.UFuncAlign(dfs[0], op, meta, kwargs, *args))
    return handle_out(out, result)


def handle_out(out, result):
    """Handle out parameters

    If out is a dask.DataFrame, dask.Series or dask.Scalar then
    this overwrites the contents of it with the result. The method
    replaces the expression of the out parameter with the result
    from this operation to perform something akin to an inplace
    modification.
    """
    if isinstance(out, tuple):
        if len(out) == 1:
            out = out[0]
        elif len(out) > 1:
            raise NotImplementedError(
                "The `out` parameter with length > 1 is not supported"
            )
        else:
            out = None

    if out is not None and out.__class__ != result.__class__:
        raise TypeError(
            "Mismatched types between result and out parameter. "
            "out=%s, result=%s" % (str(type(out)), str(type(result)))
        )

    if isinstance(out, DataFrame):
        if len(out.columns) != len(result.columns):
            raise ValueError(
                "Mismatched columns count between result and out parameter. "
                "out=%s, result=%s" % (str(len(out.columns)), str(len(result.columns)))
            )

    if isinstance(out, (Series, DataFrame, Scalar)):
        out._expr = result._expr
    elif out is not None:
        msg = (
            "The out parameter is not fully supported."
            " Received type %s, expected %s "
            % (
                typename(type(out)),
                typename(type(result)),
            )
        )
        raise NotImplementedError(msg)
    else:
        return result


def _compute_partition_stats(
    column: Series, allow_overlap: bool = False
) -> tuple[list, list, list[int]]:
    """For a given column, compute the min, max, and len of each partition.

    And make sure that the partitions are sorted relative to each other.
    NOTE: this does not guarantee that every partition is internally sorted.
    """
    mins = column.map_partitions(M.min, meta=column)
    maxes = column.map_partitions(M.max, meta=column)
    lens = column.map_partitions(len, meta=column)
    mins, maxes, lens = compute(mins, maxes, lens)
    mins = mins.bfill().tolist()
    maxes = maxes.bfill().tolist()
    non_empty_mins = [m for m, length in zip(mins, lens) if length != 0]
    non_empty_maxes = [m for m, length in zip(maxes, lens) if length != 0]
    if (
        sorted(non_empty_mins) != non_empty_mins
        or sorted(non_empty_maxes) != non_empty_maxes
    ):
        raise ValueError(
            f"Partitions are not sorted ascending by {column.name or 'the index'}. ",
            f"In your dataset the (min, max, len) values of {column.name or 'the index'} "
            f"for each partition are: {list(zip(mins, maxes, lens))}",
        )
    if not allow_overlap and any(
        a <= b for a, b in zip(non_empty_mins[1:], non_empty_maxes[:-1])
    ):
        warnings.warn(
            "Partitions have overlapping values, so divisions are non-unique. "
            "Use `set_index(sorted=True)` with no `divisions` to allow dask to fix the overlap. "
            f"In your dataset the (min, max, len) values of {column.name or 'the index'} "
            f"for each partition are : {list(zip(mins, maxes, lens))}",
            UserWarning,
        )
    lens = methods.tolist(lens)
    if not allow_overlap:
        return (mins, maxes, lens)
    else:
        return (non_empty_mins, non_empty_maxes, lens)
