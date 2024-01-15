"""
    The basic functions of the package
"""
__all__ = ["logger", "INCLUDE",
           "Universe", "Argument", "Executable",
           "Observable", "TrajectoryAnalyzer", "ConformationAnalyzer"]

import weakref
import logging
import MDAnalysis as mda
import numpy as np
import cupy as cp
from .cudasrc import INCLUDE

logger = logging.getLogger("gamda")
console_handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s - gamda - %(levelname)s]\n%(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

class Universe(mda.Universe):
    """
        a subclass of mda.Universe
        Additional parameters:

        :param n_frame: the number of the frame used for parallel computing. 32 for default
    """
    def __init__(self, *args, **kwargs):
        n_frame = 32
        if "n_frame" in kwargs:
            n_frame = kwargs.pop(n_frame)
        super().__init__(*args, **kwargs)
        self._id_map = {atom.id: i for i, atom in enumerate(self.atoms)}
        self.exe = Executable(len(self.atoms), n_frame)

    @property
    def n_frame(self):
        """
            the number of the frame used for parallel computing.
        """
        return self.exe.n_frame.var

    @property
    def source_code(self):
        """
            the source code used in cuda kernel
        """
        return self.exe.readable_source_code

    def get_dag(self, name, ag):
        """
            get the atom index of an mda.AtomGroup

            :param name: name of the AtomGroup in device
            :param ag: the mda.AtomGroup in host
        """
        if not isinstance(ag, mda.AtomGroup):
            raise TypeError(f"the type of the input should be mda.AtomGroup, but {type(ag)} got")
        array = cp.array([self._id_map.get(atom.id, -1) for atom in ag], dtype=cp.int32)
        return Argument(name, array)

    def add_analyzer(self, analyzer):
        """
            add an analyzer to the excutable

            :param analyzer: a gamda.Analyzer
        """
        self.exe.add_analyzer(analyzer)

    def run(self, weight=None, start=0, stop=None, strip=1):
        """
            Run the analysis

            :param weight: a numpy array, the sampling weight of the frame
            :param start: the start frame of the analysis
            :param stop: the stop frame of the analysis
            :param strip: the strip frame of the analysis
        """
        run_traj = self.trajectory[start:stop:strip]
        if isinstance(weight, np.ndarray):
            if len(weight) != len(run_traj):
                raise ValueError("The length of the weight should be the same as the trajectory")
        elif weight is None:
            weight = np.ones(len(run_traj), dtype=np.float32)
        else:
            raise TypeError("The weight should eigher a np.ndarray or None")
        for i, ts in enumerate(self.trajectory[start:stop:strip]):
            self.exe.add_frame(ts.positions, ts.dimensions, weight[i])
        self.exe.execute()

    def free(self):
        """
            free the cross references
        """
        self.atoms = None
        self.residues = None
        self.segments = None
        self.exe = None

class Argument:
    """
        The basic wrapper of arguments (input, output or medium) for others

        :param name: name of the argument
        :param var: the variable to be wrapped
    """
    names = set()
    def __init__(self, name, var):
        if name in self.names:
            raise ValueError(f"There have been an argument named {name}")
        if name.startswith("local") or name.startswith("temp"):
            raise ValueError(f"The name is not allowed to start with 'local' or 'temp' ({name})")
        self.name = name
        self.prefix_bold = None
        if isinstance(var, cp.ndarray):
            self.dim = len(var.shape)
            if var.dtype == cp.float32:
                self.prefix = "float*"
                self.prefix_bold = "float"
            elif var.dtype == cp.int32:
                self.prefix = "int*"
                self.prefix_bold = "int"
            else:
                raise TypeError(f"The data type of the input cupy array should be either \
cp.float32 or cp.int32, but {var.dtype} got")
            self.is_ptr = True
        elif isinstance(var, np.generic):
            self.dim = 0
            if var.dtype == np.float32:
                self.prefix = "float"
            elif var.dtype == np.int32:
                self.prefix = "int"
            else:
                raise TypeError(f"The data type of the input numpy scalar should be either \
np.float32 or np.float32, but {var.dtype} got")
        else:
            raise TypeError(f"The input var should be either \
a cupy array or a numpy generic, but {type(var)} got")
        self.names.add(name)
        self._var = var
        self.main_iteration = 0

    @property
    def var(self):
        """
            The variable to be wrapped
        """
        return self._var

    def declare(self):
        """
            Get the declaration string
        """
        return f"{self.prefix} {self.name}"

    def use(self):
        """
            Get the usage string
        """
        if self.prefix_bold:
            return f"local_{self.name}"
        return self.name

    def declare_local(self, index):
        """
            Get the local declaration string of the pointer

            :param index: the index for the pointer
        """
        if self.dim == 1:
            return f"{self.prefix_bold} local_{self.name} = ({index} < {len(self.var)}) ? \
{self.name}[{index}] : {'nanf(\"\")' if self.prefix_bold == 'float' else 'INT_NAN'};"
        if self.dim == 2:
            return f"{self.prefix} local_{self.name} = ({index} < {len(self.var)}) ? \
{self.name} + {index} : NULL;"
        return ""

    def __del__(self):
        self.names.discard(self.name)


class _HiddenInfoList(list):
    """
        This class is to deal with the hidden information of the executable
    """
    def __init__(self):
        self.names = {}
        self.count = {}

    def append(self, obj):
        """
            Modified list appendance
        """
        if not hasattr(type(obj), "names"):
            raise TypeError("The input should be a type with names")
        if not hasattr(obj, "name"):
            raise TypeError("The input should be an instance with name")
        if obj.name not in self.names:
            self.names[obj.name] = len(self)
            self.count[obj.name] = 1
            super().append(obj)
        else:
            self.count[obj.name] += 1

    def __getitem__(self, i):
        if i in self.names:
            i = self.names[i]
        super().__getitem__(i)


class Executable:
    """
        The basic class of the analysis excutable

        :param n_atom: the number of total atoms
        :param n_frame: the number of frame to be used for paralleling, 32 for default
    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self, n_atom, n_frame=32):
        self.n_frame = Argument("n_frame", np.int32(n_frame))
        self.n_atom = Argument("n_atom", np.int32(n_atom))
        self._h_position = np.full((n_frame, n_atom, 3), np.float32("nan"), dtype=np.float32)
        self._d_position = Argument("position", cp.array(self._h_position))
        self._h_dimension = np.full((n_frame, 6), np.float32("nan"), dtype=np.float32)
        self._d_dimension = Argument("dimension", cp.array(self._h_dimension))
        self._h_weight = np.full(n_frame, np.float32("nan"), dtype=np.float32)
        self._d_weight = Argument("weight", cp.array(self._h_weight))
        self._tid = Argument("tid", np.int32(0))
        self._frame = Argument("frame", np.int32(0))
        self._frame = 0
        self._n_tid = Argument("n_tid", np.int32(0))
        self._analyzer = []
        self._input = _HiddenInfoList()
        self._output = _HiddenInfoList()
        self._medium = _HiddenInfoList()
        self._observable = _HiddenInfoList()
        self.kernel = None

    def _compile(self):
        self.kernel = cp.RawKernel(self.source_code, "executable_kernel")
        return self.kernel

    def __enter__(self):
        for obs in self._observable:
            for i in obs.main_iterable:
                obs.input[i].main_iteration += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        for obs in self._observable:
            for i in obs.main_iterable:
                obs.input[i].main_iteration -= 1

    @property
    def readable_source_code(self):
        """
            The human-readable source code
        """
        src = ""
        for n_line, line in enumerate(self.source_code.split("\n")):
            src += f"{n_line + 1: >4d}| "
            temp_line = []
            for i in range(0, len(line), 120):
                temp_line.append(line[i: i + 120])
            src += "\n    | ".join(temp_line) + "\n"
        return src

    @property
    def source_code(self):
        """
            The source code
        """
        include = ""
        if self.n_frame.var in (2, 4, 8, 16, 32):
            include += f"#define GOOD_N_FRAME {self.n_frame.var}\n"
        include += INCLUDE
        return include + r"""
extern "C" __global__
void executable_kernel(const int n_frame, const int n_tid, const int n_atom, const float* position, const float* dimension, const float* weight%s%s)
{
    int tid = blockDim.x * blockIdx.x + threadIdx.x;
    int frame = threadIdx.y;
    if (tid < n_tid && frame < n_frame)
    {
        const float local_weight = weight[frame];
        const float* local_position = position + frame * n_atom * 3;
        const float* local_dimension = dimension + frame * 6;
        %s%s
    }
}
""" %(self._get_inputs(), self._get_outputs(), self._get_declartions(), self._get_calculations())

    def _get_inputs(self):
        """ get input string """
        if self._input:
            return ", " + ", ".join([inp.declare() for inp in self._input])
        return ""

    def _get_outputs(self):
        """ get output string """
        if self._output:
            return ", " + ", ".join([out.declare() for out in self._output])
        return ""

    def _get_declartions(self):
        """ get declaration string """
        declarations = []
        max_temp_int = 0
        max_temp_float = 0
        with self:
            if self._input:
                declarations += [inp.declare_local("tid") for inp in self._input if inp.main_iteration]
        if self._medium:
            declarations += [mid.declare() + ";" for mid in self._medium]
        for ana in self._analyzer:
            if ana.temp_int > max_temp_int:
                max_temp_int = ana.temp_int
            if ana.temp_float > max_temp_float:
                max_temp_float = ana.temp_float
        declarations += [f"int temp_int_{i};" for i in range(max_temp_int)]
        declarations += [f"float temp_float_{i};" for i in range(max_temp_float)]

        if declarations:
            return "\n        " + "\n        ".join(declarations) + "\n        "
        return ""

    def _get_calculations(self):
        """ get calculation string """
        src = []
        for ana in self._analyzer:
            src += ana.source_code
        if src:
            return "\n        " + "\n        ".join(src)
        return ""

    def add_analyzer(self, analyzer):
        """
            add an analyzer to the excutable

            :param analyzer: gamda.Analyzer
        """
        self._analyzer.append(analyzer)
        for inp in analyzer.input:
            self._input.append(inp)
        for out in analyzer.output:
            self._output.append(out)
        for med in analyzer.medium:
            self._medium.append(med)
        for obs in analyzer.observable:
            self._observable.append(obs)

    def add_frame(self, positions, dimension, weight):
        """
            Add a frame to the executable.

            :param positions: ts.positions
            :param dimension: ts.dimension
            :param weight: a float
        """
        self._h_position[self._frame, :, :] = positions
        self._h_weight[self._frame] = weight
        self._h_dimension[self._frame, :] = dimension
        self._frame += 1
        if self._frame == self.n_frame.var:
            self.execute()

    def execute(self):
        """
            run the executable for analysis
        """
        if not self.kernel:
            self._compile()
        self._d_position.var.set(self._h_position)
        self._d_dimension.var.set(self._h_dimension)
        self._d_weight.var.set(self._h_weight)
        self._h_position[:] = np.float32("nan")
        self._h_dimension[:] = np.float32("nan")
        self._h_weight[:] = np.float32("nan")
        for obs in self._observable:
            if obs.is_cp:
                obs._definition(self._d_position.var, self._d_dimension.var)
        block_x = 1024 // self.n_frame.var
        grid_x = (self._n_tid.var + block_x - 1) // block_x
        with self:
            self._n_tid._var = np.int32(np.max([len(inp.var) 
                if inp.main_iteration else 1 for inp in self._input]))
        args = [self._frame, self._n_tid.var, self.n_atom.var,
                self._d_position.var, self._d_dimension.var, self._d_weight.var]
        args += [inp.var for inp in self._input]
        args += [out.var for out in self._output]
        try:
            self.kernel((grid_x,), (block_x, self.n_frame.var), args)
        except cp.cuda.compiler.CompileException as e:
            e.add_note(self.readable_source_code)
            raise e
        self._frame = 0


class Observable:
    """
        The class of the observable

        :param name: the name of the observable
        :param in_arg: a list of the input argument (cp.array, which is mda.AtomGroup in device)
        :param out_arg: the output argument (np.float32)
        :param is_cp: whether the observable is defined by cupy operators
    """
    names = set()
    def __init__(self, name, in_arg, out_arg, is_cp=False):
        self.name = name
        for i, inp in enumerate(in_arg):
            if not isinstance(inp, Argument):
                raise TypeError(f"in_arg should be list of a gamda.Argument, but element {i} is a type of {type(inp)}")
        if not is_cp and not isinstance(out_arg, Argument):
            raise TypeError(f"out_arg should be a gamda.Argument, but a {type(out_arg)} got")
        if not is_cp and out_arg.prefix not in ("float"):
            raise TypeError("out_arg should be a numpy generic of float32")
        self.input = in_arg
        self.output = out_arg
        self.names.add(name)
        self.main_iterable = []
        self.sub_iterable = []
        self._definition = None
        self.is_cp = is_cp

    @property
    def source_code(self):
        """
            The source code of the observable
        """
        raise NotImplementedError

    def __del__(self):
        self.names.discard(self.name)

class TrajectoryAnalyzer:
    """
        The class of general analyzer of the trajectory

        :param name: name of the analyzer
        :param in_arg: input arguments
        :param out_arg: output arguments
        :param med_arg: medium arguments
        :param obs_arg: observable arguments
        :param temp_float: the number of temporary floats
        :param temp_int: the number of temporary ints
    """
    def __init__(self, name, in_arg, out_arg, med_arg, obs_arg, temp_float=0, temp_int=0):
        self.name = name
        self.input = in_arg
        self.output = out_arg
        self.medium = med_arg
        self.observable = obs_arg
        self.temp_float = temp_float
        self.temp_int = temp_int

    @property
    def source_code(self):
        """
            The source code of the observable
        """
        raise NotImplementedError

class ConformationAnalyzer:
    """
        The class of general analyzer of the conformation

        :param name: name of the analyzer
    """
    def __init__(self, name):
        self.name = name
