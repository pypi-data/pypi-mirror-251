import os


def stitch_path(path_or_list, relative_path: str = None) -> str:
    """
    Stitch a list of strings to a path.

    Args:
        path_or_list:
            Either a direct path or a list where all elements are stitched together to a path
        relative_path:
            If given, this path gets in the beginning of the stitched path.

    Returns:
        A string with the combined (relative_path/path_or_list_stitched)
    """
    stitched_path = (
        os.path.join(*list(path_or_list))
        if not isinstance(path_or_list, str)
        else path_or_list
    )

    if not (relative_path is None):
        if not isinstance(relative_path, str):
            relative_path = os.path.join(*relative_path)

        stitched_path = os.path.join(relative_path, stitched_path)
    return stitched_path
