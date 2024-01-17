import torch

# See also https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3243046/


def arcsinh(x: torch.Tensor) -> torch.Tensor:
    return torch.asinh(x)


def arcsinh_param(x: torch.Tensor, a, b, c) -> torch.Tensor:
    """

    Args:
        x: Data (torch.Tensor)
        a: positive float, shifting about 0 inside arcsinh
        b: positive float, scale factor
        c: float, shifting the arcsinh result

    Returns:
        ..math::
            f(x, a, b, c) = arcsinh(a + bx) + c
    """
    return arcsinh(a + b * x) + c


def scale_low_high_01(tensor, low_high=None, inplace=False):
    if not inplace:
        tensor = tensor.clone()

    dtype = tensor.dtype
    if len(low_high) == 1:
        # generate the low_high_tensor for all features (=columns)
        low_high = low_high * tensor.shape[1]
    # With the following line I ensure that there are _always_ low AND high values.
    # If there is only one value (len(x) == 1), then
    #   low -> x
    #   high -> low + 1
    # which results in
    #   (tensor - low) / (high - low) =
    #   (tensor - low) / (low + 1 - low) =
    #   (tensor - low) / (1) = tensor - low

    low_high_lowhigh = [[x[0], x[0] + 1] if len(x) == 1 else x for x in low_high]
    if not all([len(x) == 2 for x in low_high_lowhigh]):
        raise ValueError("There are not always exactly 2 values, one low and one high.")
    low_high_tensor = torch.as_tensor(
        low_high_lowhigh, dtype=dtype, device=tensor.device
    )
    if len(low_high_tensor) != tensor.shape[1]:
        raise ValueError(
            "Neither only one, nor a matching number of low_high "
            + f"scalings{len(low_high_tensor)} to the number of features.{tensor.shape[1]}"
        )

    # See QminmaxPointCloud for the transpose
    low_high_tensor = low_high_tensor.t()
    return (tensor - low_high_tensor[0, :]) / (
        low_high_tensor[1, :] - low_high_tensor[0, :]
    )


def scale_featurewise(tensor, feature_scaling_vector=None, inplace=False):
    """
    Divide the tensor per column by the corresponding value in feature_scaling_vector
    """
    if not inplace:
        tensor = tensor.clone()

    dtype = tensor.dtype
    if len(feature_scaling_vector) == 1:
        # generate the low_high_tensor for all features (=columns)
        feature_scaling_vector = feature_scaling_vector * tensor.shape[1]
    feature_scaling_vector_tensor = torch.as_tensor(
        feature_scaling_vector, dtype=dtype, device=tensor.device
    )
    if len(feature_scaling_vector_tensor) != tensor.shape[1]:
        raise ValueError(
            "Neither only one, nor a matching number of scalings "
            + f"{len(feature_scaling_vector_tensor)} to the number of features.{tensor.shape[1]}"
        )
    tensor.div_(feature_scaling_vector_tensor)
    return tensor
