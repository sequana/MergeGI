import click.testing as cli_test
import pytest

from mergegi import cli

from . import test_dir


@pytest.fixture(scope="module")
def runner():
    return cli_test.CliRunner()


def test_mergegi_cli(runner, tmpdir):
    outdir = tmpdir / "results"
    result = runner.invoke(
        cli.main,
        [
            "--samplesheet",
            test_dir / "resources" / "samplesheet.csv",
            "--input-directory",
            test_dir / "resources" / "mgi_se",
            "--output-directory",
            outdir,
        ],
    )
    assert result.exit_code == 0
    assert outdir.exists()


def test_default_mergegi_cli(runner):
    result = runner.invoke(cli.main, input="\n")
    assert result.exit_code == 2


def test_mergegi_convert_cli(runner, tmpdir):
    output = tmpdir / "mergegi.csv"
    result = runner.invoke(
        cli.convert,
        ["--samplesheet", test_dir / "resources" / "samplesheet_barcode.csv", "--output-csv", output],
    )
    assert result.exit_code == 0
    assert output.exists()
