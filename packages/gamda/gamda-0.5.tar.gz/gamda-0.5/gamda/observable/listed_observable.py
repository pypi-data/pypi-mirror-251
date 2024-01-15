from ..core import Observable, Argument

__all__ = ["ListedObservable",
           "PositionX", "PositionY", "PositionZ",
           "ListedDistance"]

#pylint: disable=too-few-public-methods
class ListedObservable(Observable):
    """
        The subclass of the observable which is calculated as listed AtomGroup

        :param name: the name of the observable
        :param in_arg: a list of the input argument (cp.array, which is mda.AtomGroup in device)
        :param out_arg: the output argument (np.float32)
    """
    @property
    def source_code(self):
        formatter = {"O": self.output.use()}
        formatter.update({"I" + str(i): inp.use() for i, inp in enumerate(self.input)})
        return [f"{self.output.use()} = nanf(\"\");",
                f"if ({ ' && '.join([ '!isnan(%s)'%inp.use() for inp in self.input])})",
                r"{",
                *["    " + defi.format(**formatter) for defi in self._definition],
                r"}"]

class PositionZ(ListedObservable):
    """
        The coordinate of position Z

        :param dag: the AtomGroup in device
        :param out_arg: the output argument (np.float32)
    """
    def __init__(self, name, dag, out_arg):
        super().__init__(name, [dag], out_arg)
        self.main_iterable.append(0)
        self._definition = ["{O} = local_position[{I0} * 3 + 2];"]


class PositionY(ListedObservable):
    """
        The coordinate of position Y

        :param dag: the AtomGroup in device
        :param out_arg: the output argument (np.float32)
    """
    def __init__(self, name, dag, out_arg):
        super().__init__(name, [dag], out_arg)
        self.main_iterable.append(0)
        self._definition = ["{O} = local_position[{I0} * 3 + 1];"]


class PositionX(ListedObservable):
    """
        The coordinate of position X

        :param dag: the AtomGroup in device
        :param out_arg: the output argument (np.float32)
    """
    def __init__(self, name, dag, out_arg):
        super().__init__(name, [dag], out_arg)
        self.main_iterable.append(0)
        self._definition = ["{O} = local_position[{I0} * 3];"]

class ListedDistance(ListedObservable):
    """
        The distance between atoms

        :param dag1: the AtomGroup in device
        :param dag2: the AtomGroup in device
        :param out_arg: the output argument (np.float32)
        :param pbc: whether consider the periodic boundary conditions
    """
    def __init__(self, name, dag1, dag2, out_arg, pbc):
        super().__init__(name, [dag1, dag2], out_arg)
        self.main_iterable += [0, 1]
        self.pbc = pbc

    @property
    def pbc(self):
        """ whether consider the periodic boundary conditions """
        return self._pbc

    @pbc.setter
    def pbc(self, pbc):
        self._pbc = pbc
        if not pbc:
            self._definition = ["{O} = get_distance(local_position, {I0}, {I1});"]
        else:
            self._definition = ["{O} = get_distance(local_position, {I0}, {I1}, local_dimension);"]