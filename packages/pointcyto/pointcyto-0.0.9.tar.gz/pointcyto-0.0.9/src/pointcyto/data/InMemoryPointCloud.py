import os
import pickle
import shutil
import warnings
from pathlib import Path
from typing import Union

import datatable as dt
import flowio
import torch
from numpy.random import seed
from torch_geometric.data import Data, InMemoryDataset
from torch_geometric.data.dataset import _repr as tg_function_repr

from pointcyto.data.metadata_base import MetaDataBase
from pointcyto.io.parse_by_ext import parse_by_ext

try:
    import pyarrow.feather as feather

    pyarrow_installed = True
except ImportError:
    pyarrow_installed = False
    pass


class InMemoryPointCloud(InMemoryDataset):
    """
    For many examples check out the test suites: :class:`tests.datasets.test_InMemoryPointCloud.TestInMemoryPointCloud`
    """

    def __init__(
        self,
        metadata: Union[MetaDataBase, Path, str],
        transform=None,
        pre_pre_transform_param_onlist=None,
        pre_transform=None,
        clear_processed: bool = False,
        loading_function=parse_by_ext,
        loading_function_arguments=None,
    ):
        """
        Generates an InMemoryPointCloud based on the files inside metadata.

        In this root-directory, if not present, "raw/" and "processed/" directories are created.
        In "raw/", the original data can but does not have to lie.
        In "processed/", the processed data is saved.

        Args:
            metadata:
                A MetaData object containing all relevant information
            transform:
                Transformations for the pytorch_geometric Data object
            pre_pre_transform_param_onlist:
                Transformations for a list of pytorch_geometric Data objects.
                Must be a transformation on the dataset and returns a tuple:
                ::

                    data_list, {'name': self.name, 'related_transform': self.related_transform,
                                'param': {'mean': self.mean, 'std': self.std}}

                This tuple holds the transformed data_list and a dictionary for further use.
                The dictionary includes the name of the transformation, the related **not onlist** transformation and
                the parameters which are a result from the onlist-transformation to be used in the
                related transformation. The standard way to use the related transformation is to loop over
                ``self.pretransform_parameter`` as shown in
                 :meth:`tests/transforms/test_pre_pre_transforms_onlist.TestPrePreTransformsOnList.test_NormalizePointCloudParam_pre_pre_transform_param_list_save_load`
                (Look at the part with the ``recreated_transform``)


                ``pre_pre_transforms`` are applied *before* ``pre_transform``.

                Examples:
                    - :class:`pointcyto.transforms.transform_param_onlist.NormalizePointCloudParam`
                    - :class:`tests.transforms.test_pre_pre_transforms_onlist.TestPrePreTransformsOnList`

            pre_transform:
                Transformations for the pytorch_geometric Data object
            loading_function:
                function used in process() to load the data.
                Should return a dictionary with the following keys
                - ``features``: A list with names of the features
                - ``point_data``: A torch.Tensor with the actual loaded data.

            loading_function_arguments:
                Arguments additionally supplied to function used in process() to load the data.
                The function call is:

                .. code-block:: python

                    parsed = self.loading_function(
                        path=os.path.join(self.metadata.orig_dir, metadata_X["raw_filenames"]),
                        y=metadata_X["y"],
                        **self.loading_function_args
                    )

        Returns:
            No return
        """
        self.loading_function = loading_function
        if loading_function_arguments is None:
            self.loading_function_args = {}
        else:
            self.loading_function_args = loading_function_arguments

        self.y_from_metadata_selection: str = None

        if clear_processed:
            try:
                shutil.rmtree(os.path.join(metadata.root, "processed"))
            except FileNotFoundError:  # then it was already deleted
                pass

        self.warnings_captured = {}
        self.loaded_or_processed = "loaded"
        if isinstance(metadata, str) or isinstance(metadata, Path):
            if os.path.isdir(metadata):
                # then it might be the given autoroot, otherwise will fail
                metadata_file = os.path.join(
                    metadata, "processed", "pointcloud_metadata.pickle"
                )
            else:
                metadata_file = metadata
                # Then it should be an actual <somename_pickled_MetaData_object>.pickle
            with open(os.path.join(metadata_file), "rb") as f:
                self.metadata = pickle.load(f)
            # A given, pickled metadata FILE must always be in the folder
            #   rootdir/processed/pointcloud_metadata.pickle
            # Therefore, the new root is  rootdir/processed/.. -> rootdir
            self.metadata.root = os.path.realpath(
                os.path.join(os.path.dirname(metadata_file), os.pardir)
            )
        else:
            self.metadata = metadata

        # self._reloading_processed_dir = False
        # if isinstance(metadata, str) or isinstance(metadata, Path):
        #     if os.path.isdir(metadata):
        #         # then it might be the given autoroot, otherwise will fail
        #         metadata_file = os.path.join(
        #             metadata, "processed", "pointcloud_metadata.pickle"
        #         )
        #     else:
        #         metadata_file = metadata
        #         # Then it should be an actual <somename_pickled_MetaData_object>.pickle
        #     with open(os.path.join(metadata_file), "rb") as f:
        #         self.metadata = pickle.load(f)

        #     # A given, pickled metadata FILE must always be in the folder
        #     #   rootdir/processed/pointcloud_metadata.pickle
        #     # Therefore, the new root is  rootdir/processed/.. -> rootdir
        #     self.metadata.root = os.path.realpath(
        #         os.path.join(os.path.dirname(metadata_file), os.pardir)
        #     )
        #     self._reloading_processed_dir = True
        # else:
        #     self.metadata = metadata

        if (
            isinstance(pre_pre_transform_param_onlist, list)
            or pre_pre_transform_param_onlist is None
        ):
            self.pre_pre_transform_param_onlist = pre_pre_transform_param_onlist
        else:
            self.pre_pre_transform_param_onlist = [pre_pre_transform_param_onlist]
        self.pretransform_parameter = list()

        # process is called inside here, therefore everything which is used in process must be defined before.
        super(InMemoryPointCloud, self).__init__(
            root=self.metadata.root, transform=transform, pre_transform=pre_transform
        )
        # # delattr(self, "raw_dir")
        # del self.raw_dir
        # self.raw_dir = self.metadata.orig_dir  # origdir might be something different than the root/raw-directory.
        self.data, self.slices = torch.load(
            os.path.join(self.processed_dir, self.processed_file_names[0])
        )
        for warning_location in self.warnings_captured:
            if (
                warning_location == "_process_userwarnings"
                and self.loaded_or_processed == "loaded"
            ):
                continue
            else:
                for warning_i in self.warnings_captured[warning_location]:
                    warnings.warn(warning_i, category=UserWarning)

    # Overwrite the raw_dir property from DataSet because
    # origdir might be something different than the "root/raw/" -directory.
    @property
    def raw_dir(self):
        return self.metadata.orig_dir

    @property
    def raw_file_names(self):
        # A list of files in the raw_dir which needs to be found in order to skip the download.
        return self.metadata.raw_filenames

    @property
    def processed_file_names(self):
        # A list of files in the processed_dir which needs to be found in order to skip the processing.
        return ["pointcloud_inmemory.pt"]

    def _to_xxx(
        self,
        outdir=".",
        verbose: bool = True,
        filetype="csv",
        shift=0,
        manual_seed=213124876,
    ):
        if manual_seed is not None:
            seed(manual_seed)  # np.random.seed(manual_seed)
            torch.manual_seed(manual_seed)
        for sample_i, sample_x in enumerate(self):
            if manual_seed is not None:
                seed(manual_seed)  # np.random.seed(manual_seed)
                torch.manual_seed(manual_seed)
            if verbose:
                print(sample_x)
            featurenames = self.metadata.sample_feature_names[sample_i]
            if featurenames is None:
                featurenames = ["f_" + str(i) for i in range(sample_x.pos.shape[1])]
            # Similar to
            #   /home/gugl/.conda_envs/ccc_optuna_III/lib/python3.8/site-packages/flowkit/_models/sample.py
            current_fp = os.path.join(
                outdir, self.raw_file_names[sample_i] + "." + filetype
            )
            os.makedirs(os.path.dirname(current_fp), exist_ok=True)
            if shift != 0:
                # FCS files make problems in Kaluza if they have values below 0.
                # Therefore we introduce a way to add shifts to the data.
                # All cells get the exact same shift
                sample_x.pos += torch.tensor(shift)
            if filetype == "pt":
                # Have to clone because subsetting does not actually create a new tensor
                # https://discuss.pytorch.org/t/saving-tensor-with-torch-save-uses-too-much-memory/46865/3
                torch.save(obj=[sample_x.pos.clone(), featurenames], f=current_fp)
            else:
                pos_numpy = sample_x.pos.numpy()
                pos_numpy_max_ceiling = sample_x.pos.max(axis=0)[0].ceil().int()
                if filetype == "fcs":
                    metadata_dict = {
                        f"response_element_{i}": str(element_i)
                        for i, element_i in enumerate(
                            sample_x.y.numpy().flatten().tolist()
                        )
                    }
                    # Update pNr for "parameter N range"
                    metadata_dict.update(
                        {
                            f"p{feature_i}r": str(
                                int(pos_numpy_max_ceiling[feature_i] * 1.2 + 10)
                            )
                            for feature_i in range(sample_x.pos.shape[1])
                        }
                    )
                    with open(current_fp, "wb") as f:
                        flowio.create_fcs(
                            event_data=pos_numpy.flatten().tolist(),
                            metadata_dict=metadata_dict,
                            channel_names=featurenames,
                            file_handle=f,
                        )
                elif filetype == "csv":
                    pos_dt = dt.Frame(pos_numpy, names=featurenames)
                    pos_dt.to_csv(current_fp)
                elif filetype == "jay":
                    pos_dt = dt.Frame(pos_numpy, names=featurenames)
                    pos_dt.to_jay(current_fp)
                elif filetype == "feather":
                    if not pyarrow_installed:
                        raise ImportError(
                            "Did not find pyarrow, cannot save feather files"
                        )
                    pos_dt = dt.Frame(pos_numpy, names=featurenames)
                    feather.write_feather(
                        df=feather.Table.from_pandas(pos_dt.to_pandas()),
                        dest=current_fp,
                    )

            if verbose:
                print("Saved ", current_fp, "\n")

    def to_csv(self, outdir=".", verbose: bool = True):
        warnings.warn(
            "In contrast to to_fcs(), only the pointcloud is saved, not the responses."
        )
        self._to_xxx(outdir=outdir, verbose=verbose, filetype="csv")

    def to_fcs(self, outdir=".", verbose: bool = True, shift: bool = 0):
        self._to_xxx(outdir=outdir, verbose=verbose, filetype="fcs", shift=shift)

    def to_pt(self, outdir=".", verbose: bool = True):
        self._to_xxx(outdir=outdir, verbose=verbose, filetype="pt")

    def to_feather(self, outdir=".", verbose: bool = True):
        self._to_xxx(outdir=outdir, verbose=verbose, filetype="feather")

    def to_jay(self, outdir=".", verbose: bool = True):
        self._to_xxx(outdir=outdir, verbose=verbose, filetype="jay")

    def download(self):
        """
        I will never download data as they are assumed to be local.

        But here you could  download raw data into raw_dir.

        """
        pass

    def _process(self):
        f = os.path.join(self.processed_dir, "str_pre_pre_transform_param.pickle")
        self.warnings_captured.update({"pre_pre_transform_param": []})
        if os.path.exists(f):
            # if os.path.exists(f):
            with open(f, "rb") as myfile:
                previous_param_as_str = pickle.load(myfile)
            if previous_param_as_str != tg_function_repr(
                self.pre_pre_transform_param_onlist
            ):
                warnstring = (
                    "The `pre_pre_transform_param` argument differs from the one used in "
                    + "the pre-processed version of this dataset. If you really "
                    + "want to make use of another pre-processing technique, make "
                    + "sure to delete `{}` first.".format(self.processed_dir)
                )
                # warnings.warn(warnstring)
                self.warnings_captured.update({"pre_pre_transform_param": warnstring})
        try:
            with open(
                os.path.join(self.processed_dir, "pretransform_parameter.pickle"), "rb"
            ) as f:
                self.pretransform_parameter = pickle.load(f)
        except FileNotFoundError:
            pass  # then the pre_pre_transform_param.pt just does not exist

        _process_userwarnings = []
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            super(InMemoryPointCloud, self)._process()
        for warning_x in w:
            if isinstance(warning_x.category(), UserWarning):
                _process_userwarnings += [warning_x]
            else:
                warnings.warn(warning_x, category=warning_x.category)
        self.warnings_captured.update({"_process_userwarnings": _process_userwarnings})

    def process(self):
        """
        Processes raw data and saves it into the processed_dir.
        Reads data into huge `Data` list.

        It
         - iterates over all ``raw_filenames`` from self.metadata
         - reads(parses) the file
         - Extracts the feature names and adds them to the respective metadata sample
         - Applies ``pre_filter``
         - Applies ``pre_pre_transform_param_onlist``
         - Saves the parameters and transformations from ``pre_pre_transform_param_onlist``
         into ``self.processed_dir/'pretransform_parameter.pickle'``
         - Applies ``pre_transform``s
         - Collates (combines) and saved the final processed dataset.

        Returns:
            None
        """
        self.loaded_or_processed = "processed"
        sample_feature_names = []
        data_list = []
        self.y_from_metadata_selection = self.metadata.selection
        for metadata_N, metadata_X in enumerate(self.metadata):
            print(
                str(metadata_N + 1),
                "/",
                str(len(self.metadata)),
                "  ",
                os.path.join(self.metadata.orig_dir, metadata_X["raw_filenames"]),
            )
            # Read data from `raw_path`.
            # now the data are in the format of tuple:(Tensor, markernames)
            # locals()["myfunction"]()
            current_response = metadata_X["y"]
            parsed = self.loading_function(
                path=os.path.join(self.metadata.orig_dir, metadata_X["raw_filenames"]),
                y=current_response,
                **self.loading_function_args,
            )

            sample_feature_names += [parsed["features"]]
            # hasattr to be backwards compatible.
            if (
                not hasattr(self.metadata, "ignore_unequal_feature_names")
                or not self.metadata.ignore_unequal_feature_names
            ):
                if sample_feature_names[0] != parsed["features"]:
                    raise ValueError(
                        "Unequal feature names of \n"
                        + "".join([self.metadata.raw_filenames[metadata_N]])
                        + ":"
                        + "\n  featurenames: "
                        + ", ".join(parsed["features"])
                        + "\n  sample 0:     "
                        + ", ".join(sample_feature_names[0])
                    )
            data_list += [parsed["point_data"]]
        self.metadata.sample_feature_names = sample_feature_names
        print("pre_filter")
        if self.pre_filter is not None:
            data_list = [data for data in data_list if self.pre_filter(data)]

        print("pre_pre_transform_param_onlist")
        if self.pre_pre_transform_param_onlist is not None:
            for transformation in self.pre_pre_transform_param_onlist:
                data_list, param_list = transformation(data_list)
                self.pretransform_parameter.append(param_list)

        print("pre_pre_transform_param_onlist saving")
        with open(
            os.path.join(self.processed_dir, "str_pre_pre_transform_param.pickle"), "wb"
        ) as f:
            pickle.dump(tg_function_repr(self.pre_pre_transform_param_onlist), f)
        with open(
            os.path.join(self.processed_dir, "pretransform_parameter.pickle"), "wb"
        ) as f:
            pickle.dump(self.pretransform_parameter, f)

        print("pre_transform")
        if self.pre_transform is not None:
            data_list = [self.pre_transform(data) for data in data_list]

        print("collate")
        data, slices = self.collate(data_list)

        print("saving")
        torch.save((data, slices), self.processed_paths[0])
        with open(
            os.path.join(self.processed_dir, "pointcloud_metadata.pickle"), "wb"
        ) as f:
            pickle.dump(self.metadata, file=f)

    def select_y_from_metadata(self, selection: str, reload: bool = False) -> None:
        """
        It might happen that you want to process your dataset only once but then learn on different responses coming
        from the metadata object.

        Args:
            selection:
                The new selection of the :class:`pointcyto.data.metadata.MetaData` object.

            reload:
                If the selection is the same as previously and ``reload=False`` (default) then nothing happens.
                Only if ``reload=True`` the selection is "updated".
        Returns:
            None

        """
        if self.y_from_metadata_selection == selection and not reload:
            raise ValueError(
                "No new y selected as the selection is the same as the previous and reload=False"
            )
        self.metadata.selection = selection
        self.y_from_metadata_selection = selection
        # self.metadata.y automatically holds the response for the current selection
        self._data.y = torch.tensor(self.metadata.y)
        # Invalidate the cache. I am not sure what happens exactly within pytorch_geometric,
        # but this seems to work. See
        # https://pytorch-geometric.readthedocs.io/en/2.0.1/_modules/torch_geometric/data/in_memory_dataset.html?highlight=self._data_list%20%3D%20None%20#
        # https://pytorch-geometric.readthedocs.io/en/latest/_modules/torch_geometric/data/in_memory_dataset.html
        #   --> @data.setter does the same thing.
        self._data_list = None

    def __getitem__(self, item) -> Union["InMemoryPointCloud", Data]:
        data = super(InMemoryPointCloud, self).__getitem__(item)
        if not isinstance(item, int):
            data.metadata = data.metadata[item, :]

        return data
