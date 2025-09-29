import sys, unittest
from md import calcenergy
from ase.lattice.cubic import FaceCenteredCubic
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from asap3 import EMT

class MdTests(unittest.TestCase):
    def test_calcenergy(self):
        atoms = FaceCenteredCubic(
            directions=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            symbol='Cu',
            size=(10, 10, 10),
            pbc=True
        )

        # Describe the interatomic interactions with the Effective Medium Theory
        atoms.calc = EMT()

        # Set the momenta corresponding to T=300K
        MaxwellBoltzmannDistribution(atoms, temperature_K=300)

        epot, ekin, temp, etot = calcenergy(atoms)

        # Assertions: check the types and that energies are finite numbers
        self.assertIsInstance(epot, float)
        self.assertIsInstance(ekin, float)
        self.assertIsInstance(temp, float)
        self.assertIsInstance(etot, float)

        self.assertTrue(epot < 0) 
        self.assertTrue(ekin > 0)
        self.assertTrue(temp > 0)
        self.assertAlmostEqual(etot, epot + ekin, places=12)

if __name__ == "__main__":
    tests = [unittest.TestLoader().loadTestsFromTestCase(MdTests)]
    testsuite = unittest.TestSuite(tests)
    result = unittest.TextTestRunner(verbosity=0).run(testsuite)
    sys.exit(not result.wasSuccessful())