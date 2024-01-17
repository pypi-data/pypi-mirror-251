import torch


def randompointcloud(n_points: int = 4, n_features: int = 5):
    """
    Generate a random torch point cloud

    Args:
        n_points:
            Number of points
        n_features:
            Number of features

    Returns:
        a random torch point cloud with dimension (n_points, n_features)
    """
    return torch.rand((n_points, n_features))
