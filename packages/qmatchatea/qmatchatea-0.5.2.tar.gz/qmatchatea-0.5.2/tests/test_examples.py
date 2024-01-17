import unittest
import subprocess
import numpy as np

try:
    import mpi4py

    has_mpi = True
except ImportError:
    has_mpi = False


class TestExamples(unittest.TestCase):
    """Test that all the examples works correctly"""

    def setUp(self):
        """Define 'global' variables"""
        self.num_sites = 4
        # Set seed
        np.random.seed(123)

    def test_convergence_analysis(self):
        """
        Test the convergence analysis example
        """
        res = subprocess.run(["python3", "examples/convergence_analysis.py"])
        self.assertIsNone(res.stderr, "Example failed")

    def test_get_started(self):
        """
        Test the get started example
        """
        res = subprocess.run(["python3", "examples/get_started.py"])
        self.assertIsNone(res.stderr, "Example failed")

    @unittest.skipIf(has_mpi, "mpi4py not installed")
    def test_mpi_example(self):
        """
        Test the mpi_example example
        """
        res = subprocess.run(["mpiexec", "python3", "examples/mpi_example.py", "-n=4"])
        self.assertIsNone(res.stderr, "Example failed")

    def test_mps_ttn_comparison(self):
        """
        Test the mps_ttn_comparison example
        """
        res = subprocess.run(["python3", "examples/mps_ttn_comparison.py"])
        self.assertIsNone(res.stderr, "Example failed")

    def test_quantum_fourier_transform(self):
        """
        Test the quantum_fourier_transform example
        """
        res = subprocess.run(["python3", "examples/quantum_fourier_transform.py"])
        self.assertIsNone(res.stderr, "Example failed")

    def test_random_quantum_circuit(self):
        """
        Test the random_quantum_circuit example
        """
        res = subprocess.run(["python3", "examples/random_quantum_circuit.py"])
        self.assertIsNone(res.stderr, "Example failed")

    def test_teleportation(self):
        """
        Test the teleportation example
        """
        res = subprocess.run(["python3", "examples/teleportation.py"])
        self.assertIsNone(res.stderr, "Example failed")

    def test_variational_quantum_eigensolver(self):
        """
        Test the variational_quantum_eigensolver example
        """
        res = subprocess.run(["python3", "examples/variational_quantum_eigensolver.py"])
        self.assertIsNone(res.stderr, "Example failed")
