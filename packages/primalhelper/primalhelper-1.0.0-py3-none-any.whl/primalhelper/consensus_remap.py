from Bio import SeqIO
import numpy as np
import pathlib

from primalscheme3.core.bedfiles import read_in_bedprimerpairs, BedPrimerPair


def consensus_remap(msa: pathlib.Path, bedfile: pathlib.Path, refid: str):
    # Read in the bedfile
    primerpairs: list[BedPrimerPair] = read_in_bedprimerpairs(bedfile)
    # If there is more than one MSA in the bedfile, raise an error
    if len(set([primerpair.chromname for primerpair in primerpairs])) > 1:
        raise ValueError(
            "Primers for more than one MSA is present in the bedfile, cannot remap"
        )

    # Find which reference genome should be used
    input_genomes = SeqIO.index(msa, "fasta")
    # Check reference genome is in the MSA
    if refid not in input_genomes:
        raise ValueError(
            f"The reference genome with ID '{refid}' is not present in the MSA"
        )
    else:
        # Get the reference sequence
        ref_seq = str(input_genomes[refid].seq)  # type: ignore

    # Create a lookup array for the MSA indexing to the referance genome
    mapping_array: list[None | int] = [None] * len(ref_seq)

    ref_index = 0
    for msa_index in range(len(ref_seq)):
        # If gap, skip
        if ref_seq[msa_index] == "-":
            continue
        else:
            mapping_array[msa_index] = ref_index
            ref_index += 1

    # Mapp each primerpair
    for primerpair in primerpairs:
        new_end = mapping_array[primerpair.fprimer.end]
        mapped = False

        if new_end is None:
            # Walk left until a non-gap is found
            new_index = primerpair.fprimer.end
            while new_index >= 0:
                new_end = mapping_array[new_index]
                # If valid index, break
                if new_end is not None:
                    primerpair.fprimer.end = new_end
                    mapped = True
                    break
                else:
                    new_index -= 1

            # Ensure all primers are in the index
            if not mapped:
                primerpair.fprimer.end = 0 + max(
                    [len(x) for x in primerpair.fprimer.seqs]
                )

        else:
            primerpair.fprimer.end = new_end

        new_start = mapping_array[primerpair.rprimer.start]
        if new_start is not None:
            primerpair.rprimer.start = new_start
        else:
            # Walk right until a non-gap is found
            new_index = primerpair.rprimer.start
            mapped = False
            while new_index < len(mapping_array):
                new_start = mapping_array[new_index]
                # If valid index, break
                if new_start is not None:
                    primerpair.rprimer.start = new_start
                    mapped = True
                    break
                else:
                    new_index += 1

            if not mapped:
                primerpair.rprimer.start = len(ref_seq.replace("-", "")) - max(
                    [len(x) for x in primerpair.rprimer.seqs]
                )

        primerpair.chromname = refid
        print(primerpair, end="")
