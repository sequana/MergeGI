import csv
from pathlib import Path
from typing import Generator, Optional, Union

TRANSTAB = str.maketrans("atgcATGC", "tacgTACG")


def create_mergegi_csv(
    samplesheet: Union[str, Path], mergegi_csv: Union[str, Path], dualindex: Optional[Union[str, Path]] = None
):
    with open(samplesheet) as csvfhin, open(mergegi_csv, "w") as mergeout:
        csv_reader = csv.reader(csvfhin, skipinitialspace=True)
        samplename, indexid, *indexes, project, lane = next(csv_reader)
        iter_csv = iter_illumina_convertion(csv_reader) if len(indexes) == 2 else iter_mgi(csv_reader)
        index_added = {}
        # header for mergegi file
        print("samplename,barcode,project,lane", file=mergeout)
        for samplename, indexid, barcode, project, lane in iter_csv:
            print(f"{samplename},{indexid},{project},{lane}", file=mergeout)
            if indexid not in index_added:
                index_added[indexid] = barcode
    if dualindex:
        with open(dualindex, "w") as fhout:
            for indexid, barcode in index_added.items():
                print(f"{indexid}\t{barcode}", file=fhout)


def iter_illumina_convertion(csv_reader) -> Generator:
    """Return concatenated barcodes with i5 reverse-complemented and i7."""
    for samplename, indexid, i7, i5, project, lane in csv_reader:
        yield samplename, indexid, f"{i5.translate(TRANSTAB)[::-1]}{i7}", project, lane


def iter_mgi(csv_reader):
    """MGI has only i7 barcode."""
    for samplename, indexid, i7, project, lane in csv_reader:
        yield samplename, indexid, i7, project, lane
