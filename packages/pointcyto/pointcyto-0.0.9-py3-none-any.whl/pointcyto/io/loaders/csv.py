from typing import List, Tuple

import pandas as pd
import torch

try:
    import datatable

    def csv_reader(*args, **kwargs):
        read_data = datatable.fread(*args, **kwargs)
        return torch.tensor(read_data.to_numpy()), list(read_data.names)

except ImportError:
    # fallback to pandas
    def csv_reader(*args, **kwargs):
        read_data = pd.read_csv(*args, **kwargs)
        return torch.tensor(read_data.values), [x.strip() for x in read_data.columns]


def read_csv(
    path: str, sep: str = ",", *args, **kwargs
) -> Tuple[torch.Tensor, List[str]]:
    """
    read_csv reads the csv
    - first line are assumed to be feature names.
    - All further lines must be numeric

    Returns:
         Tuple of point cloud data and the column names

    """
    values_torch, colnames_list = csv_reader(path, *args, sep=sep, **kwargs)
    return values_torch, colnames_list
