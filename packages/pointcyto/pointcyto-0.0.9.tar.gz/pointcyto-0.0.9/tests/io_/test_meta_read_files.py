import os
import shutil
from unittest import TestCase

from pointcyto.io.meta_read_foldering import (
    find_classes,
    gen_csv_meta,
    gen_foldering_meta,
    gen_meta_filenames,
    make_dataset,
)
from pointcyto.io.utils import convert_class_id_names
from pointcyto.testutils.helpers import find_dirname_above

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
# Now build the base-test directory (necessary if you want to use tests/testdata)
TESTS_DIR = find_dirname_above(THIS_DIR)

pointcloud_toy_dataset = os.path.join(
    "testdata", "flowcytometry", "PointClouds_toy_dataset"
)
pointcloud_toy_dataset_csvpheno = os.path.join(
    "testdata", "flowcytometry", "PointClouds_toy_phenocsv"
)


class Test(TestCase):
    def test_generate_foldering_meta(self):
        tmp = gen_foldering_meta(
            os.path.realpath(os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw"))
        )
        repr(tmp)
        # Add additional optional parameters to MetaData
        tmp = gen_foldering_meta(
            os.path.realpath(os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")),
            root="asdf",
            savetype="csv",
        )
        repr(tmp)
        os.rmdir("asdf")

    def test_convert_class_id_names(self):
        orig_dir = os.path.join(TESTS_DIR, pointcloud_toy_dataset, "raw")
        classes_classtoidx = find_classes(orig_dir)
        fullpath_class_metadata = make_dataset(orig_dir, classes_classtoidx[1])
        relative_paths_class = [
            (path[len(orig_dir) + 1 :], class_id)
            for path, class_id in fullpath_class_metadata
        ]
        classes = [class_id for path, class_id in relative_paths_class]
        assert classes == [0, 0, 0, 1, 1, 1]
        assert convert_class_id_names(classes, classes_classtoidx[1], out="name") == [
            "A",
            "A",
            "A",
            "B",
            "B",
            "B",
        ]
        # The following cannot work because classes are already ids, so it regards "classes" as class_ids
        # With allow_missings it wont find anything.
        assert convert_class_id_names(
            classes, classes_classtoidx[1], out="id", allow_missings=True
        ) == [-1] * len(classes)
        # The following cannot work because classes are already ids, so it regards "classes" as class_ids
        try:
            convert_class_id_names(classes, classes_classtoidx[1], out="id")
        except ValueError:
            pass  # I inserted id and tried to convert to id, that must fail.

        converted_to_name = convert_class_id_names(
            classes, classes_classtoidx[1], out="name"
        )
        assert classes == convert_class_id_names(
            converted_to_name, classes_classtoidx[1], out="id"
        )

    def test_generate_meta_from_files_plus_pheno_csv(self):
        tmp = gen_csv_meta(
            os.path.realpath(os.path.join(TESTS_DIR, pointcloud_toy_dataset_csvpheno)),
            path_phenodata="samples_pheno.csv",
        )
        print(tmp.class_name)
        assert tmp.class_name == ["P0H.fcs", "P0Q.fcs", "PAG.fcs", "PAJ.fcs", "PAU.fcs"]
        tmp.selection = "label"
        assert tmp.class_name == [0, 0, 0, 0, 1]
        tmp.selection = "secondlabel"
        print(tmp.class_name)
        assert tmp.class_name == ["A", "A", "B", "B", "B"]
        repr(tmp)  # to test the printing without actually printing

    def test_subsetting(self):
        meta_AB = gen_csv_meta(
            os.path.join(TESTS_DIR, pointcloud_toy_dataset_csvpheno),
            path_phenodata="samples_pheno.csv",
        )
        meta_AB_train = meta_AB[0:2, :]
        meta_AB_train.rm_root(are_you_sure=True)
        print(meta_AB_train.processed_filenames)

    def test_gen_meta_filenames(self):
        meta_AB = gen_meta_filenames(
            os.path.realpath(
                os.path.join(
                    TESTS_DIR, "testdata", "flowcytometry", "info_in_filenames"
                )
            ),
            sep="_",
        )
        repr(meta_AB)
        # pd.Dataframe returns a "Series" when indexed
        assert meta_AB.pheno["column2"].tolist() == ["A", "B", "A"]

    def test_gen_meta_filenames_new_colnames(self):
        meta_AB = gen_meta_filenames(
            os.path.realpath(
                os.path.join(
                    TESTS_DIR, "testdata", "flowcytometry", "info_in_filenames"
                )
            ),
            sep="_",
            colnames=["sample", "smart_colname", "another_smart_colname"],
        )
        print(meta_AB)
        # # pd.Dataframe returns a "Series" when indexed
        # assert meta_AB.pheno["column2"].tolist() == ['A', 'B', 'A']

        with self.assertRaises(ValueError):
            meta_AB = gen_meta_filenames(
                os.path.realpath(
                    os.path.join(
                        TESTS_DIR, "testdata", "flowcytometry", "info_in_filenames"
                    )
                ),
                sep="_",
                colnames=[
                    "sample",
                    "a",
                    "b",
                    "more_colnames_than_necessary_NOT_allowed",
                ],
            )
            print(meta_AB)

        with self.assertRaises(ValueError):
            meta_AB = gen_meta_filenames(
                os.path.realpath(
                    os.path.join(
                        TESTS_DIR, "testdata", "flowcytometry", "info_in_filenames"
                    )
                ),
                sep="_",
                colnames=["sample", "less_colnames_than_necessary_NOT_allowed"],
            )
            print(meta_AB)

    def test_generate_meta_from_csv_wrong_path_delimiter(self):
        tmp = gen_csv_meta(
            os.path.realpath(os.path.join(TESTS_DIR, pointcloud_toy_dataset_csvpheno)),
            path_phenodata="samples_pheno_wrong_delimiter.csv",
        )
        tmp.selection = "label"
        assert tmp.class_name == [0, 0, 0, 0, 1]
        tmp.selection = "secondlabel"
        assert tmp.class_name == ["A", "A", "B", "B", "B"]
        repr(tmp)  # to test the printing without actually printing
        tmp = gen_csv_meta(
            os.path.realpath(os.path.join(TESTS_DIR, pointcloud_toy_dataset_csvpheno)),
            path_phenodata="samples_pheno_wrong_delimiter_2.csv",
        )
        tmp.selection = "label"
        assert tmp.class_name == [0, 0, 0, 0, 1]
        tmp.selection = "secondlabel"
        assert tmp.class_name == ["A", "A", "B", "B", "B"]
        repr(tmp)  # to test the printing without actually printing

    def tearDown(self) -> None:
        shutil.rmtree(
            os.path.join(
                TESTS_DIR,
                pointcloud_toy_dataset_csvpheno,
                os.pardir,
                "autoroot_PointClouds_toy_phenocsv",
            ),
            ignore_errors=True,
        )
