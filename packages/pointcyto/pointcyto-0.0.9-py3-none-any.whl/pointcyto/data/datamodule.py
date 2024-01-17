import copy
import pickle
import re
from typing import Any, Dict, List, Literal, Union

import pytorch_lightning as pl
import torch_geometric

from pointcyto.data.InMemoryPointCloud import InMemoryPointCloud
from pointcyto.data.metadata_base import MetaDataBase


class PCDataModule(pl.LightningDataModule):
    def __init__(
        self,
        meta_train: Dict[str, Union[MetaDataBase, str, Dict[str, Any]]] = None,
        meta_val: Dict[str, Union[MetaDataBase, str, Dict[str, Any]]] = None,
        meta_test: Dict[str, Union[MetaDataBase, str, Dict[str, Any]]] = None,
        meta_predict: Dict[str, Union[MetaDataBase, str, Dict[str, Any]]] = None,
        pointcloud_args_datapart: Dict[str, Dict[str, Any]] = None,
        pointcloud_generator=InMemoryPointCloud,
        batch_size: int = 43,
        num_workers: int = 0,
        must_prepare: bool = True,
        clear_processed: bool = False,
    ):
        """Pointcloud DataModule

        https://pytorch-lightning.readthedocs.io/en/latest/data/datamodule.html#lightningdatamodule-api

        Args:
            meta_XXX (Dict[str, Union[MetaDataBase str]], optional):
                `meta_["train", "val", "test", "predict"]`
                For tvtp-part, give a dictionary for the dataparts.
                If an element contains a _dictionary_, this is directly fed into `InMemoryPointcloud(**kwargs)` AND
                takes precedence over `pointcloud_args_datapart`!

                E.g.
                ```
                    meta_train = {
                        "dataA": "path_to_metadata_object",
                        "dataB": MetaDataBaseobject_B,
                        "dataC": {
                            "metadata": <path_OR_MetaDataObject>,
                            "pre_pre_transform_param_onlist": ...,
                            <further InMemoryPointCloud arguments>: <their values>
                        }
                    }

                Each element is finally brought into the format
                    "dataC": {
                        "metadata": <path_OR_MetaDataObject>,
                        "pre_pre_transform_param_onlist": ...,
                        <further InMemoryPointCloud arguments>: <their values>
                    }
                using `pointcloud_args_datapart`. If `pointcloud_args_datapart` is None, the
                result will be:
                    "dataC": {
                        "metadata": <path_OR_MetaDataObject>,
                    }
                and therefore an InMemoryPointCloud WITHOUT any parameters will be generated
                ```

                Defaults to None.
            pointcloud_args_datapart Dict[str, Dict[str, Any]]:
                If given, the datapart args
            pointcloud_generator (_type_, optional): _description_. Defaults to InMemoryPointCloud.
            batch_size (int, optional):
                Given to torch_geometric.loader.DataLoader(). Defaults to 43.
            num_workers (int, optional):
                Given to torch_geometric.loader.DataLoader(). Defaults to 0.
            must_prepare (bool, optional):
                When calling calling `PCDataModule.setup()`, is it mandatory to have called
                `PCDataModule.prepare_data()` first?

                Defaults to True.
            clear_processed (bool, optional):
                If True force all dataparts to have clear_processed = True therefore all PointClouds
                get reprocessed.
        """

        super().__init__()
        self.pointcloud_generator = pointcloud_generator
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.must_prepare = must_prepare
        self.meta_conf_xxx = {
            "train": copy.deepcopy(meta_train),
            "val": copy.deepcopy(meta_val),
            "test": copy.deepcopy(meta_test),
            "predict": copy.deepcopy(meta_predict),
        }
        dataparts = None
        for meta_key, meta_dataparts in self.meta_conf_xxx.items():
            if meta_dataparts is None:
                continue
            if not isinstance(meta_dataparts, dict):
                raise ValueError(
                    f"meta_{meta_key} should be a dictionary like"
                    + "{'dataA': metadata}"
                )
            # Check that all existing dataparts have the same datapart-names
            if dataparts is None:
                dataparts = set(meta_dataparts.keys())
            else:
                if dataparts != set(meta_dataparts.keys()):
                    raise ValueError(
                        f"Given {meta_key} contains different part-names than the existing ones."
                        + f"\nExisting: {*dataparts,}"
                        + f"\nNew ({meta_key}): {*list(meta_dataparts.keys()),}"
                    )

            # Generate the dictionary containing the metadata paths and arguments for InMemoryPointCloud
            # "dp" := "datapart"
            for dp_name, dp_value in meta_dataparts.items():
                if isinstance(dp_value, dict):
                    if "metadata" in dp_value.keys():
                        # Then we have a defined PointCloud already, do nothing
                        pass
                    else:
                        # Then we have a defined PointCloud already, but the metadata
                        # (where to load the data from) is missing
                        raise ValueError(
                            f"Given {meta_key}:{dp_name} is a dict but does not contain 'metadata' as key (It HAS to)."
                        )
                else:
                    if isinstance(dp_value, str):
                        # Then the current dp_value is
                        #   "dataA": "path_to_metadata_object",
                        with open(dp_value, "rb") as f:
                            metadata = pickle.load(f)
                    elif isinstance(dp_value, MetaDataBase):
                        #   "dataA": MetaDataBaseobject_B,
                        metadata = dp_value
                    else:
                        raise ValueError(
                            f"Given {meta_key}:{dp_name} is neither a dict, nor a string, not a MetaDataBase object."
                        )
                    new_dp_value = {"metadata": metadata}
                    if pointcloud_args_datapart is not None:
                        # pointcloud_args_datapart: Dict[str, Dict[str, Any]]
                        # {
                        #     "dataA": {
                        #         "transform": FixedPoints(100, replace=True),
                        #     },
                        # }
                        if set(pointcloud_args_datapart.keys()) != dataparts:
                            raise ValueError(
                                "pointcloud_args_datapart had different keys than dataparts:"
                                + f"\n{set(pointcloud_args_datapart.keys())}\n{dataparts}\n"
                            )
                        new_dp_value.update(pointcloud_args_datapart[dp_name])
                    self.meta_conf_xxx[meta_key][dp_name] = new_dp_value
        # After this initialization,
        # `self.meta_xxx` is a dictionary where for every element (train, val, test, predict)
        # it looks as following:
        #   {
        #     "dataA": {
        #         "metadata": MetaDataObject,
        #         <further InMemoryPointCloud arguments>: <values>
        #     },
        #     "dataB": {
        #         "metadata": MetaDataObject,
        #         <further InMemoryPointCloud arguments>: <values>
        #     }
        #   }

        if clear_processed:
            # Then force all dataparts to have clear_processed = True
            # therefore all PointClouds get reprocessed
            for meta_key, meta_dataparts in self.meta_conf_xxx.items():
                if meta_dataparts is not None:
                    # "dp" := "datapart"
                    for dp_name, dp_value in meta_dataparts.items():
                        self.meta_conf_xxx[meta_key][dp_name]["clear_processed"] = True

        # pointcloud_xxx (xxx = train, val, test, predict)
        # Is not necessarily InMemoryPointCloud but could be usual PointCloud
        self.pc_xxx: Dict[
            Literal["train", "val", "test", "predict"], InMemoryPointCloud
        ] = {}

    def prepare_data(self, clear_processed: bool = False):
        """Prepare the data

        Downloading and preprocessing. Usually set up all given data sources with InMemoryPointCloud.

        From pytorch-lightning documentation:
            prepare_data is called from the main process. It is not recommended to assign state here
            (e.g. self.x = y) since it is called on a single process and if you assign states here
            then they won't be available for other processes.
        """
        for tvt_name, tvt in self.meta_conf_xxx.items():
            if tvt is not None:
                # "dp" := "datapart"
                for dp_name, dp_value in tvt.items():
                    if clear_processed:
                        dp_value["clear_processed"] = True
                    self.pointcloud_generator(**dp_value)
                    # If `clear_processed` was True in the beginning, after the data was initially
                    # loaded (=prepared), this should not be loaded over and over again, therefore
                    # set `clear_processed` to False
                    self.meta_conf_xxx[tvt_name][dp_name].update(
                        {"clear_processed": False}
                    )
        self.must_prepare = False

    def _stage_interpreter(
        self, stage: Literal["fit", "validate", "test", "predict"] = None
    ) -> List[Literal["train", "val", "test", "predict"]]:
        if stage in ["train", "val", "test", "predict"]:
            return [stage]

        if stage is None:
            stage_list = list(self.meta_conf_xxx.keys())
        else:
            if stage == "fit":
                stage_list = ["train", "val"]
            elif stage == "validate":
                stage_list = ["val"]
            elif stage in ["test", "predict"]:
                stage_list = [stage]
            else:
                raise ValueError(f"DataModule: I do not know how to .setup() {stage}")
        return stage_list

    def setup(self, stage: Literal["fit", "validate", "test", "predict"] = None):
        if self.must_prepare:
            raise ValueError(
                "self.must_prepare is True, call PCDataModule.prepare_data() before .setup()"
            )
        stage_list = self._stage_interpreter(stage)

        for stage in stage_list:
            if self.meta_conf_xxx[stage] is not None:
                self.pc_xxx[stage] = {}
                for dp_name, dp_value in self.meta_conf_xxx[stage].items():
                    self.pc_xxx[stage][dp_name] = self.pointcloud_generator(**dp_value)

    def _part_dataloader(self, tvtp: Literal["train", "val", "test", "predict"]):
        try:
            return pl.utilities.combined_loader.CombinedLoader(
                {
                    datapart: torch_geometric.loader.DataLoader(
                        pc_xxx_datapart,
                        batch_size=self.batch_size,
                        shuffle=False,
                        num_workers=self.num_workers,
                    )
                    for datapart, pc_xxx_datapart in self.pc_xxx[tvtp].items()
                }
            )
        except KeyError:
            raise KeyError(f"Did you call PCDataModule.setup({tvtp})?")

    def train_dataloader(self):
        return self._part_dataloader("train")

    def val_dataloader(self):
        return self._part_dataloader("val")

    def test_dataloader(self):
        return self._part_dataloader("test")

    def predict_dataloader(self):
        return self._part_dataloader("predict")

    def __repr__(self) -> str:
        rstr = ""
        for tvtp, tvtp_values in self.meta_conf_xxx.items():
            rstr += f"\n\n{tvtp}\n"
            if tvtp_values is not None:
                for dp_name, dp_value in tvtp_values.items():
                    rstr += f"\n  {dp_name}" + re.sub(
                        r"\n", r"\n     ", r"\n" + dp_value.__repr__() + "\n"
                    )

        return rstr
