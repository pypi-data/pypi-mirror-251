import os

# from pathlib import Path, PurePath
import pathlib
import re
import sys
from typing import Dict, List, Tuple, Union

import pandas as pd

from pointcyto.data.metadata_base import MetaDataBase
from pointcyto.data.metadata_classification import MetaDataClassification
from pointcyto.io.utils import convert_class_id_names


# Taken from https://github.com/pytorch/vision/blob/master/torchvision/datasets/folder.py
def has_file_allowed_extension(filename: str, extensions: Tuple[str]) -> bool:
    """
    Checks if a file is an allowed extension.

    Args:
        filename (string):
            path to a file
        extensions (tuple of strings):
            extensions to consider (lowercase)

    Returns:
        bool: True if the filename ends with one of given extensions
    """
    return filename.lower().endswith(extensions)


def make_dataset(
    basedir,
    class_to_idx: dict,
    extensions: Tuple[str, ...] = (".csv", ".fcs"),
    is_valid_file=None,
) -> List[Tuple[str, int]]:
    """
    Traverse through all (direct) subfolders of basedir
    Each subfolder is the respective class for all files inside

    Args:
        basedir:
            The root directory which should be searched
        class_to_idx:
            Dictionary to enumerate the subfolders/classes. E.g. {classA: 0, classB: 1}
        extensions:
            File extensions which should be seen as valid, checked by has_file_allowed_extension
        is_valid_file:
            Alternatively give a function which says if the file is valid

    Returns:
         List of tuples with (filepath, classID)
    """
    samples_path_label = []

    if not ((extensions is None) ^ (is_valid_file is None)):
        raise ValueError(
            "Both extensions and is_valid_file cannot be None or not None at the same time"
        )
    if extensions is not None:

        def is_valid_file(file_x):
            return has_file_allowed_extension(file_x, extensions)

    # Traverse through all subfolders of self.raw_dir
    # Each subfolder is the respective class for all files inside
    for target in sorted(class_to_idx.keys()):
        tmp_dir = os.path.join(basedir, target)
        if not os.path.isdir(tmp_dir):
            continue
        for root, _, fnames in sorted(os.walk(tmp_dir, followlinks=True)):
            for fname in sorted(fnames):
                path = os.path.join(root, fname)
                if is_valid_file(path):
                    item = (path, class_to_idx[target])
                    samples_path_label.append(item)
    return samples_path_label


def find_classes(whichdir: str) -> Tuple[List[str], Dict[str, int]]:
    """
    Finds the class folders in whichdir. Not recursive.

    Args:
        whichdir:
            The starting directory where all directories are listed.

    Returns:
        tuple: (classes, class_to_idx) where classes are relative to (dir), and class_to_idx is a dictionary.

    Ensures:
        No class is a subdirectory of another.
    """
    if sys.version_info >= (3, 5):
        # Faster and available in Python 3.5 and above
        classes = [d.name for d in os.scandir(whichdir) if d.is_dir()]
    else:
        classes = [
            d for d in os.listdir(whichdir) if os.path.isdir(os.path.join(whichdir, d))
        ]
    classes.sort()
    class_to_idx = {classes[i]: i for i in range(len(classes))}
    return classes, class_to_idx


def gen_foldering_meta(
    orig_dir: str, root: str = None, **kwargs
) -> MetaDataClassification:
    """
    Generate a MetaData object based on "foldered" data. Looks as following:

    orig_dir/
        A/
            file1
            file2
            file3
        B/
            file4
            file5

    Then the MetaData object will be of length 5 and have two classes: "A" and "B".

    Args:
        orig_dir:
            Data containing the raw data in folders. Each direct sub-folder of this directory is regarded as unique
            class name.
        root:
            The root dir might differ from orig_dir. If given, MetaData processed/ directory is created inside this
            root. If not given, MetaData processed/ directory is created in "orig_dir/../processed"
        **kwargs:
            Further arguments to MetaData

    Returns:
        A MetaData object
    """
    classes_classtoidx = find_classes(orig_dir)
    fullpath_class_metadata = make_dataset(orig_dir, classes_classtoidx[1])
    #  len(orig_dir)+1 to get rid of the \
    relative_paths_class = [
        (path[len(orig_dir) + 1 :], class_id)
        for path, class_id in fullpath_class_metadata
    ]
    relative_paths = [path for path, class_id in relative_paths_class]
    class_ids = [class_id for path, class_id in relative_paths_class]
    class_names = convert_class_id_names(class_ids, classes_classtoidx[1], out="name")
    return MetaDataClassification(
        raw_filenames=relative_paths,
        orig_dir=orig_dir,
        class_name=class_names,
        root=root,
        **kwargs
    )


