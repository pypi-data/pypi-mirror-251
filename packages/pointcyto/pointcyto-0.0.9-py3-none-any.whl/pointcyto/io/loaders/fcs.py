from typing import List, Tuple

import flowkit
import torch


def read_fcs(path: str) -> Tuple[torch.Tensor, List[str]]:
    """
    read_fcs extracts the original events *without* applying compensation, transformation or anything else.
    If you want to have compensated values, you must do this beforehand,
    - store it into '_orig_events'
    - export it into the new .fcs

    Example:

        .. code-block::

            import flowkit

            orig = flowkit.Sample('removeme_original.fcs')
            a = orig.get_orig_events()
            a[:, :] = 0  # compensate here whatever you want
            orig._orig_events = a
            orig.export("removeme_zeroed_by_python.fcs")



    Args:
        path:
            Path to csv file. Must contain a head line
    Returns:
        Tuple of point cloud data and the column names
    :param path:

    Examples:

    .. code-block::

        print(read_fcs("data/Tcell/P0H.fcs"))

    """
    fk_sample = flowkit.Sample(path, cache_original_events=True)

    labels_pns = fk_sample.pns_labels
    labels_pnn = fk_sample.pnn_labels

    combined_labels = [
        value + "_" + labels_pnn[index] for index, value in enumerate(labels_pns)
    ]
    combined_labels_no_spaces = [
        namex.strip().replace(" ", "_") for namex in combined_labels
    ]
    return torch.from_numpy(fk_sample._orig_events), combined_labels_no_spaces
