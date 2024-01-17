import os
from unittest import TestCase

import torch

from pointcyto.data.InMemoryPointCloud import InMemoryPointCloud
from pointcyto.io.meta_read_foldering import gen_foldering_meta
from pointcyto.testutils.helpers import find_dirname_above_currentfile
from pointcyto.transforms.transforms import (
    CalculateOutlierness,
    QminmaxPointCloud,
    global_mean,
    global_sd,
    qminmax,
)

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
# Now build the base-test directory (necessary if you want to use tests/testdata)
TESTS_DIR = find_dirname_above_currentfile()

pointcloud_toy_dataset = os.path.join(
    "testdata", "flowcytometry", "PointClouds_toy_dataset"
)

pointcloud_toy_dataset_mean = torch.tensor(
    [
        15.1515,
        20.7125,
        15.1940,
        8.9993,
        8.7140,
        7.5958,
        7.6895,
        6.9978,
        8.0298,
        5.7519,
        7.8421,
        8.2171,
        11.3506,
        4120.7495,
    ]
)

pointcloud_toy_dataset_sd = torch.tensor(
    [
        0.71723,
        0.21693,
        1.0523,
        1.5938,
        2.4265,
        4.7020,
        5.0719,
        5.7231,
        3.9511,
        6.3471,
        2.7981,
        3.7452,
        3.0114,
        2554.4,
    ]
)


