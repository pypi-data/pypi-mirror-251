import os
import unittest

import torch

from pointcyto.io.loaders.csv import read_csv
from pointcyto.testutils.helpers import find_dirname_above

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
# Now build the base-test directory (necessary if you want to use tests/testdata)
TESTS_DIR = find_dirname_above(THIS_DIR)

flowcyto_testdata_dir = os.path.join(TESTS_DIR, "testdata", "flowcytometry")

target_tensor = torch.tensor([[1.0, 1.0, 1.0, 1.0], [13.0, 2.0, 4.0, 12.0]])
target_tensor = target_tensor.double()

target_markernames = ["Marker1", "Marker2", "Marker3", "Marker4"]


class Test(unittest.TestCase):
    def test_is_testdata_present(self):
        if not os.path.exists(flowcyto_testdata_dir):
            self.fail(msg=flowcyto_testdata_dir + " does not exist")

    def test_csv_loader(self):
        single_csv_file = os.path.join(
            flowcyto_testdata_dir, "Tcell_csv", "ultra_small_test_sample.csv"
        )
        if not os.path.exists(single_csv_file):
            self.fail(msg=single_csv_file + " does not exist")

        loaded_csv = read_csv(single_csv_file)

        assert torch.all(torch.eq(target_tensor, loaded_csv[0]))
        self.assertEqual(target_markernames, loaded_csv[1])
