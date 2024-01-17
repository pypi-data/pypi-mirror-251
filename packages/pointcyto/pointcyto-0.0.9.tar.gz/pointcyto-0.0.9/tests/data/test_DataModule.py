import os
import shutil
from unittest import TestCase

import torch
from torch_geometric.transforms.fixed_points import FixedPoints

from pointcyto.data.datamodule import PCDataModule
from pointcyto.data.PointCloud import PointCloud
from pointcyto.io.meta_read_foldering import gen_foldering_meta
from pointcyto.io.pickle_open_dump import pickle_open_dump
from pointcyto.testutils.helpers import find_dirname_above_currentfile

# Now build the base-test directory (necessary if you want to use tests/testdata)
TESTS_DIR = find_dirname_above_currentfile()


pointcloud_toy_dataset = os.path.join(
    "testdata", "flowcytometry", "PointClouds_toy_dataset"
)
tcell_toy_dataset = os.path.join("testdata", "flowcytometry", "Tcell_foldering")


class TestPCDataModule(TestCase):
    def test_PointCloud(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        a = PointCloud(metadata=mymeta, clear_processed=True)
        a = PointCloud(metadata=mymeta)
        shutil.rmtree(os.path.join(TESTS_DIR, pointcloud_toy_dataset, "autoroot_raw"))
        a = PointCloud(metadata=mymeta)
        repr(a)

    def test_DataModule(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        with self.assertRaises(ValueError):
            # Cannot create a PCDataModule with only one dataset. Use (InMemory)PointCloud
            dm = PCDataModule(meta_train=mymeta)
        dm = PCDataModule(meta_train={"dataA": mymeta})
        print(dm)

    def test_repr(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        with self.assertRaises(ValueError):
            dm = PCDataModule(meta_train=mymeta)
        dm = PCDataModule(meta_train={"dataA": mymeta})
        print(dm)

    def test_meta_inputs(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )

        pickle_open_dump(mymeta, "mymeta.pickle")
        with self.assertRaises(ValueError):
            dm = PCDataModule(meta_train=mymeta)

        dm = PCDataModule(
            meta_train={
                "dataA": mymeta,
                "dataB": "mymeta.pickle",
                "dataC": {"metadata": mymeta},
            }
        )
        assert dm.meta_conf_xxx["train"]["dataA"] == dm.meta_conf_xxx["train"]["dataB"]
        assert dm.meta_conf_xxx["train"]["dataA"] == dm.meta_conf_xxx["train"]["dataC"]

    def test_meta_missingParts(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        with self.assertRaises(ValueError):
            # Missing dataB in meta_test
            dm = PCDataModule(
                meta_train={
                    "dataA": mymeta,
                    "dataB": mymeta,
                },
                meta_test={"dataA": mymeta},
            )

        dm = PCDataModule(
            meta_train={
                "dataA": mymeta,
                "dataB": mymeta,
            },
            meta_test={
                "dataA": mymeta,
                "dataB": mymeta,
            },
        )
        assert dm.meta_conf_xxx["train"]["dataA"] == dm.meta_conf_xxx["train"]["dataB"]
        assert dm.meta_conf_xxx["train"]["dataA"] == dm.meta_conf_xxx["test"]["dataA"]
        assert dm.meta_conf_xxx["train"]["dataA"] == dm.meta_conf_xxx["test"]["dataB"]

    def test_prepare(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )

        dm = PCDataModule(
            meta_train={
                "dataA": mymeta,
                "dataB": mymeta,
            },
            meta_test={
                "dataA": mymeta,
                "dataB": mymeta,
            },
        )
        assert dm.must_prepare
        assert list(dm.meta_conf_xxx["train"]["dataA"].keys()) == ["metadata"]
        dm.prepare_data()
        assert list(dm.meta_conf_xxx["train"]["dataA"].keys()) == [
            "metadata",
            "clear_processed",
        ]
        assert not dm.must_prepare  # gets changed by .prepare_data()
        assert not dm.meta_conf_xxx["train"]["dataA"]["clear_processed"]
        assert not dm.meta_conf_xxx["train"]["dataB"]["clear_processed"]
        assert not dm.meta_conf_xxx["test"]["dataA"]["clear_processed"]
        assert not dm.meta_conf_xxx["test"]["dataB"]["clear_processed"]

    def test_setup(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )

        dm = PCDataModule(
            meta_train={
                "dataA": mymeta,
                "dataB": mymeta,
            },
            meta_test={
                "dataA": mymeta,
                "dataB": mymeta,
            },
        )
        with self.assertRaises(ValueError):
            dm.setup("train")

        dm.prepare_data()
        dm.setup("train")

        print(dm.pc_xxx)
        assert torch.allclose(
            dm.pc_xxx["train"]["dataA"].pos, dm.pc_xxx["train"]["dataB"].pos
        )
        with self.assertRaises(KeyError):
            torch.allclose(
                dm.pc_xxx["test"]["dataA"].pos, dm.pc_xxx["test"]["dataB"].pos
            )

        dm.setup("test")
        assert torch.allclose(
            dm.pc_xxx["test"]["dataA"].pos, dm.pc_xxx["test"]["dataB"].pos
        )

    def test_clear_processed(self):
        # From this test, the printed output should be  4 x 2 times from InMemoryPointCloud.process()
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )

        dm = PCDataModule(
            meta_train={
                "dataA": mymeta,
                "dataB": mymeta,
            },
            meta_test={
                "dataA": mymeta,
                "dataB": mymeta,
            },
            clear_processed=True,
        )
        dm.prepare_data()
        dm = PCDataModule(
            meta_train={
                "dataA": mymeta,
                "dataB": mymeta,
            },
            meta_test={
                "dataA": mymeta,
                "dataB": mymeta,
            },
            clear_processed=False,
        )
        dm.prepare_data()
        dm = PCDataModule(
            meta_train={
                "dataA": mymeta,
                "dataB": mymeta,
            },
            meta_test={
                "dataA": mymeta,
                "dataB": mymeta,
            },
            clear_processed=False,
        )
        dm.prepare_data(clear_processed=True)

    def test_setup_None(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )

        dm = PCDataModule(
            meta_train={
                "dataA": mymeta,
                "dataB": mymeta,
            },
            meta_test={
                "dataA": mymeta,
                "dataB": mymeta,
            },
            clear_processed=True,
        )
        dm.prepare_data()
        dm.setup()
        assert torch.allclose(
            dm.pc_xxx["train"]["dataA"].pos, dm.pc_xxx["train"]["dataB"].pos
        )
        assert torch.allclose(
            dm.pc_xxx["test"]["dataA"].pos, dm.pc_xxx["test"]["dataB"].pos
        )

    def test_check_Dataloader(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )

        dm = PCDataModule(
            meta_train={
                "dataA": mymeta,
                "dataB": mymeta,
            },
            meta_test={
                "dataA": mymeta,
                "dataB": mymeta,
            },
            clear_processed=True,
            batch_size=4,  # there are 6 samples, therefore now there should be 2 batches
        )
        dm.prepare_data()

        with self.assertRaises(KeyError):
            for loader in dm.train_dataloader():
                print(loader["dataA"])

        dm.setup("train")

        counter = 0
        # for loader in dm.train_dataloader():
        for batch, batch_idx, dataloader_idx in dm.train_dataloader():
            assert counter == batch_idx
            counter += 1
            assert isinstance(batch, dict)
            assert list(batch.keys()) == ["dataA", "dataB"]
            assert torch.allclose(batch["dataA"].pos, batch["dataB"].pos)
            assert dataloader_idx == 0  # always the same dataloader is used here
        assert counter == 2

    def test_check_pointcloud_args_datapart(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        with self.assertRaises(ValueError):
            dm = PCDataModule(
                meta_train={
                    "dataA": mymeta,
                },
                meta_val={
                    "dataA": mymeta,
                },
                clear_processed=True,
                batch_size=4,  # there are 6 samples, therefore now there should be 2 batches
                pointcloud_args_datapart={
                    "transform": FixedPoints(
                        num=100, replace=False, allow_duplicates=True
                    )
                },
            )
        dm = PCDataModule(
            meta_train={
                "dataA": mymeta,
            },
            meta_val={
                "dataA": mymeta,
            },
            clear_processed=True,
            batch_size=4,  # there are 6 samples, therefore now there should be 2 batches
            pointcloud_args_datapart={
                "dataA": {
                    "transform": FixedPoints(
                        num=100, replace=False, allow_duplicates=True
                    )
                }
            },
        )
        print(dm)

    def tearDown(self) -> None:
        try:
            shutil.rmtree(os.path.join(TESTS_DIR, pointcloud_toy_dataset, "processed"))
            pass
        except FileNotFoundError:
            pass
        try:
            shutil.rmtree(
                os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw", "processed")
            )
            shutil.rmtree(os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw", "raw"))
            pass
        except FileNotFoundError:
            pass
