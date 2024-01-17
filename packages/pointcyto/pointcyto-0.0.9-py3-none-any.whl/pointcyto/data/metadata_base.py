import copy
import os
import re
import shutil
import warnings
from abc import abstractmethod
from typing import Dict, Iterable, List, Union

import pandas as pd
import torch
from pandas.core.series import Series


def size_repr(value):
    if torch.is_tensor(value):
        return list(value.size())
    elif isinstance(value, int) or isinstance(value, float):
        return [1]
    elif isinstance(value, list) or isinstance(value, tuple):
        return [len(value)]
    else:
        return value


def replace_file_extension(
    filename: str, to_ext: str = ".csv", regex: str = r"\.[^.]*$"
):
    return re.sub(regex, to_ext, filename)


# This class is heavily based on torch_geometric.data.data
class MetaDataBase(object):
    """
    A plain python object containing pheno information about a sample
    """

    def __init__(
        self,
        raw_filenames: List[str] = None,
        read_with: List[str] = "parse_by_ext",
        pheno: Union[dict, List[str], pd.DataFrame] = None,
        orig_dir: str = os.path.abspath("."),
        root: str = None,
        savetype: str = "torch",
        ignore_unequal_feature_names: bool = False,
    ):
        """

        Args:
            raw_filenames (List[str]):
                The raw filenames as list, relative path to orig_dir
            read_with:
                A list how the respective file should be read. Default: "ext" to read from file extension.
                2020-02-25: possible could be "parse_fcs", "parse_csv" or "sql"
            orig_dir:
                The directory where raw_filenames are inside
            root:
                The directory where the folders "raw/" and "processed/" should be inside.
                In "root/processed/", the processed filenames will be saved.

                If root is not given, root is defined as inside the orig_dir.
            savetype:
                How the processed files should be saved. Currently (2020-02-25) only implemented: "torch" and "csv".
                Future extension could be "sql" but then the conversion of raw_filenames -> processed_filenames
                must be handled extra. At the moment, each raw_filename is directly translated
                (by changing the extension) to a processed filename
            class_name:
                See MetaDataBase this is only to not break later MetaDataBasehandling and REPLACES `pheno`
                if given.
            ignore_unequal_feature_names:
                When building the Pointcloud, should unequal featurenames be ignored?
        """

        self._selection = None
        self._pheno = None
        self.savetype = savetype
        self.ignore_unequal_feature_names = ignore_unequal_feature_names

        # 1. Define all elements of this class
        # 1.1 List-like metadata, each element is one sample
        self.raw_filenames = raw_filenames

        if self.raw_filenames is not None:
            self.sample_feature_names = [
                None for _ in raw_filenames
            ]  # Is set outside of the Class
            # read_with should be a character vector of the function which
            #   1) reads the respective raw_filename
            #   2) Saves it in processed_filenames
            self.add_pheno_single(
                new_pheno_column=[read_with for _ in self.raw_filenames]
                if isinstance(read_with, str)
                else read_with,
                col_name="read_with",
            )
        else:
            self.sample_feature_names = []

        self.pheno = pheno
        if self.pheno is not None:
            if self.pheno.shape[1] > 1:
                self.selection = self.pheno.columns.values[1]
        # self._listlike_metadata is a set of listlike metadata elements
        self._listlike_metadata = {
            "raw_filenames",
            "processed_filenames",
            "sample_feature_names",
            "read_with",
            "y",
        }

        # 1.2 Single value or dictionary metadata, each value is relevant for all samples
        self.orig_dir = os.path.abspath(orig_dir)
        # If root is not given, root is defined as one folder above the orig_dir.
        only_orig_dir = os.path.basename(self.orig_dir)
        default_root_dir = os.path.realpath(
            os.path.join(self.orig_dir, os.pardir, "autoroot_" + only_orig_dir)
        )
        self.root = root if root is not None else default_root_dir
        os.makedirs(self.root, exist_ok=True)

    @property
    def selection(self) -> None:
        """
        When accessing :property:`~pointcyto.datametadata.MetaData.y` the returned values
        refer to a specific column of :property:`~pointcyto.datametadata.MetaData.pheno`.
        Which column should be used can be set by replacing the selection:

        .. code-block::

            self.selection = '<name_of_a_pheno_column>'
            self.selection = <number of a pheno column>

        Returns:
            None

        Examples:
            See :func:`tests.datasets.test_metadata.TestMetaData.metadata_testing`


        """
        return self._selection

    @selection.setter
    def selection(self, classname):
        if classname is None:
            self._selection = None
        elif isinstance(classname, int):
            self._selection = self.pheno.columns.values[classname]
        elif classname in self.pheno.columns.values:
            self._selection = classname
        else:
            raise KeyError(
                classname, "does not exist in self.pheno columns and is not integer."
            )

    @property
    def raw_filenames(self) -> List[str]:
        """
        Returns the raw filenames

        The ``raw_filenames.setter`` additionally generates the processed filenames using :meth:`proc_from_raw_filename`
        and stores it into ``self._processed_filenames`` so you can access it via (non-writable)
        :property:`processed_filenames`.

        Returns:
            A list of names for your files.
        """
        return self._raw_filenames

    @raw_filenames.setter
    def raw_filenames(self, filenames):
        self._raw_filenames = filenames
        if self.raw_filenames is not None:
            self._processed_filenames = [
                self.proc_from_raw_filename(file_x) for file_x in self.raw_filenames
            ]
        else:
            self._processed_filenames = None

    def proc_from_raw_filename(self, filename: str) -> str:
        """
        Each raw file might be processed and saved in a new file. This is mainly relevant for out-of-memory pointclouds
        as in-memory-pointclouds do not save each processed file one by one but one big file where all processed data
        is inside.

        The rawfile file-extension is replaced by a different extension based on ``self.savetype``.
        Args:
            filename:
                A string of the filename

        Returns:
            The filename string with the extension replaced.
        """
        if self.savetype == "torch":
            transformed = replace_file_extension(filename, ".pt")
        elif self.savetype == "csv":
            transformed = replace_file_extension(filename, ".csv")
        elif self.savetype == "sql":
            raise NotImplementedError
        else:
            raise NotImplementedError
        return transformed

    @property
    def processed_filenames(self) -> List[str]:
        return self._processed_filenames

    @property
    def pheno(self) -> pd.DataFrame:
        """
        The underlying phenodata for each raw_filename. Each raw_filename might have multiple values related to it,
        these values are organized in this dataframe.

        Note that the column ``read_with`` is always added here and set to the class constructor value ``read_with``

        Read-access to the phenodata by using self.pheno.
        Write-access by

        1. Setting the complete pheno `mymeta.pheno = <Dataframe or something which can be converted into one>`
        2. (Preferred) **adding** phenodata, see :meth:`add_pheno`

        Returns:
            The pheno dataframe
        """
        return self._pheno

    @pheno.setter
    def pheno(self, newpheno):
        if isinstance(newpheno, pd.DataFrame):
            newpheno_df = newpheno
        else:
            newpheno_df = pd.DataFrame(newpheno)
        self.add_pheno(newpheno_df)

    @property
    def n_pheno(self) -> int:
        """

        Returns:
            Returns how many phenodata-columns there are. Mind that ``read_with`` is generated by MetaData.__init__().
        """
        return len(self.pheno.columns)

    def add_pheno(
        self,
        new_pheno: Union[pd.DataFrame, Dict[str, List]],
        replace_new_df_index: bool = False,
    ) -> None:
        """
        Add new_pheno to the current phenodata.

        Args:
            new_pheno:
                Calls self.add_pheno_single() on every column of the given dataframe or creates a dataframe from a given
                ``{column_name: column_values_list}`` dictionary.
            replace_new_df_index:
                Forwarded to :meth:`add_pheno_single`
        Returns:
            None
        """
        if isinstance(new_pheno, Dict):
            new_pheno = pd.DataFrame(new_pheno)
        for colname in new_pheno.columns:
            self.add_pheno_single(
                new_pheno_column=new_pheno[colname],
                col_name=colname,
                replace_new_df_index=replace_new_df_index,
            )

    @abstractmethod
    def add_pheno_single(
        self,
        new_pheno_column: Union[pd.DataFrame, List],
        col_name: str = None,
        replace_new_df_index: bool = True,
    ) -> None:
        """
        Adds a single new pheno column to the ``mymeta.pheno``. Make sure that if you
        supply a dataframe that it really is only one column, if you have more than one
        column use :meth:`add_pheno`.

        Args:
            new_pheno_column:
                A dataframe or list of elements.
            col_name:
                How should the new column be named? You always have to give this.
            replace_new_df_index:
                If you gave a dataframe in ``new_pheno_column``, should the existing index be removed?
                Examples where this is relevant are in
                :func:`tests.datasets.test_metadata.test_add_pheno_single_missing_index` and
                :func:`tests.datasets.test_metadata.test_add_pheno_single_switched_index`.

        Returns:

        """

    @property
    def read_with(self) -> List[str]:
        """
        Extract the read_with column from the phenodata, used inside
        :class:`pointcyto.dataInMemoryPointCloud.InMemoryPointCloud`

        Returns:
            List[str] containing an identifier how the respective raw_filename should be read.
            Possibly in the future this could be a function, not only a string.
        """
        return self.pheno["read_with"].tolist()

    @property
    @abstractmethod
    def y(self):
        """
        Return the currently selected y values as a list, depending on ``self.selection``

        For classification: classIDs
        For regression: float values

        Returns:
            List[Union[float, int]]
        """

    @property
    def sample_feature_names(self) -> List[List[str]]:
        """
        Each sample might have feature names assigned to its raw_filename, you can set them here.

        Setter:
            Args:
                val:
                    Either supply the values(=val) as list(n_samples) of list(n_features) of str (single feature name)
                    or as a dictionary defining `{'feature_names': List[str], 'sample_number': List[int]}`
        """
        return self._sample_feature_names

    @sample_feature_names.setter
    def sample_feature_names(self, val: Union[dict, List[List[str]], List[str]]):
        if isinstance(val, dict):
            new_feature_names = val["feature_names"]
            sample_n = val["sample"]
            self._sample_feature_names[sample_n]: List[str] = new_feature_names
        else:
            if len(val) == len(self):
                self._sample_feature_names: List[List[str]] = val
            else:
                raise ValueError(
                    "List of feature names per sample has not the same length ("
                    + str(len(val))
                    + ")  as self ("
                    + str(len(self))
                    + ")"
                )

        self._set_feature_names()

    @property
    def feature_names(self) -> List[str]:
        """
        Holds the feature names over all samples in this MetaDataBaseobject. In contrast to
        :property:`sample_feature_names` this property does not hold the feature names *per sample*
        but *over all samples*.

        If the feature names are identical over all samples this is it. If the feature names are NOT identical over all
        samples a warning occurs AND this values becomes ``Feature names NOT identical over samples!``. You should
        probably take this warning very seriously because features of different samples might not be matching in order.
        If that is the case you have to fix your data first.

        Returns:
            A list of feature names over all samples.
        """
        return self._feature_names

    def _set_feature_names(self):
        self._feature_names_identical = True
        if len(self.sample_feature_names) == 0:
            allsamples_fn = None
        elif all(
            [
                self.sample_feature_names[0] == feature_names_sample_N
                for feature_names_sample_N in self.sample_feature_names
            ]
        ):
            allsamples_fn = self.sample_feature_names[0]
        else:
            self._feature_names_identical = False
            if not self.ignore_unequal_feature_names:
                warnings.warn("Feature names are not identical!", UserWarning)
            allsamples_fn = ["Feature names NOT identical over samples!"]
        self._feature_names = allsamples_fn

    @property
    def feature_names_identical(self):
        """
        Boolean value if the feature_names are identical over all samples.

        Returns:
            True/False
        """
        return self._feature_names_identical

    def _del_pheno_column(self, column: Union[str, int]) -> None:
        """
        Only removing a column of self.pheno is not enough to really purge the column as in ``classes_base_cmap``,
        ``class_colors`` and ``class_name_id_map`` still the values exist. This function completely removes those and
        the column in the phenodata.

        Args:
            column:
                Column name or index

        Returns:
            None
        """
        if isinstance(column, int):
            column = self.pheno.columns[column]
        if column == "read_with":
            raise IndexError("Cannot delete read_with column")
        self._pheno.drop(column, axis=1, inplace=True)
        if self.selection == column:
            self.selection = 0

    def __getitem__(self, key: Union[int, slice, tuple] = None):
        if isinstance(key, tuple) and len(key) == 2:
            new_metadata = copy.deepcopy(self)
            samples = key[0]
            pheno = key[1]
            if pheno is not None:
                if isinstance(pheno, int):
                    pheno_index = [pheno]
                elif isinstance(pheno, slice):
                    # See https://stackoverflow.com/questions/2936863/python-implementing-slicing-in-getitem
                    #   Eric Cousineau answer how slicing behaves
                    pheno_cn = list(new_metadata.pheno.columns.values)
                    start = pheno.start if pheno.start is not None else 0
                    stop = pheno.stop if pheno.stop is not None else len(pheno_cn)
                    step = pheno.step if pheno.step is not None else 1
                    pheno_index = [
                        pheno_cn.index(mypheno) if isinstance(mypheno, str) else mypheno
                        for mypheno in range(start, stop, step)
                    ]
                else:
                    pheno_cn = list(new_metadata.pheno.columns.values)
                    pheno_index = [
                        pheno_cn.index(mypheno) if isinstance(mypheno, str) else mypheno
                        for mypheno in pheno
                    ]
                if 0 not in pheno_index:
                    pheno_index = [0] + pheno_index
                del_pheno_indices = [
                    p_col
                    for p_col in range(len(self.pheno.columns))
                    if p_col not in pheno_index
                ]
                del_pheno_names = self.pheno.columns.values[del_pheno_indices]
                for single_pheno in del_pheno_names:
                    new_metadata._del_pheno_column(single_pheno)

            check_samples = samples != slice(None, None, None)
            # Checks *first* if check_samples is boolean
            #   If it is NOT, then it is probably something with greater length (e.g. a numpy array or a list)
            #   then go subset the filenames
            # If it is, then take its logical value.
            if not isinstance(check_samples, bool) or check_samples:
                try:
                    new_raw_filenames = []
                    for index, value in enumerate(samples):
                        if isinstance(value, bool):
                            if value:
                                new_raw_filenames.append(
                                    new_metadata.raw_filenames[index]
                                )
                        else:
                            new_raw_filenames.append(new_metadata.raw_filenames[value])
                except TypeError:  # then samples was no iterable
                    new_raw_filenames = new_metadata.raw_filenames[samples]

                if not isinstance(new_raw_filenames, list):
                    new_raw_filenames = [new_raw_filenames]

                new_metadata.raw_filenames = new_raw_filenames

                # Restrict phenodata but without updating the pheno keys (self._build_pheno_column())
                if isinstance(samples, int):
                    new_metadata._pheno = new_metadata._pheno.iloc[[samples]]
                    new_metadata.sample_feature_names = [
                        self.sample_feature_names[samples]
                    ]
                elif isinstance(samples, Series):
                    new_metadata._pheno = new_metadata._pheno.loc[samples, :]
                    new_metadata.sample_feature_names = [
                        self.sample_feature_names[index]
                        for index, value in enumerate(samples.values)
                        if value
                    ]
                else:
                    new_metadata._pheno = new_metadata._pheno.iloc[samples, :]
                    if isinstance(samples, Iterable):
                        if sum([isinstance(x, bool) for x in samples]) == 0:
                            new_metadata.sample_feature_names = [
                                self.sample_feature_names[index] for index in samples
                            ]
                        elif sum([isinstance(x, bool) for x in samples]) == len(
                            samples
                        ):
                            new_metadata.sample_feature_names = [
                                self.sample_feature_names[index]
                                for index, value in enumerate(samples)
                                if value
                            ]
                        else:
                            raise ValueError(
                                "Your given samples (metadata[samples, :]) are "
                                + "neither all boolean nor all not boolean. There seems to be a mistake. "
                            )
                    else:
                        new_metadata.sample_feature_names = self.sample_feature_names[
                            samples
                        ]

                # if isinstance(samples, int):
                #     new_metadata.sample_feature_names = [self.sample_feature_names[samples]]
                # else:
                #     print(samples)
                #     print([self.sample_feature_names[x] for x in samples])
                #     new_metadata.sample_feature_names = [self.sample_feature_names[x] for x in samples]

                # Now make a new auto_root_directory for fast later loading.
                # List current directory with root-directories inside.
                base_root_dir = os.path.basename(new_metadata.root)
                dir_with_root_dir = new_metadata.root[
                    0 : len(new_metadata.root) - len(base_root_dir) - 1
                ]
                base_root_dir_nonumber = re.sub(r"___[0-9]+$", "", base_root_dir)
                # https://stackoverflow.com/questions/7124778/how-to-match-anything-up-until-this-sequence-of-characters-in-a-regular-expres
                last_part_number = [
                    re.sub(r".+?(___([0-9]+))?$", r"\2", directory)
                    for directory in os.listdir(dir_with_root_dir)
                    if base_root_dir_nonumber in directory
                ]
                last_part_number = [
                    int(number) for number in last_part_number if number != ""
                ]
                last_part_number += [0]
                new_metadata.root = os.path.join(
                    dir_with_root_dir,
                    base_root_dir + "___" + str(max(last_part_number) + 1),
                )
                os.mkdir(new_metadata.root)

            return new_metadata
        else:
            samples = key
            return {
                key_x: getattr(self, key_x)[samples]
                for key_x in self._listlike_metadata
            }

    @abstractmethod
    def append(self, new_listlike_dict: dict) -> None:
        """
        You can append new samples to the MetaDataBaseobject using append.

        Args:
            new_listlike_dict:

        Returns:
            None

        Examples:
            See
            - :meth:`tests.datasets.test_metadata.test_metadata_append_only_filename`
            - :meth:`tests.datasets.test_metadata.test_metadata_append_with_sample_feature_names`
            - :meth:`tests.datasets.test_metadata.test_metadata_append_with_pheno`

        """
        if len(new_listlike_dict["raw_filenames"]) > 1:
            raise ValueError("Only supply a single raw_filename as list.")
        self._raw_filenames += new_listlike_dict["raw_filenames"]
        self._processed_filenames += [
            self.proc_from_raw_filename(new_listlike_dict["raw_filenames"][0])
        ]
        del new_listlike_dict["raw_filenames"]
        # Possible further keys: sample_feature_names
        try:
            self.sample_feature_names += [new_listlike_dict["sample_feature_names"]]
        except KeyError:
            pass

    @property
    def keys(self):
        r"""Returns all names of attributes."""
        keys = [key for key in self.__dict__.keys()]
        keys = [key for key in keys if key[:2] != "__" and key[-2:] != "__"]
        return keys

    def __len__(self):
        r"""Returns the number of raw files (read "samples")."""
        if self.raw_filenames is None:
            return 0
        else:
            return len(self.raw_filenames)

    def __contains__(self, key):
        r"""Returns :obj:`True`, if the attribute :obj:`key` is present in the
        data."""
        return key in self.keys

    def __iter__(self):
        r"""Iterates over all samples, so list elements in the "list-like metadata".
        Yielding a dictionary of all list-like metadata for the respective sample_n"""
        for sample_n in range(len(self.raw_filenames)):
            yield self[sample_n]

    def __call__(self, *keys):
        r"""Iterates over all samples given in *keys (int), so list elements in the "list-like metadata".
        Yielding a dictionary of all list-like metadata for the respective sample_n.

        If *keys is not given, iterates over all samples like __iter__()

        """
        if len(keys) > 0:
            for sample_n in keys:
                yield self[sample_n]
        else:
            for sample_n in range(len(self.raw_filenames)):
                yield self[sample_n]

    def __eq__(self, other):
        all_keys_present = all([key_x in other.keys for key_x in self.keys])
        if not all_keys_present:
            return False
        retval = True
        for key_x in self.keys:
            if isinstance(getattr(self, key_x, None), pd.DataFrame):
                retval = getattr(self, key_x, None).equals(getattr(other, key_x, None))
            elif getattr(self, key_x, None) != getattr(other, key_x, None):
                retval = False
        return retval

    def __repr__(self):
        feature_names = (
            ", ".join(self.feature_names) if self.feature_names is not None else "None"
        )
        if len(self) == 0:
            pheno_col_values = "None"
        else:
            pheno_col_values = self.pheno.columns.values

        return "\n".join(
            [
                "{} samples".format(len(self)),
                "pheno columns: {}".format(pheno_col_values),
                "selection: {}".format(str(self.selection)),
                "global feature names: {}".format(feature_names),
                "orig dir: {}".format(self.orig_dir),
                "root dir: {}".format(self.root),
                "savetype: {}".format(self.savetype),
            ]
        )

    def rm_root(self, are_you_sure: bool = False) -> None:
        """
        The PointCloud generation lateron will process the MetaDataBaseobject based on ``raw_filenames`` into
        ``processed_filenames`` into the ``self.root`` directory.

        If you want to delete this root directory you will loose all processed data (depending on your data
        this could take a bit of time) and if your ``root`` directory is the same as your ``orig_dir`` (do not do that)
        you might even loose your raw data.

        This is helpful because when subsetting a ``MetaDataBase` object, new root directories are generated
        and therefore it might be hard to track which ``MetaDataBase` object refers to which root-directory.

        Args:
            are_you_sure:
                Boolean, are you really sure you want to delete this?
                Introduced this parameter with default ``false`` that you cannot delete your data by error.

        Returns:
            None
        """
        if are_you_sure:
            if os.path.realpath(self.root) == os.path.realpath(self.orig_dir):
                raise ValueError(
                    "You specified root as orig_dir where the raw-data are located.\n"
                    + "I will not delete this for safety reasons."
                )
            shutil.rmtree(self.root)
        else:
            warnings.warn(
                "Did not remove root, specify are_you_sure as true. \n!!CAREFUL!!"
                + "\nYou will loose all of your processed data.\n"
                + "You might loose your original data if you specified "
            )
