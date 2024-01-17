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
MPS python simulator.
Mimicks exactly the behavior of the FORTRAN simulator if it is
called with the :py:func:`run_simulation`, reading from files.

It can also enable full python simulations without the IO interface
by using the :py:class:`QCEmulator` class.

Functions and classes
~~~~~~~~~~~~~~~~~~~~~

"""

import os
import time
from warnings import warn
from copy import deepcopy

import numpy as np
from qiskit import QuantumCircuit
from qtealeaves import read_tensor
from qtealeaves.convergence_parameters import TNConvergenceParameters
from qtealeaves.emulator import MPS, TTN, _AbstractTN
from qtealeaves.observables import TNObservables

# Try to import cupy
try:
    import cupy as cp
    from cupy_backends.cuda.api.runtime import CUDARuntimeError

    try:
        _ = cp.cuda.Device()
        GPU_AVAILABLE = True
    except CUDARuntimeError:
        GPU_AVAILABLE = False
except ImportError:
    cp = None
    GPU_AVAILABLE = False

from .circuit import Qcircuit
from .circuit.observables import QCObservableStep
from .preprocessing import preprocess
from .tn_utils import read_nml, QCOperators, write_tensor
from .qk_utils import qk_transpilation_params
from .utils import QCIO, QCConvergenceParameters, simulation_results
from .utils import QCBackend

__all__ = ["QcMps", "QCEmulator", "mock_fortran", "run_py_simulation"]


class QCEmulator:
    """
    Emulator class to run quantum circuits, powered by either
    TTNs or MPS.


    Parameters
    ----------

    num_sites: int
        Number of sites
    num_clbits: int
        Number of classical bits
    convergence_parameters: :py:class:`QCConvergenceParameters`
        Class for handling convergence parameters. In particular, in the MPS simulator we are
        interested in:
        - the *maximum bond dimension* :math:`\\chi`;
        - the *cut ratio* :math:`\\epsilon` after which the singular values are neglected, i.e.
          if :math:`\\lambda_1` is the bigger singular values then after an SVD we neglect all the
          singular values such that :math:`\\frac{\\lambda_i}{\\lambda_1}\\leq\\epsilon`
    local_dim: int, optional
        Local dimension of the degrees of freedom. Default to 2.
    """

    def __init__(
        self,
        num_sites,
        convergence_parameters=QCConvergenceParameters(),
        local_dim=2,
        dtype=np.complex128,
        device="cpu",
        ansatz="MPS",
    ):
        if not isinstance(convergence_parameters, TNConvergenceParameters):
            raise TypeError(
                "convergence_parameters must be of the QCConvergenceParameters class"
            )

        self._trunc_tracking_mode = convergence_parameters.trunc_tracking_mode
        self.ansatz = ansatz

        # Classical registers to hold qiskit informations
        self.cl_regs = {}

        # Observables measured
        self.is_measured = [
            True,
            False,
            False,
            True,
            True,
            True,
            True,
            True,
            True,
            False,
            False,
        ]

        if ansatz.upper() == "MPS":
            self.emulator = MPS(
                num_sites=num_sites,
                convergence_parameters=convergence_parameters,
                local_dim=local_dim,
                dtype=dtype,
                device=device,
            )
        elif ansatz.upper() == "TTN":
            zero_state = np.zeros((num_sites, local_dim), dtype=dtype)
            zero_state[:, 0] = 1
            self.emulator = TTN.product_state_from_local_states(
                zero_state,
                convergence_parameters=convergence_parameters,
                dtype=dtype,
                device=device,
            )
        else:
            raise ValueError(f"Ansatz {ansatz} is not available for QCEmulator")

    def __getattr__(self, __name: str):
        """
        Check for the attribute in emulator, i.e. the QCEmulator inherits all
        the emulator calls.
        This call is for convenience and for retrocompatibility

        .. warning::
            The method `__getattr__` is called when `__getattribute__` fails,
            so it already covers the possibility of the attribute being in the
            base class
        """
        return self.emulator.__getattribute__(__name)

    @classmethod
    def from_emulator(cls, emulator, conv_params=None, dtype=None):
        """
        Initialize the QCEmulator class starting from an emulator class, i.e. either
        MPS or TTN

        Parameters
        ----------
        emulator : :class:`_AbstractTN`
            Either an MPS or TTN emulator
        conv_params : :class:`TNConvergenceParameters`, optional
            Convergence parameters. If None, the convergence parameters of the emulator
            are used
        dtype : type, optional
            Type to be used, If None, the dtype of the emulator is used

        Return
        ------
        QCEmulator
            The quantum circuit emulator class
        """
        if not isinstance(emulator, _AbstractTN):
            raise TypeError("The emulator should be a TN emulator class")
        if conv_params is None:
            conv_params = emulator.convergence_parameters
        if dtype is None:
            dtype = emulator.dtype

        simulator = cls(
            emulator.num_sites, conv_params, emulator.local_dim, dtype=dtype
        )
        simulator.emulator = emulator
        simulator.ansatz = str(emulator)

        return simulator

    @classmethod
    def from_tensor_list(cls, tensor_list, conv_params=None, dtype=None):
        """
        Initialize the QCEmulator class starting from a tensor list, i.e. either
        MPS or TTN

        Parameters
        ----------
        tensor_list : list of tensors
            Either an MPS or TTN list of tensors
        conv_params : :class:`TNConvergenceParameters`, optional
            Convergence parameters. If None, the convergence parameters of the emulator
            are used
        dtype : type, optional
            Type to be used, If None, the dtype of the emulator is used

        Return
        ------
        QCEmulator
            The quantum circuit emulator class
        """
        # A list of lists is a TTN, while a list of tensors is an MPS
        if isinstance(tensor_list[0], list):
            initial_state = TTN.from_tensor_list(tensor_list)
        else:
            initial_state = MPS.from_tensor_list(tensor_list)

        simulator = cls.from_emulator(
            initial_state, conv_params=conv_params, dtype=dtype
        )

        return simulator

    def meas_projective(
        self, nmeas=1024, qiskit_convention=True, seed=None, unitary_setup=None
    ):
        """See the parent method"""
        return self.emulator.meas_projective(
            nmeas=nmeas,
            qiskit_convention=qiskit_convention,
            seed=seed,
            unitary_setup=unitary_setup,
        )

    def to_statevector(self, qiskit_order=True, max_qubit_equivalent=20):
        """See the parent method"""
        return self.emulator.to_statevector(qiskit_order, max_qubit_equivalent)

    def apply_two_site_gate(self, operator, control, target):
        """Apply a two-site gate, regardless of the position on the chain

        Parameters
        ----------
        operator : np.ndarray
            Gate to be applied
        control : int
            control qubit index
        target : int
            target qubit index

        Returns
        -------
        singvals_cut
            singular values cut in the process
        """
        xp = self._device_checks()
        if operator.shape == (4, 4):
            operator = operator.reshape(2, 2, 2, 2)
        # Reorder for qiskit convention on the two-qubits gates
        if control < target or self.ansatz == "TTN":
            operator = xp.transpose(operator, [1, 0, 3, 2])

        singvals_cut = self.apply_two_site_operator(operator, [control, target])

        # Avoid errors due to no singv cut
        singvals_cut = np.append(singvals_cut, 0)
        if self._trunc_tracking_mode == "M":
            singvals_cut = max(0, xp.max(singvals_cut))
        elif self._trunc_tracking_mode == "C":
            singvals_cut = xp.sum(singvals_cut**2)

        return [singvals_cut]

    def meas_observables(self, observables, op_list, op_mapping=None, approach="PF"):
        """Measure all the observables

        Parameters
        ----------
        observables : :py:class:`TNObservables`
            All the observables to be measured
        op_list : list of tensors
            List of operators that form the circuit stored in THE CORRECT DEVICE.
            If you are running on GPU the operators should be on the GPU.
        op_mapping : dict
            Mapping between the operators name and the operators idx
        approach : string, optional
            Approach of the simulation, if 'PY', 'PF'

        Returns
        -------
        TNObservables
            Observables with the results in results_buffer
        """
        if not isinstance(observables, TNObservables):
            raise TypeError("observables must be TNObservables")

        keys = np.array(list(observables.obs_list.keys()))[self.is_measured]
        ii = 0
        ## LOCAL OBSERVABLES ##
        local = observables.obs_list[keys[ii]]
        for name, idx in zip(local.name, local.operator):
            if approach == "PF":
                idx = op_mapping[idx] - 1
            local.results_buffer[name] = self.meas_local(op_list[idx])
        ii += 1

        ## SAVE STATE ##
        state_obs = observables.obs_list[keys[ii]]
        if len(state_obs.name) > 0:
            if approach == "PY":
                observables.results_buffer["tn_state"] = self.emulator.to_tensor_list()
            else:
                name = state_obs.name[0]
                state_obs.results_buffer[name] = name
                self.emulator.write(name)
        ii += 1

        ## TENSOR PRODUCT OBSERVABLES ##
        tensor_prod = observables.obs_list[keys[ii]]
        for name, ops, sites in zip(
            tensor_prod.name, tensor_prod.operators, tensor_prod.sites
        ):
            sites = [site[0] for site in sites]
            if approach == "PF":
                operators = [op_list[op_mapping[ii] - 1] for ii in ops]
            else:
                operators = [op_list[ii] for ii in ops]
            tensor_prod.results_buffer[name] = np.complex128(
                self.emulator.meas_tensor_product(operators, sites)
            )
        ii += 1

        ## WEIGHTED SUM OBSERVABLES ##
        wsum = observables.obs_list[keys[ii]]
        for name, coef, tp_ops in zip(wsum.name, wsum.coeffs, wsum.tp_operators):
            op_string = []
            idxs_string = []
            if isinstance(tp_ops, list):
                tp_op = tp_ops[0]
            else:
                tp_op = tp_ops
            for ops, sites in zip(tp_op.operators, tp_op.sites):
                sites = [site[0] for site in sites]
                if approach == "PF":
                    operators = [op_list[op_mapping[ii] - 1] for ii in ops]
                else:
                    operators = [op_list[ii] for ii in ops]
                idxs_string.append(sites)
                op_string.append(operators)

            wsum.results_buffer[name] = np.complex128(
                self.emulator.meas_weighted_sum(op_string, idxs_string, coef)
            )
        ii += 1

        ## FINAL PROJECTIVE MEASUREMENT OBSERVABLES ##
        proj_obs = observables.obs_list[keys[ii]]
        proj_obs.results_buffer[proj_obs.name[0]] = self.meas_projective(
            nmeas=proj_obs.num_shots
        )
        ii += 1

        ## PROBABILITY MEASURE ##
        prob_obs = observables.obs_list[keys[ii]]
        for name, prob_type, prob_param in zip(
            prob_obs.name, prob_obs.prob_type, prob_obs.prob_param
        ):
            if isinstance(name, list):
                name = name[0]
            if prob_type == "U":
                prob_obs.results_buffer[
                    name
                ] = self.emulator.meas_unbiased_probabilities(prob_param, True)
            elif prob_type == "E":
                prob_obs.results_buffer[name] = self.emulator.meas_even_probabilities(
                    prob_param, True
                )
            elif prob_type == "G":
                prob_obs.results_buffer[name] = self.emulator.meas_greedy_probabilities(
                    prob_param, True
                )
        ii += 1

        ## ENTANGLEMENT MEASURE ##
        ent_obs = observables.obs_list[keys[ii]]
        if len(ent_obs.name) == 1:
            bond_entropy = self.emulator.meas_bond_entropy()
            ent_obs.results_buffer[ent_obs.name[0]] = bond_entropy
        ii += 1

        return observables

    def run_circuit_from_instruction(self, op_list, instr_list):
        """Run a circuit

        Parameters
        ----------
        op_list : list of tensors
            List of operators that form the circuit
        instr_list : list of instructions
            Instruction for the circuit, i.e. [op_name, op_idx, [sites] ]

        Return
        ------
        singvals_cut : list of float
            Singular values cutted, selected through the _trunc_tracking_mode
        """
        singvals_cut = []
        for instr in instr_list:
            sites = instr[2]
            num_sites = len(sites)
            idx = instr[1]
            if instr[0] == "barrier":
                continue

            if num_sites == 1:
                self.emulator.apply_one_site_operator(op_list[idx], *sites)

            elif num_sites == 2:
                singv_cut = self.apply_two_site_gate(op_list[idx], sites[0], sites[1])

                # Avoid errors due to no singv cut
                singv_cut = np.append(singv_cut, 0)
                if self._trunc_tracking_mode == "M":
                    singvals_cut.append(np.max(singv_cut, initial=0.0))
                elif self._trunc_tracking_mode == "C":
                    singvals_cut.append(np.sum(singv_cut**2))

            else:
                raise ValueError("Only one and two-site operations are implemented")
        return singvals_cut

    def run_from_qk(self, circuit):
        """
        Run a qiskit quantum circuit on the simulator

        Parameters
        ----------
        circuit : :py:class:`QuantumCircuit`
            qiskit quantum circuit

        Returns
        -------
        list of floats
            singular values cutted in the simulation
        """
        xp = self._device_checks()
        data = circuit.data  # data structure of the quantum circuit
        singvals_cut = []
        for creg in circuit.cregs:
            self.cl_regs[creg.name] = np.zeros(creg.size)

        # Run over instances
        for instance in data:
            gate_name = instance[0].name
            num_qubits = len(instance[1])
            qubits = [circuit.find_bit(qub).index for qub in instance[1]]

            if gate_name == "barrier":
                continue
            elif gate_name == "measure":
                meas_state, _ = self.apply_projective_operator(*qubits)
                self.cl_regs[instance[2][0].register.name][0] = meas_state
                continue
            elif gate_name == "reset":
                self.reset(qubits)
                continue
            else:
                gate_mat = instance[0].to_matrix()

            if instance[0].condition is None:
                apply_gate = True
            else:
                bit_idx = [clbit.index for clbit in instance[0].condition[0]]
                bit_value = self.cl_regs[instance[0].condition[0].name][bit_idx[0]]
                apply_gate = bit_value == instance[0].condition[1]

            if apply_gate:
                # Move the operator to the GPU
                if xp == cp:
                    gate_mat = cp.asarray(gate_mat)
                if num_qubits == 1:
                    self.emulator.apply_one_site_operator(gate_mat, *qubits)
                elif num_qubits == 2:
                    singv_cut = self.apply_two_site_gate(gate_mat, *qubits)
                    singvals_cut += singv_cut
                else:
                    raise ValueError("Only one and two-site operations are implemented")
        return singvals_cut

    def run_from_qcirc(self, qcirc, starting_idx=0):
        """
        Run a simulation starting from a Qcircuit on a portion of the MPS state

        Parameters
        ----------
        qcirc : :class:`Qcircuit`
            Quantum circuit
        starting_idx : int, optional
            MPS index that correspond to the index 0 of the Qcircuit. Default to 0.
        """
        if not isinstance(qcirc, Qcircuit):
            raise TypeError(f"qcirc must be of type Qcircuit, not {type(qcirc)}")
        xp = self._device_checks()
        results = {}
        svd_cuts = []
        start_time = time.time()
        for layer in qcirc:
            for instruction in layer:
                sites = [ss + starting_idx for ss in instruction[1]]
                operation = instruction[0]

                # Check for classical conditioning
                appy_operation = operation.c_if.is_satisfied(qcirc)
                if appy_operation:
                    # First, check for particular keywords
                    if isinstance(operation, QCObservableStep):
                        obs = self.meas_observables(
                            operation.observables,
                            operation.operators.ops,
                            approach="PY",
                        )
                        obs.results_buffer["time"] = time.time() - start_time
                        obs.results_buffer["norm"] = self.norm()
                        operation.observables = obs
                        operation.postprocess_obs_indexing()  # Postprocess for qregisters
                        for elem in obs.obs_list:
                            obs.results_buffer.update(obs.obs_list[elem].results_buffer)
                        results[operation.name] = deepcopy(
                            operation.observables.results_buffer
                        )
                        del obs

                    # Check for particular keywords
                    elif operation.name == "renormalize":
                        self.normalize()
                    elif operation.name == "measure":
                        res = self.emulator.apply_projective_operator(
                            *sites, operation.selected_output
                        )
                        # Update measured value
                        qcirc.modify_cregister(
                            res, operation.cregister, operation.cl_idx
                        )
                    elif operation.name == "add_site":
                        self.emulator.add_site(operation.position)
                    elif operation.name == "remove_site":
                        self.apply_projective_operator(operation.position, remove=True)

                    # Apply gates
                    elif len(sites) == 1:
                        if xp == cp:
                            gate_mat = cp.asarray(gate_mat)
                        self.site_canonize(*sites, keep_singvals=True)
                        self.apply_one_site_operator(operation.operator, *sites)
                    else:
                        if xp == cp:
                            gate_mat = cp.asarray(gate_mat)
                        svd_cut = self.apply_two_site_gate(operation.operator, *sites)
                        svd_cuts += svd_cut

        # Truncation
        results["singular_values_cut"] = svd_cuts
        return results


class QcMps(QCEmulator):
    """
    Class for retrocompatibility with QCEmulator
    """

    def __init__(self, *args, **kwargs):
        warn("Using deprecated QcMps, please switch to QCEmulator")
        super().__init__(*args, **kwargs)


def mock_fortran(command_line, observables, op_mapping):
    """
    Mock the execution of the Fortran program, by doing the exact same things Fortran would do

    Parameters
    ----------
    command_line : list of str
        List of commands that should be run on terminal for the compiled fortran simulator
    """
    input_dict_path = command_line[-1]
    if not os.path.isfile(input_dict_path):
        raise ValueError(
            'The given PATH "%s" for the input file is not a file.'
            % (str(input_dict_path))
        )

    _, input_dict = read_nml(command_line[-1])

    # Checks and retrieval on input parameters
    if input_dict["checkpoint_frequency"] > 0:
        raise NotImplementedError(
            "Checkpoints are not implemented in the python simulator"
        )
    io_info = QCIO(
        inPATH=input_dict["inPATH"],
        outPATH=input_dict["outPATH"],
        sparse=input_dict["sparse"],
    )
    conv_params = QCConvergenceParameters(
        max_bond_dimension=input_dict["max_bond_dimension"],
        cut_ratio=input_dict["cut_ratio"],
        trunc_tracking_mode=input_dict["trunc_tracking_mode"],
    )

    # Retrieve input information on operators and circuit
    op_list, instruction_list, num_sites, num_cl_bits = _mock_fortran_input(io_info)

    # Initialize the state
    emulator = QCEmulator(
        num_sites,
        num_cl_bits,
        conv_params,
        input_dict["local_dim"],
        ansatz=input_dict["ansatz"],
    )

    # Retrieve initial state if present
    if input_dict["initial_state"] != "Vacuum":
        initial_state_path = os.path.join(io_info.inPATH, input_dict["initial_state"])
        emulator.read(initial_state_path)

    # Run the circuit
    start = time.time()
    singvals_cut = emulator.run_circuit_from_instruction(op_list, instruction_list)
    simulation_time = time.time() - start

    # Perform measurements and final operations
    observables = _mock_fortran_measurements(emulator, observables, op_list, op_mapping)
    observables.results_buffer["time"] = simulation_time

    # Write everithing in the output directory
    _mock_fortran_output(emulator, io_info, input_dict, singvals_cut, observables)

    return True


def _mock_fortran_input(io_info):
    """
    Perform the reading necessary for the python emulator

    Parameters
    ----------
    io_info : :py:class:`QCIO`
        IO informations

    Returns
    -------
    op_list: list of ndarray
        List of operators
    instruction_list: list
        list of instruction for the circuit
    num_sites: int
        Number of sites in the MPS
    num_cl_bits : int
        Number of classical bits in the MPS
    """
    if not isinstance(io_info, QCIO):
        raise TypeError("io_info must be of type QCIO")

    # Retrieve operators
    op_path = os.path.join(io_info.inPATH, "TENSORS/operators.dat")
    op_list = []
    with open(op_path, "r") as fh:
        op_num = int(fh.readline().replace("\n", ""))
        for _ in range(op_num):
            tens = read_tensor(fh)
            op_list.append(tens)

    # Retrieve circuit
    instruction_path = os.path.join(io_info.inPATH, "circuit.dat")
    instruction_list = []
    with open(instruction_path, "r") as fh:
        num_sites = int(fh.readline().replace("\n", ""))
        num_cl_bits = int(fh.readline().replace("\n", ""))
        num_lines = int(fh.readline().replace("\n", ""))
        for _ in range(num_lines):
            line_1 = fh.readline().replace("\n", "").split(" ")
            line_2 = fh.readline().replace("\n", "").split(" ")
            line_2.remove("")
            # [ name, op_idx, [qubits] ]
            instruction = [
                line_1[0],
                int(line_1[1]) - 1,
                [int(site) - 1 for site in line_2],
            ]

            instruction_list.append(instruction)

    return op_list, instruction_list, num_sites, num_cl_bits


def _mock_fortran_measurements(emulator, observables, op_list, op_mapping):
    """
    Perform the different measurements to mock with python a fortran simulation

    Parameters
    ----------
    emulator : :py:class:`QCEmulator`
        Matrix product state class
    observables : :py:class:`TNObservables`
        Observables class
    op_list : list of ndarray
        List of operators

    Return
    ------
    measurements : OrderedDict
        Ordered dictionary with as keys:
            - proj_meas, the projective measurements dictionary
            - statevector, the statevector
            - entanglement, the entanglement
            - obs_results, the observables results

    """
    if not isinstance(emulator, QCEmulator):
        raise TypeError("mps_state must be of type emulator")
    elif not isinstance(observables, TNObservables):
        raise TypeError("observables must be of type TNObservables")

    # Observables with measured quantities
    observables = emulator.meas_observables(observables, op_list, op_mapping)
    observables.results_buffer["energy"] = 999e300
    observables.results_buffer["norm"] = emulator.norm()

    return observables


def _mock_fortran_output(emulator, io_info, input_dict, singval_cut, observables):
    """
    Mock the fortran simulator by writing the same output files it would
    write

    Parameters
    ----------
    emulator : :py:class:`QCEmulator`
        QCEmulator state class
    io_info : :py:class:`QCIO`
        Info about the output file path
    input_dict : OrderedDict
        Ordered dictionary with the input parameters
    singval_cut : array-like
        Singular values cut in the simulation
    observables : :py:class:`TNObservables`
        Observables
    """
    if not isinstance(emulator, QCEmulator):
        raise TypeError("mps_state must be of type QCEmulator")
    elif not isinstance(io_info, QCIO):
        raise TypeError("io_info must be of type QCIO")

    # Observables
    obs_path = os.path.normpath(input_dict["observables_filename"])
    obs_path = os.path.join(io_info.outPATH, obs_path)
    observables.write_results(obs_path, emulator.is_measured, {})

    with open(os.path.join(io_info.outPATH, "singular_values_cut.txt"), "w") as fh:
        _write_value(singval_cut, fh)


def run_py_simulation(
    circ,
    local_dim=2,
    convergence_parameters=QCConvergenceParameters(),
    operators=QCOperators(),
    observables=TNObservables(),
    initial_state=None,
    transpilation_parameters=qk_transpilation_params(),
    backend=QCBackend(),
):
    """
    Transpile the circuit to adapt it to the linear structure of the MPS and run the circuit,
    obtaining in output the measurements.

    Parameters
    ----------
    circ: QuantumCircuit or strawberryfields.Program
        qiskit quantum circuit object to simulate
    local_dim: int, optional
        Local dimension of the single degree of freedom. Default is 2, for qubits
    convergence_parameters: :py:class:`QCConvergenceParameters`, optional
        Maximum bond dimension and cut ratio. Default to max_bond_dim=10, cut_ratio=1e-9.
    operators: :py:class:`QCOperators`, optional
        Operator class with the observables operators ALREADY THERE. If None, then it is
        initialized empty. Default to None.
    observables: :py:class:`TNObservables`, optional
        The observables to be measured at the end of the simulation. Default to TNObservables(),
        which contains no observables to measure.
    initial_state : list on ndarray, optional
        Initial state of the simulation. If None, ``|00...0>`` is considered. Default to None.
    transpilation_parameters: :py:class:`qk_transpilation_params`, optional
        Parameters used in the qiskit transpilation phase. Default to qk_transpilation_params().
    backend: :py:class:`QCBackend`, optional
        Backend containing all the information for where to run the simulation

    Returns
    -------
    result: qmatchatea.simulation_results
        Results of the simulation, containing the following data:
        - Measures
        - Statevector
        - Computational time
        - Singular values cut
        - Entanglement
        - Measure probabilities
        - MPS state
        - MPS file size
        - Observables measurements
    """
    # Preprocess the circuit to adapt it to the MPS constraints (linearity)
    preprocessed_circ = preprocess(circ, qk_params=transpilation_parameters)

    if isinstance(circ, QuantumCircuit):
        num_qubits = circ.num_qubits
        # num_clbits = circ.num_clbits
    else:
        raise TypeError(
            "Only qiskit Quantum Circuits are implemented for pure python"
            + f" simulation, not {type(circ)}"
        )
    tn_type = np.complex128 if backend.precision == "Z" else np.complex64
    start = time.time()
    if initial_state is None or initial_state == "Vacuum":
        simulator = QCEmulator(
            num_qubits,
            convergence_parameters,
            local_dim=local_dim,
            dtype=tn_type,
            ansatz=backend.ansatz,
        )
    elif isinstance(initial_state, _AbstractTN):
        simulator = QCEmulator.from_emulator(
            initial_state, conv_params=convergence_parameters, dtype=tn_type
        )
    else:
        simulator = QCEmulator.from_tensor_list(
            initial_state, conv_params=convergence_parameters, dtype=tn_type
        )

    simulator.to_device(backend.device)
    singvals_cut = simulator.run_from_qk(preprocessed_circ)
    end = time.time()

    observables = simulator.meas_observables(observables, operators.ops, approach="PY")
    observables.results_buffer["time"] = end - start
    observables.results_buffer["energy"] = None
    observables.results_buffer["norm"] = simulator.norm()

    result_dict = observables.results_buffer
    for elem in observables.obs_list:
        result_dict.update(observables.obs_list[elem].results_buffer)

    results = simulation_results()
    results.set_results(result_dict, singvals_cut)

    return results


def _write_value(value, fh):
    """
    Print a value for the mock fortran output
    based on its type

    Parameters
    ----------
    value : scalar, dict or array-like
        value to be saved
    fh : file handler
        Where to write the values
    """

    # None case
    if value is not None:
        # Writing scalar results
        if np.isscalar(value):
            if np.iscomplexobj(value):
                fh.write(f"{np.real(value) }, {np.imag(value) } \n")
            else:
                fh.write(f"{value} \n")

        # Writing dictionary results
        elif isinstance(value, dict):
            fh.write(f"{len(value)} \n")
            for subkey, subvalue in value.items():
                fh.write(f"{subkey} | {subvalue} \n")

        # Writing vector results
        elif len(np.array(value[0]).shape) < 2:
            fh.write(f"{len(value)} \n")
            if np.iscomplexobj(value):
                for subvalue in value:
                    fh.write(f"{np.real(subvalue) }, {np.imag(subvalue) } \n")
            else:
                for subvalue in value:
                    fh.write(f"{subvalue} \n")
        else:
            fh.write(f"{len(value)} \n")
            for subvalue in value:
                write_tensor(subvalue, fh, np.iscomplexobj(subvalue))
