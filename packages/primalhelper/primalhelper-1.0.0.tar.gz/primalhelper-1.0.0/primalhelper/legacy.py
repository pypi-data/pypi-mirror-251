import pathlib

from primalhelper.bedfile import read_bed_file


def get_amplicon_number(primerpair: list[str]) -> int:
    return int(primerpair[3].split("_")[1])


def primer_name_prefix(primerpair: list[str]) -> str:
    return "_".join(primerpair[3].split("_")[:-1])


def legacy_convert(bedfilepath: pathlib.Path, include_circular: bool = False):
    # Read in the bedfile
    primerpairs, _headers = read_bed_file(bedfilepath)

    # Get all reference names
    reference_names = set(pp[0] for pp in primerpairs)
    # Get all amplicon numbers
    amplicon_numbers = set(get_amplicon_number(pp) for pp in primerpairs)

    for reference_name in reference_names:
        primerpairs_for_reference = [
            pp for pp in primerpairs if pp[0] == reference_name
        ]

        # For each amplicon number, get all primerpairs
        for amplicon_number in amplicon_numbers:
            primerpairs_for_amplicon = [
                pp
                for pp in primerpairs_for_reference
                if get_amplicon_number(pp) == amplicon_number
            ]

            # Get the forward and reverse primers
            forward_primers = [fp for fp in primerpairs_for_amplicon if fp[5] == "+"]
            reverse_primers = [rp for rp in primerpairs_for_amplicon if rp[5] == "-"]

            # Get the furthest indexes
            fp_start_indexes = min([int(fp[1]) for fp in forward_primers])
            fp_end_indexes = max([int(fp[2]) for fp in forward_primers])
            rp_start_indexes = min([int(rp[1]) for rp in reverse_primers])
            rp_end_indexes = max([int(rp[2]) for rp in reverse_primers])

            # FPrimer Stem
            fp_name = primer_name_prefix(forward_primers[0])
            rp_name = primer_name_prefix(reverse_primers[0])

            # fp pool
            fp_pool = forward_primers[0][4]
            rp_pool = reverse_primers[0][4]

            # longest_seq
            fp_longest_seq = max([fp[6] for fp in forward_primers], key=len)
            rp_longest_seq = max([rp[6] for rp in reverse_primers], key=len)

            if include_circular:
                # Print Fp
                print(
                    f"{reference_name}\t{fp_start_indexes}\t{fp_end_indexes}\t{fp_name}\t{fp_pool}\t+\t{fp_longest_seq}"
                )
                # Print rp
                print(
                    f"{reference_name}\t{rp_start_indexes}\t{rp_end_indexes}\t{rp_name}\t{rp_pool}\t+\t{rp_longest_seq}"
                )
            elif fp_start_indexes < rp_start_indexes:  # Filter out circular primers
                # Print Fp
                print(
                    f"{reference_name}\t{fp_start_indexes}\t{fp_end_indexes}\t{fp_name}\t{fp_pool}\t-\t{fp_longest_seq}"
                )
                # Print rp
                print(
                    f"{reference_name}\t{rp_start_indexes}\t{rp_end_indexes}\t{rp_name}\t{rp_pool}\t-\t{rp_longest_seq}"
                )


if __name__ == "__main__":
    legacy_convert(
        bedfilepath=pathlib.Path(
            "/Users/kentcg/primerschemes-fork/primerschemes/hbv/500/v1.1.0/primer.bed"
        ),
        include_circular=True,
    )
