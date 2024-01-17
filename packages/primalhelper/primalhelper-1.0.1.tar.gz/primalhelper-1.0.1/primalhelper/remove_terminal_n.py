import numpy as np
from Bio import SeqIO, Seq
import pathlib


def remove_terminal_n_func(msa: pathlib.Path, outpath: pathlib.Path):
    """
    Replaces the terminal Ns in the MSA with gaps
    """
    records_index = SeqIO.parse(msa, "fasta")

    with open(outpath, "w") as outfile:
        for record in records_index:
            seq_list: list[str] = list(str(record.seq).upper())
            seq_len = len(seq_list)

            # Solves the 5' end
            for col_index in range(0, seq_len):
                if seq_list[col_index] == "N" or seq_list[col_index] == "-":
                    seq_list[col_index] = "-"
                else:
                    break

            # Sovles the 3' end
            for rev_col_index in range(seq_len - 1, 0, -1):
                if seq_list[rev_col_index] == "N" or seq_list[rev_col_index] == "-":
                    seq_list[rev_col_index] = "-"
                else:
                    break

            # Recreate a Seq object
            seq = Seq.Seq("".join(seq_list))
            record.seq = seq
            # Write out the record
            SeqIO.write(record, outfile, "fasta")
