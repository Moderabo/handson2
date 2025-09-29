import unittest
import os
import md

class TestMDIntegration(unittest.TestCase):
	def setUp(self):
		# Remove cu.traj if it exists before test
		try:
			os.remove("cu.traj")
		except FileNotFoundError:
			pass

	def test_run_md_creates_traj(self):
		md.run_md()
		self.assertTrue(os.path.getsize("cu.traj") > 0, "cu.traj file was not created")

	def tearDown(self):
		# Clean up cu.traj after test
		try:
			os.remove("cu.traj")
		except FileNotFoundError:
			pass

if __name__ == "__main__":
	unittest.main()
