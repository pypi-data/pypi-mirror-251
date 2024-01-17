import unittest
import sys
import numpy as np

from qmatchatea.utils import fidelity
from qmatchatea.qk_utils import GHZ_qiskit, W_qiskit, qiskit_get_statevect
from qmatchatea import tensor_compiler
from qiskit import QuantumCircuit, transpiler, transpile
from qiskit.circuit.library import QuantumVolume

sys.argv = [""]
avail_gates = [
    "x",
    "y",
    "z",
    "h",
    "id",
    "s",
    "sdg",
    "sx",
    "sxdg",
    "t",
    "tdg",
    "swap",
    "dcx",
    "ecr",
    "iswap",
    "ch",
    "cx",
    "cy",
    "cz",
    "p",
    "r",
    "rx",
    "ry",
    "rz",
    "u",
    "u1",
    "u2",
    "rxx",
    "ryy",
    "rzx",
    "rzz",
    "cp",
    "cry",
    "crz",
    "cu",
    "cu1",
]


def qvol_circ(num_qub=3):
    qc = QuantumVolume(num_qub)
    qc = qc.decompose()
    lin_map = transpiler.CouplingMap.from_line(num_qub)
    qc = transpile(qc, coupling_map=lin_map, basis_gates=avail_gates)

    return qc


class TestTensorCompiler(unittest.TestCase):
    def setUp(self):
        np.random.seed(123)

    def test_GHZ(self):
        """
        Check that the GHZ circuit is compiled correctly
        """
        num_qubits = 10
        qc = QuantumCircuit(num_qubits)
        GHZ_qiskit(qc)
        true_state = qiskit_get_statevect(qc)
        compiled_qc = tensor_compiler(qc)
        statevect = qiskit_get_statevect(compiled_qc)
        fid = fidelity(statevect, true_state)
        self.assertAlmostEqual(
            fid, 1, places=12, msg="GHZ state not compiled correctly"
        )

        return

    def test_W(self):
        """
        Check that the W circuit is compiled correctly
        """
        num_qubits = 10
        qc = QuantumCircuit(num_qubits)
        W_qiskit(qc)
        true_state = qiskit_get_statevect(qc)
        compiled_qc = tensor_compiler(qc)
        statevect = qiskit_get_statevect(compiled_qc)
        fid = fidelity(statevect, true_state)
        self.assertAlmostEqual(fid, 1, places=12, msg="W state not compiled correctly")

        return

    def test_QVOLUME(self):
        """
        Check that the QVOLUME circuit is compiled correctly
        """
        num_qubits = 10
        qc = qvol_circ(num_qubits)
        true_state = qiskit_get_statevect(qc)
        compiled_qc = tensor_compiler(qc)
        statevect = qiskit_get_statevect(compiled_qc)
        fid = fidelity(statevect, true_state)
        self.assertAlmostEqual(
            fid, 1, places=12, msg=f"QVOLUME state not compiled correctly"
        )

        return
