import click.testing as cli_test
import pytest
import os

from mergegi import cli
from . import test_dir


@pytest.fixture(scope="module")
def runner():
    return cli_test.CliRunner()


def test_mergegi_cli(runner, tmpdir):
    outdir = tmpdir.join("results")
    result = runner.invoke(cli.main, [
        "--samplesheet", os.path.join(test_dir, 'resources', 'samplesheet.csv'),
        "--input-directory", os.path.join(test_dir, 'resources', 'mgi'),
        "--output-directory", outdir,
    ])
    assert result.exit_code == 0
    assert os.path.exists(outdir)


def test_default_mergegi_cli(runner):
    result = runner.invoke(cli.main, input='\n')
    assert result.exit_code == 2
