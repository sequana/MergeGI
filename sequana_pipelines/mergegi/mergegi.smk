#  This file is part of Sequana software
#
#  Copyright (c) 2016-2023 - Sequana Dev Team (https://sequana.readthedocs.io)
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  Website:       https://github.com/sequana/sequana
#  Website:       https://github.com/sequana/lora
#  Documentation: http://sequana.readthedocs.io
#  Documentation: https://github.com/sequana/lora/README.rst
##############################################################################
"""Pipeline to demultiplex MGI"""
from pathlib import Path

from sequana_pipetools.snaketools import PipelineManager


configfile: "config.yml"


# get lanes
fastqs = {
    lane.name: sorted([fastq for fastq in lane.glob(config["input_pattern"])])
    for lane in Path(f"{config['input_directory']}").glob("L0*")
}


def get_fastq_files(wildcards):
    """Get raw data"""
    return fastqs[wildcards.lane]


rule mergegi_pipeline:
    input:
        "fastq"


rule create_csv_files:
    input:
        config["input_samplesheet"],
    output:
        barcodes="barcodes.tsv",
        mergegi_csv="mergegi_samplesheet.csv",
    shell:
        """
        mergegi_convert -s {input} -o {output.mergegi_csv} -b {output.barcodes}
        """


rule split_barcode:
    input:
        barcodes="barcodes.tsv",
        fastq=get_fastq_files,
    output:
        directory("demultiplex_fastq/{lane}"),
    params:
        barcode1=config["split_barcode"]["barcode1"],
        barcode2=config["split_barcode"]["barcode2"],
        options=config["split_barcode"]["options"],
    threads: config["split_barcode"]["threads"]
    resources:
        **config["split_barcode"]["resources"],
    shell:
        """
        # string to array conversion
        IFS=" " read -r -a array <<< {input.fastq}
        if [[ ${{#array[@]}} -eq 2 ]]; then
            fastqs="-1 ${{array[0]}} -2 ${{array[1]}}"
        else
            fastqs="-1 ${{array[0]}}"
        fi
        if [[ -n "{params.barcode2}" ]]; then
            bc2="-b {params.barcode2}"
        else
            bc2=""
        fi
        splitBarcode {params.options} \
                     -B {input.barcodes} \
                     $fastqs \
                     -b {params.barcode1} \
                     $bc2 \
                     -n {threads} \
                     -m {resources.mem} \
                     -o {output}
        """


rule mergegi:
    input:
        rawdata=expand("demultiplex_fastq/{lane}", lane=fastqs.keys()),
        mergegi_csv="mergegi_samplesheet.csv",
    output:
        directory("fastq"),
    params:
        paired="--paired" if len(next(iter(fastqs.values()))) == 2 else "",
        options=config["mergegi"]["options"],
    resources:
        **config["mergegi"]["resources"],
    shell:
        """
        mergegi {params.options} {params.paired} -s {input.mergegi_csv} -i demultiplex_fastq -o {output}
        """
