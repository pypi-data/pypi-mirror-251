import re
from typing import List, Union

import numpy as np
import torch
from torch_geometric.data.dataset import Dataset

from pointcyto.transforms.utils import standard_repr


def global_mean(pointclouds: Dataset, dataset_attribute: str = "pos") -> torch.Tensor:
    """
    Calculate the mean over all points in all samples of pointclouds

    Args:
        pointclouds:
            A torch_geometric.data.dataset.
        dataset_attribute:
            The attribute of Dataset where the mean will be taken

    Returns:
        A torch.tensor holding the calculated means over all samples per feature

    """
    means = torch.stack(
        [getattr(sample, dataset_attribute).mean(dim=0) for sample in pointclouds]
    )
    overall_mean = means.mean(dim=0)
    return overall_mean


def global_var(
    pointclouds: Dataset,
    dataset_attribute: str = "pos",
    global_means: torch.Tensor = None,
) -> torch.Tensor:
    """
    Calculate the variance over all points in all samples of pointclouds

    Args:
        pointclouds:
            A torch_geometric.data.dataset.
        dataset_attribute:
            The attribute of Dataset where the variance will be calculated
        global_means:
            If the global mean was calculated before, the result of it can be given to global_var

    Returns:
        A torch.tensor holding the calculated variance over all samples per feature

    """
    if global_means is not None:
        mean_overall = global_means
    else:
        mean_overall = global_mean(pointclouds, dataset_attribute)
    x_minus_global_mean = torch.cat(
        [getattr(sample, dataset_attribute) - mean_overall for sample in pointclouds]
    )
    x_minus_g_squared = x_minus_global_mean**2
    summed_squares = x_minus_g_squared.sum(dim=0)
    return summed_squares / x_minus_global_mean.shape[0]


def global_sd(
    pointclouds: Dataset,
    dataset_attribute: str = "pos",
    global_means: torch.Tensor = None,
) -> torch.Tensor:
    """
    Calculate the standard deviation over all points in all samples of pointclouds

    Args:
        pointclouds:
            A torch_geometric.data.dataset.
        dataset_attribute:
            The attribute of Dataset where the standard deviation will be taken
        global_means:
            If the global mean was calculated before, the result of it can be given to global_var

    Returns:
        A torch.tensor holding the calculated standard deviation over all samples per feature

    """
    return global_var(pointclouds, dataset_attribute, global_means).sqrt()


def functional_transform_adapter(
    data: Dataset, transform, dataset_attribute: str = "pos", *args, **kwargs
) -> Dataset:
    """
    To be able to use existing transforms on the :class:`torch_geometric.data.dataset.Dataset` I need this adapter.
    You have to defined the data, the transform and on which attribute of the given dataset the transform should be
    applied. *args and **kwargs go into the transform.

    Args:
        data:
            The :class:`torch_geometric.data.dataset.Dataset` where you want to apply the transform on.
        transform:
            The transform you want to apply.
        dataset_attribute:
            The attribute of :class:`torch_geometric.data.dataset.Dataset` where you want to apply the transform on.
        *args and **kwargs:
            Further arguments for ``transform``

    Returns:
        The transformed dataset_attribute of :class:`torch_geometric.data.dataset.Dataset` (not a dataset anymore!).

    """
    return transform(getattr(data, dataset_attribute), *args, **kwargs)


class NormalizePointCloud(object):
    def __init__(
        self, mean, std, inplace: bool = False, dataset_attribute: str = "pos"
    ):
        """

        Args:
            mean:
                1D-Tensor with the means for each column.
                The i-th value is subtracted from all values of the i-th column of the matrix given by
                dataset_attribute.
            std:
                 1D-Tensor with the standard deviations for each column.
                The i-th value is subtracted from all values of the i-th column of the matrix given by
                dataset_attribute.
            inplace:
                Calculation in place or clone the tensor first?
            dataset_attribute:
                Data from pytorch-geometric has multiple data matrices where you can work on. Default for us: "pos"
        """
        self.mean = mean
        self.std = std
        self.inplace = inplace
        self.attr = dataset_attribute

    def __call__(self, data: Dataset) -> Dataset:
        """
        Normalizes the ``dataset_attribute`` from the given dataset.
        ((x - mean(x)) / sd(x)) per feature using ``self.mean`` and ``self.std`` over all samples.
        """
        setattr(
            data,
            self.attr,
            functional_transform_adapter(
                data, normalize, self.attr, self.mean, self.std, self.inplace
            ),
        )
        return data

    def __repr__(self):
        return standard_repr(self)


