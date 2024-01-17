# Files originally taken from https://git.uni-regensburg.de/ccc_verse/ccc/tests/testdata
all_files <- list.files(pattern = "*.fcs$", recursive = TRUE, full.names = TRUE)

# read with flowcore
for (x in all_files) {
    print(x)
    tmp <- flowCore::read.FCS(x)
    tmp_subset <- tmp[1:min(1000, nrow(tmp)), ]
    flowCore::write.FCS(tmp_subset, x)
}
