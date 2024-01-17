import os
import os.path
import unittest
from shutil import rmtree
import subprocess

try:
    import mpi4py

    mpi_is_present = True
except ModuleNotFoundError:
    mpi_is_present = False


class TestSimulationParallelization(unittest.TestCase):
    def setUp(self):
        if not os.path.isdir("TMP_TEST"):
            os.makedirs("TMP_TEST")
        self.exe_is_present = os.path.isfile("main_qmatchatea.exe")

    def tearDown(self):
        if os.path.isdir("TMP_TEST"):
            rmtree("TMP_TEST")

    # def test_exe_presence(self):
    #    """
    #    Test if the serial executable is present
    #    """
    #    self.assertTrue(self.exe_is_present, 'Executable file is present')
    #    return

    @unittest.skipIf(not mpi_is_present, "MPI is nor present")
    def test_mpi4py(self):
        """
        Test if the parallelization of multiple simulations is working using GHZ states.
        Since it is not possible to directly run this test we perform a workaround:
        through subprocess the unittest calls the actual test
        """
        if not self.exe_is_present:
            return

        result = subprocess.run(
            ["mpiexec", "-n", "4", "python3", "python/tests/_testmpi.py"],
            capture_output=True,
        )

        out = str(result.stdout).split("\n")
        condition = bool(out[-1])

        self.assertTrue(
            condition,
            msg="GHZ circuits simulated parallely on multiple processes correts",
        )

        return
