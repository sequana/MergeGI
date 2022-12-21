import gzip

import pytest

from mergegi import mergegi

from . import test_dir


def test_mergegi_single_end(tmpdir):
    """Test MergeGI main script."""
    # run merge barcode
    samplesheet = test_dir / "resources" / "samplesheet.csv"
    data_dir = test_dir / "resources" / "mgi_se"
    output_dir = tmpdir / "mergegi_output"
    mergegi(samplesheet, data_dir, output_dir, paired=False)

    # check if files exist
    b_sample = output_dir / "toto" / "B.fq.gz"
    assert (output_dir / "toto" / "A.fq.gz").exists()
    assert b_sample.exists()
    assert (output_dir / "tata" / "C.fq.gz").exists()

    # compare with expected file
    expected_file = test_dir / "resources" / "expected" / "B_1.fq"
    with gzip.open(b_sample) as filin:
        assert expected_file.read_bytes() == filin.read()


def test_mergegi_paired(tmpdir):
    """Test MergeGI main script."""
    # run merge barcode
    samplesheet = test_dir / "resources" / "samplesheet.csv"
    data_dir = test_dir / "resources" / "mgi_pe"
    output_dir = tmpdir / "mergegi_output"
    mergegi(samplesheet, data_dir, output_dir, paired=True)

    # check if files exist
    b_sample = output_dir / "toto" / "B_2.fq.gz"
    assert (output_dir / "toto" / "A_2.fq.gz").exists()
    assert b_sample.exists()
    assert (output_dir / "tata" / "C_2.fq.gz").exists()

    # compare with expected file
    expected_file = test_dir / "resources" / "expected" / "B_2.fq"
    with gzip.open(b_sample) as filin:
        assert expected_file.read_bytes() == filin.read()


def test_mergegi_per_lane(tmpdir):
    """Test MergeGI main script."""
    # run merge barcode
    samplesheet = test_dir / "resources" / "samplesheet.csv"
    data_dir = test_dir / "resources" / "mgi_pe"
    output_dir = tmpdir / "mergegi_output"
    mergegi(samplesheet, data_dir, output_dir, paired=True, merge_lanes=False)

    # check if files exist
    b_sample = output_dir / "toto" / "B_L01_1.fq.gz"
    assert (output_dir / "toto" / "A_L01_2.fq.gz").exists()
    assert b_sample.exists()
    assert (output_dir / "tata" / "C_L02_1.fq.gz").exists()

    # compare with expected file
    expected_file = test_dir / "resources" / "expected" / "B_L01_1.fq"
    with gzip.open(b_sample) as filin:
        assert expected_file.read_bytes() == filin.read()


def test_bad_csv(tmpdir):
    # run merge barcode
    samplesheet = test_dir / "resources" / "bad_samplesheet.csv"
    data_dir = test_dir / "resources" / "mgi_pe"
    output_dir = tmpdir / "mergegi_output"
    with pytest.raises(SystemExit):
        mergegi(samplesheet, data_dir, output_dir, paired=True)
