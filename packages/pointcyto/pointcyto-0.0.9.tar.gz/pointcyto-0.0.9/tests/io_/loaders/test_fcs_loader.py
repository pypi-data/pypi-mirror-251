import os
from unittest import TestCase

import torch

from pointcyto.io.loaders.fcs import read_fcs
from pointcyto.testutils.helpers import find_dirname_above

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
# Now build the base-test directory (necessary if you want to use tests/testdata)
TESTS_DIR = find_dirname_above(THIS_DIR)

flowcyto_testdata_dir = os.path.join(TESTS_DIR, "testdata", "flowcytometry")
ultrasmall_fcs = os.path.join(flowcyto_testdata_dir, "ultra_small_fcs.fcs")

# The following code was used in R (project: 2019-09-14_facs_melanoma) to generate the exemplary data ultrasmall fcs
# library(flowCore)
# a <- read.FCS("Data/OperationalData/Tcell/P0H.fcs")
# exprs(a)
# exprs(a[1:10, ])
# write.FCS(a[1:3, 1:4], filename = "ultra_small_fcs.fcs")

target_tensor = torch.Tensor(
    [
        [15.83853, 20.82897, 15.71305, 8.452956],
        [13.82324, 20.64287, 13.55996, 6.616665],
        [16.00134, 20.70882, 15.53644, 8.520460],
    ]
)
target_tensor = target_tensor.double()

target_markernames = [
    "FS_INT_LIN_FS_INT",
    "FS_TOF_LIN_FS_TOF",
    "SS_INT_LIN_SS_INT",
    "CD45RA_FITC_CD45RA",
]


class Test(TestCase):
    def test_fcs_loader(self):
        if not os.path.exists(ultrasmall_fcs):
            self.fail(msg=ultrasmall_fcs + " does not exist")

        loaded_csv = read_fcs(ultrasmall_fcs)

        assert torch.allclose(target_tensor, loaded_csv[0])
        self.assertEqual(target_markernames, loaded_csv[1])
