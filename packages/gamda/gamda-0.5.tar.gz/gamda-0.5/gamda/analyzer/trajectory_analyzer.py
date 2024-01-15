"""
"""
import numpy as np
import cupy as cp
from ..core import *
from ..observable import ListedObservable, PairwiseObservable, CupyObservable

__all__ = ["Histogrammer"]

class Histogrammer(TrajectoryAnalyzer):
    """
        The histogram analysis

        :param minimal: the minimal of the value
        :param maximum: the maximum of the value
        :param n_bin: the bin of the histogram
        :param observable: the observable to be analyzed
        :param w_def: the definition of the weight. None for default
    """
    def __init__(self, name, minimal, maximum, n_bin, observable, w_def=None):
        self.min = np.float32(minimal)
        self.max = np.float32(maximum)
        self.n_bin = np.int32(n_bin)
        self.value = Argument(name, cp.zeros(n_bin, dtype=cp.float32))
        if observable.output is not None:
            med = [observable.output]
        else:
            med = []
        super().__init__(name, observable.input,
                         [self.value], med, [observable], temp_int = 1)
        self._definition = [
                r"if ({O} >= {min}f && {O} < {max}f && !isnan({O}))",
                r"{{",
                r"    temp_int_0 = ({O} - {min}f) / ({max}f - {min}f) * {n_bin};",
                r"    if (temp_int_0 >= 0 && temp_int_0 < {n_bin})",
                r"        atomicAdd({self_value_name} + temp_int_0, {w_def});",
                r"}}",
            ]
        if w_def is None:
            self.w_def = "local_weight"
        else:
            self.w_def = w_def

    @property
    def source_code(self):
        """
            The source code of the analyzer
        """
        obs = self.observable[0]
        formatter = {"min": self.min, "max": self.max,
            "n_bin": self.n_bin, "self_value_name": self.value.name, "w_def": self.w_def}
        if isinstance(obs, CupyObservable):
            formatter["O"] = obs._obs.use()
        else:
            formatter["O"] = obs.output.use()
        _definition = [line.format(**formatter) for line in self._definition]
        if isinstance(obs, ListedObservable):
            return obs.source_code + _definition
        if isinstance(obs, PairwiseObservable):
            tail = ["}" * len(obs.sub_iterable) + " // for sub iterables"]
            return obs.source_code + _definition + tail
        if isinstance(obs, CupyObservable):
            return _definition
        raise TypeError("The input observable should be either ListedObservable, PairwiseObservable, or CupyObservable")
    def normalize(self):
        """
            Normalize the results
        """
        bin_length = (self.max - self.min) / self.n_bin
        norm = cp.sum(self.value.var)
        if norm == 0:
            raise ZeroDivisionError("the sum of the values is zero")
        self.value.var[:] /= norm * bin_length

    def save(self, filename):
        """
            Save the results to the filename

            :param filename: the name of the file
        """
        towrite = ""
        delta = (self.max - self.min) / self.n_bin
        for i, v in enumerate(self.value.var):
            towrite += f"{i * delta + self.min:12.7e}    {v:12.7e}\n"
        with open(filename, "w") as f:
            f.write(towrite)