def normalize(tensor, mean, std, inplace=False) -> torch.Tensor:
    """Normalize a tensor with mean and standard deviation.

    .. note::
        This transform acts out of place by default, i.e., it does not mutates the input tensor.

    See :class:`~torchvision.transforms.Normalize` for more details.

    Args:
        tensor (Tensor):
            Tensor image of size (C, H, W) to be normalized.
        mean (sequence):
            Sequence of means for each channel.
        std (sequence):
            Sequence of standard deviations for each channel.
        inplace(bool,optional):
            Bool to make this operation inplace.

    Returns:
        Tensor: Normalized Tensor image.
    """

    if not inplace:
        tensor = tensor.clone()

    dtype = tensor.dtype
    mean = torch.as_tensor(mean, dtype=dtype, device=tensor.device)
    std = torch.as_tensor(std, dtype=dtype, device=tensor.device)
    tensor.sub_(mean).div_(std)
    return tensor


class SelectFeaturesPointCloud(object):
    def __init__(
        self,
        features: Union[List[int], slice, int],
        original_featurenames: List[str] = None,
        inplace: bool = False,
        dataset_attribute: str = "pos",
    ):
        """
        Restrict the data.dataset_attribute to the specified features.

        Args:
            features:
                The features which should be present *after* the selection. Define via integers, List[int] or a slice.
            original_featurenames:
                All features **before** restriction. If given, ``self.featurenames`` holds the restricted featurenames
                (which are based on index) already after initialization of the class, not only after calling it.
            inplace:
                Inplace or not.
            dataset_attribute:
                Which attribute should this function be applied to.

        """
        self.attr = dataset_attribute
        self.inplace = inplace
        self.orig_featurenames = original_featurenames
        self.feature_indices = features
        if self.orig_featurenames is not None:
            self.featurenames = [
                self.orig_featurenames[i] for i in self.feature_indices
            ]
        else:
            self.featurenames = None

    def __call__(self, data: Dataset) -> Dataset:
        setattr(
            data,
            self.attr,
            functional_transform_adapter(
                data, select_features, self.attr, self.feature_indices, self.inplace
            ),
        )
        return data


def select_features(tensor, col_indices, inplace=False):
    """
    Select certain columns of a 2d tensor

    .. note::
        This transform acts out of place by default, i.e., it does not mutates the input tensor.

    Args:
        tensor (Tensor): Tensor image of size (H, W) where col_indices from W are selected
        col_indices (index): Indices of the columns to retain
        inplace(bool,optional): Bool to make this operation inplace.

    Returns:
        Tensor: Normalized Tensor image.
    """
    if len(tensor.shape) != 2:
        raise ValueError("tensor.shape should have len 2")
    if not inplace:
        tensor = tensor.clone()
    return tensor[:, col_indices]


# Heavily based on
# https://pytorch-geometric.readthedocs.io/en/latest/_modules/torch_geometric/transforms/fixed_points.html#FixedPoints
class WeightedFixedPoints(object):
    r"""
    Samples a fixed number of :obj:`num` points and features from a point
    cloud where each point receives a weight to be sampled.

    Args:
        num (int):
            The number of points to sample.
        n_reference:
            The number of points which are sampled randomly.
            Those num_selection points are used as base.
            Outlierness-score is calculated relative to this random selection.
        data_selection:
            The torch_geometric.data.data.Data attribute which should be used for outlierness-calculation

        replace (bool, optional):
            Sample with (True) or without (False) replacement
    """

    def __init__(
        self,
        num: int,
        n_reference: int,
        replace: bool = True,
        data_selection: str = "pos",
        percentage_outlierness_points: float = 0.5,
    ):
        self.num = num
        self.num_selection = n_reference
        self.data_selection = data_selection
        self.percentage_outlierness_points = percentage_outlierness_points
        self.replace = replace

    def __call__(self, data):
        num_nodes = data.num_nodes

        # Get the random points
        if self.num_selection > num_nodes:
            current_num_selection = num_nodes
        else:
            current_num_selection = self.num_selection
        random_point_choice = np.random.choice(
            a=num_nodes, size=current_num_selection, replace=False
        )
        random_points = getattr(data, self.data_selection)[
            random_point_choice, :
        ].cuda()

        # Calculate outlierness-score
        distance_randompoints_to_allpoints: torch.Tensor = torch.cdist(
            random_points, getattr(data, self.data_selection).cuda()
        )
        outlierness_score = distance_randompoints_to_allpoints.min(dim=0)[
            0
        ]  # ['values']
        outlierness_score = outlierness_score.cpu().numpy()
        outlierness_probabilites = outlierness_score / outlierness_score.sum()

        # Sample indices randomly (with/without replacement) with weights from all points
        # Higher outlierness-score means higher probability to be chosen.
        n_outlierness_points = int(self.num * self.percentage_outlierness_points)
        n_random_points = self.num - n_outlierness_points

        choice_outlierness = np.random.choice(
            a=num_nodes,
            size=n_outlierness_points,
            p=outlierness_probabilites,
            replace=self.replace,
        )
        choice_random = np.random.choice(
            a=num_nodes, size=n_random_points, replace=self.replace
        )
        choice = np.concatenate([choice_outlierness, choice_random])

        # Actually sample the data.
        for key, item in data:
            if bool(re.search("edge", key)):
                continue
            if torch.is_tensor(item) and item.size(0) == num_nodes and num_nodes != 1:
                data[key] = item[choice]

        return data

    def __repr__(self):
        return standard_repr(self)


