import os
import shutil
from unittest import TestCase

import torch

from pointcyto.data.InMemoryPointCloud import InMemoryPointCloud
from pointcyto.io.meta_read_foldering import gen_foldering_meta
from pointcyto.testutils.helpers import find_dirname_above

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
# Now build the base-test directory (necessary if you want to use tests/testdata)
TESTS_DIR = find_dirname_above(THIS_DIR)

pointcloud_toy_dataset = os.path.join(
    "testdata", "flowcytometry", "PointClouds_toy_dataset"
)
tcell_toy_dataset = os.path.join("testdata", "flowcytometry", "Tcell_foldering")
empty_sample_dataset = os.path.join("testdata", "flowcytometry", "empty_sample")


class TestInMemoryPointCloud(TestCase):
    def test_InMemoryPointCloud(self):
        orig_data_dir = os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        new_data_dir = os.path.join(TESTS_DIR, pointcloud_toy_dataset, "removeme_raw")
        shutil.copytree(src=orig_data_dir, dst=new_data_dir, dirs_exist_ok=True)
        # generate the metadata
        mymeta = gen_foldering_meta(new_data_dir)
        # make sure that this dir was previously empty
        shutil.rmtree(mymeta.root, ignore_errors=True)

        # Process the data the first time
        a = InMemoryPointCloud(metadata=mymeta)
        assert len(a) == 6

        # Moving the rootdir should be fine, just the data is preprocessed again
        mymeta.root = os.path.join(new_data_dir, os.pardir, "autoroot_second")
        # make sure that this dir was previously empty
        shutil.rmtree(mymeta.root, ignore_errors=True)

        # Now the following should break because neither the root dir exists, nor the original data
        b = InMemoryPointCloud(
            metadata=mymeta
        )  # that must fail now because the data are missing? NO?
        assert len(b) == 6

        # Now forcefully remove the original data
        # Which is mimiking the behaviour of going to a different server!
        shutil.rmtree(new_data_dir)

        # should be processed automatically
        # that should be fine because the data was already processed
        #   It searches under os.path.join(mymeta.root, 'processed')
        b = InMemoryPointCloud(metadata=mymeta)
        assert len(b) == 6

        # print(mymeta.root)
        # # /home/gugl/programming/ccc/tests/testdata/flowcytometry/PointClouds_toy_dataset/autoroot_removeme_raw
        mymeta.root = os.path.join(new_data_dir, os.pardir, "autoroot_removeme_raw")
        # that should ALSO be fine because the data was already processed, I just want to check
        # if changing the root breaks anything unintentionally
        #   It searches under os.path.join(mymeta.root, 'processed')
        b = InMemoryPointCloud(metadata=mymeta)
        assert len(b) == 6

        mymeta.root = os.path.join(new_data_dir, os.pardir, "NEW_UNSEEN_autoroot")
        # Now the following should break because neither the root dir exists, nor the original data
        with self.assertRaises(FileNotFoundError):
            b = InMemoryPointCloud(metadata=mymeta)

    def test_reload_processed_meta(self):
        orig_data_dir = os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        new_data_dir = os.path.join(TESTS_DIR, pointcloud_toy_dataset, "removeme_raw")
        shutil.copytree(src=orig_data_dir, dst=new_data_dir, dirs_exist_ok=True)
        # generate the metadata
        mymeta = gen_foldering_meta(new_data_dir)
        # make sure that this dir was previously empty
        shutil.rmtree(mymeta.root, ignore_errors=True)

        # Process the data the first time
        a = InMemoryPointCloud(metadata=mymeta)
        assert len(a) == 6

        import pickle

        with open(
            os.path.join(a.processed_dir, "pointcloud_metadata.pickle"), "rb"
        ) as f:
            x = pickle.load(f)

        a_reloaded = InMemoryPointCloud(metadata=x)
        assert a_reloaded.metadata == a.metadata
        assert torch.equal(a_reloaded.pos, a.pos)

        # now move the complete processed folder
        new_autoroot = os.path.join(
            TESTS_DIR, pointcloud_toy_dataset, "removeme_new_autoroot"
        )
        shutil.rmtree(new_autoroot, ignore_errors=True)
        shutil.copytree(src=a.root, dst=new_autoroot)

        # remove all processed folders
        shutil.rmtree(a.root, ignore_errors=True)
        # remove the original data such that RE-processing would throw an error
        shutil.rmtree(new_data_dir, ignore_errors=True)

        with self.assertRaises(FileNotFoundError):
            a_moved_reloaded = InMemoryPointCloud(metadata=x)

        # But if we change the metadata root to the newly copied autoroot it should work again
        x.root = new_autoroot
        a_moved_reloaded = InMemoryPointCloud(metadata=x)

        # test it with new_autoroot as string
        a_moved_reloaded = InMemoryPointCloud(metadata=new_autoroot)
        print(a_moved_reloaded)

    def test_reload_processed_meta_pre_transform_warning(self):
        orig_data_dir = os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        # generate the metadata
        mymeta = gen_foldering_meta(orig_data_dir)
        # make sure that this dir was previously empty
        shutil.rmtree(mymeta.root, ignore_errors=True)

        from torch_geometric.transforms.fixed_points import FixedPoints

        # Process the data the first time
        a = InMemoryPointCloud(metadata=mymeta, pre_transform=FixedPoints(10))
        # now reloading, should not give a warning
        import warnings

        # b = InMemoryPointCloud(metadata=a.root)
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            b = InMemoryPointCloud(metadata=a.root)
            print(b)
