import os
import shutil
from unittest import TestCase

import torch
from torch_geometric.transforms.compose import Compose

from pointcyto.data.InMemoryPointCloud import InMemoryPointCloud
from pointcyto.io.meta_read_foldering import gen_foldering_meta
from pointcyto.testutils.helpers import find_dirname_above_currentfile
from pointcyto.transforms.transform_param_onlist import (
    FixedPointsOnList,
    NormalizePointCloudParam,
)

TESTS_DIR = find_dirname_above_currentfile()


pointcloud_toy_dataset = os.path.join(
    "testdata", "flowcytometry", "PointClouds_toy_dataset"
)


class TestPrePreTransformsOnList(TestCase):
    def test_NormalizePointCloudParam_as_list_and_as_single_transform(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        complete_data = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=[NormalizePointCloudParam()],
            clear_processed=True,
        )
        complete_data = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=NormalizePointCloudParam(),
            clear_processed=True,
        )
        print(complete_data)

    def test_NormalizePointCloudParam_multiple(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        complete_data = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=[
                NormalizePointCloudParam(),
                NormalizePointCloudParam(),
            ],
            clear_processed=True,
        )
        repr(complete_data)

    def test_NormalizePointCloudParam_faulty_in_pre_transform(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        with self.assertRaises(TypeError):
            complete_data = InMemoryPointCloud(
                mymeta,
                pre_transform=[NormalizePointCloudParam(), NormalizePointCloudParam()],
                clear_processed=True,
            )
        with self.assertRaises(AttributeError):
            complete_data = InMemoryPointCloud(
                mymeta, pre_transform=NormalizePointCloudParam(), clear_processed=True
            )
            print(complete_data)

    def test_NormalizePointCloudParam_pre_pre_transform_param_list_save_load(self):
        from pointcyto.transforms.transform_param_onlist import NormalizePointCloudParam

        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        prepre_trans_list = [NormalizePointCloudParam(), NormalizePointCloudParam()]
        mydataset = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=prepre_trans_list,
            clear_processed=True,
        )

        import pickle

        with open("pretransform_parameter.pickle", "wb") as f:
            pickle.dump(mydataset.pretransform_parameter, f)
        with open("pretransform_parameter.pickle", "rb") as f:
            loaded_pretransform_parameter = pickle.load(f)

        transform_list = []
        for single_pretransform in loaded_pretransform_parameter:
            recreated_transform = single_pretransform["related_transform"](
                **single_pretransform["param"]
            )
            with self.assertRaises(TypeError):
                repr(single_pretransform["related_transform"]())
            transform_list += [recreated_transform]
        composed_transform_list = Compose(transform_list)

        with self.assertWarns(UserWarning):
            # Here a UserWarning is issues because we use the same mymeta but different transforms as before
            # This is absolutely expected behaviour
            mydataset_reloaded = InMemoryPointCloud(
                mymeta, pre_transform=composed_transform_list
            )

        import warnings

        with warnings.catch_warnings(record=True) as w:
            # In contrast to before, here we clear the Pointcloud related to mymeta, so no warning must occur
            mydataset_reloaded = InMemoryPointCloud(
                mymeta, pre_transform=composed_transform_list, clear_processed=True
            )
            if any(issubclass(w_.category, UserWarning) for w_ in w):
                raise AssertionError("UserWarning was issued")

        assert torch.allclose(mydataset_reloaded[0].pos, mydataset[0].pos)

    def test_NormalizePointCloudParam_FixedPoints(self):
        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        complete_data = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=[
                FixedPointsOnList(num=100),
                NormalizePointCloudParam(),
            ],
            clear_processed=True,
        )
        repr(complete_data)
        assert complete_data.pos.shape[0] == 600

    def test_ScaleLowHigh01(self):
        from pointcyto.transforms.transform_param_onlist import ScaleLowHigh01OnList

        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        original_data = InMemoryPointCloud(
            mymeta,
            clear_processed=True,
        )
        last_pos_value = original_data.pos[-1, -1]

        a = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=[
                ScaleLowHigh01OnList(),
            ],
            clear_processed=True,
        )
        repr(a)

        # one low-high shift for all samples
        a = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=[
                # ScaleLowHigh01OnList([[[0, tensor(6406.0)]]]),
                ScaleLowHigh01OnList([[[0, last_pos_value]]]),
            ],
            clear_processed=True,
        )

        assert a.pos[-1, -1] == 1
        # A low-high shift per feature for all samples
        with self.assertRaises(ValueError):
            # Wrong brackets multiplied
            a = InMemoryPointCloud(
                mymeta,
                pre_pre_transform_param_onlist=[
                    ScaleLowHigh01OnList([[[0, last_pos_value] * 14]]),
                ],
                clear_processed=True,
            )
        a = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=[
                ScaleLowHigh01OnList([[[0, last_pos_value]] * 14]),
            ],
            clear_processed=True,
        )
        assert a.pos[-1, -1] == 1
        with self.assertRaises(ValueError):
            a = InMemoryPointCloud(
                mymeta,
                pre_pre_transform_param_onlist=[
                    ScaleLowHigh01OnList([[[0, last_pos_value]] * 13]),
                ],
                clear_processed=True,
            )
        a = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=[
                ScaleLowHigh01OnList([[[1]] * 14]),
            ],
            clear_processed=True,
        )
        assert torch.allclose(original_data.pos - a.pos, torch.tensor(1.0))
        a = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=[
                ScaleLowHigh01OnList([[[1]]]),
            ],
            clear_processed=True,
        )
        assert torch.allclose(original_data.pos - a.pos, torch.tensor(1.0))
        a = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=[
                ScaleLowHigh01OnList([[[i] for i in range(14)]]),
            ],
            clear_processed=True,
        )
        assert torch.allclose(
            (original_data.pos - a.pos)[1, :],
            torch.tensor(
                [
                    0.0,
                    1.0,
                    2.0,
                    3.0,
                    4.0,
                    5.0,
                    6.0,
                    7.0,
                    8.0,
                    9.0,
                    10.0,
                    11.0,
                    12.0,
                    13.0,
                ]
            ),
        )
        assert torch.allclose(
            (original_data.pos - a.pos)[-1, :],
            torch.tensor(
                [
                    0.0,
                    1.0,
                    2.0,
                    3.0,
                    4.0,
                    5.0,
                    6.0,
                    7.0,
                    8.0,
                    9.0,
                    10.0,
                    11.0,
                    12.0,
                    13.0,
                ]
            ),
        )

    def test_ReTransformShiftAsinhOnList(self):
        try:
            shutil.rmtree("removeme")
        except FileNotFoundError:
            pass
        from pointcyto.transforms.transform_param_onlist import (
            ReTransformShiftAsinhOnList,
        )

        mymeta = gen_foldering_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        )
        original_data = InMemoryPointCloud(
            mymeta,
            clear_processed=True,
        )
        # Apply on already asinh-transformed values
        from pointcyto.transforms.transforms_flowcore import ArcsinhTransform

        asinh_transformed = InMemoryPointCloud(
            mymeta,
            pre_transform=ArcsinhTransform(
                a=0,
                b=1 / 5.12,
                c=0,
            ),
            clear_processed=True,
        )
        asinh_transformed.to_fcs("removeme")
        asinh_trans_meta = gen_foldering_meta("removeme")
        with self.assertWarns(UserWarning):
            # UserWarning: Do not use this transformation on transformed AND
            # shifted values, only on transformed and NOT shifted.
            asinh_RE_transformed = InMemoryPointCloud(
                asinh_trans_meta,
                pre_pre_transform_param_onlist=[
                    ReTransformShiftAsinhOnList(
                        # dataset_attribute="pos",
                        samplewise_feature_shifts_asinhspace=[[[0]]],
                        do_shift_in_rawspace=False,
                        original_asinh_cofactors=[5.12],
                        original_asinh_cofactors_applied=True,
                        new_asinh_cofactors=[5.12],
                        inplace=True,
                    ),
                ],
                clear_processed=True,
            )
        assert torch.allclose(asinh_transformed.pos, asinh_RE_transformed.pos)

        with self.assertRaises(ValueError):
            # "100" is a totally unreasonable value after asinh transformation
            a = InMemoryPointCloud(
                mymeta,
                pre_pre_transform_param_onlist=[
                    ReTransformShiftAsinhOnList(
                        # dataset_attribute="pos",
                        samplewise_feature_shifts_asinhspace=[[[1, 100]]],
                        do_shift_in_rawspace=False,
                        original_asinh_cofactors=[1],
                        original_asinh_cofactors_applied=False,
                        new_asinh_cofactors=[1],
                        inplace=True,
                    ),
                ],
                clear_processed=True,
            )

        with self.assertRaises(ValueError):
            # Different length of cofactors
            a = InMemoryPointCloud(
                mymeta,
                pre_pre_transform_param_onlist=[
                    ReTransformShiftAsinhOnList(
                        # dataset_attribute="pos",
                        samplewise_feature_shifts_asinhspace=[[[0]]],
                        do_shift_in_rawspace=False,
                        original_asinh_cofactors=[1],
                        original_asinh_cofactors_applied=False,
                        new_asinh_cofactors=[1] * 14,
                        inplace=True,
                    ),
                ],
                clear_processed=True,
            )
        a = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=[
                ReTransformShiftAsinhOnList(
                    # dataset_attribute="pos",
                    samplewise_feature_shifts_asinhspace=[[[0]]],
                    do_shift_in_rawspace=False,
                    original_asinh_cofactors=[1],
                    original_asinh_cofactors_applied=False,
                    new_asinh_cofactors=[1],
                    inplace=True,
                ),
            ],
            clear_processed=True,
        )
        assert torch.allclose(a.pos, torch.asinh(original_data.pos))

        with self.assertRaises(ValueError):
            a = InMemoryPointCloud(
                mymeta,
                pre_pre_transform_param_onlist=[
                    ReTransformShiftAsinhOnList(
                        # dataset_attribute="pos",
                        samplewise_feature_shifts_asinhspace=[[[0]]],
                        do_shift_in_rawspace=False,
                        original_asinh_cofactors=[1] * 14,
                        original_asinh_cofactors_applied=False,
                        new_asinh_cofactors=[1] * 14,
                        inplace=True,
                    ),
                ],
                clear_processed=True,
            )
        with self.assertRaises(ValueError):
            # Wrong bracket multiplied
            a = InMemoryPointCloud(
                mymeta,
                pre_pre_transform_param_onlist=[
                    ReTransformShiftAsinhOnList(
                        # dataset_attribute="pos",
                        samplewise_feature_shifts_asinhspace=[[[0] * 14]],
                        do_shift_in_rawspace=False,
                        original_asinh_cofactors=[1] * 14,
                        original_asinh_cofactors_applied=False,
                        new_asinh_cofactors=[1] * 14,
                        inplace=True,
                    ),
                ],
                clear_processed=True,
            )
        a = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=[
                ReTransformShiftAsinhOnList(
                    # dataset_attribute="pos",
                    samplewise_feature_shifts_asinhspace=[[[0]] * 14],
                    do_shift_in_rawspace=False,
                    original_asinh_cofactors=[1] * 14,
                    original_asinh_cofactors_applied=False,
                    new_asinh_cofactors=[1] * 14,
                    inplace=True,
                ),
            ],
            clear_processed=True,
        )
        assert torch.allclose(a.pos, torch.asinh(original_data.pos))

        # Single and dual values per sample combined
        # print([[[0]] * 13 + [[1, 3]]])
        a = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=[
                ReTransformShiftAsinhOnList(
                    # dataset_attribute="pos",
                    samplewise_feature_shifts_asinhspace=[[[0]] * 13 + [[1, 3]]],
                    do_shift_in_rawspace=False,
                    original_asinh_cofactors=[1] * 14,
                    original_asinh_cofactors_applied=False,
                    new_asinh_cofactors=[1] * 14,
                    inplace=True,
                ),
            ],
            clear_processed=True,
        )
        a = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=[
                ReTransformShiftAsinhOnList(
                    # dataset_attribute="pos",
                    samplewise_feature_shifts_asinhspace=[[[1]]],
                    do_shift_in_rawspace=False,
                    original_asinh_cofactors=[1],
                    original_asinh_cofactors_applied=False,
                    new_asinh_cofactors=[1],
                    inplace=True,
                ),
            ],
            clear_processed=True,
        )
        assert torch.allclose(a.pos, torch.asinh(original_data.pos) - 1, atol=1e-4)
        a = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=[
                ReTransformShiftAsinhOnList(
                    # dataset_attribute="pos",
                    samplewise_feature_shifts_asinhspace=[[[1, 4]]],
                    do_shift_in_rawspace=False,
                    original_asinh_cofactors=[1],
                    original_asinh_cofactors_applied=False,
                    new_asinh_cofactors=[1],
                    inplace=True,
                ),
            ],
            clear_processed=True,
        )
        assert torch.allclose(
            a.pos, (torch.asinh(original_data.pos) - 1) / (4 - 1), atol=1e-4
        )
        a = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=[
                ReTransformShiftAsinhOnList(
                    # dataset_attribute="pos",
                    samplewise_feature_shifts_asinhspace=[[[0]]],
                    do_shift_in_rawspace=False,
                    original_asinh_cofactors=[1],
                    original_asinh_cofactors_applied=False,
                    new_asinh_cofactors=[2],
                    inplace=True,
                ),
            ],
            clear_processed=True,
        )
        assert torch.allclose(a.pos, torch.asinh(original_data.pos / 2.0), atol=1e-4)

        a = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=[
                ReTransformShiftAsinhOnList(
                    # dataset_attribute="pos",
                    samplewise_feature_shifts_asinhspace=[[[1, 4]] * 14],
                    do_shift_in_rawspace=False,
                    original_asinh_cofactors=[1] * 14,
                    original_asinh_cofactors_applied=False,
                    new_asinh_cofactors=[2] * 14,
                    inplace=True,
                ),
            ],
            clear_processed=True,
        )
        assert torch.allclose(
            a.pos,
            (
                (
                    torch.asinh(original_data.pos / 2.0)
                    - (torch.asinh(torch.sinh(torch.tensor(1)) / 2))
                )
                / (
                    torch.asinh(torch.sinh(torch.tensor(4)) / 2)
                    - torch.asinh(torch.sinh(torch.tensor(1)) / 2)
                )
            ),
            atol=1e-4,
        )
        a = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=[
                ReTransformShiftAsinhOnList(
                    # dataset_attribute="pos",
                    samplewise_feature_shifts_asinhspace=[[[1, 4]] * 14],
                    do_shift_in_rawspace=False,
                    original_asinh_cofactors=[3] * 14,
                    original_asinh_cofactors_applied=False,
                    new_asinh_cofactors=[2] * 14,
                    inplace=True,
                ),
            ],
            clear_processed=True,
        )
        assert torch.allclose(
            a.pos,
            (
                (
                    torch.asinh(original_data.pos / 2.0)
                    - (torch.asinh(torch.sinh(torch.tensor(1)) / 2 * 3))
                )
                / (
                    torch.asinh(torch.sinh(torch.tensor(4)) / 2 * 3)
                    - torch.asinh(torch.sinh(torch.tensor(1)) / 2 * 3)
                )
            ),
            atol=1e-4,
        )

        a = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=[
                ReTransformShiftAsinhOnList(
                    # dataset_attribute="pos",
                    samplewise_feature_shifts_asinhspace=[[[0]] * 14],
                    do_shift_in_rawspace=False,
                    original_asinh_cofactors=[x + 1 for x in range(14)],
                    original_asinh_cofactors_applied=False,
                    new_asinh_cofactors=[x + 1 for x in range(14)],
                    inplace=True,
                ),
            ],
            clear_processed=True,
        )
        from pointcyto.transforms.transforms_functional import scale_featurewise

        assert torch.allclose(
            a.pos,
            torch.asinh(
                scale_featurewise(
                    original_data.pos,
                    feature_scaling_vector=[x + 1 for x in range(14)],
                )
            ),
        )

        a = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=[
                ReTransformShiftAsinhOnList(
                    # dataset_attribute="pos",
                    samplewise_feature_shifts_asinhspace=[[[0]] * 14],
                    do_shift_in_rawspace=False,
                    original_asinh_cofactors=[x + 1 for x in range(14)],
                    original_asinh_cofactors_applied=False,
                    new_asinh_cofactors=[x + 2 for x in range(14)],
                    inplace=True,
                ),
            ],
            clear_processed=True,
        )
        assert torch.allclose(
            a.pos,
            torch.asinh(
                scale_featurewise(
                    original_data.pos,
                    feature_scaling_vector=[x + 2 for x in range(14)],
                )
            ),
        )

        old_cof = [x + 1 for x in range(14)]
        new_cof = [x * 2 + 5 for x in range(14)]
        a = InMemoryPointCloud(
            mymeta,
            pre_pre_transform_param_onlist=[
                ReTransformShiftAsinhOnList(
                    # dataset_attribute="pos",
                    samplewise_feature_shifts_asinhspace=[[[1, 4]] * 14],
                    do_shift_in_rawspace=False,
                    original_asinh_cofactors=old_cof,
                    original_asinh_cofactors_applied=False,
                    new_asinh_cofactors=new_cof,
                    inplace=True,
                ),
            ],
            clear_processed=True,
        )
        for col_i in range(14):
            # assert torch.allclose(
            print(
                a.pos[:, col_i],
                (
                    (
                        torch.asinh(original_data.pos[:, col_i] / new_cof[col_i])
                        - (
                            torch.asinh(
                                torch.sinh(torch.tensor(1))
                                / new_cof[col_i]
                                * old_cof[col_i]
                            )
                        )
                    )
                    / (
                        torch.asinh(
                            torch.sinh(torch.tensor(4))
                            / new_cof[col_i]
                            * old_cof[col_i]
                        )
                        - torch.asinh(
                            torch.sinh(torch.tensor(1))
                            / new_cof[col_i]
                            * old_cof[col_i]
                        )
                    )
                ),
                # atol=1e-4
            )

    def tearDown(self) -> None:
        try:
            os.remove("pretransform_parameter.pickle")
            pass
        except FileNotFoundError:
            pass
