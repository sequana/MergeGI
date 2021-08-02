import csv
import glob
import os
import shutil
import sys
from collections import defaultdict
from contextlib import ExitStack


# Set the logger
import logging
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    '%(asctime)s :: %(levelname)s :: %(message)s',
    "%Y-%m-%d %H:%M:%S"
))
logger = logging.getLogger(__name__)
logger.setLevel('ERROR')
logger.addHandler(handler)


def mergegi(barcodes_csv, raw_data_dir, merged_data_dir, paired=False, merge_lanes=True):
    """ Merging MGI fastq from different barcodes.

    :param str barcodes_csv: CSV file with the samples names, barcodes, projects names and lane.
    :param str raw_data_dir: The directory with raw fastqs.
    :param str merged_data_dir: The directory where to put the merged fastqs.
    :param bool paired: Set data as paired-end.
    :param bool merge_lanes: Merge all data or keep separate per lanes.
    """
    # Create cluster per project/sample
    file_to_merge = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    with open(barcodes_csv) as csvfile:
        csv_reader = csv.reader(csvfile, skipinitialspace=True)
        try:
            # skip header and check if column count is good
            samplename, barcode, barcode2, project, lane = next(csv_reader)
        except ValueError:
            msg = ("Your sample sheet seems to be ill-formed. You must have 5 columns corresponding to:"
                   " sample names, barcode1, barcode2, project names and lanes."
                   " They are expected to be found in this order.")
            logger.error(msg)
            sys.exit(1)
        # Cluster barcode that need to be merge
        for samplename, barcode, barcode2, project, lane in csv_reader:
            file_to_merge[project][samplename][lane.rstrip()].append(barcode)

    # Choosing merge function
    merge_sample_files = merge_all if merge_lanes else merge_per_lane
    # Set the input format for glob
    input_fformat = f"{raw_data_dir}/L0{{lane}}/*_L0{{lane}}_{{barcode}}{{p}}.fq.gz"
    pair = ['_1', '_2'] if paired else ['']
    # Merge files
    for project_name, samples in file_to_merge.items():
        # Create project output directories
        output_dir = os.path.join(merged_data_dir, project_name)
        try:
            os.makedirs(output_dir)
        except FileExistsError:
            pass
        for sample_name, lanes in samples.items():
            for p in pair:
                merge_sample_files(sample_name, lanes, p, input_fformat, output_dir)


def merge_all(sample_name, lanes, p, inputff, outdir):
    """ Merge lanes and barcode for one sample.

    :param str sample_name: sample name.
    :param dict lanes: dict with barcodes per lane to merge.
    :param str p: indicates if it is read 1 or 2
    :param str inputff: input format for the glob
    :param str outdir: output directory to write merged file
    """
    # Iter on files to merge
    files_to_merge = (
        filename for lane, barcodes in lanes.items() for barcode in barcodes
        for filename in glob.iglob(inputff.format(lane=lane, barcode=barcode, p=p))
    )
    # Merge all files
    with ExitStack() as stack:
        files = [stack.enter_context(open(filename, 'rb')) for filename in files_to_merge]
        with open(os.path.join(outdir, f'{sample_name}{p}.fq.gz'), 'wb') as filout:
            for filin in files:
                shutil.copyfileobj(filin, filout)


def merge_per_lane(sample_name, lanes, p, inputff, outdir):
    """ Merge barcode per lane for one sample.

    :param str sample_name: sample name.
    :param dict lanes: dict with barcodes per lane to merge.
    :param str p: indicates if it is read 1 or 2
    :param str inputff: input format for the glob
    :param str outdir: output directory to write merged file
    """
    for lane, barcodes in lanes.items():
        with ExitStack() as stack:
            files = [
                stack.enter_context(open(filename, 'rb')) for barcode in barcodes for filename in glob.iglob(
                    inputff.format(lane=lane, barcode=barcode, p=p)
                )
            ]
            with open(os.path.join(outdir, f'{sample_name}_L0{lane}{p}.fq.gz'), 'wb') as filout:
                for filin in files:
                    shutil.copyfileobj(filin, filout)
