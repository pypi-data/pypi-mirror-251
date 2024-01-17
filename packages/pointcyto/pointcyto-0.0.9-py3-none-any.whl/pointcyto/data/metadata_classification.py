import copy
import os
import re
import warnings
from typing import Dict, List, Tuple, Union

import matplotlib.colors
import numpy as np
import pandas as pd

from pointcyto.data.metadata_base import MetaDataBase
from pointcyto.io.utils import convert_class_id_names
from pointcyto.plot.colors import discrete_cmap


# This class is heavily based on torch_geometric.data.data
class MetaDataClassification(MetaDataBase):
    """
    A plain python object containing pheno information about a sample
    """

    def __init__(
        self,
        raw_filenames: List[str] = None,
        read_with: List[str] = "parse_by_ext",
        class_name: Union[dict, List[str], pd.DataFrame] = None,
        orig_dir: str = os.path.abspath("."),
        root: str = None,
        savetype: str = "torch",
        allow_class_extension: bool = True,
        sort_class_name_map: bool = True,
        ignore_unequal_feature_names: bool = False,
    ):
        """

        Args:
            raw_filenames (List[str]):
                The raw filenames as list, relative path to orig_dir
            read_with:
                A list how the respective file should be read. Default: "ext" to read from file extension.
                2020-02-25: possible could be "parse_fcs", "parse_csv" or "sql"
            class_name:
                Either a list of class names for each filename
                or a dict of list of class names for each filename.
                Is transformed internally to a pandas.Dataframe. If no dict is given, the column names are generated
                automatically.
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
            allow_class_extension:
                When appending a new sample, including phenodata - is it allowed to rebuild the present classes?
                If the sample has an unseen class for one of the phenodata:

                If ``False``:

                    Throws a ValueError.

                If ``True``:

                    self._build_pheno_column() is called
            sort_class_name_map:
                If True, during building the class_name_id_map, the names are sorted before giving an ID.
                See the test tests/datasets/test_metadata.py: test_multiple_metadata_same_classmap() for exemplary use.
        """
        self._class_name_id_map: Dict[Dict] = dict()
        self._class_colors: Dict[matplotlib.colors.LinearSegmentedColormap] = dict()
        self._classes_base_cmap: Dict[str] = dict()
        self.allow_class_extension = allow_class_extension
        # sort_class_name_map is needed before super().__init__ because of self._build_pheno_column()
        self.sort_class_name_map = sort_class_name_map

        super(MetaDataClassification, self).__init__(
            raw_filenames=raw_filenames,
            read_with=read_with,
            orig_dir=orig_dir,
            root=root,
            savetype=savetype,
            pheno=class_name,
            ignore_unequal_feature_names=ignore_unequal_feature_names,
        )

        if self.raw_filenames is not None:
            self._build_pheno_column("read_with")

        self._listlike_metadata = self._listlike_metadata.union({"class_name"})

    def add_pheno_single(
        self,
        new_pheno_column: Union[pd.DataFrame, List],
        col_name: str = None,
        replace_new_df_index: bool = True,
    ) -> None:
        """
        Adds a single new pheno column to the ``mymeta.pheno``. Make sure that if you supply a dataframe that it really
        is only one column, if you have more than one column use :meth:`add_pheno`.

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
        if not isinstance(new_pheno_column, pd.DataFrame):
            new_pheno_column = pd.DataFrame({col_name: new_pheno_column})

        if self._pheno is not None:
            if not new_pheno_column.index.equals(self._pheno.index):
                warnmessage_part1 = "new_pheno_column.index is NOT equal to the current self.pheno.index **"
                if replace_new_df_index:
                    new_pheno_column.index = self._pheno.index
                    # warnings.warn(
                    #     warnmessage_part1 +
                    #     '\n  ** but I was allowed to replace the index (what I did now with self.pheno.index)')
                else:
                    warnings.warn(
                        warnmessage_part1
                        + "\n  ** your given new_pheno_column is reordered and/or can contain Nan!"
                    )

        if self._pheno is None:
            self._pheno = new_pheno_column
        else:
            if len(new_pheno_column) != len(self):
                raise ValueError("New pheno must be equal length as the raw_filenames")
            if col_name is None:
                if isinstance(new_pheno_column, pd.DataFrame):
                    col_name = new_pheno_column.columns[0]
                if col_name is None:
                    col_name = "pheno_" + str(len(self._pheno.columns))
            elif col_name == 0:
                col_name = "pheno_" + str(len(self._pheno.columns))

            self._pheno[col_name] = new_pheno_column
            self._build_pheno_column(col_name)

    def _is_pheno_column_valid(self, column_name: str):
        saved_selection = self.selection
        self.selection = column_name
        if not all(
            [
                value in list(self.class_name_id_map.keys())
                for value in self.class_name
                if value is not np.nan
            ]
        ):
            retval = False
        else:
            retval = True
        self.selection = saved_selection
        return retval

    def _build_pheno_column(self, column_name: str):
        """
        If a phenodata column is selected based on ``self.selection``, the following values are directly related to it:

        :meth:`class_name_id_map`
            A dictionary relating the class name to the class id

        :meth:`class_colors`
            Which class relates to which color (if you want to plot anytime this can then be consistent)

        :meth:`classes_base_cmap`
            The colormap for the selection which was the basis for class_colors

        These values come from the respective private (``__``) propierties. In constrast to the public property, the
        privates are each a dictionary of the following form:

        ::

            {
                pheno_column_X: values,
                pheno_column_Y: values,
            }

        To create these maps and colors ``__build_pheno_column`` is applied. Do not use that in your own analysis,
        instead if you really need it use :meth:`update_selection`.

        Args:
            column_name:
                Which of the phenodata should be rebuild.

        Returns:

        """
        saved_selection = self.selection
        self.selection = column_name
        # If an empty dict or None is supplied, the class_name_id_map is inferred from the data.
        self.class_name_id_map = None
        self.classes_base_cmap = "jet"
        self.class_colors = None  # If None is supplied, class_colors are inferred.
        if saved_selection is not None:
            self.selection = saved_selection

    def update_selection(self, sort_class_name_map: bool = True) -> None:
        """
        Usually you will not need this as the color and class/id maps are generated when adding phenodata. However if
        you need to update the class/id/colors for a specific selection you can call this and the class/id/colors data
        will be rebuilt.

        This might be usefull if you restrict your previously generated MetaDataClassification and therefore
        "loose" a unique value from all levels of the phenodata column.

        Always the current ``selection`` will be updated.

        Returns:
            None

        Example:
            :func:`tests.datasets.test_InMemoryPointCloud.test_InMemoryPointCloud_change_metadata`

        """
        self.sort_class_name_map = sort_class_name_map
        self._build_pheno_column(self.selection)

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
        del self._classes_base_cmap[column]
        del self._class_colors[column]
        del self._class_name_id_map[column]
        super(MetaDataClassification, self)._del_pheno_column(column)

    @property
    def class_name(self) -> List[str]:
        """
        Return the currently selected class names as a list, depending on ``self.selection``

        Returns:
            Usually List[str] but in principle it can also be List[Any], respective to raw_filenames.
        """
        return self.pheno[self.selection].tolist()

    @property
    def y(self):
        """
        Return the currently selected class IDs as a list, depending on ``self.selection``
        and ``self.class_name_id_map``

        Returns:
            List[int] according to the conversion accessible over ``self.class_name_id_map``
        """
        return convert_class_id_names(
            classes_id_or_name=self.pheno[self.selection],
            class_name_to_id=self._class_name_id_map[self.selection],
            out="id",
        )

    @property
    def class_name_id_map(self):
        """
        Returns:
            The current ``class_name_id_map``, a dictionary with the class names as keys and the class ids as values.

        Setter:

            Generated the class_name_id_map for the current selection.

            Args:
                name_id_map:
                    Default is None, then the class name and id map is extracted from the data.
                    If you supply this map directly:

                    .. code-block::

                        {
                            class_name_1: class_id_1,
                            class_name_2: class_id_2,
                            ...: ...,
                            class_name_k: class_id_k,
                        }

                    it is checked that all existing values in the currently selected pheno column (``self.selection``)
                    are inside this map.

                    If ``None`` is given (thus the class_name_id_map) is inferred from the data
                    the function additionally depends on if ``self.sort_class_name_map``.

                    If ``True`` (default):

                        The class names are sorted before assigning class ids

                    If ``False``:

                        The class names are NOT sorted before assigning class ids, therefore depending on
                        your input data if you split it for example into train and test that for train
                        ``classA = 0, classB = 1`` and for test  ``classA = 1, classB = 0``


        """
        return self._class_name_id_map[self.selection]

    @class_name_id_map.setter
    def class_name_id_map(self, name_id_map: dict = None):
        temp_class_name_id_map: Dict = dict()
        class_number = 0
        all_classes_set = list(
            dict.fromkeys(self.class_name)
        )  # unique values preserving order
        if self.sort_class_name_map:
            try:
                all_classes_set = sorted(all_classes_set)
            except TypeError as e:
                # THen was not able To compare values, returning UNSORTED + a warning
                warnings.warn(
                    "Did NOT sort the values in class_name_id_map because: \n" + str(e)
                )

        for class_x in all_classes_set:
            if class_x not in temp_class_name_id_map.keys():
                temp_class_name_id_map.update({class_x: class_number})
                class_number += 1
        if name_id_map is None or len(name_id_map) == 0:
            new_class_name_id_map = temp_class_name_id_map
        else:
            new_class_name_id_map = name_id_map
            missing_keys = []
            for key in temp_class_name_id_map:
                if key not in new_class_name_id_map:
                    missing_keys.append(key)
            if len(missing_keys) > 0:
                raise ValueError(
                    "Missing key(s) in supplied class_to_idx: ", missing_keys
                )

        if self.selection in self._class_name_id_map.keys():
            self._class_name_id_map[self.selection] = new_class_name_id_map
        else:
            self._class_name_id_map.update({self.selection: new_class_name_id_map})

    @property
    def class_colors(self) -> matplotlib.colors.Colormap:
        """
        Returns:
            The matplotlib.colormap for the current selection.
        """
        return self._class_colors[self.selection]

    @class_colors.setter
    def class_colors(self, cmap=None):
        if cmap is None:
            new_colormap = discrete_cmap(
                n=len(self.class_name_id_map), base_cmap=self.classes_base_cmap
            )
        else:
            new_colormap = cmap
        if self.selection in self._class_colors.keys():
            self._class_colors[self.selection] = new_colormap
        else:
            self._class_colors.update({self.selection: new_colormap})

    @property
    def classes_base_cmap(self):
        return self._classes_base_cmap[self.selection]

    @classes_base_cmap.setter
    def classes_base_cmap(self, base_cmap: str = "jet"):
        if self.selection in self._class_colors.keys():
            self._classes_base_cmap[self.selection] = base_cmap
        else:
            self._classes_base_cmap.update({self.selection: base_cmap})

    def class_id_color_dict(self) -> Dict[int, Tuple[float, float, float, float]]:
        """
        ``self.class_colors()`` returns a colormap which is of ``len(self.class_name_id_map)``. The color-coding is then
        1:1, so class_name_id become directly colors.
        class_id_color_dict is an actual dictionary making this explicit.

        .. code-block::

            {class_id: class_color}

        Returns:
            A dictionary:

            .. code-block::

                {class_id: class_color}

            where class_color is the result of self.class_colors(class_id),
            so a Tuple of RGBA values (see matplotlib.colors.Colormap)
        """
        return {id: self.class_colors(id) for id in self.class_name_id_map.values()}

    def class_name_color_dict(self) -> Dict[str, Tuple[float, float, float, float]]:
        """
        ``self.class_colors()`` returns a colormap which is of ``len(self.class_name_id_map)``. The color-coding is then
        1:1, so class_name_id become directly colors.
        class_name_color_dict is a actual dictionary:
        .. code-block::

            {'class_name': class_color}


        Returns:
            A dictionary:
            .. code-block::

                {class_name: class_color}

            where class_color is the result of self.class_colors(class_id) and class_id is gotten from class_id_name_map
            for the class_id. So a Tuple of RGBA values (see matplotlib.colors.Colormap)
        """
        class_id_name_map = {
            value: key for key, value in self.class_name_id_map.items()
        }
        return {
            class_id_name_map[id]: color
            for id, color in self.class_id_color_dict().items()
        }

    def append(self, new_listlike_dict: dict) -> None:
        """
        You can append new samples to the MetaDataClassification object using append.

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
        super(MetaDataClassification, self).append(new_listlike_dict)
        try:
            tmp = pd.concat(
                [self.pheno, new_listlike_dict["pheno"]], sort=False, ignore_index=True
            )
            self._pheno = tmp
            for pheno_col in self._pheno.columns.values[1:]:
                if self.allow_class_extension:
                    self._build_pheno_column(pheno_col)
                elif not self._is_pheno_column_valid(pheno_col):
                    raise ValueError(
                        "Unknown class ",
                        new_listlike_dict["pheno"][pheno_col],
                        " in column ",
                        pheno_col,
                    )
        except KeyError:
            # Add a row of NA as last row to _pheno
            self._pheno.loc[self._pheno.shape[0]] = pd.NA

    def concat(
        self,
        other: "MetaDataClassification",
        inplace=False,
        ignore_identical_filenames: bool = False,
    ) -> "MetaDataClassification":
        # ignore_identical_filenames:
        #   Might be useful in some test cases? But usually not.
        if not inplace:
            self = copy.deepcopy(self)

        if not isinstance(other, MetaDataClassification):
            raise ValueError("Supply another MetaDataClassification object")
        if self.orig_dir != other.orig_dir:
            raise ValueError(
                "Can only concat MetaDataClassification with the same orig_dir "
                + "because raw_filenames are relative to that."
            )
        if not ignore_identical_filenames and any(
            [
                os.path.join(self.orig_dir, self_names)
                == os.path.join(other.orig_dir, other_names)
                for self_names, other_names in zip(
                    self.raw_filenames, other.raw_filenames
                )
            ]
        ):
            raise ValueError("Some (self.orig_dir, self_names) filenames are identical")
        self._raw_filenames += other.raw_filenames
        self._processed_filenames += other.processed_filenames
        self._sample_feature_names += other._sample_feature_names

        tmp = pd.concat([self.pheno, other.pheno], sort=False, ignore_index=True)
        self._pheno = tmp
        selection_saved = self.selection
        for pheno_col in self._pheno.columns.values[1:]:
            self.selection = pheno_col
            self.update_selection(sort_class_name_map=True)
        self.selection = selection_saved

        if not inplace:
            return self

    def __eq__(self, other):
        all_keys_present = all([key_x in other.keys for key_x in self.keys])
        if not all_keys_present:
            return False
        retval = True
        for key_x in self.keys:
            if key_x == "_class_colors":
                # class_colors is a matplotlib.colors.LinearSegmentedColormap object
                # which lives in a memory-place. This memory-place is compared
                # (and never equal) Thus, class_colors is just ignored during comparison.
                pass
            elif isinstance(getattr(self, key_x, None), pd.DataFrame):
                retval = getattr(self, key_x, None).equals(getattr(other, key_x, None))
            elif getattr(self, key_x, None) != getattr(other, key_x, None):
                retval = False
        return retval

    def __repr__(self):
        base_repr = super(MetaDataClassification, self).__repr__()

        if len(self) == 0:
            selected_class_levels = "None"
        else:
            selected_class_levels = str(list(self.class_name_id_map.keys()))
        # inject _after_ "selection" line
        base_repr = re.sub(
            pattern=r"(\nselection:.*\n)",
            repl=r"\1___AAAAAAAAAAAAAAAAAAAAAAAA___PLACEHOLDER___\n",
            string=base_repr,
        )
        return re.sub(
            "___AAAAAAAAAAAAAAAAAAAAAAAA___PLACEHOLDER___",
            "selected class levels: {}".format(selected_class_levels),
            base_repr,
        )
