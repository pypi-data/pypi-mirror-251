from typing import List, Tuple

import torch

try:
    # https://arrow.apache.org/docs/python/generated/pyarrow.feather.read_feather.html
    import pyarrow.feather as feather

    def feather_reader(*args, **kwargs):
        read_data = feather.read_feather(*args, **kwargs)
        return torch.tensor(read_data.to_numpy()), list(read_data.columns)

    # Alternatively could use pandas, but pandas just calls pyarrow.
    # # https://pandas.pydata.org/docs/reference/api/pandas.read_feather.html
    # import pandas as pd
    # # Pandas fallback.
    # # 2023-03-13: I am not sure if pandas or pyarrow is better, but if pyarrow is installed it is
    # # used.
    # def feather_reader(*args, **kwargs):
    #     read_data = pd.read_feather(*args, **kwargs)
    #     return torch.tensor(read_data.to_numpy()), list(read_data.columns)

except ImportError:
    # No fallback
    def feather_reader(*args, **kwargs):
        raise ImportError("Did not find pyarrow, cannot read feather files")


def read_feather(path: str, *args, **kwargs) -> Tuple[torch.Tensor, List[str]]:
    """
    read_feather reads the feather file
    - first line are assumed to be feature names.
    - All further lines must be numeric

    Returns:
         Tuple of point cloud data and the column names

    """
    values_torch, colnames_list = feather_reader(path, *args, **kwargs)
    return values_torch, colnames_list
