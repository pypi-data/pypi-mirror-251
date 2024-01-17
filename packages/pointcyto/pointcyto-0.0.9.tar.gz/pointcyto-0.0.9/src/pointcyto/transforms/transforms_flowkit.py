import inspect
from typing import List, Union

import flowkit as fk
import torch
from torch_geometric.data.dataset import Dataset


class FKtransform(object):
    """
    FKtransform is a class to access the transformations supplied by flowkit.

    I explain the parameters for all possible (2020-05-15) transformations from flowkit here also using information
    from Section 6.1 https://bioconductor.org/packages/devel/bioc/vignettes/flowCore/inst/doc/HowTo-flowCore.pdf
    Logicle and Hyperlog cannot be represented in closed form, so they are defined in terms of their inverse functions.
    https://www.bioconductor.org/packages/release/bioc/vignettes/flowCore/inst/doc/hyperlog.notice.html

    LinearTransform[t, a]

    .. math:`f(x) = \\frac{x + a}{b + a}`

    LogTransform[t, m]:

    .. math::

        f(x) = \\frac{1}{m} \\cdot \\log_{10}(x / t) +1

    HyperlogTransform[t, w, m, a]:
    (from https://github.com/whitews/FlowUtils/blob/master/flowutils/logicle_c_ext/logicle.c)

    .. math::

        f^{-1}(x) =


    LogicleTransform[t, w, m, a]:
    (from https://github.com/whitews/FlowUtils/blob/master/flowutils/logicle_c_ext/logicle.c)

    .. math::

        f^{-1}(x) =

    AsinhTransform[t, m, a]:

    .. math::

        f(x) =

        f^{-1}(x) =



    """

    def __init__(
        self,
        flowkit_transform_classname: str,
        feature_indices: Union[List[int], slice, int] = None,
        dataset_attribute: str = "pos",
        **kwargs
    ):
        # find all possible transforms from flowkit
        if flowkit_transform_classname not in fk.transforms.__all__:
            raise ValueError(
                flowkit_transform_classname + " does not exist in flowkit.transforms"
            )
        if flowkit_transform_classname == "RatioTransform":
            raise ValueError(
                "RatioTransform is special and not implemented because "
                + "it accesses pnn_labels from flowkit's sample class"
            )
        all_fk_transforms = {
            x[0]: x[1] for x in inspect.getmembers(fk.transforms, inspect.isclass)
        }
        # instantiate the chosen (flowkit_transform_classname) class with named arguments
        self.transform_class = all_fk_transforms[flowkit_transform_classname](
            transform_id=flowkit_transform_classname, **kwargs
        )

        self.attr = dataset_attribute
        self.feature_indices = feature_indices

    def __call__(self, data: Dataset):
        myattr = getattr(data, self.attr)
        if self.feature_indices is None:
            self.feature_indices = [*range(myattr.shape[1])]
        try:
            myattr[:, self.feature_indices] = self.transform_class.apply(
                myattr[:, self.feature_indices]
            )
        except AttributeError:
            #   File "/home/gugl/.conda_envs/ccc_optuna_III/lib/python3.8/site-packages/flowutils/transforms.py",
            #   line 231, in asinh
            #     data_copy = data.copy()
            # AttributeError: 'Tensor' object has no attribute 'copy'
            tmp = self.transform_class.apply(myattr[:, self.feature_indices].numpy())
            myattr[:, self.feature_indices] = torch.tensor(tmp)
        setattr(data, self.attr, myattr)
        return data
