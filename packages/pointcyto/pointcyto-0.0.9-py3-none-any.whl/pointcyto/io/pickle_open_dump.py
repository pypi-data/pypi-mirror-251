import pickle


def pickle_open_dump(obj, path: str, verbose: bool = True) -> None:
    """

    Args:
        obj:
            The object to pickle
        path:
            Where the pickle should be saved
        verbose:
            If verbose the output path is printed.

    Returns:

    """
    with open(path, "wb") as f:
        pickle.dump(obj, f)
    if verbose:
        print("Saved: " + path)
