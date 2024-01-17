from typing import Any, Dict

from pointcyto.io.loaders.csv import read_csv
from pointcyto.io.loaders.fcs import read_fcs
from pointcyto.io.loaders.feather import read_feather
from pointcyto.io.loaders.jay import read_jay
from pointcyto.io.loaders.pt import read_pt
from pointcyto.io.utils import parse_matrix_class

POINTCLOUD_EXTENSIONS = [".fcs", ".csv", ".jay", ".pt", ".feather"]


def parse_by_ext(path: str, y: int = 0, *args, **kwargs) -> Dict[str, Any]:
    """
    Parse (=make a torch_geometric.data.Data object) file at <path> based on its extension.

    Args:
        path:
            Path to file
        y:
            What is the class response? Necessary for parse_matrix_class. Could also be left empty and set afterwards.
        *args:
        **kwargs:

    Returns:
        A Dict:
        ``point_data``:

            The torch_geometric.data.Data object

        ``features``:

            The feature names of the file
    """
    lowpath = path.lower()
    if lowpath.endswith(".jay"):
        point_set, col_names = read_jay(path, *args, **kwargs)
    elif lowpath.endswith(".pt"):
        point_set, col_names = read_pt(path, *args, **kwargs)
    elif lowpath.endswith(".csv"):
        point_set, col_names = read_csv(
            path, *args, **kwargs
        )  # further arguments go inside pandas.read_csv
    elif lowpath.endswith(".fcs"):
        point_set, col_names = read_fcs(path)
    elif lowpath.endswith(".feather"):
        point_set, col_names = read_feather(path, *args, **kwargs)
    else:
        raise NotImplementedError(
            "I can only handle the following extensions: "
            + ", ".join(POINTCLOUD_EXTENSIONS)
            + "\nYou gave the following file: "
            + lowpath
        )

    point_data = parse_matrix_class(point_set, y)
    return {"point_data": point_data, "features": col_names}