class CalculateOutlierness(object):
    def __init__(
        self,
        n_reference: int,
        from_attribute: str = "pos",
        new_attribute: str = "outlierness",
        use_cuda: bool = True,
        calculate_in_batches: int = None,
    ):
        self.from_attr = from_attribute
        self.new_attr = new_attribute
        self.n_reference = n_reference
        self.use_cuda = use_cuda
        self.calculate_in_batches = calculate_in_batches

    def __call__(self, data: Dataset):
        """
        Args:

        Returns:
            Tensor: Normalized Tensor image.
        """
        setattr(
            data,
            self.new_attr,
            functional_transform_adapter(
                data,
                calculate_outlierness,
                self.from_attr,
                self.n_reference,
                self.use_cuda,
                self.calculate_in_batches,
            ),
        )
        return data

    def __repr__(self):
        return standard_repr(self)


def calculate_outlierness(
    tensor: torch.Tensor,
    n_reference: int,
    use_cuda: bool = True,
    cdist_max_points: int = None,
) -> torch.Tensor:
    # Get the random points
    if n_reference > tensor.shape[0]:
        current_num_selection = tensor.shape[0]
    else:
        current_num_selection = n_reference
    random_point_choice = np.random.choice(
        a=tensor.shape[0], size=current_num_selection, replace=False
    )
    random_points = tensor[random_point_choice, :]
    if use_cuda:
        random_points = random_points.cuda()

    # Calculate outlierness-score
    if cdist_max_points is not None and cdist_max_points > 1:
        num_batches = tensor.shape[0] // cdist_max_points
        outlierness_score = torch.tensor([], dtype=torch.float)
        if use_cuda:
            outlierness_score = outlierness_score.cuda()
        for batch_i in range(
            1, num_batches + 1 + (tensor.shape[0] % cdist_max_points != 0)
        ):
            end = batch_i * cdist_max_points
            if end > tensor.shape[0]:
                end = tensor.shape[0]
            batch_slice = slice((batch_i - 1) * cdist_max_points, end)
            part_tensor = tensor[batch_slice, :]
            if use_cuda:
                part_tensor = part_tensor.cuda()
            distance_randompoints_to_part_tensor: torch.Tensor = torch.cdist(
                random_points, part_tensor
            )
            part_outlierness_score = distance_randompoints_to_part_tensor.min(dim=0)[
                0
            ]  # ['values']
            outlierness_score = torch.cat([outlierness_score, part_outlierness_score])
    else:
        if use_cuda:
            tensor = tensor.cuda()
        distance_randompoints_to_allpoints: torch.Tensor = torch.cdist(
            random_points, tensor
        )
        outlierness_score = distance_randompoints_to_allpoints.min(dim=0)[
            0
        ]  # ['values']

    # If I had to set cdist_max_points, I most probable also have to convert the gpu-vector to cpu because of
    # GPU overflow.
    # This seems to take longer but better than not working at all.
    if cdist_max_points is not None:
        return outlierness_score.cpu()
    else:
        return outlierness_score


