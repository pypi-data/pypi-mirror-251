import os
import pathlib
import shutil
import warnings
from unittest import TestCase

import torch
import torch_geometric as tgeo

# from torch.utils.data.dataloader import DataLoader as t_DataLoader
from torch_geometric.loader import DataLoader as tg_DataLoader
from torch_geometric.transforms.fixed_points import FixedPoints

from pointcyto.data.InMemoryPointCloud import InMemoryPointCloud
from pointcyto.io.meta_read_foldering import gen_foldering_meta, gen_meta_filenames
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
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        a = InMemoryPointCloud(metadata=mymeta, clear_processed=True)
        b = InMemoryPointCloud(metadata=mymeta)
        assert b.metadata == a.metadata
        assert torch.equal(b.pos, a.pos)
        assert a != b

        shutil.rmtree(os.path.join(TESTS_DIR, pointcloud_toy_dataset, "autoroot_raw"))
        # Now the dataset must be rebuilt
        c = InMemoryPointCloud(metadata=mymeta)
        assert c.metadata == a.metadata
        assert torch.equal(c.pos, a.pos)
        assert a != c
        repr(a)

    def test_InMemoryPointCloud_regression(self):
        from pointcyto.io.meta_read_foldering import gen_csv_meta

        pointcloud_toy_dataset_csvpheno = os.path.join(
            "testdata", "flowcytometry", "PointClouds_toy_phenocsv"
        )

        from pointcyto.data.metadata_regression import MetaDataRegression

        mymeta = gen_csv_meta(
            os.path.realpath(os.path.join(TESTS_DIR, pointcloud_toy_dataset_csvpheno)),
            path_phenodata="samples_pheno.csv",
            metadata_type=MetaDataRegression,
        )

        a = InMemoryPointCloud(metadata=mymeta, clear_processed=True)
        b = InMemoryPointCloud(metadata=mymeta)
        assert b.metadata == a.metadata
        assert torch.equal(b.pos, a.pos)
        assert a != b

        b.metadata.rm_root(True)
        # Now the dataset must be rebuilt
        c = InMemoryPointCloud(metadata=mymeta)
        assert c.metadata == a.metadata
        assert torch.equal(c.pos, a.pos)
        assert a != c
        repr(a)
        print(b)
        print(b.metadata)
        print(b._data)  # just for testing

    def test_InMemoryPointCloud_Reloading_with_str(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        a = InMemoryPointCloud(metadata=mymeta, clear_processed=True)
        b = InMemoryPointCloud(metadata=a.root)
        assert a != b
        assert b.metadata == a.metadata
        assert torch.equal(b.pos, a.pos)

        c = InMemoryPointCloud(metadata=pathlib.Path(a.root))
        assert a != c
        assert c.metadata == a.metadata
        assert torch.equal(c.pos, a.pos)

    def test_InMemoryPointCloud_item(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        a = InMemoryPointCloud(metadata=mymeta, clear_processed=True)
        # When a slice is selected, the returned value is again an InMemoryPointCloud
        # print(a[0:2])
        assert isinstance(a[0:2], InMemoryPointCloud)
        # If an int is selected, the returned value is a torch_geometric Data instance.
        # print(a[0])
        assert isinstance(a[0], tgeo.data.Data)

    def test_InMemoryPointCloud_subsetting(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        mymeta_train = mymeta[0:2, :]
        mymeta_val = mymeta[2:, :]
        a_train = InMemoryPointCloud(metadata=mymeta_train, clear_processed=True)
        a_val = InMemoryPointCloud(metadata=mymeta_val, clear_processed=True)
        assert len(a_train) == 2
        assert len(a_val) == 4

        complete_pointcloud = InMemoryPointCloud(metadata=mymeta)
        complete_pointcloud.process()
        pc_train = complete_pointcloud[0:2]
        pc_val = complete_pointcloud[2:]
        assert all(mymeta_train.pheno == pc_train.metadata.pheno)
        assert all(mymeta_val.pheno == pc_val.metadata.pheno)

        assert (
            mymeta_train.sample_feature_names == pc_train.metadata.sample_feature_names
        )
        assert mymeta_val.sample_feature_names == pc_val.metadata.sample_feature_names

    def test_InMemoryPointCloud_raw_dir_already_present(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw"),
            root=os.path.join(TESTS_DIR, pointcloud_toy_dataset),
        )
        a = InMemoryPointCloud(metadata=mymeta, clear_processed=True)
        print(a)

    def test_InMemoryPointCloud_sample_with_one_point_no_transform(self):
        mymeta = gen_foldering_meta(os.path.join(TESTS_DIR, empty_sample_dataset))
        a = InMemoryPointCloud(metadata=mymeta, clear_processed=True)
        # print(a)
        for sample_x in a:
            # print(sample_x)
            assert len(sample_x.y) == 1
        b = InMemoryPointCloud(metadata=mymeta)
        for sample_x in b:
            # print(sample_x)
            assert len(sample_x.y) == 1

    def test_InMemoryPointCloud_sample_with_one_point_transform(self):
        # This is a pytorch-geometric/FixedPoints issue, see
        #   https://github.com/rusty1s/pytorch_geometric/issues/1090
        mymeta = gen_foldering_meta(os.path.join(TESTS_DIR, empty_sample_dataset))
        random_select_n_points = FixedPoints(num=100)
        a = InMemoryPointCloud(
            metadata=mymeta, clear_processed=True, transform=random_select_n_points
        )
        for sample_x in a:
            print(sample_x)
            assert len(sample_x.y) == 1

    def test_root_of_previous_test_issue(self):
        from torch_geometric.data.data import Data

        pointcloud = Data(pos=torch.randn(100, 3), y=torch.tensor([1]))
        single_point = Data(pos=torch.randn(1, 3), y=torch.tensor([1]))

        random_select_n_points = FixedPoints(num=10)

        print(random_select_n_points(pointcloud))
        # Data(pos=[10, 3], y=[1])
        assert len(random_select_n_points(pointcloud).y) == 1
        print(random_select_n_points(single_point))
        # Data(pos=[10, 3], y=[10])
        assert len(random_select_n_points(single_point).y) == 1

    def test_InMemoryPointCloud_different_raw_dirs_without_root(self):
        mymeta_toy = gen_foldering_meta(os.path.join(TESTS_DIR, pointcloud_toy_dataset))
        pointcloud_toy = InMemoryPointCloud(metadata=mymeta_toy, clear_processed=True)
        mymeta_tcell = gen_foldering_meta(os.path.join(TESTS_DIR, tcell_toy_dataset))
        pointcloud_tcell = InMemoryPointCloud(
            metadata=mymeta_tcell, clear_processed=True
        )
        assert (
            pointcloud_toy != pointcloud_tcell
        )  # the two pointclouds MUST not be the same.

        pointcloud_toy = InMemoryPointCloud(metadata=mymeta_toy)
        # Even after loading pointcloud_toy a second time, the data MUST NOT be the same
        if pointcloud_toy[0].pos.shape == pointcloud_tcell[0].pos.shape:
            assert not torch.allclose(pointcloud_toy[0].pos, pointcloud_tcell[0].pos)

    def test_InMemoryPointCloud_different_featurenames_in_data(self):
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
            my_pc = InMemoryPointCloud(metadata=mymeta)
            repr(my_pc)
        assert saved_meta == mymeta

    def test_InMemoryPointCloud_with_transform(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        random_select_n_points = FixedPoints(num=2)
        import numpy as np

        np.random.seed(123)
        a = InMemoryPointCloud(
            mymeta, transform=random_select_n_points, clear_processed=True
        )
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

    def test_InMemoryPointCloud_FixedPoints_get_twice(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        random_select_n_points = FixedPoints(num=2)
        import numpy as np

        np.random.seed(123)
        a = InMemoryPointCloud(
            mymeta, transform=random_select_n_points, clear_processed=True
        )

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

    def test_InMemoryPointCloud_DataLoader(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        random_select_n_points = FixedPoints(num=2)
        import numpy as np

        np.random.seed(123)
        a = InMemoryPointCloud(
            mymeta, transform=random_select_n_points, clear_processed=True
        )

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

    def test_InMemoryPointCloud_DataLoader_more_batches_than_samples(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        n_points_per_draw = 2
        random_select_n_points = FixedPoints(num=n_points_per_draw)
        import numpy as np

        np.random.seed(123)
        a = InMemoryPointCloud(
            mymeta, transform=random_select_n_points, clear_processed=True
        )

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

    def test_InMemoryPointCloud_prepretransforms(self):
        from pointcyto.transforms.transform_param_onlist import NormalizePointCloudParam

        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )

        mydataset = InMemoryPointCloud(mymeta, clear_processed=True)
        posmat: torch.Tensor = mydataset[0].pos
        # Without any normalization, the means are quite high.
        # 1 is just an empirical observation and has no further meaning
        assert torch.all(posmat.mean(dim=0).abs() > 1)

        mydataset = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=NormalizePointCloudParam(),
            clear_processed=True,
        )
        posmat: torch.Tensor = mydataset[0].pos
        # With normalization subtracting mean and dividing through standard deviation, the means are comparably.
        # 1 is just an empirical observation and has no further meaning
        assert torch.all(posmat.mean(dim=0).abs() < 1)

    def test_InMemoryPointCloud_reuse_prepretransforms(self):
        from pointcyto.transforms.transform_param_onlist import NormalizePointCloudParam

        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        mydataset = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=NormalizePointCloudParam(),
            clear_processed=True,
        )

        # Ususally you would not reuse the same metadata!
        # But instead apply the pre_transform with parameters on a different metadata object.
        # But for testing this is enough.
        my_new_dataset_reusing_normalization_parameters = InMemoryPointCloud(
            mymeta,
            pre_transform=mydataset.pretransform_parameter[0]["related_transform"](
                **mydataset.pretransform_parameter[0]["param"]
            ),
            clear_processed=True,
        )
        posmat: torch.Tensor = my_new_dataset_reusing_normalization_parameters[0].pos
        # Even if I did not use the pre_pre_transform_param, the pre_transform also makes the normalization
        # But with given mean and standard deviation
        assert torch.all(posmat.mean(dim=0).abs() < 1)

    def test_InMemoryPointCloud_pre_pre_transform_param_list(self):
        from pointcyto.transforms.transform_param_onlist import NormalizePointCloudParam

        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        mydataset = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=[
                NormalizePointCloudParam(),
                NormalizePointCloudParam(),
            ],
            clear_processed=True,
        )
        # The second normalization parameters are not zero
        # but much closer to zero than before
        # Probably the rest is just numerical instability
        assert torch.allclose(
            mydataset.pretransform_parameter[1]["param"]["mean"],
            torch.tensor(0, dtype=torch.float),
            atol=1e-2,
        )

    def test_InMemoryPointCloud_pre_pre_transform_param_None(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        mydataset = InMemoryPointCloud(
            mymeta, pre_pre_transform_param_onlist=None, clear_processed=True
        )
        print(mydataset)

    def test_InMemoryPointCloud_pre_pre_transform_param_list_when_reloading(self):
        from pointcyto.transforms.transform_param_onlist import NormalizePointCloudParam

        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        mydataset = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=NormalizePointCloudParam(),
            clear_processed=True,
        )
        with self.assertWarns(UserWarning):
            mydataset_reloaded = InMemoryPointCloud(
                mymeta,
                pre_pre_transform_param_onlist=NormalizePointCloudParam(),
                clear_processed=False,
            )
        assert torch.allclose(
            mydataset.pretransform_parameter[0]["param"]["mean"],
            mydataset_reloaded.pretransform_parameter[0]["param"]["mean"],
        )
        assert torch.allclose(
            mydataset.pretransform_parameter[0]["param"]["std"],
            mydataset_reloaded.pretransform_parameter[0]["param"]["std"],
        )
        assert torch.allclose(
            mydataset.pre_pre_transform_param_onlist[0].mean,
            mydataset_reloaded.pretransform_parameter[0]["param"]["mean"],
        )
        assert torch.allclose(
            mydataset.pre_pre_transform_param_onlist[0].std,
            mydataset_reloaded.pretransform_parameter[0]["param"]["std"],
        )

    def test_InMemoryPointCloud_change_metadata(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        a = InMemoryPointCloud(metadata=mymeta, clear_processed=True)

        # 1. Change only metadata.
        #       Problem: The PointCloud is already generated and does not get its information from the MetaData-object
        #                anymore. (It only uses it during .process())
        #                So even if the MetaData object and its "selection" is changed, that wont change anything for
        #                the processed PointCloud.
        # 1.1 Additional column
        df = a.metadata.pheno
        # adding a column to the phenodata
        # DO NOT DO IT LIKE THAT! (See error below and solution with MetaData.add_pheno_single())
        df.loc[:, "new_col"] = "a"
        print(a.metadata)

        # Selecting the new column works
        a.metadata.selection = "new_col"
        # BUT, accessing it NOT!
        with self.assertRaises(KeyError):
            # This cannot work as the MetaData object does not know about the new column.
            # class_name_id_map is missing
            print(a.metadata)
            # File "C:\Users\mi_so\PycharmProjects\ccc\ccc\datasets\metadata.py", line 245, in class_name_id_map
            #     return self._class_name_id_map[self.selection]
            # KeyError: 'D'
            #
            # That error occurs because it tries (but cannot) print the selected class levels.

        # To add a new column, do this:
        a.metadata.add_pheno_single(
            new_pheno_column=["a", "c", "c", "c", "e", "e"], col_name="new_col"
        )
        print(a.metadata)

        # 1.2 Changing existing data
        a.metadata.selection = "pheno_1"
        pre_selection_update_y = [str(single_pointcloud.y) for single_pointcloud in a]
        a.metadata.pheno.loc[:, "pheno_1"] = "X"
        a.metadata.selection = "pheno_1"
        a.metadata.update_selection()
        print(a.metadata.pheno)
        post_selection_update_y = [str(single_pointcloud.y) for single_pointcloud in a]

        # So here comes the problem:
        # The following holds TRUE, where we thought to have changed the metadata already!
        assert pre_selection_update_y == post_selection_update_y

    def test_InMemoryPointCloud_change_response(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        a = InMemoryPointCloud(metadata=mymeta, clear_processed=True)
        y_1 = [str(single_pointcloud.y) for single_pointcloud in a]
        # adding a column to the phenodata
        a.metadata.add_pheno_single(
            new_pheno_column=["a", "c", "c", "c", "c", "e"], col_name="new_col"
        )
        pre_selection_update_y = [str(single_pointcloud.y) for single_pointcloud in a]
        assert y_1 == pre_selection_update_y
        a.select_y_from_metadata("new_col")
        post_selection_update_y = [str(single_pointcloud.y) for single_pointcloud in a]
        assert pre_selection_update_y != post_selection_update_y

        a = InMemoryPointCloud(metadata=mymeta)
        pre_reloaded_selection_update_y = [
            str(single_pointcloud.y) for single_pointcloud in a
        ]
        assert pre_reloaded_selection_update_y == pre_selection_update_y

    def test_InMemoryPointCloud_split_pointcloud(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        a = InMemoryPointCloud(metadata=mymeta, clear_processed=True)

        assert len(a[1:3]) == 2
        data_part = [x.pos for x in a[1:3]]
        assert [x.shape for x in data_part] == [
            torch.Size([1000, 14]),
            torch.Size([1000, 14]),
        ]
        assert torch.allclose(data_part[0], a[1].pos)
        assert torch.allclose(data_part[1], a[2].pos)
        # mymeta.raw_filenames
        # ['A/P0I.fcs', 'A/PAB.fcs', 'A/PAB_copy.fcs', 'B/P0G.fcs', 'B/PAO.fcs', 'B/PAV.fcs']
        assert torch.allclose(data_part[0], data_part[1])
        assert len(a[1:4]) == 3

        data_part = [x.pos for x in a[1:4]]
        assert [x.shape for x in data_part] == [
            torch.Size([1000, 14]),
            torch.Size([1000, 14]),
            torch.Size([1000, 14]),
        ]
        assert torch.allclose(data_part[0], a[1].pos)
        assert torch.allclose(data_part[1], a[2].pos)
        assert torch.allclose(data_part[2], a[3].pos)
        # mymeta.raw_filenames
        # ['A/P0I.fcs', 'A/PAB.fcs', 'A/PAB_copy.fcs', 'B/P0G.fcs', 'B/PAO.fcs', 'B/PAV.fcs']
        assert torch.allclose(data_part[0], data_part[1])
        assert not torch.allclose(data_part[0], data_part[2])
        assert len(a[1:4]) == 3

        # NOTE: The complete data (_data) seems to stay the same always!
        # I hope that is no problem.
        assert a.pos.shape != a[1:3].pos.shape
        assert a._data.pos.shape == a[1:3]._data.pos.shape

    def test_InMemoryPointCloud_export_fcs(self):
        import flowio
        from numpy import reshape

        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        a = InMemoryPointCloud(metadata=mymeta, clear_processed=True)
        a.to_fcs("removeme")
        assert len(os.listdir("removeme")) == 2
        assert len(os.listdir("removeme/A")) == 3
        assert len(os.listdir("removeme/B")) == 3
        tmp = flowio.FlowData("removeme/B/PAO.fcs.fcs")
        assert tmp.text["p1r"] == "36"
        a.to_fcs("removeme_shifted", shift=100)
        npy_data_a = reshape(tmp.events, (-1, tmp.channel_count))
        assert len(os.listdir("removeme_shifted")) == 2
        assert len(os.listdir("removeme_shifted/A")) == 3
        assert len(os.listdir("removeme_shifted/B")) == 3
        tmp = flowio.FlowData("removeme_shifted/B/PAO.fcs.fcs")
        assert tmp.text["p1r"] != "36"
        npy_data_a_shifted = reshape(tmp.events, (-1, tmp.channel_count))

        assert npy_data_a.min() + 100 - npy_data_a_shifted.min() < 1e-4

    def test_InMemoryPointCloud_export_csv(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        a = InMemoryPointCloud(metadata=mymeta, clear_processed=True)
        with self.assertWarns(UserWarning):
            # UserWarning: In contrast to to_fcs(), only the pointcloud is saved, not the responses.
            a.to_csv("removeme")
        assert len(os.listdir("removeme")) == 2
        assert len(os.listdir("removeme/A")) == 3
        assert len(os.listdir("removeme/B")) == 3

    def test_InMemoryPointCloud_export_pt(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        a = InMemoryPointCloud(metadata=mymeta, clear_processed=True)
        a.to_pt("removeme")
        assert len(os.listdir("removeme")) == 2
        assert len(os.listdir("removeme/A")) == 3
        assert len(os.listdir("removeme/B")) == 3

    def test_InMemoryPointCloud_export_xxx(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        a = InMemoryPointCloud(metadata=mymeta, clear_processed=True)
        for xxx in ["jay", "fcs", "csv", "pt"]:
            a._to_xxx("removeme", filetype=xxx)
            assert len(os.listdir("removeme")) == 2
            assert len(os.listdir("removeme/A")) == 3
            assert len(os.listdir("removeme/B")) == 3
            shutil.rmtree("removeme")

    def test_benchmark_InMemoryPointCloud_export_xxx(self):
        do_large_benchmark = False  # Done 2021-01-19
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        if do_large_benchmark:
            benchmark_size = 7  # Done 2021-01-19
            for i in range(benchmark_size):
                # for i in range(2):
                # 0, 1, 2, 3, 4, 5,
                # 6, 12, 24, 48, 96, 192, xxx, 768
                mymeta = mymeta.concat(mymeta, ignore_identical_filenames=True)

        a = InMemoryPointCloud(metadata=mymeta, clear_processed=True)
        # to have unique files:
        tmp = [f"file_{i}.fcs" for i in range(len(a))]
        a.metadata.raw_filenames = tmp

        import time

        times = {}
        dir_sizes = {}
        difftimes = {"write": {}, "read_meta": {}, "read_data": {}}
        # all_types = ["pt", "jay", "fcs", "csv", "feather"]
        # all_types = [
        #     f.replace(".py", "")
        #     for f in os.listdir("src/pointcyto/io/loaders")
        #     if f.endswith(".py") and f != "__init__.py"
        # ]
        from pointcyto.io.parse_by_ext import POINTCLOUD_EXTENSIONS as all_types_dot

        all_types = [x.replace(".", "") for x in all_types_dot]

        print("\n ------- Start saving -------\n")
        for xxx in all_types:
            times[xxx] = {}
            times[xxx]["start_write"] = time.time()
            a._to_xxx(f"removeme_{xxx}", filetype=xxx, verbose=True)
            times[xxx]["end_write"] = time.time()
            timediff_write = times[xxx]["end_write"] - times[xxx]["start_write"]
            print(f"{xxx:10}: {timediff_write}")
            difftimes["write"][xxx] = timediff_write
            dir_sizes[xxx] = sum(
                os.path.getsize(os.path.join(f"removeme_{xxx}", f)) / 1048576
                for f in os.listdir(f"removeme_{xxx}")
            )

        print("\n ------- Start reading -------\n")
        for xxx in all_types:
            times[xxx] = {}
            times[xxx]["start_read_meta"] = time.time()
            meta_removeme = gen_meta_filenames(f"removeme_{xxx}")
            times[xxx]["start_read_data"] = time.time()
            impc_removeme = InMemoryPointCloud(
                metadata=meta_removeme, clear_processed=True
            )
            times[xxx]["end_read_data"] = time.time()
            print(impc_removeme)
            d_read_meta = times[xxx]["start_read_data"] - times[xxx]["start_read_meta"]
            d_read_data = times[xxx]["end_read_data"] - times[xxx]["start_read_data"]
            print(f"Read meta {xxx:10}: {d_read_meta}")
            print(f"Read data {xxx:10}: {d_read_data}\n")
            difftimes["read_meta"][xxx] = d_read_meta
            difftimes["read_data"][xxx] = d_read_data
        print("\n ------- End reading -------\n")

        for key, value in difftimes.items():
            print(key)
            for k, v in value.items():
                print("   ", k, v)
        print(f"Directory sizes for {len(meta_removeme)} files")
        for key, value in dir_sizes.items():
            print("    ", key, round(value, 2), "MB")
        # Test 2023-01-19, rhskl1
        # write
        #     pt 4.566260099411011
        #     jay 27.967937707901
        #     fcs 59.25578022003174
        #     csv 16.594340324401855
        # read_meta
        #     pt 0.008815765380859375
        #     jay 0.007297039031982422
        #     fcs 0.0071790218353271484
        #     csv 0.007416725158691406
        # read_data
        #     pt 8.280493259429932
        #     jay 35.553593158721924
        #     fcs 15.747443675994873
        #     csv 51.12806057929993
        # Directory sizes for 768 files
        #      pt 5471.66 MB
        #      jay 5471.54 MB
        #      fcs 5471.8 MB
        #      csv 12922.16 MB

        for xxx in all_types:
            shutil.rmtree(f"removeme_{xxx}")

    def test_InMemoryPointCloud_different_featurenames(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        a = InMemoryPointCloud(metadata=mymeta, clear_processed=True)

        with self.assertWarns(UserWarning):
            # UserWarning: In contrast to to_fcs(), only the pointcloud is saved, not the responses.
            a.to_csv("removeme")

        assert len(os.listdir("removeme")) == 2
        assert len(os.listdir("removeme/A")) == 3
        assert len(os.listdir("removeme/B")) == 3

        import pandas as pd

        single_sample = pd.read_csv("removeme/A/PAB.fcs.csv")
        single_sample.columns = ["new_" + x for x in single_sample.columns]
        single_sample.to_csv("removeme/A/PAB.fcs.csv", index=False)

        mymeta_different_featurenames = gen_foldering_meta("removeme")

        with self.assertRaises(ValueError):
            # The following error must occur:
            #   ValueError: Unequal feature names of
            #   A/PAB.fcs.csv:
            a_different_featurenames = InMemoryPointCloud(
                metadata=mymeta_different_featurenames, clear_processed=True
            )
            print(a_different_featurenames)

        mymeta_different_featurenames_ignore = gen_foldering_meta(
            "removeme", ignore_unequal_feature_names=True
        )
        # catch all warnings, there must not be any userwarnings
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            a_different_featurenames_ignore = InMemoryPointCloud(
                metadata=mymeta_different_featurenames_ignore, clear_processed=True
            )
        a_different_featurenames_ignore = InMemoryPointCloud(
            metadata=mymeta_different_featurenames_ignore,
            clear_processed=True,
        )
        assert (
            a_different_featurenames_ignore.metadata.feature_names[0]
            == "Feature names NOT identical over samples!"
        )

        with self.assertWarns(UserWarning):
            # UserWarning: In contrast to to_fcs(), only the pointcloud is saved, not the responses.
            a_different_featurenames_ignore.to_csv("removeme_2")

        single_sample = pd.read_csv("removeme_2/A/PAB.fcs.csv.csv")
        assert all([x.startswith("new_") for x in single_sample.columns])
        single_sample = pd.read_csv("removeme_2/A/P0I.fcs.csv.csv")
        assert all([not x.startswith("new_") for x in single_sample.columns])
        assert len(os.listdir("removeme_2")) == 2
        assert len(os.listdir("removeme_2/A")) == 3
        assert len(os.listdir("removeme_2/B")) == 3

    def tearDown(self) -> None:
        try:
            shutil.rmtree(os.path.join(TESTS_DIR, pointcloud_toy_dataset, "processed"))
            pass
        except FileNotFoundError:
            pass
        try:
            shutil.rmtree("removeme")
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
