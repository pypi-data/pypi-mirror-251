# These transformations follow the nomenclature from flowCore
# https://bioconductor.org/packages/devel/bioc/vignettes/flowCore/inst/doc/HowTo-flowCore.pdf
# Section 6.1 "Standard transformations
from typing import List

from torch_geometric.data.dataset import Dataset

from pointcyto.transforms.transforms import functional_transform_adapter
from pointcyto.transforms.transforms_functional import arcsinh_param
from pointcyto.transforms.utils import standard_repr


class TransformFunctional(object):
    def __init__(
        self, original_featurenames: List[str] = None, dataset_attribute: str = "pos"
    ):
        self.attr = dataset_attribute
        self.orig_featurenames = original_featurenames

    def __call__(self, data: Dataset):
        # setattr(data, self.attr,
        #         functional_transform_adapter(
        #             # these parameters must always be present for functional_transform_adapter()
        #             data, <the_function>, self.attr,
        #             # These are the actual arguments to the function
        #             self.feature_indices, self.inplace))
        # return data
        raise NotImplementedError


class TransformFunctionalListadapter(object):
    def __init__(
        self, original_featurenames: List[str] = None, dataset_attribute: str = "pos"
    ):
        self.attr = dataset_attribute
        self.orig_featurenames = original_featurenames

    def __call__(self, data_list: List[Dataset]):
        # for sample in data_list:
        #     setattr(sample, self.attr,
        #             functional_transform_adapter(
        #                 # these parameters must always be present for functional_transform_adapter()
        #                 data, <the_function>, self.attr,
        #                 # These are the actual arguments to the function
        #                 self.feature_indices, self.inplace))
        # return data_list, {'return_parameter1': self.mean, 'return_parameter2': self.std}
        raise NotImplementedError


class ArcsinhTransform(TransformFunctional):
    def __init__(
        self,
        original_featurenames: List[str] = None,
        dataset_attribute: str = "pos",
        a: float = 1,
        b: float = 1,
        c: float = 0,
    ):
        super(ArcsinhTransform, self).__init__(
            original_featurenames=original_featurenames,
            dataset_attribute=dataset_attribute,
        )
        self.a = a
        self.b = b
        self.c = c

    def __call__(self, data: Dataset):
        setattr(
            data,
            self.attr,
            functional_transform_adapter(
                # these parameters must always be present for functional_transform_adapter()
                data,
                arcsinh_param,
                self.attr,
                # These are the actual arguments to the function
                a=self.a,
                b=self.b,
                c=self.c,
            ),
        )
        return data

    def __repr__(self):
        return standard_repr(self)


class ArcsinhTransformList(ArcsinhTransform):
    def __call__(self, data_list: List[Dataset]):
        for sample in data_list:
            setattr(
                sample,
                self.attr,
                functional_transform_adapter(
                    # these parameters must always be present for functional_transform_adapter()
                    sample,
                    arcsinh_param,
                    self.attr,
                    # These are the actual arguments to the function
                    a=self.a,
                    b=self.b,
                    c=self.c,
                ),
            )
        return data_list, {}
