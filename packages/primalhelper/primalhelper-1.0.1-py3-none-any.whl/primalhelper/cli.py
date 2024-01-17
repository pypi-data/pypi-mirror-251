import pathlib
import typer
from typing_extensions import Annotated
from enum import Enum
from Bio import SeqIO, Seq, SeqRecord

# Import module
from primalhelper.__init__ import __version__
from primalhelper.hamming_remap import remap_func
from primalhelper.consensus_remap import consensus_remap
from primalhelper.legacy import legacy_convert
from primalhelper.remove_terminal_n import remove_terminal_n_func


# Create the typer app
app = typer.Typer()


class RemapMethod(Enum):
    hamming = "hamming"
    consensus = "consensus"


@app.command()
def remap(
    msa: Annotated[
        pathlib.Path,
        typer.Option(help="The path to the scheme directory", readable=True),
    ],
    bedfile: Annotated[
        pathlib.Path, typer.Option(help="The path to the bedfile", readable=True)
    ],
    refid: Annotated[str, typer.Option(help="The ID of the reference genome")],
    RemapMethod: Annotated[
        RemapMethod, typer.Option(help="The ID of the reference genome")
    ] = RemapMethod.consensus,
):
    """
    Remaps the given multiple sequence alignment (MSA) using the specified method.

    Args:
        msa (pathlib.Path): The path to the scheme directory.
        bedfile (pathlib.Path): The path to the bedfile.
        refid (str): The ID of the reference genome.
        RemapMethod (RemapMethod, optional): The remap method to use. Defaults to RemapMethod.consensus.

    Raises:
        NotImplementedError: If the specified remap method is not yet stable.

    """
    match RemapMethod:
        case RemapMethod.consensus:
            consensus_remap(msa, bedfile, refid)
        case RemapMethod.hamming:
            raise NotImplementedError("Hamming remap is not yet stable")
            remap_func(msa, bedfile, refid)


@app.command()
def legacy(
    bedfile: Annotated[
        pathlib.Path, typer.Option(help="The path to the bedfile", readable=True)
    ],
    include_circular: Annotated[
        bool, typer.Option(help="Include circular primers")
    ] = False,
):
    """
    Convert a new V2 style bedfile to V1 format for use with fieldbioinfomatics.

    Args:
        bedfile (pathlib.Path): The path to the bedfile.
    """
    legacy_convert(bedfile, include_circular)


@app.command()
def merge_segments(
    reference: Annotated[
        list[pathlib.Path],
        typer.Option(help="The referance genomes to merge", readable=True),
    ],
    bedfile: Annotated[pathlib.Path, typer.Option(help="The path to the bedfile")],
    output: Annotated[
        pathlib.Path,
        typer.Option(help="The dir to the output file"),
    ],
):
    spacer_len = 400
    fasta_list: list[str] = []

    for ref in reference:
        fasta_list.append(SeqIO.read(ref, "fasta").seq)

    # Merge the fasta
    merged_fasta = Seq.Seq(
        ("N" * spacer_len).join(fasta_list),
    )
    # Write out the fasta
    SeqIO.write(SeqRecord.SeqRecord(merged_fasta, id="merged_ref"), output, "fasta")


@app.command()
def remove_terminal_n(
    msa: Annotated[
        pathlib.Path,
        typer.Option(help="The path to the scheme directory", readable=True),
    ],
    output: Annotated[
        pathlib.Path, typer.Option(help="The path to the output file", writable=True)
    ],
):
    remove_terminal_n_func(msa, output)


if __name__ == "__main__":
    app()