class TestTransforms(TestCase):
    def test_global_mean(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        complete_data = InMemoryPointCloud(mymeta, clear_processed=True)
        assert torch.allclose(
            global_mean(complete_data),
            pointcloud_toy_dataset_mean,
            rtol=1e-3,
        )

    def test_global_sd(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        complete_data = InMemoryPointCloud(mymeta, clear_processed=True)
        assert torch.allclose(
            global_sd(complete_data),
            pointcloud_toy_dataset_sd,
            rtol=1e-3,
        )

    def test_global_sd_precalculate_mean(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        complete_data = InMemoryPointCloud(mymeta, clear_processed=True)
        means = global_mean(complete_data)
        assert torch.allclose(
            global_sd(complete_data, global_means=means),
            pointcloud_toy_dataset_sd,
            rtol=1e-3,
        )

    def test_NormalizePointCloud(self):
        from pointcyto.transforms.transforms import NormalizePointCloud

        repr(NormalizePointCloud(mean=torch.zeros((14)), std=torch.ones((14))))
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )

        no_transformation = InMemoryPointCloud(
            mymeta,
            clear_processed=True,
        )
        # You cannot use NormalizePointCloud without defining mean and std.
        with self.assertRaises(TypeError):
            complete_data = InMemoryPointCloud(
                mymeta, clear_processed=True, pre_transform=NormalizePointCloud()
            )
            print(complete_data)

        transformation_but_useless = InMemoryPointCloud(
            mymeta,
            clear_processed=True,
            pre_transform=NormalizePointCloud(
                mean=torch.zeros((14)), std=torch.ones((14))
            ),
        )

        transformation_halved = InMemoryPointCloud(
            mymeta,
            clear_processed=True,
            pre_transform=NormalizePointCloud(
                mean=torch.zeros((14)), std=torch.ones((14)) * 2
            ),
        )
        assert torch.allclose(no_transformation.pos, transformation_but_useless.pos)
        assert torch.allclose(no_transformation.pos, transformation_halved.pos * 2)

    def test_WeightedFixedPoints_repr(self):
        from pointcyto.transforms.transforms import WeightedFixedPoints

        a = WeightedFixedPoints(10, 5)
        repr(a)

    def test_CalculateOutlierness_repr(self):
        from pointcyto.transforms.transforms import CalculateOutlierness

        a = CalculateOutlierness(10)
        repr(a)

    def test_CalculateOutlierness(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        complete_data = InMemoryPointCloud(
            mymeta,
            pre_transform=CalculateOutlierness(n_reference=500, use_cuda=False),
            clear_processed=True,
        )
        assert "outlierness" in complete_data._data.keys()
        assert complete_data.outlierness.shape[0] == complete_data.pos.shape[0]

    def test_CalculateOutlierness_with_without_cuda_checkType(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        complete_data = InMemoryPointCloud(
            mymeta,
            pre_transform=CalculateOutlierness(n_reference=500, use_cuda=False),
            clear_processed=True,
        )
        assert "outlierness" in complete_data._data.keys()
        assert complete_data.outlierness.shape[0] == complete_data.pos.shape[0]

        if not torch.cuda.is_available():
            pass
        else:
            complete_data_cuda = InMemoryPointCloud(
                mymeta,
                pre_transform=CalculateOutlierness(n_reference=500, use_cuda=True),
                clear_processed=True,
            )
            assert "outlierness" in complete_data._data.keys()
            assert complete_data.outlierness.shape[0] == complete_data_cuda.pos.shape[0]

            assert not complete_data.outlierness.is_cuda
            assert complete_data_cuda.outlierness.is_cuda
            # The following assertion must be false because The 500 points in both cases drawn ar different.
            assert not torch.allclose(
                complete_data.outlierness,
                complete_data_cuda.outlierness.cpu(),
            )

    def test_CalculateOutlierness_with_without_cuda_check_euqal_cpu(self):
        import numpy as np

        from pointcyto.transforms.transform_param_onlist import NormalizePointCloudParam

        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        np.random.seed(164)
        complete_data = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=NormalizePointCloudParam(),
            pre_transform=CalculateOutlierness(n_reference=1, use_cuda=False),
            clear_processed=True,
        )
        if not torch.cuda.is_available():
            pass
        else:
            np.random.seed(164)
            complete_data_cuda = InMemoryPointCloud(
                mymeta,
                pre_pre_transform_param_onlist=NormalizePointCloudParam(),
                pre_transform=CalculateOutlierness(n_reference=1, use_cuda=True),
                clear_processed=True,
            )

            assert torch.allclose(
                complete_data.outlierness,
                complete_data_cuda.outlierness.cpu(),
                atol=1e-1,
            )

    def test_CalculateOutlierness_in_batches(self):
        import numpy as np

        from pointcyto.transforms.transform_param_onlist import NormalizePointCloudParam

        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        np.random.seed(164)
        complete_data_10 = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=NormalizePointCloudParam(),
            pre_transform=CalculateOutlierness(
                n_reference=10, use_cuda=False, calculate_in_batches=10
            ),
            clear_processed=True,
        )
        np.random.seed(164)
        complete_data_1 = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=NormalizePointCloudParam(),
            pre_transform=CalculateOutlierness(
                n_reference=10, use_cuda=False, calculate_in_batches=1
            ),
            clear_processed=True,
        )
        np.random.seed(164)
        complete_data_None = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=NormalizePointCloudParam(),
            pre_transform=CalculateOutlierness(n_reference=10, use_cuda=False),
            clear_processed=True,
        )
        assert torch.allclose(
            complete_data_1[0]["outlierness"], complete_data_None[0]["outlierness"]
        )
        assert torch.allclose(
            complete_data_1[0]["outlierness"],
            complete_data_10[0]["outlierness"],
            atol=1e3,
        )

    def test_CalculateOutlierness_drawMorePointsThanPresent(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        import torch_geometric as tg

        from pointcyto.transforms.transforms import FixedPointsOutlierness

        with self.assertRaises(ValueError):
            # Too little number of points, cannot draw 500k from each sample.
            complete_data = InMemoryPointCloud(
                mymeta,
                pre_transform=tg.transforms.compose.Compose(
                    [
                        CalculateOutlierness(n_reference=100, use_cuda=False),
                        FixedPointsOutlierness(num=500000, replace=False),
                    ]
                ),
                clear_processed=True,
            )

        complete_data = InMemoryPointCloud(
            mymeta,
            pre_transform=tg.transforms.compose.Compose(
                [
                    CalculateOutlierness(n_reference=100, use_cuda=False),
                    FixedPointsOutlierness(
                        num=500000, replace=False, allow_duplicates=True
                    ),
                ]
            ),
            clear_processed=True,
        )
        assert "outlierness" in complete_data._data.keys()
        assert complete_data.outlierness.shape[0] == complete_data.pos.shape[0]

    def test_qminmax_function(self):
        # 10 cells, 4 parameters
        new_tensor = torch.rand(size=(100, 4)) * 10
        print(new_tensor)
        print(new_tensor.shape)
        a = qminmax(tensor=new_tensor, quantile_range=[0.1, 0.9])
        print(a)

    def test_Qminmax_normalize(self):
        import numpy as np

        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        np.random.seed(164)
        complete_data_10 = InMemoryPointCloud(
            mymeta,
            pre_transform=QminmaxPointCloud(quantile_range=[0.01, 0.99]),
            clear_processed=True,
        )
        print(complete_data_10)
