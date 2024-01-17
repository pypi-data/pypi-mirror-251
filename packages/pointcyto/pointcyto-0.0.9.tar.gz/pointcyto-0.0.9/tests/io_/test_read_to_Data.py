import os
from unittest import TestCase

import torch

from pointcyto.io.loaders.csv import read_csv
from pointcyto.io.loaders.fcs import read_fcs
from pointcyto.io.loaders.feather import read_feather
from pointcyto.io.meta_read_foldering import gen_csv_meta
from pointcyto.io.utils import parse_matrix_class
from pointcyto.testutils.helpers import find_dirname_above

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
# Now build the base-test directory (necessary if you want to use tests/testdata)
TESTS_DIR = find_dirname_above(THIS_DIR)


pointcloud_toy_dataset = os.path.join(
    "testdata", "flowcytometry", "PointClouds_toy_dataset"
)
pointcloud_toy_dataset_csvpheno = os.path.join(
    "testdata", "flowcytometry", "PointClouds_toy_phenocsv"
)
tcell_dataset_singlefile = os.path.join(
    "testdata", "flowcytometry", "Tcell_csv", "ultra_small_test_sample.csv"
)


class Test(TestCase):
    def test_manual_readin_and_data_convertion(self):
        tmp = gen_csv_meta(
            os.path.realpath(os.path.join(TESTS_DIR, pointcloud_toy_dataset_csvpheno)),
            path_phenodata="samples_pheno.csv",
        )
        for single_sample in tmp:
            print(single_sample)
            single_fcs, colnames = read_fcs(
                os.path.join(tmp.orig_dir, single_sample["raw_filenames"])
            )
            myclass = parse_matrix_class(
                point_position_matrix=single_fcs, class_id=single_sample["y"]
            )
            print(myclass)
            print(myclass.pos)
            break

    def test_readcsv(self):
        read_tcell_file = read_csv(os.path.join(TESTS_DIR, tcell_dataset_singlefile))
        print(read_tcell_file)
        assert torch.equal(
            read_tcell_file[0],
            (
                torch.tensor(
                    [
                        [
                            1,
                            1,
                            1,
                            1,
                        ],
                        [13, 2, 4, 12],
                    ],
                    dtype=torch.int32,
                )
            ),
        )
        assert read_tcell_file[1] == ["Marker1", "Marker2", "Marker3", "Marker4"]

    def test_readcsv_datatable(self):
        import datatable

        def csv_reader(*args, **kwargs):
            read_data = datatable.fread(*args, **kwargs)
            return torch.tensor(read_data.to_numpy()), list(read_data.names)

        read_tcell_file = csv_reader(os.path.join(TESTS_DIR, tcell_dataset_singlefile))
        print(read_tcell_file)
        assert torch.equal(
            read_tcell_file[0],
            (
                torch.tensor(
                    [
                        [
                            1,
                            1,
                            1,
                            1,
                        ],
                        [13, 2, 4, 12],
                    ],
                    dtype=torch.int32,
                )
            ),
        )
        assert read_tcell_file[1] == ["Marker1", "Marker2", "Marker3", "Marker4"]

    def test_readcsv_pandas(self):
        import pandas as pd

        # fallback to pandas
        def csv_reader(*args, **kwargs):
            print("I am inside the fallback function")
            read_data = pd.read_csv(*args, **kwargs)
            return torch.tensor(read_data.values), [
                x.strip() for x in read_data.columns
            ]

        read_tcell_file = csv_reader(os.path.join(TESTS_DIR, tcell_dataset_singlefile))
        print(read_tcell_file)
        assert torch.equal(
            read_tcell_file[0],
            (
                torch.tensor(
                    [
                        [
                            1,
                            1,
                            1,
                            1,
                        ],
                        [13, 2, 4, 12],
                    ],
                    dtype=torch.int64,
                )
            ),
        )
        assert read_tcell_file[1] == ["Marker1", "Marker2", "Marker3", "Marker4"]

    def test_read_feather_pyarrow(self):
        # Run within R:
        #   tmp <- data.table::fread("tests/testdata/flowcytometry/Tcell_csv/ultra_small_test_sample.csv")
        #   dir.create("tests/testdata/flowcytometry/Tcell_feather")
        #   feather::write_feather(tmp, "tests/testdata/flowcytometry/Tcell_feather/ultra_small_test_sample.feather")
        read_tcell_file = read_feather(
            os.path.join(
                TESTS_DIR,
                "testdata",
                "flowcytometry",
                "Tcell_feather",
                "ultra_small_test_sample.feather",
            )
        )
        print(read_tcell_file)
        assert torch.equal(
            read_tcell_file[0],
            (
                torch.tensor(
                    [
                        [
                            1,
                            1,
                            1,
                            1,
                        ],
                        [13, 2, 4, 12],
                    ],
                    dtype=torch.int32,
                )
            ),
        )
        assert read_tcell_file[1] == ["Marker1", "Marker2", "Marker3", "Marker4"]
