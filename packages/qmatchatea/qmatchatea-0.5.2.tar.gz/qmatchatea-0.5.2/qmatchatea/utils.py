# This code is part of qmatchatea.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
General utility functions and classes for the simulation
"""

# Import necessary packages
import os
import pickle
import shutil
from warnings import warn
from datetime import datetime
from typing import OrderedDict
import numpy as np
from qtealeaves import write_nml
from qtealeaves.convergence_parameters import TNConvergenceParameters
from qtealeaves.emulator import MPS, TTN

from qtealeaves.observables import TNObservables

from .tn_utils import QCOperators, read_mps

EXE_PATH_DIR = os.path.dirname(__file__)
EXE_PATH = os.path.join(EXE_PATH_DIR, "bin/qmatchatea.exe")

__all__ = [
    "simulation_results",
    "print_state",
    "fidelity",
    "QCCheckpoints",
    "QCIO",
    "QCConvergenceParameters",
    "QCBackend",
    "SimpleHamiltonian",
]


class SimpleHamiltonian(dict):
    """
    Simple class for an Hamiltonian that extends a normal dictionary.
    The keys are the pauli strings, the values the coefficients.
    It is used for simplicity, since it has a `to_pauli_dict` method
    equivalent to qiskit and other methods to ease the construction.
    """

    def set_num_qubits(self, num_qubits):
        """
        Set the number of qubits the Hamiltonian is describing

        Parameters
        ----------
        num_qubits : int
            Number of qubits
        """
        self["num_qubits"] = num_qubits

    def add_term(self, hterms, qubits, coeff):
        """
        Add a term to the Hamiltonian acting on the
        qubits qubits. You do not need to specify the identities

        Parameters
        ----------
        hterms : str or array-like
            Pauli matrices to apply
        qubits : int or array-like
            Qubits where the terms acts
        coeff : complex
            Coefficient of the term

        Returns
        -------
        None
        """
        if np.isscalar(qubits):
            qubits = np.array([qubits])
            hterms = np.array([hterms])
        ordering = np.argsort(qubits)
        qubits = qubits[ordering]
        hterms = hterms[ordering]

        pauli_string = ""
        for hterm, qubit in zip(hterms, qubits):
            last_qubit = len(pauli_string)
            pauli_string += "I" * (qubit - last_qubit)
            pauli_string += hterm
        last_qubit = len(pauli_string)
        pauli_string += "I" * (self["num_qubits"] - last_qubit)

        self[pauli_string[::-1]] = coeff

    def to_pauli_dict(self):
        """
        Get the qiskit pauli dict representation, that can be later
        used in the observable class

        Returns
        -------
        dict
            dictionary with qiskit pauli_dict old format
        """
        pauli_dict = {"paulis": []}
        for key, val in self.items():
            if key == "num_qubits":
                continue

            pauli_dict["paulis"].append(
                {"label": key, "coeff": {"real": np.real(val), "imag": np.imag(val)}}
            )
        return pauli_dict


class simulation_results:
    """
    This class is used to handle the results of a simulation with qmatchatea.
    You can use it to:

    - Retrieve the results of a FORTRAN simulation;
    - Save the results of a simulation (see the `save_results()` method);
    - Load the results of a simulation (see the `load_results()` method);

    The results can be then accessed in python through the following properties.

    Input Properties
    ----------------
    date_time: str
        The date-time when the simulation started as ``Year-month-day-Hour:Minute:Second``
    input_params : dict
        Dictionary containing all the input informations
    initial_state : List[np.ndarray] or str
        The initial state of the simulation

    Output Properties
    -----------------
    fidelity: float
        Lower bound on the fidelity of the final state
    singular_values_cut : np.ndarray
        Singular values cut during the simulation
    measures: dict
        Projective measures of the simulation, in the format `{"000":15, "011":24}`
    measure_probabilities: List[dict or None]
        The 0th element is the result of the unbiased (OPES) sampling, with a format
        `{"000" : (0, 1)}` where the values are the left and right boundaries of the
        probability interval.
        The 1st element is even probability and the 2nd element greedy probabilities,
        with the format `{"000": 1}`, where the value is the probability of the state
    tens_net : List[np.ndarray]
        The tensor network state
    statevector: np.ndarray or None
        The statevector of the final state. Returned only if `num_sites<30`
    entanglement: dict or None
        Entanglement across bipartition, where the key is the bipartition. An example
        for a 2-site MPS system in a product state is `{(0,1) : 0}`
    observables : dict
        The dictionary containing ALL the observables of the simulation
    computational_time: float or None
        Time of the simulation
    """

    def __init__(self, input_params=None, observables=None):
        """
        Initialization. Provide a input params dictionary only if you want to retrieve
        the result directly from the Fortran working folder.
        Otherwise, if you want to load previous results, just initialize the class
        without parameters.

        Parameters
        ----------
        input_params: dict, optional
            If provided contains all the input parameters of the simulation.
            If it is empty than you should use this class to upload a previous experiment
        observables: TNObservables, optional
            observables used in the simulation
        """
        # Name of the input parameters in a simulation
        self._input_params_names = [
            "num_sites",
            "local_dim",
            "approach",
            "observables_filename",
            "max_bond_dimension",
            "cut_ratio",
            "trunc_tracking_mode",
            "inPATH",
            "outPATH",
            "sparse",
            "initial_state",
            "checkpoint_PATH",
            "checkpoint_frequency",
            "initial_line",
        ]

        self._input_params = {} if input_params is None else input_params
        self._from_simulation = (
            False  # flag set to True if you have to obtain data from Fortran,
        )
        # i.e. if you provide a suitable input parameter dictionary

        if all("settings%" + k in self._input_params for k in self._input_params_names):
            self.inPATH = input_params["settings%inPATH"]
            self.outPATH = input_params["settings%outPATH"]
            assert os.path.isdir(self.inPATH), "Input PATH is not a folder"
            assert os.path.isdir(self.outPATH), "Output PATH is not a folder"
            self._from_simulation = True

        self._datetime = datetime.today().strftime("%Y-%m-%d-%H:%M:%S")

        # Set to None all the variables
        self._initial_state = "Vacuum"
        if "settings%initial_state" in self._input_params:
            if self._input_params["settings%initial_state"] == "Vacuum":
                pass
            elif int(self._input_params["settings%initial_line"]) == 1:
                self._initial_state = read_mps(
                    os.path.join(
                        self.inPATH, self._input_params["settings%initial_state"]
                    )
                )
            else:
                self._initial_state = read_mps(
                    os.path.join(
                        self._input_params["settings%checkpoint_PATH"],
                        self._input_params["settings%initial_state"],
                    )
                )

        self._observables = {} if observables is None else observables
        self._singular_values_cut = None
        self._statevector = None

    def _get_results(self):
        """
        Load the results on python from the output files
        """

        assert (
            self._from_simulation
        ), "Cannot retrieve results if no input parameters are provided"

        if self._observables is not None:
            self._observables = self._observables.read(
                self._input_params["settings%observables_filename"],
                self.outPATH,
                {},
            )

            tensorlist = None
            for key in self._observables.keys():
                # The only key with the '/' is the MPS state
                if "/" in key:
                    tensorlist = read_mps(self._observables[key])
            if tensorlist is not None:
                self._observables["tn_state"] = tensorlist

        self._singular_values_cut = np.loadtxt(
            os.path.join(self.outPATH, "singular_values_cut.txt")
        )

    # ----------------------------
    # Methods to save/load results
    # ----------------------------
    def save_results(self, PATH, name, README=""):
        """Save the results in the folder PATH, creating a new subfolder named name

        Parameters
        ----------
        PATH: str
            path to the folder where to save the results
        README: str, optional
            String to save as additional README file inside the result folder.
            Default to empty string.
        name: str, optional
            Name to add before the date_time information in the folder name

        Returns
        -------
        _PATH: str
            The PATH to the new subfolder
        """
        if not os.path.isdir(PATH):
            os.makedirs(PATH)

        # Create result folder
        _PATH = os.path.join(PATH, name)
        os.makedirs(_PATH)

        # Save results
        # Input parameters
        np.save(os.path.join(_PATH, "input_params.npy"), self.input_params)
        # Singular values
        np.save(
            os.path.join(_PATH, "singular_values_cut.npy"), self.singular_values_cut
        )
        # Initial state
        np.save(os.path.join(_PATH, "initial_state.npy"), self.initial_state)
        # Observables expectation values
        np.save(os.path.join(_PATH, "observables.npy"), self.observables)
        # README
        README = self.date_time + "\n" + README
        with open(os.path.join(_PATH, "README.txt"), "w") as RM:
            RM.write(README)

        return _PATH

    def load_results(self, PATH):
        """Load the results of a previous simulation

        Parameters
        ----------
        PATH: str
            PATH to the folder from which we want to load the results

        Returns
        -------
        README: str
            The text contained in the README file inside the folder
        """
        assert os.path.isdir(PATH), f"{PATH} is not an existing folder"

        # Act on protected variables
        # Input parameters
        self._input_params = np.load(
            os.path.join(PATH, "input_params.npy"), allow_pickle="TRUE"
        ).item()
        # Singular values
        self._singular_values_cut = np.load(
            os.path.join(PATH, "singular_values_cut.npy"), allow_pickle="TRUE"
        )
        # Initial state
        self._initial_state = np.load(
            os.path.join(PATH, "initial_state.npy"), allow_pickle="TRUE"
        )
        # Probabilities
        self._observables = np.load(
            os.path.join(PATH, "observables.npy"), allow_pickle="TRUE"
        ).item()
        # README
        with open(os.path.join(PATH, "README.txt"), "r") as RM:
            README = RM.read()
        self._datetime = README.split("\n")[0]

        return README

    def set_results(self, result_dict, singvals_cut):
        """Set the results of a simulation

        Parameters
        ----------
        result_dict: dict
            Dictionary of the attribute to be set
        singvals_cut: array-like
            Array of singular values cut through the simulation
        """
        self._observables = result_dict
        self._singular_values_cut = singvals_cut

        tensorlist = None
        for key in result_dict.keys():
            # The only key with the '/' is the MPS state
            if "/" in key:
                tensorlist = read_mps(result_dict[key])
        if tensorlist is not None:
            self._observables["tn_state"] = tensorlist

    # -----------------------------
    # Methods to access the results
    # -----------------------------
    @property
    def fidelity(self):
        """
        Return the lower bound for the fidelity of the simulation,
        using the method described in
        If you are interested in the evolution of the fidelity through
        the simulation compute it yourself using `np.cumprod(1-self.singular_values_cut)`.

        Returns
        -------
        float
            fidelity of the final state
        """

        fid = np.prod(1 - np.array(self.singular_values_cut))
        return fid

    @property
    def measures(self):
        """Obtain the measures of the simulation as a dictionary.
        The keys are the measured states, the values the number of occurrencies

        Returns
        -------
        measures: dict
            Measures of the simulation
        """
        if "projective_measurements" in self.observables.keys():
            measures = self.observables["projective_measurements"]
        else:
            measures = None
        return measures

    @property
    def statevector(self):
        """Obtain the statevector as a complex numpy array

        Returns
        -------
        statevector: np.array or None
            The statevector of the simulation
        """
        if self._statevector is None:
            if "tn_state" in self.observables.keys():
                tensor_list = self.observables["tn_state"]
                if isinstance(tensor_list[0], list):
                    tn_state = TTN.from_tensor_list(tensor_list)
                else:
                    tn_state = MPS.from_tensor_list(tensor_list)
                if tn_state.num_sites < 30:
                    self._statevector = tn_state.to_statevector(qiskit_order=True)
        return self._statevector

    @property
    def singular_values_cut(self):
        """Obtain the singular values cutted through the simulation, depending on the mode
        chosen. If 'M' for maximum (default), 'C' for cumulated.

        Returns
        -------
        singular_values_cut: np.array
            Singular values cut during the simulation
        """
        return self._singular_values_cut

    @property
    def computational_time(self):
        """Obtain the computational time of the simulation

        Returns
        -------
        computational_time: double
            computational time of the simulation
        """
        if "time" in self.observables.keys():
            time = self.observables["time"]
        else:
            time = None
        return time

    @property
    def entanglement(self):
        """Obtain the bond entanglement entropy measured along each bond of the MPS at
        the end of the simulation

        Returns
        -------
        entanglement: dict or None
            Bond entanglement entropy
        """
        if "bond_entropy" in self.observables.keys():
            entanglement = self.observables["bond_entropy"]
        elif "bond_entropy0" in self.observables.keys():
            entanglement = self.observables["bond_entropy0"]
        else:
            entanglement = None
        return entanglement

    @property
    def measure_probabilities(self):
        """Return the probability of measuring a given state, which is computed using a
        binary tree by eliminating all the branches with probability under a certain threshold.

        Returns
        -------
        measure_probabilities: dict or None
            probability of measuring a certain state if it is greater than a threshold
        """
        keys = ["unbiased_probability", "even_probability", "greedy_probability"]
        probs = []
        for key in keys:
            if key in self.observables.keys():
                probs += [self.observables[key]]
            else:
                probs += [None]
        return probs

    @property
    def date_time(self):
        """Obtain the starting date and time of the simulation, in the format
        ``Year-month-day-Hour:Minute:Second``

        Returns
        -------
        datetime: string
            The date-time when the simulation started
        """
        return self._datetime

    @property
    def input_params(self):
        """Obtain the input parameters used in the simulation, which are the following:
            - 'num_sites',              number of sites of the mps
            - 'local_dim',              local dimension of the single site
            - 'max_bond_dim',           maximum bond dimension of the mps
            - 'cut_ratio',              cut ration used in the SVD truncation
            - 'in_name',                path to the fortran input folder
            - 'out_name',               path to the Fortran output folder
            - 'trunc_tracking_mode',           mode to save the singular values cut
            - 'sparse',                 if the input gate tensors are saved as sparse
            - 'par_approach',           parallel approach of the simulation. Can be
                'SR' (serial), 'MW' (master/workers) or 'CT' (cartesian)
            - 'initial_state',          initial state of the simulation. 'Vacuum' or
                the PATH to the initial state
            - 'do_observables',         True if there are some observables to compute at
                the end

        Returns
        -------
        input_params: dict or None
            Input parameters
        """
        return self._input_params

    @property
    def tens_net(self):
        """
        Returns the tensor list in row-major format.
        The indexing of the single tensor is as follows:

        .. code-block::

            1-o-3
             2|

        Returns
        -------
        mps: list
            list of np.array tensors
        """
        if "tn_state" in self.observables.keys():
            tn_state = self.observables["tn_state"]
        else:
            tn_state = None
        return tn_state

    @property
    def initial_state(self):
        """Returns the initial state of the simulation, as an MPS in row-major format or as
        a string if starting from the Vacuum state

        Returns
        -------
        initial_state: list or str
            list of np.array tensors or Vacuum
        """
        return self._initial_state

    @property
    def observables(self):
        """Returns the expectation values of the observables as a dict with the format
            observable_name : observable_expectation_value

        Returns
        -------
        observables: dict or None
            Expectation values of the observables
        """
        return self._observables


class QCCheckpoints:
    """
    Class to handle checkpoint parameters

    Parameters
    ----------
    PATH: str, optional
        PATH to the checkpoint directory. Default `data/checkpoints/`.
    frequency: float, optional
        Decide the frequency, in **hours**, of the checkpoints.
        If negative no checkpoints are present. Default to -1.
    input_nml: str, optional
        Name of the input namelist. Default 'input.nml'
    """

    def __init__(self, PATH="data/checkoints/", frequency=-1, input_nml="input.nml"):
        self._PATH = PATH if (PATH.endswith("/")) else PATH + "/"
        self._frequency = frequency
        self._input_nml = input_nml

    def set_up(
        self,
        input_dict,
        operators=QCOperators(),
        observables=TNObservables(),
        circ_str="",
    ):
        """Set up the checkpoints directory

        Parameters
        ----------
        input_dict : dict
            Input parameter dictionary
        operators : :py:class:`QCOperators`, optional
            Tensor operators
        obervables : :py:class: `TNObservables`, optional
            Tensor observables
        circ_str: str
            circuit string
        """
        if not isinstance(operators, QCOperators):
            raise TypeError("Operators must be QCOperators type")
        elif not isinstance(observables, TNObservables):
            raise TypeError("observables must be TNObservables type")

        if not os.path.isdir(self.PATH):
            os.mkdir(self.PATH)

        # Modify for new PATH
        input_dict["inPATH"] = self.PATH

        # Write files that can be already written
        with open(os.path.join(self.PATH, "observables.pk"), "wb") as fh:
            pickle.dump(observables, fh)
        _, operator_mapping = operators.write_input_3(self.PATH)
        observables.write(self.PATH, {}, operator_mapping)
        write_nml("INPUT", input_dict, os.path.join(self.PATH, self.input_nml))
        with open(os.path.join(self.PATH, "circuit.dat"), "w") as fh:
            fh.write(circ_str)

    @property
    def PATH(self):
        """PATH property"""
        return self._PATH

    @property
    def frequency(self):
        """Checkpoint frequency property"""
        return self._frequency

    @property
    def input_nml(self):
        """Input namelist property"""
        return self._input_nml

    def to_dict(self):
        """Return the ordered dictionary of the properties of
        the class

        Returns
        -------
        dictionary: OrderedDict
            Ordered dictionary of the class properties
        """
        dictionary = OrderedDict()

        dictionary["checkpoint_PATH"] = self.PATH
        dictionary["checkpoint_frequency"] = self.frequency
        dictionary["initial_line"] = 1

        return dictionary


class QCIO:
    """
    Class to handle Input/Output parameters

    Parameters
    ----------
    inPATH: str, optional
        PATH to the directory containing the input files.
        Default to 'data/in/'
    outPATH: str, optional
        PATH to the directory containing the output files.
        Default to 'data/out/'
    input_namelist: str, optional
        Name of the input namelist file. Name, NOT PATH.
        Default to 'input.nml'
    exe_file: list of str, optional
        Path to the executable plus additional commands
        Default to `[EXE_PATH_SERIAL]`.
    initial_state: str or :py:class:`MPS`, optional
        If an MPS, then the list of tensors is used as initial state for
        a starting point of the FORTRAN simulation, saving the file to
        inPATH/initial_state.dat. If 'Vacuum' start from |000...0>. Default to 'Vacuum'.
        If a PATH it is a PATH to a saved MPS.
    sparse: bool, optional
        Weather to write operators in a semi-sparse format or not.
        Default to False
    """

    def __init__(
        self,
        inPATH="data/in/",
        outPATH="data/out/",
        input_namelist="input.nml",
        exe_file=None,
        initial_state="Vacuum",
        sparse=False,
    ):
        self._inPATH = inPATH if inPATH.endswith("/") else inPATH + "/"
        self._outPATH = outPATH if outPATH.endswith("/") else outPATH + "/"
        self._input_namelist = input_namelist

        if exe_file is None:
            self._exe_file = [EXE_PATH]
        # Check if people don't read docstring
        # and use strings nevertheless
        elif isinstance(exe_file, str):
            self._exe_file = [exe_file]
        else:
            self._exe_file = exe_file
        self._sparse = sparse
        self._initial_state = initial_state

    def setup(self):
        """Setup the io files"""

        # Directories
        if not os.path.isdir(self.inPATH):
            os.makedirs(self.inPATH)
        if not os.path.isdir(self.outPATH):
            os.makedirs(self.outPATH)

        # Executable
        if self.exe_file[-1] != os.path.join(self.inPATH, self.input_namelist):
            self._exe_file += [os.path.join(self.inPATH, self.input_namelist)]

        # Initial state
        if self.initial_state != "Vacuum":
            if isinstance(self.initial_state, str):
                # Handle the string case assuming it is a path
                if not os.path.isfile(self.initial_state):
                    raise Exception("Path to input file does not exist.")
                else:
                    new_path = os.path.join(
                        self.inPATH, os.path.basename(self.initial_state)
                    )
                    if not os.path.samefile(self._initial_state, new_path):
                        shutil.move(self.initial_state, new_path)
                        self._initial_state = os.path.basename(self.initial_state)
            else:
                # Assume it is an MPS that we can write
                self.initial_state.write(os.path.join(self.inPATH, "initial_state.dat"))
                self._initial_state = "initial_state.dat"

    @property
    def inPATH(self):
        """Input PATH property"""
        return self._inPATH

    @property
    def exe_cmd(self):
        """Executable command to run on the terminal"""
        return [self.exe_file, self._inPATH + self._input_namelist]

    @property
    def outPATH(self):
        """Output PATH property"""
        return self._outPATH

    @property
    def input_namelist(self):
        """Input namelist property"""
        return self._input_namelist

    @property
    def exe_file(self):
        """Executable file and commands property"""
        return self._exe_file

    @property
    def sparse(self):
        """Tensor sparsity property"""
        return self._sparse

    @property
    def initial_state(self):
        """Initial state property"""
        return self._initial_state

    # @initial_state.setter
    def set_initial_state(self, initial_state):
        """Modify the initial state property"""
        if not isinstance(initial_state, str):
            if not isinstance(initial_state, MPS):
                raise TypeError(
                    "A non-str initial state must be initialized as MPS class"
                )
        self._initial_state = initial_state

    # @exe_file setter
    def set_exe_file(self, exe_file):
        """Modify exe file"""
        if not isinstance(exe_file, list):
            raise TypeError(f"exe_file must be a list of strings, not {type(exe_file)}")
        self._exe_file = exe_file

    def to_dict(self):
        """Return the ordered dictionary of the properties of
        the class

        Returns
        -------
        dictionary: OrderedDict
            Ordered dictionary of the class properties
        """
        dictionary = OrderedDict()
        for prop, value in vars(self).items():
            if prop in ("_exe_file", "_input_namelist"):
                continue
            dictionary[prop[1:]] = value

        return dictionary


class QCConvergenceParameters(TNConvergenceParameters):
    """Convergence parameter class, inhereting from the
    more general Tensor Network type. Here the convergence
    parameters are only the bond dimension and the cut ratio.

    Parameters
    ----------
    max_bond_dimension : int, optional
        Maximum bond dimension of the problem. Default to 10.
    cut_ratio : float, optional
        Cut ratio for singular values. If :math:`\\lambda_n/\\lambda_1 <` cut_ratio then
        :math:`\\lambda_n` is neglected. Default to 1e-9.
    trunc_tracking_mode : str, optional
        Modus for storing truncation, 'M' for maximum, 'C' for
        cumulated (default).

    """

    def __init__(
        self,
        max_bond_dimension=10,
        cut_ratio=1e-9,
        trunc_tracking_mode="C",
        singval_mode=None,
    ):
        if singval_mode is not None:
            warn(
                "singval_mode parameter is deprecated. Please use trunc_tracking_mode instead"
            )
            trunc_tracking_mode = singval_mode
        TNConvergenceParameters.__init__(
            self,
            max_bond_dimension=max_bond_dimension,
            cut_ratio=cut_ratio,
            trunc_tracking_mode=trunc_tracking_mode,
        )

    def to_dict(self):
        """Return the ordered dictionary of the properties of
        the class

        Returns
        -------
        dictionary: OrderedDict
            Ordered dictionary of the class properties
        """
        dictionary = OrderedDict()
        dictionary["max_bond_dimension"] = self.max_bond_dimension
        dictionary["cut_ratio"] = self.cut_ratio
        dictionary["trunc_tracking_mode"] = self.trunc_tracking_mode

        return dictionary


class QCBackend:
    """
    Backend for the simulation. Contains all the informations about
    which executable you want to run

    Parameters
    ----------
    backend : str, optional
        First backend definition. Either "PY" (python) or "FR" (fortran).
        Default to "PY".
    precision: str, optional
        Precision of the simulation. Either "Z" (double complex) or "C"
        (single complex). Default to "Z".
    device: str, optional
        Device of the simulation. Either "cpu" or "gpu". Default to "cpu".
    num_procs: int, optional
        Number of processes for the MPI simulation. Default to 1.
    mpi_approach: str, optional
        Approach for the MPI simulation. Either "MW", "CT" or "SR".
        Default to "SR".
    ansatz : str, optional
        Weather to run the circuit with MPS or TTN tensor network ansatz.
        Default to "MPS".
    """

    def __init__(
        self,
        backend="PY",
        precision="Z",
        device="cpu",
        num_procs=1,
        mpi_approach="SR",
        ansatz="MPS",
    ):
        if backend == "PY" and mpi_approach != "SR":
            raise ValueError("Only serial simulation available in python")
        if backend == "FR" and device == "gpu" and precision == "C":
            raise ValueError(
                "Only double precision complex available "
                + "in fortran with the GPU device"
            )
        if num_procs == 1:
            mpi_approach = "SR"

        self._backend = backend.upper()
        self._precision = precision.upper()
        self._device = device
        self._num_procs = num_procs
        self._mpi_approach = mpi_approach.upper()
        if backend == "FR" and ansatz.upper() != "MPS":
            warn(
                f"Only MPS ansatz available on fortran simulation, not {ansatz}."
                + "The ansatz is set back to MPS."
            )
            ansatz = "MPS"
        self._ansatz = ansatz.upper()

    def to_dict(self):
        """
        Map the backend to a dictionary for fortran
        """
        dictionary = OrderedDict({})
        mpi = "T" if self._num_procs > 1 else "F"
        gpu = "T" if self.device == "gpu" else "F"
        dictionary["simulation_mode"] = self.precision + mpi + gpu
        dictionary["approach"] = self.mpi_approach
        # dictionary["ansatz"] = self.ansatz

        return dictionary

    @property
    def backend(self):
        """Backend property"""
        return self._backend

    @property
    def precision(self):
        """Precision property"""
        return self._precision

    @property
    def device(self):
        """Device property"""
        return self._device

    @property
    def num_procs(self):
        """Number of processes property"""
        return self._num_procs

    @property
    def mpi_approach(self):
        """mpi_approach property"""
        return self._mpi_approach

    @property
    def ansatz(self):
        """ansatz property"""
        return self._ansatz

    @property
    def identifier(self):
        """Identifier combining all properties."""
        return ":".join(
            [
                self.backend,
                self.precision,
                self.device,
                str(self.num_procs),
                self.mpi_approach,
                self.ansatz,
            ]
        )


def merge_ordered_dicts(dicts):
    """Merge ordered dicts together, concatenating them in the order provided in the list

    Parameters
    ----------
    dicts : list of OrderedDict
        OrderedDict to concatenate

    Return
    ------
    final_dict: OrderedDict
        Concatenated OrderedDict
    """
    for dictionary in dicts:
        if not isinstance(dictionary, OrderedDict):
            raise TypeError("Only OrderedDict can be concatenated using this function")

    final_dict = dicts[0]
    for dictionary in dicts[1:]:
        final_dict.update(dictionary)

    return final_dict


def print_state(dense_state):
    """
    Prints a *dense_state* with kets. Compatible with quimb states.

    Parameters
    ----------
    dense_state: array_like
            Dense representation of a quantum state

    Returns
    -------
    None: None
    """

    NN = int(np.log2(len(dense_state)))

    binaries = [bin(ii)[2:] for ii in range(2**NN)]
    binaries = ["0" * (NN - len(a)) + a for a in binaries]  # Pad with 0s

    ket = []
    for ii, coef in enumerate(dense_state):
        if not np.isclose(np.abs(coef), 0.0):
            if np.isclose(np.imag(coef), 0.0):
                if np.isclose(np.real(coef), 1.0):
                    ket.append("|{}>".format(binaries[ii]))
                else:
                    ket.append("{:.3f}|{}>".format(np.real(coef), binaries[ii]))
            else:
                ket.append("{:.3f}|{}>".format(coef, binaries[ii]))
    print(" + ".join(ket))


def fidelity(psi, phi):
    """
    Returns the fidelity bewteen two quantum states *psi*, *phi* defined as
    :math:`|\\langle\\psi|phi\\rangle|^2`

    Parameters
    ----------
    psi: complex np.array or quimb.core.qarray
            Quantum state
    phi: complex np.array or quimb.core.qarray
            Quantum state

    Returns
    -------
    Fidelity: double real
            Fidelity of the two quantum states
    """

    # Enforcing normalization
    psi /= np.sqrt(np.abs(np.sum(psi.conj() * psi)))
    phi /= np.sqrt(np.abs(np.sum(phi.conj() * phi)))

    return np.abs(np.vdot(psi, phi)) ** 2
