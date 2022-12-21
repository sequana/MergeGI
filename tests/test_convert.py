from pathlib import Path
from mergegi.samplesheet_converter import create_mergegi_csv
from . import test_dir


def test_create_csv(tmpdir):
    """ Test script to create mergegi csv file"""
    samplesheet = test_dir / 'resources' / 'samplesheet_barcode.csv'
    output_csv: Path = tmpdir / "mergegi.csv"
    create_mergegi_csv(samplesheet, output_csv)

    assert output_csv.exists()
    assert len(output_csv.read_text(encoding="utf-8").rstrip().split("\n")) == 5


def test_create_barcode_csv(tmpdir):
    """ Test script to create mergegi csv file"""
    samplesheet = test_dir / 'resources' / 'samplesheet_barcode.csv'
    output_csv: Path = tmpdir / "mergegi.csv"
    output_index: Path = tmpdir / "dualindex.csv"
    create_mergegi_csv(samplesheet, output_csv, output_index)

    assert output_index.exists()
    assert len(output_index.read_text(encoding="utf-8").rstrip().split("\n")) == 2
