import os
import re
import warnings
from typing import List, Union

import pandas as pd

from pointcyto.data.metadata_base import MetaDataBase


# This class is heavily based on torch_geometric.data.data
class MetaDataRegression(MetaDataBase):
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
        class_name: Union[dict, List[str], pd.DataFrame] = None,
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
                See MetaData, this is only to not break later MetaData handling and REPLACES `pheno`
                if given.
        """
        if pheno is None:
            pheno = class_name
        super(MetaDataRegression, self).__init__(
            raw_filenames=raw_filenames,
            read_with=read_with,
            pheno=pheno,
            orig_dir=orig_dir,
            root=root,
            savetype=savetype,
            ignore_unequal_feature_names=ignore_unequal_feature_names,
        )
        if self.pheno is not None:
            if self.pheno.shape[1] > 1:
                self.selection = self.pheno.columns.values[1]

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

    @property
    def y(self):
        """
        Return the currently selected class values as a list, depending on ``self.selection``

        Returns:
            List[Union[float, int]]
        """
        return self.pheno[self.selection].tolist()

    def append(self, new_listlike_dict: dict) -> None:
        """
        You can append new samples to the MetaData object using append.

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
        super().append(new_listlike_dict=new_listlike_dict)
        try:
            tmp = pd.concat(
                [self.pheno, new_listlike_dict["pheno"]], sort=False, ignore_index=True
            )
            self._pheno = tmp
        except KeyError:
            # Add a row of NA as last row to _pheno
            self._pheno.loc[self._pheno.shape[0]] = pd.NA

    def __repr__(self):
        base_repr = super(MetaDataRegression, self).__repr__()
        if len(self) == 0:
            selected_y_range = "None"
        else:
            selected_y_range = f"[{min(self.y)}, {max(self.y)}]"
        base_repr = re.sub(
            pattern=r"(\nselection:.*\n)",
            repl=r"\1___AAAAAAAAAAAAAAAAAAAAAAAA___PLACEHOLDER___\n",
            string=base_repr,
        )
        return re.sub(
            "___AAAAAAAAAAAAAAAAAAAAAAAA___PLACEHOLDER___",
            "selected y range: {}".format(selected_y_range),
            base_repr,
        )
