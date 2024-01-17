import os
import pickle
import shutil
import warnings
from typing import Any, Dict

import torch
from torch_geometric.data import Dataset

from pointcyto.data.metadata_base import MetaDataBase
from pointcyto.io.parse_by_ext import parse_by_ext


class PointCloud(Dataset):
    """
    Currently **DEPRECATED**
    """

    def __init__(
        self,
        metadata: MetaDataBase,
        transform=None,
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
                A MetaDataBase object containing all relevant information
            transform:
                Transformations for the pytorch_geometric Data object
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

                .. code-block::

                    parsed = self.loading_function(
                        path=os.path.join(self.metadata.orig_dir, metadata_X["raw_filenames"]),
                        y=metadata_X["y"],
                        **self.loading_function_args
                    )

        Returns:
            No return
        """
        warnings.warn(
            "PointCloud is deprecated at the moment but not needed for probably up to 1k samples and "
            + "25k points per samples depending on your RAM - use InMemoryPointCloud until this is not "
            + "deprecated anymore.",
            DeprecationWarning,
        )

        self.loading_function = loading_function
        self.loading_function_args: Dict[str, Any]
        if loading_function_arguments is None:
            self.loading_function_args = {}
        else:
            self.loading_function_args = loading_function_arguments

        self.metadata = metadata
        if clear_processed:
            try:
                shutil.rmtree(os.path.join(self.metadata.root, "processed"))
            except FileNotFoundError:  # then it was already deleted
                pass

        # process is called inside here, therefore everything which is used in process must be defined before.
        super(PointCloud, self).__init__(
            root=metadata.root, transform=transform, pre_transform=pre_transform
        )

        previous_pointcloud_metadata_path = os.path.join(
            self.processed_dir, "pointcloud_metadata.pickle"
        )
        if os.path.exists(previous_pointcloud_metadata_path):
            # if it doesnt exist it may not have been initialized anytime before.
            with open(previous_pointcloud_metadata_path, "rb") as f:
                self.metadata = pickle.load(f)

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
        return self.metadata.processed_filenames

    # I will never download data as they are assumed to be local.
    def download(self):
        # Would download raw data into raw_dir.
        pass

    def process(self):
        # Processes raw data and saves it into the processed_dir.
        # Read data into huge `Data` list.
        sample_feature_names = []
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
            parsed = self.loading_function(
                path=os.path.join(self.metadata.orig_dir, metadata_X["raw_filenames"]),
                y=metadata_X["y"],
                **self.loading_function_args
            )
            sample_feature_names += [parsed["features"]]
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
            data = parsed["point_data"]

            if self.pre_filter is not None:
                data = self.pre_filter(data)

            if self.pre_transform is not None:
                data = self.pre_transform(data)

            current_proc_dir = os.path.realpath(
                os.path.join(self.processed_paths[metadata_N], os.pardir)
            )
            if not os.path.exists(current_proc_dir):
                os.makedirs(current_proc_dir)

            # Todo: If I want to use different savetypes, self.metadata.savetype is the thing to look at
            #       and here is the place to insert it. (Probably also in __getitem__() or get())
            torch.save(data, self.processed_paths[metadata_N])
        self.metadata.sample_feature_names = sample_feature_names
        with open(
            os.path.join(self.processed_dir, "pointcloud_metadata.pickle"), "wb"
        ) as f:
            pickle.dump(self.metadata, file=f)

    def select_output_of_meta(self):
        # Todo: This must be done!
        raise NotImplementedError

    def len(self):
        return len(self.raw_file_names)

    def get(self, idx):
        return torch.load(self.processed_paths[idx])

    def __getitem__(self, item) -> "PointCloud":
        data = super(PointCloud, self).__getitem__(item)
        if not isinstance(item, int):
            print("\n\n\nasldfkjh")
            print(data.metadata)
            data.metadata = data.metadata[item, :]
            print(data.metadata)
            print("\n\n\n")
        return data
