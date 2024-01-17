import pathlib


def read_bed_file(bedfilepath: pathlib.Path) -> tuple[list[list[str]], list[str]]:
    """
    Reads a bed file and returns a list of lists of strings.

    :return: bedfile_list, bedfile_header
    """

    with open(bedfilepath, "r") as bedfile:
        bedfile_list: list[list[str]] = []
        bedfile_header: list[str] = []

        for line in bedfile:
            line = line.strip()
            # Header line
            if line.startswith("#"):
                bedfile_header.append(line)
            elif line:  # If not empty
                bedfile_list.append(line.split("\t"))

    return bedfile_list, bedfile_header