def list_files_recursive(dirpath, full_names: bool = False) -> List[str]:
    """
    List all files inside the dirpath recursively

    Args:
        dirpath:
            Starting point for recursion
        full_names:
            should full paths be returned?

    Returns:
        List of file paths.
    """
    full_paths = [
        os.path.join(dp, f) for dp, dn, filenames in os.walk(dirpath) for f in filenames
    ]
    if full_names:
        retval = full_paths
    else:
        retval = [filename[len(dirpath) + 1 :] for filename in full_paths]
    return retval


def gen_csv_meta(
    orig_dir: str,
    path_phenodata: str,
    regex_include: str = r".fcs$",
    read_csv_kwargs: dict = None,
    subject_name_col: Union[int, str] = 0,
    regex_sub_subject_name_col: Tuple[str, str] = None,
    restrict_to_present_pheno: bool = False,
    verbose: bool = False,
    metadata_type=MetaDataClassification,
    **kwargs
) -> MetaDataBase:
    """
    Generate a MetaData object based on data plus phenodata

    orig_dir/
        file1
        file2
        A/
            file3
            file4
        pheno_file.csv

    Where in pheno_file.csv there must be atleast 2 columns (but can be more):
        column1, column2, column3
        file1, 1, A
        file2, 2, B
        A/file3, 0, A
        A/file4, 0, A
    The first column always holds the path to the files.
    Second( or more) columns hold classes.

    Then the MetaData object will be of length 4 and have two possible "selection"s: column2 and column3.
    Selection column2 has 3 classes: 0, 1, 2
    Selection column3 has 2 classes: "A", "B"

    Args:
        orig_dir:
            The directory where all files (possibly in multiple subfolders) are located
        path_phenodata:
            path to phenodata. The phenodata file
                - must have the first column as paths to the files, relative to orig_dir
                - must have all found files in origdir in the first column
                - should have atleast 2 columns (including the filepath-column)
                - can have multiple columns
                - can have more rows than files, only the matched to filenames are selected
        read_csv_kwargs:
            Arguments given (**read_csv_kwargs) to pandas.read_csv
            (Used in examples/02_gen_MetaData/06_Putzel_meta.py)
        regex_include:
            Include only files to the metadata matching this regex. Default: r'.fcs' --> all .fcs or .FCS files
            Ignore case because , "re.IGNORECASE"
        subject_name_col:
            Default 0: The column of path_phenodata containing the filenames of the files to load.
            Can be numeric (column number) or string (exact column name)
        restrict_to_present_pheno:
            If True, only the files are included where phenodata[subject_name_col] is present.
        **kwargs:
            Further arguments to MetaDataClassification()

    Returns:
        MetaData object
    """

    if not os.path.exists(path_phenodata):
        path_phenodata = os.path.join(orig_dir, path_phenodata)
        if not os.path.exists(path_phenodata):
            raise FileNotFoundError("Phenodata file not found")
    if read_csv_kwargs is not None:
        phenodata = pd.read_csv(path_phenodata, **read_csv_kwargs)
    else:
        phenodata = pd.read_csv(path_phenodata)
    # If string values, remove trailing and leading whitespace
    for column_x in phenodata.columns:
        if isinstance(phenodata[column_x][0], str):
            phenodata[column_x] = phenodata[column_x].str.strip()

    if isinstance(subject_name_col, int):
        subject_col = phenodata.columns.values[subject_name_col]
    elif isinstance(subject_name_col, str):
        subject_col = subject_name_col

    pheno_subject_paths: List[str] = []
    for x in phenodata[subject_col].tolist():
        if regex_sub_subject_name_col is not None:
            x = re.sub(regex_sub_subject_name_col[0], regex_sub_subject_name_col[1], x)
        from_posix_path = pathlib.Path(pathlib.PurePosixPath(x))
        from_nt_path = pathlib.Path(pathlib.PureWindowsPath(x))
        if os.path.exists(os.path.join(orig_dir, from_posix_path)):
            found_path = str(from_posix_path)
        elif os.path.exists(os.path.join(orig_dir, from_nt_path)):
            found_path = str(from_nt_path)
        else:
            found_path = x + "___not_found_in_orig_dir"
        pheno_subject_paths += [found_path]
    phenodata[subject_col] = pheno_subject_paths
    phenodata.set_index(subject_col, inplace=True)
    if verbose:
        print("phenodata", phenodata)

    # find all files inside origdir
    all_files = list_files_recursive(orig_dir, full_names=False)
    if verbose:
        print("all_files", all_files)

    # include only matching regex
    included_files = [
        filename
        for filename in all_files
        if bool(re.search(regex_include, filename, re.IGNORECASE))
    ]
    if verbose:
        print("included_files", included_files)

    # sort all_files because windows and linux seem to sort differently, then the test assertion goes wrong.
    included_files.sort()
    files_not_in_pheno = [
        filex
        for filex in included_files
        if pathlib.Path(filex).__str__() not in pheno_subject_paths
    ]
    if verbose:
        print("files_not_in_pheno", files_not_in_pheno)

    if restrict_to_present_pheno:
        # if restrict to present pheno: restrict the included files to those present in the phenodata.
        included_files = [
            filex
            for filex in included_files
            if pathlib.Path(filex).__str__() in pheno_subject_paths
        ]
    else:
        if len(files_not_in_pheno) > 0:
            raise ValueError(
                "The following file indexes are missing in the phenodata: \n"
                + ", ".join(files_not_in_pheno)
            )
    if verbose:
        print("included_files", included_files)

    included_files_pathed = [pathlib.Path(filex).__str__() for filex in included_files]
    if verbose:
        print("included_files_pathed", included_files_pathed)

    # match the phenodata with the read in files
    matched_pheno = phenodata.loc[included_files_pathed, :]
    if verbose:
        print("matched_pheno", matched_pheno)

    if any(phenodata.index.duplicated()):
        raise ValueError(
            "You have duplicated phenodata rownames (even after subsetting to included files!)\n"
            + "--> Check your csv file. "
        )
    if len(included_files) == 0:
        raise ValueError("Empty included_files.")

    matched_pheno.reset_index(drop=False, inplace=True)
    # matched_pheno.reset_index(drop=True, inplace=True)
    if verbose:
        print("matched_pheno", matched_pheno)

    return metadata_type(
        raw_filenames=included_files,
        orig_dir=orig_dir,
        class_name=matched_pheno,
        **kwargs
    )


