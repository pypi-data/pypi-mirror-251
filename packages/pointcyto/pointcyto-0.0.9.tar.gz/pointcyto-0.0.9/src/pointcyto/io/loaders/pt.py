from typing import List, Tuple

import torch


def pt_reader(*args, **kwargs):
    read_data = torch.load(*args, **kwargs)
    return read_data[0], read_data[1]


def read_pt(path: str, *args, **kwargs) -> Tuple[torch.Tensor, List[str]]:
    """
    read_jay reads the jay file (saved by datatable usually)

    Returns:
         Tuple of point cloud data and the column names

    """
    values_torch, colnames_list = pt_reader(path, *args, **kwargs)
    return values_torch, colnames_list
