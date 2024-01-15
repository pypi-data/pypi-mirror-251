from ..core import Observable, Argument

__all__ = ["PairwiseObservable",
           "PairwiseDistance"]

#pylint: disable=too-few-public-methods
class PairwiseObservable(Observable):
    """
        The subclass of the observable which is calculated as pairwise AtomGroup

        :param name: the name of the observable
        :param in_arg: a list of the input argument (cp.array, which is mda.AtomGroup in device)
        :param out_arg: the output argument (np.float32)
    """
    @property
    def source_code(self):
        formatter = {"O": self.output.use()}
        formatter.update({"I" + str(i): inp.use() for i, inp in enumerate(self.input)})
        head = [f"for (int i{i} = 0; i{i} < {len(self.input[v].var)}; i{i}++) {{ {self.input[v].declare_local('i' + str(i))}"
            for i, v in enumerate(self.sub_iterable)] + ["// for sub iterables"]
        return head + [f"{self.output.use()} = nanf(\"\");",
                    f"if ({ ' && '.join([ '!isnan(%s)'%inp.use() for inp in self.input])})",
                    r"{",
                    *["    " + defi.format(**formatter) for defi in self._definition],
                    r"}"]

class PairwiseDistance(PairwiseObservable):
    """
        The distance between atoms

        :param dag1: the AtomGroup in device
        :param dag2: the AtomGroup in device
        :param out_arg: the output argument (np.float32)
        :param pbc: whether consider the periodic boundary conditions
    """
    def __init__(self, name, dag1, dag2, out_arg, pbc):
        super().__init__(name, [dag1, dag2], out_arg)
        self.main_iterable += [0]
        self.sub_iterable += [1]
        self.pbc = pbc

    @property
    def pbc(self):
        """ whether consider the periodic boundary conditions """
        return self._pbc

    @pbc.setter
    def pbc(self, pbc):
        self._pbc = bool(pbc)
        if not pbc:
            self._definition = ["{O} = get_distance(local_position, {I0}, {I1});"]
        else:
            self._definition = ["{O} = get_distance(local_position, {I0}, {I1}, local_dimension);"]