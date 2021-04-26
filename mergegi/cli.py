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
    help="CSV file with the samples names, barcodes, projects names and lane."
)
@click.option(
    '-i', '--input-directory',
    type=click.Path(exists=True),
    metavar='INPUT',
    nargs=1,
    required=True,
    help="MGI output directory."
)
@click.option(
    '-o', '--output-directory',
    type=click.Path(),
    metavar='OUTDIR',
    nargs=1,
    required=True,
    help="MGI output directory."
)
@click.option(
    '-p', '--paired',
    is_flag=True,
    help="Set if your data are paired-end."
)
@click.option(
    '--merge/--no-merge',
    default=True,
    help="Disable it if you need data per lanes"
)
def main(samplesheet, input_dir, output_dir, paired, merge):
    mergegi(samplesheet, input_dir, output_dir, paired, merge)
