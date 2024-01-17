import warnings
from typing import List, Union

import torch
from torch_geometric.data.dataset import Dataset
from torch_geometric.transforms.fixed_points import FixedPoints

from pointcyto.transforms.transforms import (
    NormalizePointCloud,
    functional_transform_adapter,
    global_mean,
    global_sd,
    normalize,
)
from pointcyto.transforms.transforms_functional import (
    arcsinh,
    scale_featurewise,
    scale_low_high_01,
)
from pointcyto.transforms.utils import standard_repr


# from https://stackoverflow.com/questions/12472338/flattening-a-list-recursively
def flatten(S: list):
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])


class NormalizePointCloudParam(object):
    """
    Normalization in this context means
    """

    def __init__(self, inplace: bool = False, dataset_attribute: str = "pos"):
        self.inplace = inplace
        self.attr = dataset_attribute
        self.name = "NormalizePointCloudParam"
        self.related_transform = NormalizePointCloud

        # default params
        self.mean = 0
        self.std = 1

    def __call__(self, data_list: Dataset):
        """
        Args:
            tensor (Tensor): Tensor image of size (C, H, W) to be normalized.

        Returns:
            Tensor: Normalized Tensor image.
        """

        self.mean = global_mean(data_list)
        self.std = global_sd(data_list, global_means=self.mean)

        for sample in data_list:
            setattr(
                sample,
                self.attr,
                functional_transform_adapter(
                    sample, normalize, self.attr, self.mean, self.std, self.inplace
                ),
            )

        return (
            data_list,
            {
                "name": self.name,
                "related_transform": self.related_transform,
                "param": {"mean": self.mean, "std": self.std},
            },
        )

    def __repr__(self):
        return standard_repr(self)


class FixedPointsOnList(object):
    def __init__(self, num: int, replace: bool = False, allow_duplicates: bool = False):
        self.fixedpoints = FixedPoints(
            num=num, replace=replace, allow_duplicates=allow_duplicates
        )
        self.inplace = None
        self.attr = None
        self.name = "FixedPointsOnList"
        self.related_transform = None

    def __call__(self, data_list: Dataset):
        for sample_i, sample in enumerate(data_list):
            data_list[sample_i] = self.fixedpoints(sample)

        return (
            data_list,
            {
                "name": self.name,
                "related_transform": self.related_transform,
                "param": {},
            },
        )

    def __repr__(self):
        return standard_repr(self)


class ScaleLowHigh01OnList:
    def __init__(
        self,
        samplewise_feature_shifts: List[List[Union[List, float]]] = [[[1, 100]]],
        inplace: bool = False,
        dataset_attribute: str = "pos",
    ):
        """_summary_

        Args:
            samplewise_feature_shifts (List[List[Union[List, float]]], optional):
              - A list of shifts for EACH SAMPLE. Therefore the order of samples _has_ to correspond
              to the here given samplewise shifts.
              - Each element of this list corresponds to samplewise shifts _per feature_.
                - Per feature,
                    - each element can either be
                        1)  A list with a single value, then this value will be subtracted from all
                        values for that feature
                        2)  A list of two values, then the low value will be shifted to 0 and the high value to 1.
                            This is the same as min-max transformation, just with "min" and "max" replaced
                            by the given "low" and "high" values.

                Defaults to [[1, 100]] -->
                    For all samples,
                        and all features,
                            1   -> 0
                            100 -> 1
                            by
                            (x - 1)/(100-1)

            inplace (bool, optional): _description_. Defaults to False.
            dataset_attribute (str, optional): _description_. Defaults to "pos".
        """
        self.samplewise_feature_shifts = samplewise_feature_shifts
        self.name = "ScaleLowHigh01OnList"
        self.related_transform = None
        self.inplace = inplace
        self.attr = dataset_attribute
        self.related_transform = None

    def __call__(self, data_list: Dataset):
        """
        Args:
            tensor (Tensor): Tensor image of size (C, H, W) to be normalized.

        Returns:
            Tensor: Normalized Tensor image.
        """
        samplewise_feature_shifts = self.samplewise_feature_shifts
        if len(samplewise_feature_shifts) != len(data_list):
            if len(samplewise_feature_shifts) == 1:
                samplewise_feature_shifts = samplewise_feature_shifts * len(data_list)
            else:
                ValueError(
                    "Either give the same number of shifts as samples, or only a single one."
                )

        for sample_i, sample in enumerate(data_list):
            setattr(
                sample,
                self.attr,
                functional_transform_adapter(
                    sample,
                    scale_low_high_01,
                    self.attr,
                    samplewise_feature_shifts[sample_i],
                    self.inplace,
                ),
            )

        return (
            data_list,
            {
                "name": self.name,
                "related_transform": self.related_transform,
                "param": {"samplewise_feature_shifts": self.samplewise_feature_shifts},
            },
        )

    def __repr__(self):
        return standard_repr(self)


