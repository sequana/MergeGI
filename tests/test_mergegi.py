import gzip
import os
import pytest

from mergegi import mergegi
from . import test_dir


def test_mergegi_single_end(tmpdir):
    """ Test MergeGI main script.
    """
    # run merge barcode
    samplesheet = os.path.join(test_dir, 'resources', 'samplesheet.csv')
    data_dir = os.path.join(test_dir, 'resources', 'mgi')
    output_dir = tmpdir.join("mergegi_output")
    mergegi(samplesheet, data_dir, output_dir, paired=False)

    # check if files exist
    b_sample = os.path.join(output_dir, 'toto', 'B_1.fq.gz')
    assert os.path.exists(os.path.join(output_dir, 'toto', 'A_1.fq.gz'))
    assert os.path.exists(b_sample)
    assert os.path.exists(os.path.join(output_dir, 'tata', 'C_1.fq.gz'))

    # compare with expected file
    expected_file = os.path.join(test_dir, 'resources', 'expected', 'B_1.fq')
    with open(expected_file, 'rb') as expect_file:
        with gzip.open(b_sample) as filin:
            assert expect_file.read() == filin.read()


def test_mergegi_paired(tmpdir):
    """ Test MergeGI main script.
    """
    # run merge barcode
    samplesheet = os.path.join(test_dir, 'resources', 'samplesheet.csv')
    data_dir = os.path.join(test_dir, 'resources', 'mgi')
    output_dir = tmpdir.join("mergegi_output")
    mergegi(samplesheet, data_dir, output_dir, paired=True)

    # check if files exist
    b_sample = os.path.join(output_dir, 'toto', 'B_2.fq.gz')
    assert os.path.exists(os.path.join(output_dir, 'toto', 'A_2.fq.gz'))
    assert os.path.exists(b_sample)
    assert os.path.exists(os.path.join(output_dir, 'tata', 'C_2.fq.gz'))

    # compare with expected file
    expected_file = os.path.join(test_dir, 'resources', 'expected', 'B_2.fq')
    with open(expected_file, 'rb') as expect_file:
        with gzip.open(b_sample) as filin:
            assert expect_file.read() == filin.read()


def test_mergegi_per_lane(tmpdir):
    """ Test MergeGI main script.
    """
    # run merge barcode
    samplesheet = os.path.join(test_dir, 'resources', 'samplesheet.csv')
    data_dir = os.path.join(test_dir, 'resources', 'mgi')
    output_dir = tmpdir.join("mergegi_output")
    mergegi(samplesheet, data_dir, output_dir, paired=True, merge_lanes=False)

    # check if files exist
    b_sample = os.path.join(output_dir, 'toto', 'B_L01_1.fq.gz')
    assert os.path.exists(os.path.join(output_dir, 'toto', 'A_L01_2.fq.gz'))
    assert os.path.exists(b_sample)
    assert os.path.exists(os.path.join(output_dir, 'tata', 'C_L02_1.fq.gz'))

    # compare with expected file
    expected_file = os.path.join(test_dir, 'resources', 'expected', 'B_L01_1.fq')
    with open(expected_file, 'rb') as expect_file:
        with gzip.open(b_sample) as filin:
            assert expect_file.read() == filin.read()


def test_missing_column_csv(tmpdir):
    # run merge barcode
    samplesheet = os.path.join(test_dir, 'resources', 'missing_column.csv')
    data_dir = os.path.join(test_dir, 'resources', 'mgi')
    output_dir = tmpdir.join("mergegi_output")
    with pytest.raises(SystemExit):
        mergegi(samplesheet, data_dir, output_dir, paired=True)
