import os
import pathlib
import pickle
import time
import warnings
from math import inf
from typing import Any, List, Optional

import pytorch_lightning
import torch_geometric
from torch_geometric.data.dataset import Dataset

from pointcyto.data.InMemoryPointCloud import InMemoryPointCloud
from pointcyto.data.metadata_base import MetaDataBase


def generate_load_data_wait(
    metadata: MetaDataBase,
    lock_file: str = "/tmp/lock.generate_load_data",
    wait_seconds: int = 5,
    max_wait_seconds: int = None,
    **kwargs
):
    def lock_process_data():
        # generate a lock
        open(lock_file, "a").close()
        # generate the data
        res = generate_load_data(metadata=metadata, **kwargs)
        # remove the lock after finishing
        os.remove(lock_file)
        return res

    if max_wait_seconds is None:
        max_wait_seconds = inf  # from math
    t0 = time.time()
    if os.path.exists(lock_file):
        while time.time() - t0 < max_wait_seconds:
            if os.path.exists(lock_file):
                print("Waiting because ", lock_file, " exists")
                time.sleep(wait_seconds)
            else:
                # when the lock_file does not exist anymore we can load the data
                res = generate_load_data(metadata=metadata, **kwargs)
                # After loading we can exit the waiting-loop.
                break
        if os.path.exists(lock_file):
            # If the file STILL exists after the waiting time, remove it by force, maybe the
            # generating process failed?
            print(
                "Removing ",
                lock_file,
                " EVEN IF IT EXISTS after max_wait_seconds was exceeded!",
            )
            os.remove(lock_file)
            res = lock_process_data()
    else:
        res = lock_process_data()

    return res


def generate_load_data(
    metadata: MetaDataBase,
    datagenerator_seed: int = 51284,
    basis_pointcloud: InMemoryPointCloud = None,
    prepretrans_parameters_picklefile: pathlib.Path = None,
    pointcloud_generator: Dataset = InMemoryPointCloud,
    transform: Optional[Any] = None,
    pre_transform: List[Any] = None,
    pre_pre_transform_param_onlist=None,
    clear_processed: bool = False,
    **kwargs
):
    """_summary_

    Args:
        metadata (MetaDataBase): _description_
        datagenerator_seed (int): _description_
        basis_pointcloud (InMemoryPointCloud, optional): _description_. Defaults to None.
        pointcloud_generator (Dataset, optional): _description_. Defaults to InMemoryPointCloud.
        transform (Optional[Any], optional): _description_. Defaults to None. E.g.
            FixedPoints(
                num=n_points_per_sample, replace=False, allow_duplicates=False
            )
        pre_transform (List[Any], optional): _description_. Defaults to None.
        pre_pre_transform_param_onlist (_type_, optional): _description_. Defaults to None.
        clear_processed (bool, optional): _description_. Defaults to False.
        kwargs:
            Further arguments to pointcloud_generator

    Returns:
        _type_: _description_
    """
    if basis_pointcloud is not None or prepretrans_parameters_picklefile is not None:
        if prepretrans_parameters_picklefile is None:
            # If there is a basis pointcloud (usually the training data) which should be used, load their
            # pretransform_parameters.
            prepretrans_parameters_picklefile = os.path.join(
                basis_pointcloud.processed_dir, "pretransform_parameter.pickle"
            )
        else:
            warnings.warn(
                "You gave basis_pointcloud and prepretrans_parameters_picklefile\n"
                + "Only the prepretrans_parameters_picklefile is used."
            )

        # Use the saved pretransform parameters which are saved by pre_pre_transform_param_onlist
        # to use then as pre_transform for the validation dataset
        with open(prepretrans_parameters_picklefile, "rb") as f:
            pre_pre_transforms_saved = pickle.load(f)

        insert_ppt = [
            single_pretransform["related_transform"](**single_pretransform["param"])
            for single_pretransform in pre_pre_transforms_saved
        ]
        if pre_transform is not None:
            if not isinstance(pre_transform, list):
                pre_transform = [pre_transform]
            pre_transform = pre_transform + insert_ppt

        else:
            pre_transform = insert_ppt
        pre_transform_composed = torch_geometric.transforms.compose.Compose(
            pre_transform
        )
        if pre_pre_transform_param_onlist is not None:
            warnings.warn(
                "Are you sure you want to add a pre_pre_transform_param_onlist when supplying a basis_pointcloud?"
            )
    else:
        pre_transform_composed = pre_transform

    pytorch_lightning.seed_everything(datagenerator_seed)
    generated_pointcloud = pointcloud_generator(
        metadata=metadata,
        transform=transform,
        pre_transform=pre_transform_composed,
        pre_pre_transform_param_onlist=pre_pre_transform_param_onlist,
        clear_processed=clear_processed,
        **kwargs
    )
    return generated_pointcloud
