import cupy as cp
from ..core import Observable, Argument

__all__ = ["CupyObservable",
           "TotalDipole"]

#pylint: disable=too-few-public-methods
class CupyObservable(Observable):
    """
        The subclass of the observable which is calculated using cupy

        :param name: the name of the observable
        :param n_frame: the number of frame
    """
    def __init__(self, name, n_frame):
        self._obs = Argument(name, cp.zeros(n_frame, dtype=cp.float32))
        super().__init__(name, [self._obs], None, is_cp=True)
        self.main_iterable.append(0)
        self.cupy = True
        self._definition = self._def

    @property
    def out(self):
        return self._obs.var

    @property
    def source_code(self):
        return ""

class TotalDipole(CupyObservable):
    """
        Calculate the total dipole of the AtomGroup

        :param name: the name of the observable
        :param dag: the atom group in device
        :param q: the atom charge of the atom group, either in host or in device
        :param direction: the direction of the dipole. 0 for x, 1 for y, 2 for z
        :param n_frame: the number of frame
    """
    def __init__(self, name, dag, q, n_frame, direction=None):
        super().__init__(name, n_frame)
        dag = dag.var
        self.dag = dag
        if direction is None:
            direction = [0, 1, 2]
        self.q = cp.array(q).reshape(1, -1, 1)
        self.direction = cp.array(direction).reshape(-1)

    def _def(self, position, dimension):
        temp = position.take(self.dag, axis=1)
        temp = temp.take(self.direction, axis=2)
        temp = cp.sum(temp * self.q, axis=1).reshape(temp.shape[0], temp.shape[2])
        if len(temp.shape) == 2:
            axis = 1
        else:
            axis = (1, 2)
        self.out[:] = cp.sqrt(cp.sum(temp * temp, axis=axis))