def gen_meta_filenames(
    orig_dir: str,
    colnames: List[str] = None,
    sep: str = r"_",
    regex_include: str = r"^",
    verbose: bool = False,
    metadata_type: MetaDataBase = MetaDataClassification,
    **kwargs
) -> MetaDataBase:
    """
    Generate a MetaData object based on the data's filenames, delimited through the "sep" separator.

    orig_dir/
        file1_1_A
        file2_0_A
        file3_2_B
        file4_0_B
        file5_1_B

    Then the MetaData object will be of length 5 and have two possible "selection"s: column2 and column3.
    Selection column2 has 3 classes: 0, 1, 2
    Selection column3 has 2 classes: "A", "B"

    So the interpretation of the filename works as following where <sep> is replaced be the value of sep:

        samplename<sep>column2<sep>column3

    Args:
        orig_dir:
            Data containing the raw data in folders. Each direct sub-folder of this directory is regarded as unique
            class name.
        colnames:
            If None, the colnames are set as following:
                ['sample', *['column' + str(i) for i in range(1, len(filenames_split_df.columns))]]
            resulting in something like
                ['sample', 'column1', 'column2', ..., 'columnK']
            By setting colnames you can replace these names.
        sep:
            Separator between the "columns" inside the filenames
        regex_include:
            Include only files to the metadata matching this regex. Default: r'*' --> all files
        verbose:
            Verbose output
        **kwargs:
            Further arguments to MetaData

    Returns:
        A MetaData object
    """
    # find all files inside origdir
    all_files = list_files_recursive(orig_dir, full_names=False)
    all_files.sort()  # consistency between windows and linux
    if verbose:
        print(all_files)

    # include only matching regex
    included_files = [
        filename for filename in all_files if bool(re.search(regex_include, filename))
    ]
    if verbose:
        print(included_files)

    # remove the extensions, as those are certainly no "column"
    # os.path.splitext: Split a path in root [0] and extension [1].
    matched_files_no_extension = [
        os.path.splitext(filename)[0] for filename in included_files
    ]
    if verbose:
        print(matched_files_no_extension)

    # split the "columns" by the separator
    filenames_split = [
        re.split(sep, filename) for filename in matched_files_no_extension
    ]
    if verbose:
        print(filenames_split)

    # make a dataframe and set appropriate names
    filenames_split_df = pd.DataFrame(filenames_split)
    if colnames is not None:
        if len(colnames) < len(filenames_split_df.columns):
            raise ValueError(
                "You supplied less colnames ("
                + str(len(colnames))
                + ") than there are in the filenames_split dataframe ("
                + str(len(filenames_split_df.columns))
                + ")"
            )
        elif len(colnames) > len(filenames_split_df.columns):
            raise ValueError(
                "You supplied more colnames ("
                + str(len(colnames))
                + ") than there are in the filenames_split dataframe ("
                + str(len(filenames_split_df.columns))
                + ")"
            )
        filenames_split_df.columns = colnames

    else:
        filenames_split_df.columns = [
            "sample",
            *["column" + str(i) for i in range(1, len(filenames_split_df.columns))],
        ]
    if verbose:
        print(filenames_split_df)

    return metadata_type(
        raw_filenames=included_files,
        orig_dir=orig_dir,
        class_name=filenames_split_df,
        **kwargs
    )
