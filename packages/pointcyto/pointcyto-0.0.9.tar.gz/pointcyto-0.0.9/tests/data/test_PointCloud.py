import os
import shutil
from unittest import TestCase

import torch
from torch_geometric.loader import DataLoader as tg_DataLoader
from torch_geometric.transforms.fixed_points import FixedPoints

from pointcyto.data.PointCloud import PointCloud
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


class TestPointCloud(TestCase):
    def test_PointCloud(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        a = PointCloud(metadata=mymeta, clear_processed=True)
        a = PointCloud(metadata=mymeta)
        shutil.rmtree(os.path.join(TESTS_DIR, pointcloud_toy_dataset, "autoroot_raw"))
        a = PointCloud(metadata=mymeta)
        repr(a)

    def test_Pointcloud_item(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        a = PointCloud(metadata=mymeta, clear_processed=True)
        # When a slice is selected, the returned value is again an InMemoryPointCloud
        print(a[0:2])
        # If an int is selected, the returned value is a torch_geometric Data instance.
        print(a[0])

    def test_PointCloud_subsetting(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        mymeta_train = mymeta[0:2, :]
        mymeta_val = mymeta[2:, :]
        a_train = PointCloud(metadata=mymeta_train, clear_processed=True)
        a_val = PointCloud(metadata=mymeta_val, clear_processed=True)
        assert len(a_train) == 2
        assert len(a_val) == 4

        complete_pointcloud = PointCloud(metadata=mymeta, clear_processed=True)
        print(complete_pointcloud.metadata)
        pc_train = complete_pointcloud[0:2]
        pc_val = complete_pointcloud[2:]

        assert all(mymeta_train.pheno == pc_train.metadata.pheno)
        assert all(mymeta_val.pheno == pc_val.metadata.pheno)

        assert (
            mymeta_train.sample_feature_names == pc_train.metadata.sample_feature_names
        )
        assert mymeta_val.sample_feature_names == pc_val.metadata.sample_feature_names

    def test_reloadPointcloud(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        complete_pointcloud = PointCloud(metadata=mymeta, clear_processed=True)
        loaded_pointcloud = PointCloud(metadata=mymeta)
        assert complete_pointcloud.metadata == loaded_pointcloud.metadata

    def test_PointCloud_raw_dir_already_present(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw"),
            root=os.path.join(TESTS_DIR, pointcloud_toy_dataset),
        )
        a = PointCloud(metadata=mymeta, clear_processed=True)
        print(a)

    def test_PointCloud_sample_with_one_point_no_transform(self):
        mymeta = gen_foldering_meta(os.path.join(TESTS_DIR, empty_sample_dataset))
        a = PointCloud(metadata=mymeta, clear_processed=True)
        # print(a)
        for sample_x in a:
            # print(sample_x)
            assert isinstance(sample_x.y, int)
        b = PointCloud(metadata=mymeta)
        for sample_x in b:
            # print(sample_x)
            assert isinstance(sample_x.y, int)

    def test_PointCloud_sample_with_one_point_transform(self):
        # This is a pytorch-geometric/FixedPoints issue, see
        #   https://github.com/rusty1s/pytorch_geometric/issues/1090
        mymeta = gen_foldering_meta(os.path.join(TESTS_DIR, empty_sample_dataset))
        random_select_n_points = FixedPoints(num=100)
        a = PointCloud(
            metadata=mymeta, clear_processed=True, transform=random_select_n_points
        )
        for sample_x in a:
            print(sample_x)
            assert isinstance(sample_x.y, int)

    def test_PointCloud_different_raw_dirs_without_root(self):
        mymeta_toy = gen_foldering_meta(os.path.join(TESTS_DIR, pointcloud_toy_dataset))
        pointcloud_toy = PointCloud(metadata=mymeta_toy, clear_processed=True)
        mymeta_tcell = gen_foldering_meta(os.path.join(TESTS_DIR, tcell_toy_dataset))
        pointcloud_tcell = PointCloud(metadata=mymeta_tcell, clear_processed=True)
        assert (
            pointcloud_toy != pointcloud_tcell
        )  # the two pointclouds MUST not be the same.

        pointcloud_toy = PointCloud(metadata=mymeta_toy)
        # Even after loading pointcloud_toy a second time, the data MUST NOT be the same
        if pointcloud_toy[0].pos.shape == pointcloud_tcell[0].pos.shape:
            assert not torch.allclose(pointcloud_toy[0].pos, pointcloud_tcell[0].pos)

    def test_PointCloud_different_featurenames(self):
        mymeta = gen_foldering_meta(
            os.path.join(
                TESTS_DIR,
                pointcloud_toy_dataset,
                os.pardir,
                "Tcell_foldering_corrupted_colnames",
            ),
            root=os.path.join(TESTS_DIR, "new_datasets_dir"),
        )
        import copy

        saved_meta = copy.deepcopy(mymeta)
        assert saved_meta == mymeta
        with self.assertRaises(ValueError):
            my_pc = PointCloud(metadata=mymeta, clear_processed=True)
            repr(my_pc)
        assert saved_meta == mymeta

    def test_PointCloud_with_transform(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        random_select_n_points = FixedPoints(num=2)
        import numpy as np

        np.random.seed(123)
        a = PointCloud(mymeta, transform=random_select_n_points, clear_processed=True)
        target_tensor = torch.tensor(
            [
                [
                    15.8737,
                    20.8384,
                    15.6227,
                    8.6955,
                    8.7534,
                    8.2956,
                    9.0078,
                    7.8170,
                    8.1263,
                    8.9850,
                    7.2125,
                    8.6033,
                    11.7536,
                    4107.0000,
                ],
                [
                    15.5161,
                    20.8384,
                    14.9606,
                    8.4246,
                    8.7429,
                    7.6892,
                    9.5300,
                    -5.6333,
                    11.7794,
                    8.1770,
                    6.9872,
                    8.1666,
                    12.4236,
                    2882.0000,
                ],
            ]
        )
        assert torch.allclose(a[0].pos, target_tensor, atol=1e-3, rtol=1e-3)

    def test_PointCloud_FixedPoints_get_twice(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        random_select_n_points = FixedPoints(num=2)
        import numpy as np

        np.random.seed(123)
        a = PointCloud(mymeta, transform=random_select_n_points, clear_processed=True)

        # Even the same a[N] called twice gives different results!!!
        # This is because inside, transform is called every time with a get() call.
        assert not torch.allclose(a[0].pos, a[0].pos, rtol=1e-4)

        # in contrast, when setting the seed for the RNG inside, the following results must be the same.
        # God, this is tricky.
        np.random.seed(123)
        tmp1 = a[0]
        np.random.seed(123)
        tmp2 = a[0]
        assert torch.allclose(tmp1.pos, tmp2.pos, rtol=1e-4)

    def test_PointCloud_DataLoader(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        random_select_n_points = FixedPoints(num=2)
        import numpy as np

        np.random.seed(123)
        a = PointCloud(mymeta, transform=random_select_n_points, clear_processed=True)

        # # The torch DataLoader cannot work anymore (2020-02-26) because I switched my PointCloud dataset
        # # completely to be based on torch_geometric.data.data.Data
        # t_loader = t_DataLoader(a)
        # for batch in t_loader:
        #     print(batch)
        #     break

        tg_loader = tg_DataLoader(a)
        for batch in tg_loader:
            repr(batch)
            print(batch)

    def test_PointCloud_DataLoader_more_batches_than_samples(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        n_points_per_draw = 2
        random_select_n_points = FixedPoints(num=n_points_per_draw)
        import numpy as np

        np.random.seed(123)
        a = PointCloud(mymeta, transform=random_select_n_points, clear_processed=True)

        # Default torch_geometric dataloader just selects the maximum possible amount of samples.
        tg_loader = tg_DataLoader(
            a, batch_size=len(mymeta) + 1
        )  # Draw more samples than in mymeta present
        for batch in tg_loader:
            assert batch.pos.shape[0] / len(batch.y) == n_points_per_draw
            assert len(batch.y) == len(mymeta)

        # torch_geometric.loader bases on torch.utils.data.DataLoader
        # therefore we can supply a "sampler"
        # The sampler defines the complete "sample-set" which can be drawn from during learning.
        # The batch_size splits this "sample-set" and iterating over the DataLoader then has
        #   num_samples / batch_size elements
        tg_loader = tg_DataLoader(
            a,
            batch_size=100,
            sampler=torch.utils.data.RandomSampler(
                data_source=a, replacement=True, num_samples=100
            ),
        )  # Draw more samples than in mymeta present
        for batch in tg_loader:
            assert batch.pos.shape[0] / len(batch.y) == n_points_per_draw
            assert len(batch.y) == 100

        tg_loader = tg_DataLoader(
            a,
            batch_size=20,
            sampler=torch.utils.data.RandomSampler(
                data_source=a, replacement=True, num_samples=100
            ),
        )  # Draw more samples than in mymeta present
        # 100 samples sampled randomly in total
        # 20 per batchsize
        # --> I have 5 batches
        assert len(tg_loader) == 5
        for batch in tg_loader:
            assert batch.pos.shape[0] / len(batch.y) == n_points_per_draw
            assert len(batch.y) == 20

        # What if the batch_size does not exactly part num_samples?
        tg_loader = tg_DataLoader(
            a,
            batch_size=20,
            sampler=torch.utils.data.RandomSampler(
                data_source=a, replacement=True, num_samples=90
            ),
        )  # Draw more samples than in mymeta present
        # 90 samples sampled randomly in total
        # 20 per batchsize
        # --> I have 5 batches and the last batch has just 10 samples
        assert len(tg_loader) == 5
        lenghts = []
        for batch in tg_loader:
            lenghts.append(len(batch.y))
            # assert batch.pos.shape[0] / len(batch.y) == n_points_per_draw
            # assert len(batch.y) == 20
        assert lenghts == [20, 20, 20, 20, 10]

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
        try:
            shutil.rmtree(os.path.join(TESTS_DIR, "new_datasets_dir"))
        except FileNotFoundError:
            pass
