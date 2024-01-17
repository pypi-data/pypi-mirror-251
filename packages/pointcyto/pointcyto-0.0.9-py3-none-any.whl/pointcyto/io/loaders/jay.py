from typing import List, Tuple

import torch

try:
    import datatable

    def jay_reader(*args, **kwargs):
        read_data = datatable.fread(*args, **kwargs)
        return torch.tensor(read_data.to_numpy()), list(read_data.names)

except ImportError:
    # No fallback
    def jay_reader(*args, **kwargs):
        raise ImportError("Did not find datatable, cannot read jay files")


def read_jay(path: str, *args, **kwargs) -> Tuple[torch.Tensor, List[str]]:
    """
    read_jay reads the jay file (saved by datatable usually)

    Returns:
         Tuple of point cloud data and the column names

    """
    values_torch, colnames_list = jay_reader(path, *args, **kwargs)
    return values_torch, colnames_list