class FixedPointsOutlierness(object):
    r"""Samples a fixed number of :obj:`num` points and features from a point
    cloud where the Data has an 'outlierness' attribute which accounts for the outlierness of each point.

    Args:
        num (int):
            The number of points to sample.
        outlierness_attribute:
            The torch_geometric.data.data.Data attribute which should be used as outlierness-score
        replace (bool, optional):
            Sample with (True) or without (False) replacement
        percentage_outlierness_points:
            Percentage of points which are sampled according to outlierness-score probabilities.
        outlierness_exponent:
            You might want to weight distribute your outlierness score more.
            So just take all values to some exponent > 1 before calculating the probabilities.
            The other way around if your outlierness_exponent is < 1.
            Extreme cases:
                0   -> all points randomly sampled
                Inf -> Only the point with maximum outlierness score is sampled.
        allow_duplicates (bool, optional): In case :obj:`replace` is
            :obj`False` and :obj:`num` is greater than the number of points,
            this option determines whether to add duplicated nodes to the
            output points or not.
            In case :obj:`allow_duplicates` is :obj:`False`, the number of
            output points might be smaller than :obj:`num`.
            In case :obj:`allow_duplicates` is :obj:`True`, the number of
            duplicated points are kept to a minimum. (default: :obj:`False`)
    """

    def __init__(
        self,
        num: int,
        outlierness_attribute: str = "outlierness",
        replace: bool = True,
        percentage_outlierness_points: float = 0.5,
        outlierness_exponent: float = 1.5,
        allow_duplicates: bool = False,
    ):
        self.num = num
        self.outlierness_attribute = outlierness_attribute
        self.percentage_outlierness_points = percentage_outlierness_points
        self.outlierness_exponent = outlierness_exponent
        self.replace = replace
        self.allow_duplicates = allow_duplicates

    def __call__(self, data):
        num_nodes = data.num_nodes
        if self.num > num_nodes and not self.replace:
            if not self.allow_duplicates:
                raise ValueError(
                    "There are less points than defined to sample "
                    + "in num. Also allow_duplicates was set to false"
                )
            else:
                choice_shuffled = np.random.choice(
                    a=num_nodes, size=num_nodes, replace=False
                )
                choice_duplicates = np.random.choice(
                    a=num_nodes, size=self.num - num_nodes, replace=True
                )
                choice = np.concatenate([choice_shuffled, choice_duplicates])
        else:
            # Calculate outlierness-probabilities
            outlierness_score = data[self.outlierness_attribute].cpu().numpy()
            exponented = outlierness_score**self.outlierness_exponent
            outlierness_probabilites = exponented / exponented.sum()

            # Sample indices randomly (with/without replacement) with weights from all points
            # Higher outlierness-score means higher probability to be chosen.
            # print(
            #     self.num,
            #     self.percentage_outlierness_points,
            #     self.num * self.percentage_outlierness_points,
            #     int(self.num * self.percentage_outlierness_points),
            # )
            n_outlierness_points = int(self.num * self.percentage_outlierness_points)
            n_random_points = self.num - n_outlierness_points

            choice_outlierness = np.random.choice(
                a=num_nodes,
                size=n_outlierness_points,
                p=outlierness_probabilites,
                replace=self.replace,
            )
            choice_random = np.random.choice(
                a=num_nodes, size=n_random_points, replace=self.replace
            )
            choice = np.concatenate([choice_outlierness, choice_random])

        # Actually sample the data.
        for key, item in data:
            if bool(re.search("edge", key)):
                continue
            if torch.is_tensor(item) and item.size(0) == num_nodes and num_nodes != 1:
                data[key] = item[choice]

        return data

    def __repr__(self):
        return standard_repr(self)


class QminmaxPointCloud(object):
    def __init__(
        self,
        quantile_range=[0.01, 0.99],
        inplace: bool = False,
        dataset_attribute: str = "pos",
    ):
        """

        Args:
            quantile_range (sequence):
                Two quantiles reflecting the upper and lower quantile to be used as min and max replacements.
            inplace:
                Calculation in place or clone the tensor first?
            dataset_attribute:
                Data from pytorch-geometric has multiple data matrices where you can work on. Default for us: "pos"
        """
        self.quantile_range = quantile_range
        self.inplace = inplace
        self.attr = dataset_attribute

    def __call__(self, data: Dataset) -> Dataset:
        """
        Normalizes the ``dataset_attribute`` from the given dataset.
        ((x - upper_quantile(x)) / (upper_quantile(x) - lower_quantile(x))) per feature
        """
        setattr(
            data,
            self.attr,
            functional_transform_adapter(
                data, qminmax, self.attr, self.quantile_range, self.inplace
            ),
        )
        return data

    def __repr__(self):
        return standard_repr(self)


def qminmax(tensor: torch.Tensor, quantile_range, inplace=False) -> torch.Tensor:
    """
    minmax rescaling a tensor per column,
    (https://en.wikipedia.org/wiki/Feature_scaling#Rescaling_(min-max_normalization))
    but instead of using min and max use min := lower_quantile and max := upper_quantile from quantile_range

    .. note::
        This transform acts out of place by default, i.e., it does not mutates the input tensor.

    See :class:`~torchvision.transforms.Normalize` for more details.

    Args:
        tensor (Tensor):
            Tensor image of size (C, H, W) to be normalized.
        quantile_range (sequence):
            Two quantiles reflecting the upper and lower quantile to be used as min and max replacements.
        inplace(bool,optional):
            Bool to make this operation inplace.

    Returns:
        Tensor: Normalized Tensor image.
    """

    if not inplace:
        tensor = tensor.clone()

    dtype = tensor.dtype
    quantile_range = torch.as_tensor(quantile_range, dtype=dtype, device=tensor.device)
    upper_quantile = tensor.quantile(q=torch.max(quantile_range), dim=0, keepdim=True)
    lower_quantile = tensor.quantile(q=torch.min(quantile_range), dim=0, keepdim=True)
    return (tensor - lower_quantile) / (upper_quantile - lower_quantile)
