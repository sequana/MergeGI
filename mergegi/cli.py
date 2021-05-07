import click

from . import mergegi


@click.command(
    context_settings={'help_option_names': ['-h', '--help']}
)
@click.option(
    '-s', '--samplesheet',
    type=click.Path(exists=True),
    metavar='SAMPLESHEET',
    nargs=1,
    required=True,
    help="CSV file with the samples names, barcode1, barcode2, project names and lanes."
    " The CSV should have a header and columns should be in this order.",
)
@click.option(
    '-i', '--input-directory',
    type=click.Path(exists=True),
    metavar='INPUT',
    nargs=1,
    required=True,
    help="MGI directory where raw FastQ files (by lane) are to be found."
    "Indeed, this directory should contain one directory per lane"
    " (e.g. L01, L02, etc.). Ex: MGI/F301460/OutputFq/F301460",
)
@click.option(
    '-o', '--output-directory',
    type=click.Path(),
    metavar='OUTDIR',
    nargs=1,
    required=True,
    help="Merged data output directory. The directory where the processed (merged) FastQ files will be stored.",
)
@click.option(
    '-p', '--paired', is_flag=True, help="Set it if your data are paired-end."
)
@click.option(
    '--merge/--no-merge',
    default=True,
    help="Disable it if you DO NOT want to merge data from different lanes and"
    " keep the lane information in the processed FastQ files.",
)
def main(samplesheet, input_directory, output_directory, paired, merge):
    """MergeGI is a command line tool to merge and organize sequencing data
    (FastQ files) out of a MGI sequencer according to lanes and barcodes.

    MGI DNBSEQ G400 sequencer produces FastQ files organized by
    flowcell, lanes, barcodes and pairs. For example:

    MGI/F300001460/OutputFq/F300001460/L01/F300001460_L01_22_1.fq.gz

    Where F300001460 is the flowcell, L01 the lane, 22 the number of the barcode
    and 1 shows that the FastQ corresponds to the first of the pair.

    MergeGI make use of this information linked to the samplesheet to merge FastQ
    files according to their barcodes, lanes and pairs. Barcode number will be replaced
    by the corresponding sample names in the sample sheet.

    Example:

    If Single end sequencing::

        mergegi -s samplesheet.csv -i mgi_fastq_folder -o merged_fastqs_folder

    If paired end sequencing::

        mergegi -s samplesheet.csv -i mgi_fastq_folder -o merged_fastqs_folder -p

    If single end sequencing and not merging lanes::

        mergegi -s samplesheet.csv -i mgi_fastq_folder -o merged_fastqs_folder --no-merge
    """
    mergegi(samplesheet, input_directory, output_directory, paired, merge)
