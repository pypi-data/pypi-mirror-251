from typing import Any, List

import torch
from torch_geometric.data import Data


def convert_class_id_names(
    classes_id_or_name: List[str],
    class_name_to_id: dict,
    out: str = "name",
    allow_missings: bool = False,
) -> List[Any]:
    """
    Convert from class names/ids to either name or id. Used in MetaData.

    Args:
        classes_id_or_name:
            A list of either class_ids or class_names.
        class_name_to_id:
            dictionary with class_names as keys and class_ids as values
        out:
            Either "name" or "id", then the return values are either the name or the id. Fallback is "id"
        allow_missings:
            If true, missing lookup values in class_name_to_id are allowed and the result will either contain
            "__NotFound__"  (out="name") or -1 (out="id")

    Returns:

        ``out='name'``:

            List[str]

        ``out='id'``:

            List[int]



    """
    names = list(class_name_to_id.keys())
    ids = list(class_name_to_id.values())
    if out == "name":
        converted = ["__NotFound__"] * len(classes_id_or_name)
        search_in = ids
        search_for = names
    else:
        converted = [-1] * len(classes_id_or_name)
        search_in = names
        search_for = ids
    for index, val in enumerate(classes_id_or_name):
        try:
            converted[index] = search_for[search_in.index(val)]
        except ValueError as err:
            if allow_missings:
                pass
            else:
                raise ValueError("Did you already insert " + out + "?") from err
    return converted


def parse_matrix_class(point_position_matrix: torch.Tensor, class_id: int):
    """

    Args:
        point_position_matrix:
            A torch tensor beeing the data matrix for one sample
        class_id:
            The class_id for that sample

    Returns:
        A :class:`torch_geometric.data.Data` object.

    Todo:
        For non-neighbor approaches, the edge_index is probably not necessary at all and just costs space.
    """
    point_position_matrix = point_position_matrix.to(torch.float)
    # class_id = torch.empty(point_position_matrix.shape[0], 1).fill_(class_id)
    torch_geom_data = Data(pos=point_position_matrix, y=class_id)

    # # Add an empty but self-connected adjacency matrix.
    # # Each point must point to itself.
    # torch_geom_data.edge_index, unnecessary_edge_weight = add_self_loops(
    #     edge_index=torch.empty((2, 0), dtype=torch.long),
    #     num_nodes=torch_geom_data.pos.shape[0])
    # Replaced this by just an completely empty adjacency matrix and generate the self loops always on the fly
    # to save space
    torch_geom_data.edge_index = torch.empty((2, 0), dtype=torch.long)
    return torch_geom_data
