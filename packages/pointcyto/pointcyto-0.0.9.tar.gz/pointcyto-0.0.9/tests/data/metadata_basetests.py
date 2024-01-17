import os
import shutil
from unittest import TestCase

import torch

from pointcyto.data.metadata_classification import MetaDataClassification
from pointcyto.testutils.helpers import find_dirname_above

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
# Now build the base-test directory (necessary if you want to use tests/testdata)
TESTS_DIR = find_dirname_above(THIS_DIR)


class BaseTests:
    class TestMetaData(TestCase):
        metadata = MetaDataClassification

        def test_empty_metadata(self):
            empty_meta = self.metadata()
            print(empty_meta)
            repr(empty_meta)

        def test_single_element_metadata(self):
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs"], class_name=["A"], orig_dir="."
            )
            print(my_meta)

        def test_single_element_metadata_applications(self):
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs"], class_name=["A"], orig_dir="."
            )
            # You cannot get a string value anymore from my_meta. Does not make any sense though.
            for key_x in my_meta.keys:
                with self.assertRaises(TypeError):
                    a = my_meta[key_x]
                    print(a)

            assert "is_this_key_in_meta?" not in my_meta

        def test_multiple_phenos(self):
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name={"pheno_1": ["x", "y"], "pheno_2": ["A", "B"]},
                orig_dir=".",
            )
            print(my_meta)

        def test_metadata_yaml_dump(self):
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name={"pheno_1": ["x", "y"], "pheno_2": ["A", "B"]},
                orig_dir=".",
            )
            import yaml

            with open("removeme.yaml", "w", encoding="utf-8") as yaml_file:
                dumped = yaml.dump(my_meta)
                yaml_file.write(dumped)

        def test_metadata_yaml_dump_rootproblem(self):
            # https://github.com/pandas-dev/pandas/issues/42748
            import pandas as pd

            tmp = pd.DataFrame({"col_name": [1, 2, 3, 4]})
            import yaml

            dumped = yaml.dump(tmp.to_dict())
            print(dumped)
            """
            !!python/object:pandas.core.frame.DataFrame
            _flags:
            allows_duplicate_labels: true
            _metadata: []
            _mgr: !!python/object/new:pandas.core.internals.managers.BlockManager
            state: !!python/tuple
            - &id004
                - !!python/object/apply:pandas.core.indexes.base._new_Index
                - &id002 !!python/name:pandas.core.indexes.base.Index ''
                - data: !!python/object/apply:numpy.core.multiarray._reconstruct
                    args:
                    - &id001 !!python/name:numpy.ndarray ''
                    - !!python/tuple
                        - 0
                    - !!binary |
                        Yg==
                    state: !!python/tuple
                    - 1
                    - !!python/tuple
                        - 1
                    - &id003 !!python/object/apply:numpy.dtype
                        args:
                        - O8
                        - false
                        - true
                        state: !!python/tuple
                        - 3
                        - '|'
                        - null
                        - null
                        - null
                        - -1
                        - -1
                        - 63
                    - false
                    - - col_name
                    name: null
                - !!python/object/apply:pandas.core.indexes.base._new_Index
                - !!python/name:pandas.core.indexes.range.RangeIndex ''
                - name: null
                    start: 0
                    step: 1
                    stop: 4
            - - &id005 !!python/object/apply:numpy.core.multiarray._reconstruct
                args:
                - *id001
                - !!python/tuple
                    - 0
                - !!binary |
                    Yg==
                state: !!python/tuple
                - 1
                - !!python/tuple
                    - 1
                    - 4
                - !!python/object/apply:numpy.dtype
                    args:
                    - i8
                    - false
                    - true
                    state: !!python/tuple
                    - 3
                    - <
                    - null
                    - null
                    - null
                    - -1
                    - -1
                    - 0
                - false
                - !!binary |
                    AQAAAAAAAAACAAAAAAAAAAMAAAAAAAAABAAAAAAAAAA=
            - - !!python/object/apply:pandas.core.indexes.base._new_Index
                - *id002
                - data: !!python/object/apply:numpy.core.multiarray._reconstruct
                    args:
                    - *id001
                    - !!python/tuple
                        - 0
                    - !!binary |
                        Yg==
                    state: !!python/tuple
                    - 1
                    - !!python/tuple
                        - 1
                    - *id003
                    - false
                    - - col_name
                    name: null
            - 0.14.1:
                axes: *id004
                blocks:
                - mgr_locs: !!python/object/apply:builtins.slice
                    - 0
                    - 1
                    - 1
                    values: *id005
            _typ: dataframe
            attrs: {}
            """

        def test_multiple_metadata_same_classmap(self):
            my_meta1 = self.metadata(
                raw_filenames=[
                    "nonexisting.fcs",
                    "nonexisting_2.fcs",
                    "nonexisting_3.fcs",
                ],
                class_name=["A", "B", "B"],
                orig_dir=".",
                sort_class_name_map=False,
            )
            my_meta2 = self.metadata(
                raw_filenames=[
                    "nonexisting.fcs",
                    "nonexisting_2.fcs",
                    "nonexisting_3.fcs",
                ],
                class_name=["B", "A", "B"],
                orig_dir=".",
                sort_class_name_map=False,
            )
            assert my_meta1.y == [0, 1, 1]  # Because A, B, B
            with self.assertRaises(AssertionError):
                assert my_meta2.y == [1, 0, 1]  # because B, A, B
            my_meta2.class_name_id_map = my_meta1.class_name_id_map
            assert my_meta1.y == [0, 1, 1]  # Because A, B, B
            assert my_meta2.y == [1, 0, 1]  # because B, A, B

            my_meta1 = self.metadata(
                raw_filenames=[
                    "nonexisting.fcs",
                    "nonexisting_2.fcs",
                    "nonexisting_3.fcs",
                ],
                class_name=["A", "B", "B"],
                orig_dir=".",
                sort_class_name_map=True,
            )  # this is default
            my_meta2 = self.metadata(
                raw_filenames=[
                    "nonexisting.fcs",
                    "nonexisting_2.fcs",
                    "nonexisting_3.fcs",
                ],
                class_name=["B", "A", "B"],
                orig_dir=".",
                sort_class_name_map=True,
            )  # this is default
            assert my_meta1.y == [0, 1, 1]  # Because A, B, B
            assert my_meta2.y == [1, 0, 1]  # because B, A, B

        def test_metadata_get_item(self):
            my_meta = self.metadata(
                raw_filenames=[
                    "nonexisting.fcs",
                    "nonexisting_2.fcs",
                    "nonexisting_3.fcs",
                ],
                class_name=["A", "B", "B"],
                orig_dir=".",
            )
            assert {
                "raw_filenames": "nonexisting.fcs",
                "processed_filenames": "nonexisting.pt",
                "y": 0,
                "class_name": "A",
                "sample_feature_names": None,
                "read_with": "parse_by_ext",
            } == my_meta[0]
            assert len(my_meta) == 3
            assert len(my_meta.pheno) == 3
            single_element = my_meta[0, 1]
            assert len(single_element) == 1
            assert (
                single_element.n_pheno == 2
            )  # because read_with is always part of pheno

            single_element_no_more_pheno = my_meta[0, 0]
            assert len(single_element_no_more_pheno) == 1
            assert single_element_no_more_pheno.n_pheno == 1

            assert {
                "raw_filenames": ["nonexisting.fcs", "nonexisting_2.fcs"],
                "processed_filenames": ["nonexisting.pt", "nonexisting_2.pt"],
                "y": [0, 1],
                "class_name": ["A", "B"],
                "sample_feature_names": [None, None],
                "read_with": ["parse_by_ext", "parse_by_ext"],
            } == my_meta[0:2]

            # Test different slicings of samples.
            a = my_meta[0:2, 1]
            assert ["nonexisting.fcs", "nonexisting_2.fcs"] == a.raw_filenames
            a = my_meta[0:1, 1]
            assert ["nonexisting.fcs"] == a.raw_filenames
            a = my_meta[0, 1]
            assert ["nonexisting.fcs"] == a.raw_filenames
            a = my_meta[:, 1]
            assert [
                "nonexisting.fcs",
                "nonexisting_2.fcs",
                "nonexisting_3.fcs",
            ] == a.raw_filenames
            a = my_meta[::2, 1]
            assert ["nonexisting.fcs", "nonexisting_3.fcs"] == a.raw_filenames

            # Test different slicings of phenodata
            my_meta.add_pheno_single(new_pheno_column=["x", "y", "x"])
            a = my_meta[:, 0:1]
            assert a.pheno.columns.values == ["read_with"]
            a = my_meta[:, :1]
            assert a.pheno.columns.values == ["read_with"]
            # You cannot delete read_with
            a = my_meta[:, 1:]
            assert all(a.pheno.columns.values == ["read_with", "pheno_1", "pheno_2"])
            a = my_meta[:, 2:]
            assert all(a.pheno.columns.values == ["read_with", "pheno_2"])
            a = my_meta[:, :]
            assert all(a.pheno.columns.values == ["read_with", "pheno_1", "pheno_2"])
            a = my_meta[:, ::2]
            assert all(a.pheno.columns.values == ["read_with", "pheno_2"])

        def test_metadata_get_item_by_index(self):
            import numpy as np

            my_meta = self.metadata(
                raw_filenames=[
                    "nonexisting.fcs",
                    "nonexisting_2.fcs",
                    "nonexisting_3.fcs",
                ],
                class_name=["A", "B", "B"],
                orig_dir=".",
            )
            train_indices = np.random.choice(
                len(my_meta), size=int(len(my_meta) * 0.8), replace=False
            )
            val_indices = [i for i in range(len(my_meta)) if i not in train_indices]
            assert len(my_meta[val_indices, :]) == len(val_indices)
            assert len(my_meta[train_indices, :]) == len(train_indices)
            assert len(my_meta[:, :]) == len(my_meta)

        def test_metadata_get_NO_item(self):
            my_meta = self.metadata(
                raw_filenames=[
                    "nonexisting.fcs",
                    "nonexisting_2.fcs",
                    "nonexisting_3.fcs",
                ],
                class_name=["A", "B", "B"],
                orig_dir=".",
            )
            empty_indices = []
            assert len(my_meta[empty_indices, :]) == 0

        def test_metadata_get_item_by_boolean(self):
            my_meta = self.metadata(
                raw_filenames=[
                    "nonexisting.fcs",
                    "nonexisting_2.fcs",
                    "nonexisting_3.fcs",
                ],
                class_name=["A", "B", "B"],
                orig_dir=".",
            )
            # print(my_meta)
            # print(my_meta.pheno['pheno_1'])
            boolean_b = my_meta.pheno["pheno_1"] == "B"
            # print(boolean_b)
            # print(my_meta.pheno[boolean_b])
            # print(my_meta.pheno.loc[boolean_b, :])
            part = my_meta[boolean_b, :]
            # print(part.raw_filenames)
            # print(part.pheno)

            assert len(part) == 2
            assert part.pheno["pheno_1"].tolist() == ["B", "B"]

        def test_metadata_get_item_by_boolean_list(self):
            my_meta = self.metadata(
                raw_filenames=[
                    "nonexisting.fcs",
                    "nonexisting_2.fcs",
                    "nonexisting_3.fcs",
                ],
                class_name=["A", "B", "B"],
                orig_dir=".",
            )
            boolean_b = my_meta.pheno["pheno_1"] == "B"
            boolean_b_list = [x for x in boolean_b]
            part = my_meta[boolean_b_list, :]
            # print(part.raw_filenames)
            # print(part.pheno)

            assert len(part) == 2
            assert part.pheno["pheno_1"].tolist() == ["B", "B"]

        def test_metadata_append_only_filename(self):
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            with self.assertRaises(KeyError):
                my_meta.append({"asdf": "No"})
            print(my_meta.raw_filenames)
            with self.assertRaises(ValueError):
                my_meta.append({"raw_filenames": "a.fcs"})
            my_meta.append({"raw_filenames": ["a.fcs"]})
            assert my_meta.raw_filenames == [
                "nonexisting.fcs",
                "nonexisting_2.fcs",
                "a.fcs",
            ]
            assert my_meta.processed_filenames == [
                "nonexisting.pt",
                "nonexisting_2.pt",
                "a.pt",
            ]
            import numpy as np

            assert list(my_meta.pheno.iloc[2]) == [np.nan, np.nan]

        def test_metadata_append_with_sample_feature_names(self):
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            assert my_meta.feature_names is None

            with self.assertWarns(UserWarning):
                # The appended sample (3rd sample) has different feature names than the other samples (=None)
                # UserWarning: Feature names are not identical!
                my_meta.append(
                    {
                        "raw_filenames": ["a.fcs"],
                        "sample_feature_names": ["a", "b", "c"],
                    }
                )
            assert not my_meta.feature_names_identical

            # Set the sample_feature_names of the sample 0 and 1, but different to sample 2
            with self.assertWarns(UserWarning):
                # UserWarning: Feature names are not identical!
                my_meta.sample_feature_names = {
                    "feature_names": ["a", "b"],
                    "sample": 0,
                }
            assert not my_meta.feature_names_identical
            with self.assertWarns(UserWarning):
                # UserWarning: Feature names are not identical!
                my_meta.sample_feature_names = {
                    "feature_names": ["a", "b"],
                    "sample": 1,
                }
            assert not my_meta.feature_names_identical

            # Now replace the feature names of sample 2 with the same as sample 0 and 1
            my_meta.sample_feature_names = {"feature_names": ["a", "b"], "sample": 2}
            assert my_meta.feature_names_identical

        def test_metadata_append_with_pheno(self):
            import pandas as pd

            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            with self.assertRaises(TypeError):
                my_meta.append({"raw_filenames": ["a.fcs"], "pheno": ["A"]})
            with self.assertRaises(ValueError):
                pd.DataFrame({"pheno_1": "A"})

            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            samples_pheno = pd.DataFrame({"pheno_1": ["A"]})
            my_meta.append({"raw_filenames": ["a.fcs"], "pheno": samples_pheno})

            samples_pheno = pd.DataFrame({"pheno_1": ["not_present_class"]})
            my_meta.append({"raw_filenames": ["a.fcs"], "pheno": samples_pheno})
            assert my_meta.class_name_id_map == {"A": 0, "B": 1, "not_present_class": 2}

            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
                allow_class_extension=False,
            )
            samples_pheno = pd.DataFrame({"pheno_1": ["not_present_class"]})
            with self.assertRaises(ValueError):
                my_meta.append({"raw_filenames": ["a.fcs"], "pheno": samples_pheno})

        def test_concat(self):
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            my_meta_2 = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            with self.assertRaises(ValueError):
                # Filenames are identical and orig_dir also
                my_meta.concat(my_meta_2)

            my_meta_2 = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir="asdf",
            )
            with self.assertRaises(ValueError):
                # ValueError: Can only concat MetaData with the same orig_dir because
                # raw_filenames are relative to that.
                my_meta.concat(my_meta_2)

            my_meta_2 = self.metadata(
                raw_filenames=["nonexisting_3.fcs", "nonexisting_4.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            my_meta.concat(my_meta_2, inplace=True)
            with self.assertRaises(ValueError):
                # ValueError: Supply another MetaData object
                my_meta.concat(["A", "B"])
            print(my_meta)

            assert len(my_meta) == 4
            new_copied = my_meta.concat(my_meta_2, inplace=False)
            assert len(my_meta) == 4
            assert len(new_copied) == 6

        def test_metadata_set_item(self):
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            # set a complete attribute
            my_meta.raw_filenames = ["b.fcs", "a.fcs", "asd.fcs"]
            with self.assertRaises(TypeError):
                my_meta["raw_filenames"] = ["b.fcs", "a.fcs", "asd.fcs"]
            my_meta.raw_filenames = ["b.fcs", "a.fcs"]
            # assert my_meta["raw_filenames"] == ['b.fcs', 'a.fcs']

        def test_metadata_keys(self):
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )

            a = my_meta.keys
            # I dont know how to check a now. but say this works and I just check here if it works at all.
            repr(a)

        def test_metadata_len(self):
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )

            assert len(my_meta) == 2

        def test_metadata_contains(self):
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            assert "orig_dir" in my_meta
            assert "_feature_names" in my_meta
            assert "this string cannot be in the metadata" not in my_meta

        def test_metadata_iter(self):
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )

            for iteration_X in my_meta:
                a = iteration_X
                repr(a)

        def test_metadata_call(self):
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )

            a = my_meta(0, 1)
            i = 0
            for a_part in a:
                assert a_part == my_meta[i]
                i += 1
            a = my_meta()
            i = 0
            for a_part in a:
                assert a_part == my_meta[i]
                i += 1
            assert i == len(my_meta)

            with self.assertRaises(IndexError):
                a = my_meta(2)
                next(a)

        def test_metadata_repr(self):
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            # print(my_meta)  # I dont want a printout in the test, so repr() does the same just not printing it.
            repr(my_meta)

        def test_metadata_test_equal(self):
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            assert my_meta == my_meta

            b = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            assert my_meta == b

            not_my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "different_class_here"],
                orig_dir=".",
            )
            assert my_meta != not_my_meta

        def test_metadata_cloning(self):
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            import copy

            prev_filenames = my_meta.raw_filenames[0]
            b = my_meta
            b.raw_filenames[0] = "a"
            assert (
                my_meta.raw_filenames[0] == b.raw_filenames[0]
            )  # This is expected but possibly unwanted behaviour.
            assert (
                prev_filenames != b.raw_filenames[0]
            )  # This is expected but possibly unwanted behaviour.

            # But if we do NOT want this, we have to clone. And I have to get this running.
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            b = copy.deepcopy(my_meta)
            b.raw_filenames[0] = "a"
            assert my_meta.raw_filenames[0] != b.raw_filenames[0]
            assert prev_filenames != b.raw_filenames[0]

            # To check the "special cases" (see __setitem__)
            b.class_colors = "asdf"
            assert my_meta.class_colors != b.class_colors
            print(my_meta)

        def test_feature_names_identical(self):
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            myfeatures = ["a", "b", "c"]
            assert my_meta.feature_names_identical
            # print("featurenames:", my_meta.feature_names)
            assert my_meta.feature_names is None
            my_meta.sample_feature_names = [myfeatures, myfeatures]
            assert my_meta.feature_names == myfeatures
            assert my_meta.feature_names_identical
            with self.assertWarns(UserWarning):
                my_meta.sample_feature_names = [myfeatures, None]
            assert my_meta.feature_names == [
                "Feature names NOT identical over samples!"
            ]
            assert not my_meta.feature_names_identical

            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            my_meta.sample_feature_names[0] = myfeatures
            # print(my_meta.sample_feature_names)
            assert my_meta.sample_feature_names == [myfeatures, None]
            assert (
                my_meta.feature_names_identical
            )  # Even if the feature names are not NOT identical, this is true.
            # But this is intended behaviour because my_meta.sample_feature_names[0] = myfeatures
            #   1. selects my_meta.sample_feature_names
            #   2. replaces the 0th element
            # therefore the setter of my_meta.sample_feature_names is not called anytime.

            # In contrast, the following works:
            my_meta.sample_feature_names = [myfeatures, myfeatures]
            assert my_meta.feature_names_identical
            with self.assertWarns(UserWarning):
                my_meta.sample_feature_names = [myfeatures, None]
            assert not my_meta.feature_names_identical

        def test_metadata_supply_class_to_idx(self):
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            # print(my_meta.class_name_id_map)
            repr(my_meta.class_name_id_map)
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            # print(my_meta.class_name_id_map)
            repr(my_meta.class_name_id_map)

        def test_metadata_supply_class_to_idx_missing_key(self):
            # If a n empty dict is supplied, class_to_idx is generated automatically
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            repr(my_meta.class_name_id_map)

        def test_metadata_save_load(self):
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            torch.save(my_meta, "removeme.pt")
            my_meta_loaded = torch.load("removeme.pt")
            os.remove("removeme.pt")
            assert my_meta == my_meta_loaded

            # Check if this is now really a new object and not a new pointer.
            print(my_meta.raw_filenames)
            my_meta.raw_filenames[0] = "asdf"
            print(my_meta.raw_filenames)
            print(my_meta.processed_filenames)
            assert my_meta != my_meta_loaded

        def test_proc_from_raw_filenames(self):
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            assert my_meta.processed_filenames == ["nonexisting.pt", "nonexisting_2.pt"]
            my_meta.raw_filenames = ["a.fcs", "b.fcs"]
            assert my_meta.processed_filenames == ["a.pt", "b.pt"]

        def metadata_testing(self, meta, verbose: bool = False):
            if verbose:
                print(meta.pheno)
            n_starting_columns = len(meta.pheno.columns)
            with self.assertRaises(AttributeError):
                meta.class_name = [
                    "x",
                    "y",
                ]  # I cannot set attributes here (This was possible previous 2020-02-21)
            assert len(meta.pheno.columns) == n_starting_columns
            assert meta.class_name == ["A", "B"]
            meta.add_pheno_single(["x", "y"], "new_vals")
            if verbose:
                print(meta.pheno)
            assert len(meta.pheno.columns) == n_starting_columns + 1
            assert meta.pheno.columns[2] == "new_vals"
            # I have to select the proper column before class_name also gets different values
            assert meta.class_name == ["A", "B"]
            meta.selection = "new_vals"
            print(meta.class_name)
            assert meta.class_name == ["x", "y"]
            # I can also switch the columns when selecting the column number
            meta.selection = 1
            assert meta.class_name == ["A", "B"]
            with self.assertRaises(IndexError):
                meta.selection = 3
            with self.assertRaises(ValueError):
                meta.add_pheno_single(["x", "y", "z"])
            meta.add_pheno_single(["u", "v"])
            if verbose:
                print(meta.pheno)
            assert len(meta.pheno.columns) == n_starting_columns + 2

        def test_add_pheno_single(self):
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            self.metadata_testing(my_meta)

        def test_add_pheno_single_missing_index(self):
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            my_meta.add_pheno_single([0, 2], col_name="new_index")
            # when actually using the metadata the MetaData.pheno index is probably not ordered.
            # I have to deal with that.
            my_meta.pheno.set_index("new_index", inplace=True)
            self.metadata_testing(my_meta)
            import pandas as pd

            a = pd.DataFrame({"another_col": [1, 2]})
            my_meta.add_pheno_single(new_pheno_column=a, replace_new_df_index=True)
            assert list(my_meta.pheno["another_col"]) == [1, 2]
            a = pd.DataFrame({"another_col2": [1, 2]})

            with self.assertWarns(UserWarning):
                # UserWarning: new_pheno_column.index is NOT equal to the current self.pheno.index **
                # ** your given new_pheno_column is reordered and/or can contain Nan!
                my_meta.add_pheno_single(new_pheno_column=a, replace_new_df_index=False)

            with self.assertRaises(AssertionError):
                # The index is not replaced, therefore it tries to find in the new dataset the index "2"
                # which just does not exist.
                assert list(my_meta.pheno["another_col2"]) == [1, 2]

        def test_add_pheno_single_switched_index(self):
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            # I actively set the index to something else than the default.
            # Don't do that actively, but it can happen.
            # when actually using the metadata, the MetaData.pheno index is probably not ordered.
            # I have to deal with that.
            my_meta.add_pheno_single([1, 0], col_name="new_index")
            my_meta.pheno.set_index("new_index", inplace=True)
            # print(my_meta.pheno)

            self.metadata_testing(my_meta, verbose=True)
            import pandas as pd

            a = pd.DataFrame({"another_col": [1, 2]})
            b = pd.DataFrame({"another_col2": [1, 2]})
            with self.assertWarns(UserWarning):
                # Pandas tries to merge the dataframes by index, but the index is not identical.
                # So the user now would _think_ that the added column is ordered as given
                # but it is not. So I warn the user.
                my_meta.add_pheno_single(new_pheno_column=a, replace_new_df_index=False)
                print(my_meta.pheno)
                # Note that the print() above shows that "another_col" is
                # [2, 1] instead of the given [1, 2].
                # This is because the index is not replaced.
                assert list(my_meta.pheno["another_col"]) == [2, 1]
            # With the option to replace the index, the order is as expected and no warning
            # is raised.
            my_meta.add_pheno_single(new_pheno_column=b, replace_new_df_index=True)
            assert list(my_meta.pheno["another_col2"]) == [1, 2]

        def test_add_pheno_dataframe(self):
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            self.metadata_testing(my_meta)
            import pandas as pd

            new_pheno_dict = {"another_col": [1, 2], "another_col2": [2, 4]}
            a = pd.DataFrame(new_pheno_dict)
            my_meta.add_pheno(a)
            assert list(my_meta.pheno.columns[-2:]) == ["another_col", "another_col2"]

            my_meta.add_pheno_single([0, 2], col_name="new_index")
            # when actually using the metadata the MetaData.pheno index is probably not ordered.
            # I have to deal with that.
            my_meta.pheno.set_index("new_index", inplace=True)
            a = pd.DataFrame({"blub_1": [1, 2], "blub_2": [3, 4]})
            my_meta.add_pheno(new_pheno=a, replace_new_df_index=True)
            assert list(my_meta.pheno["blub_1"]) == [1, 2]
            assert list(my_meta.pheno["blub_2"]) == [3, 4]
            a = pd.DataFrame({"blub_3": [1, 2], "blub_4": [3, 4]})

            with self.assertWarns(UserWarning):
                my_meta.add_pheno(new_pheno=a, replace_new_df_index=False)
            # print(my_meta.pheno)
            with self.assertRaises(AssertionError):
                # The index is not replaced, therefore it tries to find in the new dataset the index "2"
                # which just does not exist.
                assert list(my_meta.pheno["blub_3"]) == [1, 2]

        def test_add_pheno_dict(self):
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            self.metadata_testing(my_meta)
            new_pheno_dict = {"another_col": [1, 2], "another_col2": [2, 4]}
            my_meta.add_pheno(new_pheno_dict)
            assert list(my_meta.pheno.columns[-2:]) == ["another_col", "another_col2"]

        def test_only_numeric_classes(self):
            # Here typehinting calls you out because you supply numeric values instead of strings for the class names.
            # So.. that works BUT your class names are NOT the actual class indices!
            # (only by chance, but you can ABSOLUTELY NOT count on that!!!)
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=[1, 0],
                orig_dir=".",
            )
            repr(my_meta)

        def test_class_color_dicts(self):
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=["A", "B"],
                orig_dir=".",
            )
            repr(my_meta)
            assert my_meta.class_id_color_dict() == {
                0: (0.0, 0.0, 0.5, 0.2),
                1: (0.5, 0.0, 0.0, 0.2),
            }
            assert my_meta.class_name_color_dict() == {
                "A": (0.0, 0.0, 0.5, 0.2),
                "B": (0.5, 0.0, 0.0, 0.2),
            }

        def test_class_color_dicts_numeric_classes(self):
            # Here typehinting calls you out because you supply numeric values instead of strings for the class names.
            # So.. that works BUT your class names are NOT the actual class indices!
            # (only by chance, but you can ABSOLUTELY NOT count on that!!!)
            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=[1, 0],
                orig_dir=".",
            )
            repr(my_meta)
            assert my_meta.class_id_color_dict() == {
                0: (0.0, 0.0, 0.5, 0.2),
                1: (0.5, 0.0, 0.0, 0.2),
            }

            # Update: Values are not switched anymore because of default-sorting. But you can enforce that by the next
            # metadata call.
            assert my_meta.class_name_color_dict() != {
                1: (0.0, 0.0, 0.5, 0.2),
                0: (0.5, 0.0, 0.0, 0.2),
            }

            my_meta = self.metadata(
                raw_filenames=["nonexisting.fcs", "nonexisting_2.fcs"],
                class_name=[1, 0],
                orig_dir=".",
                sort_class_name_map=False,
            )
            assert my_meta.class_name_color_dict() == {
                1: (0.0, 0.0, 0.5, 0.2),
                0: (0.5, 0.0, 0.0, 0.2),
            }

        def tearDown(self) -> None:
            for dirX in os.listdir(os.pardir):
                if dirX.startswith("autoroot_datasets"):
                    shutil.rmtree(os.path.join(os.pardir, dirX))
