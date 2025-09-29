"""Demonstrates molecular dynamics with constant energy."""

from ase import units
from ase.lattice.cubic import FaceCenteredCubic
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
from asap3 import Trajectory

def calcenergy(atoms):
    epot = atoms.get_potential_energy() / len(atoms)
    ekin = atoms.get_kinetic_energy() / len(atoms)
    temp = ekin / (1.5 * units.kB)
    return epot, ekin, temp, epot + ekin

def run_md():
    """Run a molecular dynamics simulation of copper."""

    # Use Asap for a huge performance increase if it is installed
    use_asap = True

    if use_asap:
        from asap3 import EMT

        size = 10
    else:
        from ase.calculators.emt import EMT

        size = 3

    # Set up a crystal
    atoms = FaceCenteredCubic(
        directions=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        symbol='Cu',
        size=(size, size, size),
        pbc=True,
    )

    # Describe the interatomic interactions with the Effective Medium Theory
    atoms.calc = EMT()

    # Set the momenta corresponding to T=300K
    MaxwellBoltzmannDistribution(atoms, temperature_K=300)

    # We want to run MD with constant energy using the VelocityVerlet algorithm.
    dyn = VelocityVerlet(atoms, 1 * units.fs)  # 5 fs time step.

    traj = Trajectory("cu.traj", "w", atoms)
    dyn.attach(traj.write, interval=10)

    def printenergy(a=atoms):  # store a reference to atoms in the definition.
        """Function to print the potential, kinetic and total energy."""
        returns = calcenergy(a)
        print(
            f'Energy per atom: Epot ={returns[0]:6.3f}eV  Ekin = {returns[1]:.3f}eV '
            f'(T={returns[2]:3.0f}K) Etot = {returns[3]:.3f}eV'
        )

    # Now run the dynamics
    dyn.attach(printenergy, interval=10)
    printenergy()
    dyn.run(500)

if __name__ == "__main__":
    run_md()
