import os
from unittest import TestCase

from pointcyto.data.InMemoryPointCloud import InMemoryPointCloud
from pointcyto.io.meta_read_foldering import gen_foldering_meta
from pointcyto.testutils.helpers import find_dirname_above_currentfile
from pointcyto.transforms.transforms_flowkit import FKtransform

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
# Now build the base-test directory (necessary if you want to use tests/testdata)
TESTS_DIR = find_dirname_above_currentfile()

pointcloud_toy_dataset = os.path.join(
    "testdata", "flowcytometry", "PointClouds_toy_dataset"
)


class TestTransforms(TestCase):
    def test_AsinhTransform_repr(self):
        a = FKtransform(
            flowkit_transform_classname="AsinhTransform",
            feature_indices=None,
            dataset_attribute="pos",
            param_t=1,
            param_m=2,
            param_a=2,
        )
        repr(a)

    def test_AsinhTransform_repr_featureindices(self):
        a = FKtransform(
            flowkit_transform_classname="AsinhTransform",
            feature_indices=[1, 2, 3, 4],
            dataset_attribute="pos",
            param_t=1,
            param_m=2,
            param_a=2,
        )
        repr(a)

    def test_AsinhTransform(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        complete_data_notransform = InMemoryPointCloud(mymeta, clear_processed=True)
        # print(complete_data_notransform)
        # print(summary(complete_data_notransform.pos))

        complete_data = InMemoryPointCloud(
            mymeta,
            pre_transform=FKtransform(
                flowkit_transform_classname="AsinhTransform",
                feature_indices=[13],
                dataset_attribute="pos",
                param_t=1,
                param_m=2,
                param_a=2,
            ),
            clear_processed=True,
        )
        # print(summary(complete_data.pos))
        assert (
            complete_data_notransform.pos[:, 13].max() > complete_data.pos[:, 13].max()
        )

        complete_data_allfeatures = InMemoryPointCloud(
            mymeta,
            pre_transform=FKtransform(
                flowkit_transform_classname="AsinhTransform",
                param_t=1,
                param_m=2,
                param_a=2,
            ),
            clear_processed=True,
        )
        # print(summary(complete_data_allfeatures.pos))
        allfeatures_max = complete_data_allfeatures.pos.max(0).values
        notrans_max = complete_data_notransform.pos.max(0).values
        assert all(
            [allfeatures_max[i] < notrans_max[i] for i in range(len(allfeatures_max))]
        )

    def test_RatioTransform(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        complete_data_notransform = InMemoryPointCloud(mymeta, clear_processed=True)
        print(complete_data_notransform)
        # print(summary(complete_data_notransform.pos))

        with self.assertRaises(ValueError):
            complete_data = InMemoryPointCloud(
                mymeta,
                pre_transform=FKtransform(
                    flowkit_transform_classname="RatioTransform",
                    dataset_attribute="pos",
                    param_a=1,
                    param_b=2,
                    param_c=2,
                    dim_labels=None,
                ),
                clear_processed=True,
            )
            print(complete_data)
