#
#  This file is part of Sequana software
#
#  Copyright (c) 2021-2022 - Sequana Dev Team (https://sequana.readthedocs.io)
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  Website:       https://github.com/sequana/sequana
#  Documentation: http://sequana.readthedocs.io
#  Contributors:  https://github.com/sequana/sequana/graphs/contributors
##############################################################################
import argparse
import os
import sys

from sequana_pipetools import SequanaConfig, SequanaManager, logger
from sequana_pipetools.info import sequana_epilog, sequana_prolog
from sequana_pipetools.misc import Colors
from sequana_pipetools.options import (
    GeneralOptions,
    InputOptions,
    SlurmOptions,
    SnakemakeOptions,
    before_pipeline,
)

col = Colors()

NAME = "mergegi"


class Options(argparse.ArgumentParser):
    def __init__(self, prog=NAME, epilog=None):
        usage = col.purple(sequana_prolog.format(**{"name": NAME}))
        super(Options, self).__init__(
            usage=usage,
            prog=prog,
            description="",
            epilog=epilog,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        # add a new group of options to the parser
        so = SlurmOptions(profile="local")
        so.add_options(self)

        # add a snakemake group of options to the parser
        so = SnakemakeOptions(working_directory=NAME)
        so.add_options(self)

        so = InputOptions(input_pattern="*_[12].fq.gz", add_input_readtag=False)
        so.add_options(self)

        so = GeneralOptions()
        so.add_options(self)

        pipeline_group = self.add_argument_group("pipeline_general")
        pipeline_group.add_argument(
            "--input-samplesheet",
            dest="input_samplesheet",
            required=True,
            help="CSV file with the samples names, indexID, barcodei7, project names and lanes."
            " The CSV should have a header and columns should be in this order."
            " For Illumina conversion, you may need to add barcodei5 after barcodei7.",
        )
        pipeline_group.add_argument(
            "--no-merge", dest="no_merge", action="store_true", help="Do not merge lane."
        )

    def parse_args(self, *args):
        args_list = list(*args)
        if "--from-project" in args_list:
            if len(args_list) > 2:
                msg = (
                    "WARNING [sequana]: With --from-project option, "
                    + "pipeline and data-related options will be ignored."
                )
                print(col.error(msg))
            for action in self._actions:
                if action.required is True:
                    action.required = False
        options = super(Options, self).parse_args(*args)
        return options


def main(args=None):
    if not args:
        args = sys.argv

    # whatever needs to be called by all pipeline before the options parsing
    before_pipeline(NAME)

    # option parsing including common epilog
    options = Options(NAME, epilog=sequana_epilog).parse_args(args[1:])

    # use profile slurm if user set a slurm queue
    if options.slurm_queue != "common":
        options.profile = "slurm"

    # the real stuff is here
    manager = SequanaManager(options, NAME)

    # create the beginning of the command and the working directory
    manager.setup()

    if options.from_project is None:

        # fill the config file with input parameters
        cfg = manager.config.config
        cfg.input_directory = os.path.abspath(options.input_directory)
        cfg.input_pattern = options.input_pattern
        cfg.input_samplesheet = os.path.abspath(options.input_samplesheet)


        # The user may overwrite the default
        if options.no_merge:
            cfg.mergegi.options = "--no-merge"

    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    manager.teardown(check_input_files=False)


if __name__ == "__main__":
    main()
