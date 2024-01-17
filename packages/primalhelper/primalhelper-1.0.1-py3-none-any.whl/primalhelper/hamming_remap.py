from Bio import SeqIO
import numpy as np
import pathlib

from primalscheme3.core.bedfiles import read_in_bedprimerpairs, BedPrimerPair


MATCH_LIMIT = 15


def ref_fkmer_gen(ref_seq: str, stop_index: int):
    """
    Yeilds base by base fkmer sequences from a reference sequence
    """
    for i in range(stop_index, -1, -1):
        # Skip over gaps
        if ref_seq[i] == "-":
            continue
        yield ref_seq[i]


def fkmer_map(fkmer_seq: set[str], ref_seq: str) -> dict[int, list[int]]:
    """Calculates the index which the fkmer maps to in the MSA

    Args:
        fkmer_seq (str): The fkmer sequence
        msa_array (np.ndarray): The raw referance sequence
        start_index (int): The fixed index of the fkmer in the MSA. Non inclusive

    Returns:
        int: The fkmer stop index with the closest match using hamming distance
    """
    # Get the length of the fkmer seq

    # Key: index, Value: number of mismatches for each fkmer seq
    match_dict: dict[int, list[int]] = {}

    fkmer_max_len = max([len(x) for x in fkmer_seq])

    # Find the best match
    for stopindex in range(fkmer_max_len, len(ref_seq)):
        match_dict[stopindex] = []
        for fseq in fkmer_seq:
            # Calculate the pseudo hamming distance
            matches = 0
            for fseqbase, refbase in zip(fseq[::-1], ref_fkmer_gen(ref_seq, stopindex)):
                if fseqbase == refbase:
                    matches += 1
            # Append the mismatches
            match_dict[stopindex].append(matches)

    # Find the best scoreing index
    return match_dict


def ref_rkmer_gen(ref_seq: str, start_index: int):
    """
    Yeilds base by base rkmer sequences from a reference sequence
    """
    for i in range(start_index, len(ref_seq)):
        # Skip over gaps
        if ref_seq[i] == "-":
            continue
        yield ref_seq[i]


def rkmer_map(rkmer_seq: set[str], ref_seq: str) -> dict[int, list[int]]:
    """Calculates the index which the rkmer maps to in the MSA

    Args:
        rkmer_seq (str): The rkmer sequence
        msa_array (np.ndarray): The raw referance sequence
        start_index (int): The fixed index of the rkmer in the MSA. Non inclusive

    Returns:
        int: The rkmer start index with the closest match using hamming distance
    """
    # Get the length of the rkmer seq

    # Key: index, Value: number of mismatches for each rkmer seq
    match_dict: dict[int, list[int]] = {}

    rkmer_max_len = max([len(x) for x in rkmer_seq])

    # Find the best match
    for startindex in range(0, len(ref_seq) - rkmer_max_len):
        match_dict[startindex] = []
        for rseq in rkmer_seq:
            # Calculate the pseudo hamming distance
            matches = 0
            for rseqbase, refbase in zip(rseq, ref_rkmer_gen(ref_seq, startindex)):
                if rseqbase == refbase:
                    matches += 1
            # Append the mismatches
            match_dict[startindex].append(matches)

    # Find the best scoreing index
    return match_dict


def remap_func(msa: pathlib.Path, bedfile: pathlib.Path, refid: str):
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
        ref_seq = ref_seq.replace("-", "")

    # Use a hamming distance score to map the primers.
    # As we are not sure of the indexing system
    for primerpair in primerpairs:
        # Keep track of which primers have been mapped
        fprimer_mapped = False
        rprimer_mapped = False

        # For each fkmer
        fkmer_matches = fkmer_map(primerpair.fprimer.seqs, ref_seq)

        # Look for best matches
        fkmer_best_matches = {
            index: max(scores)
            for index, scores in fkmer_matches.items()
            if max(scores) >= MATCH_LIMIT
        }
        if len(fkmer_best_matches) == 0:
            primerpair.fprimer.end = 0
            fprimer_mapped = True
        elif len(fkmer_best_matches) == 1:
            # Remap the fkmer
            fkmer_stop_index = list(fkmer_best_matches.keys())[0]
            primerpair.fprimer.end = fkmer_stop_index
            fprimer_mapped = True
        else:
            # If there are multiple best matches, pick the best
            fkmer_best_match: int = max(fkmer_best_matches.values())
            # Check best is unique
            fkmer_best_match_index = [
                index
                for index, score in fkmer_best_matches.items()
                if score == fkmer_best_match
            ]
            if len(fkmer_best_match_index) == 1:
                # Remap the fkmer
                primerpair.fprimer.end = fkmer_best_match_index[0]
                fprimer_mapped = True
            else:
                fprimer_mapped = False  # reassign to False for clarity

        # For each rkmer
        rkmer_matches = rkmer_map(primerpair.rprimer.seqs, ref_seq)

        # Look for best matches
        rkmer_best_matches = {
            index: max(scores)
            for index, scores in rkmer_matches.items()
            if max(scores) >= MATCH_LIMIT
        }
        if len(rkmer_best_matches) == 0:
            primerpair.rprimer.start = 0
            rprimer_mapped = True
        elif len(rkmer_best_matches) == 1:
            # Remap the rkmer
            rkmer_start_index = list(rkmer_best_matches.keys())[0]
            primerpair.rprimer.start = rkmer_start_index
            rprimer_mapped = True
        else:
            # If there are multiple best matches, pick the best
            rkmer_best_match: int = max(rkmer_best_matches.values())
            # Check best is unique
            rkmer_best_match_index = [
                index
                for index, score in rkmer_best_matches.items()
                if score == rkmer_best_match
            ]
            if len(rkmer_best_match_index) == 1:
                # Remap the rkmer
                primerpair.rprimer.start = rkmer_best_match_index[0]
                rprimer_mapped = True
            else:
                rprimer_mapped = False

        # Use both primer positions to resolve ambiguity
        if rprimer_mapped == False and fprimer_mapped == False:
            print(
                f"WARNING: The primer pair {primerpair.amplicon_number} could not be mapped"
            )
        elif fprimer_mapped and rprimer_mapped == False:
            # Use the fprimer mapping to resolve the ambiguity
            closest_mapping = min(
                rkmer_best_match_index, key=lambda x: (x - primerpair.fprimer.end) * -1
            )
            primerpair.rprimer.start = closest_mapping
        elif rprimer_mapped and fprimer_mapped == False:
            # Use the rprimer mapping to resolve the ambiguity
            closest_mapping = min(
                fkmer_best_match_index,
                key=lambda x: (primerpair.rprimer.start - x) * -1,
            )
            primerpair.fprimer.end = closest_mapping

        # Check the primer pair is valid
        if primerpair.fprimer.end > primerpair.rprimer.start:
            print(f"The primer pair {primerpair.amplicon_number} is invalid")

        print(primerpair.to_bed(primerpair.chromname, primerpair.ampliconprefix))