class ReTransformShiftAsinhOnList(ScaleLowHigh01OnList):
    def __init__(
        self,
        samplewise_feature_shifts_asinhspace: List[List[Union[List, float]]] = [
            [[1, 100]]
        ],
        do_shift_in_rawspace: bool = False,
        original_asinh_cofactors: List[float] = [150],
        original_asinh_cofactors_applied: bool = False,
        new_asinh_cofactors: List[float] = [10],
        inplace: bool = False,
        dataset_attribute: str = "pos",
    ):
        """_summary_

        Args:
            samplewise_feature_shifts_asinhspace (List[List[Union[List, float]]], optional):
              - A list of shifts for EACH SAMPLE. Therefore the order of samples _has_ to correspond
              to the here given samplewise shifts.
              - Each element of this list corresponds to samplewise shifts _per feature_.
                - Per feature,
                    - each element can either be
                        1)  A list with a single value, then this value will be subtracted from all
                        values for that feature
                        2)  A list of two values, then the low value will be shifted to 0 and the high value to 1.
                            This is the same as min-max transformation, just with "min" and "max" replaced
                            by the given "low" and "high" values.

                Defaults to [[1, 100]] -->
                    For all samples,
                        and all features,
                            1   -> 0
                            100 -> 1
                            by
                            (x - 1)/(100-1)
            do_shift_in_rawspace:
                Should the inversed shifts be applied in the raw space (True)?
                If False, the inversed shifts are (properly) applied in the new_asinh_cofactor-space.
            original_asinh_cofactors:
                Each element of this list corresponds to the cofactor for the asinh:
                    asinh(x_i/cofactor_i)
                per feature i which the data have been transformed with to
                identify samplewise_feature_shifts_asinhspace.
            original_asinh_cofactors_applied:
                Are the original_asinh_cofactors still applied on the data (True) or are we loading
                raw data(False)?
            new_asinh_cofactors:
                Each element of this list corresponds to the cofactor for the asinh:
                    asinh(x_i/cofactor_i)
                per feature i which the data SHOULD be transformed with.
            inplace (bool, optional): _description_. Defaults to False.
            dataset_attribute (str, optional): _description_. Defaults to "pos".
        """

        self.samplewise_feature_shifts_asinhspace = samplewise_feature_shifts_asinhspace
        self.original_asinh_cofactors = original_asinh_cofactors
        self.original_asinh_cofactors_applied = original_asinh_cofactors_applied
        self.do_shift_in_rawspace = do_shift_in_rawspace
        self.new_asinh_cofactors = new_asinh_cofactors
        self.name = "ReTransformShiftAsinhOnList"
        self.related_transform = None
        self.inplace = inplace
        self.attr = dataset_attribute
        self.related_transform = None

        if not all(
            [
                len(self.original_asinh_cofactors) == len(x)
                for x in self.samplewise_feature_shifts_asinhspace
            ]
        ):
            raise ValueError(
                "len(samplewise_feature_shifts_asinhspace) must be identical to len(original_asinh_cofactors)"
            )

        if len(self.new_asinh_cofactors) != len(self.original_asinh_cofactors):
            raise ValueError("New and old asinh cofactors must be the same length.")

        if original_asinh_cofactors_applied:
            warnings.warn(
                "Do not use this transformation on transformed AND shifted values, only on "
                + "transformed and NOT shifted."
            )
            # In theory, I have to inverse with sinh() and the original cofactors, THEN
            # apply the new transformation as is right now.
            # raise NotImplementedError

        def recursive_apply(item, fun=torch.sinh):
            if isinstance(item, list):
                return [recursive_apply(x, fun) for x in item]
            else:
                return fun(item)

        # To identify the samplewise feature shifts (in asinh-space), we did the following:
        #   1. Apply the cofactor per feature (=divide through cofactor)
        #   2. Asinh(-) transformation of all values
        #   3. Manual identification of the shifts
        # Therefore, to inverse:
        #   1. "Un-apply" the asinh (=sinh) to the manually identified shifts
        #   2. "Un-apply" the cofactor by multiplying it per feature

        # 1. "Un-apply" (inverse) the asinh
        pre_cofactor_shifts = recursive_apply(
            samplewise_feature_shifts_asinhspace,
            lambda x: torch.sinh(torch.tensor(x) * 1.0),
        )
        if any([torch.isinf(x) for x in flatten(pre_cofactor_shifts)]):
            raise ValueError(
                "torch.sinh() resulted in atleast one inf value, are your asinhspace feature shifts reasonable?"
            )

        # 2. "Un-apply" the cofactors:
        #   Go through all samples, multiply all manually idenfied shifts with the corresponding cofactors
        rawspace_shifts = []
        newspace_shifts = []
        for sample in pre_cofactor_shifts:
            rawspace_shifts.append([])
            newspace_shifts.append([])
            for feature_i, feature_shift in enumerate(sample):
                rawspace_shifts[-1].append(
                    recursive_apply(
                        feature_shift, lambda x: x * original_asinh_cofactors[feature_i]
                    )
                )
                newspace_shifts[-1].append(
                    recursive_apply(
                        rawspace_shifts[-1][-1],
                        lambda x: arcsinh(x / new_asinh_cofactors[feature_i]),
                    )
                )
        self.rawspace_shifts = rawspace_shifts
        self.newspace_shifts = newspace_shifts

    def __call__(self, data_list: Dataset):
        # samplewise_feature_shifts = self.samplewise_feature_shifts
        # if len(samplewise_feature_shifts) != len(data_list):
        #     if len(samplewise_feature_shifts) == 1:
        #         samplewise_feature_shifts = samplewise_feature_shifts * len(data_list)
        #     else:
        #         ValueError(
        #             "Either give the same number of shifts as samples, or only a single one."
        #         )
        if self.do_shift_in_rawspace:
            samplewise_feature_shifts = self.rawspace_shifts
        else:
            samplewise_feature_shifts = self.newspace_shifts
        if len(samplewise_feature_shifts) != len(data_list):
            if len(samplewise_feature_shifts) == 1:
                samplewise_feature_shifts = samplewise_feature_shifts * len(data_list)
            else:
                ValueError(
                    "Either give the same number of shifts as samples, or only a single one."
                )
        for sample_i, sample in enumerate(data_list):
            if self.original_asinh_cofactors_applied:
                # 1. Undo the asinh transformation
                setattr(
                    sample,
                    self.attr,
                    functional_transform_adapter(sample, torch.sinh, self.attr),
                )
                # 2. Undo the original feature scalings
                setattr(
                    sample,
                    self.attr,
                    functional_transform_adapter(
                        sample,
                        scale_featurewise,
                        self.attr,
                        [1 / x for x in self.original_asinh_cofactors],
                        self.inplace,
                    ),
                )
            if self.do_shift_in_rawspace:
                setattr(
                    sample,
                    self.attr,
                    functional_transform_adapter(
                        sample,
                        scale_low_high_01,
                        self.attr,
                        samplewise_feature_shifts[sample_i],
                        self.inplace,
                    ),
                )
            # 1. Apply new cofactors
            setattr(
                sample,
                self.attr,
                functional_transform_adapter(
                    sample,
                    scale_featurewise,
                    self.attr,
                    self.new_asinh_cofactors,
                    self.inplace,
                ),
            )
            # 2. Apply asinh
            setattr(
                sample,
                self.attr,
                functional_transform_adapter(sample, arcsinh, self.attr),
            )
            if not self.do_shift_in_rawspace:
                setattr(
                    sample,
                    self.attr,
                    functional_transform_adapter(
                        sample,
                        scale_low_high_01,
                        self.attr,
                        samplewise_feature_shifts[sample_i],
                        self.inplace,
                    ),
                )
        return (
            data_list,
            {
                "name": self.name,
                "related_transform": self.related_transform,
                "param": {
                    "samplewise_feature_shifts_asinhspace": self.samplewise_feature_shifts_asinhspace,
                    "do_shift_in_rawspace": self.do_shift_in_rawspace,
                    "original_asinh_cofactors": self.original_asinh_cofactors,
                    "original_asinh_cofactors_applied": self.original_asinh_cofactors_applied,
                    "new_asinh_cofactors": self.new_asinh_cofactors,
                    # "inplace": self.inplace,
                    # "dataset_attribute": self.dataset_attribute,
                },
            },
        )

    def __repr__(self):
        return standard_repr(self)
