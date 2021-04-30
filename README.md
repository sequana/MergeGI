# MergeGI

Simple python script to merge MGI sequencing data.

## Table of Contents

- [MergeGI](#mergegi)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
  - [General Usage](#general-usage)

## Getting Started

Install the library using Pypi:
```bash
pip install mergegi
```

## General Usage

The software needs a csv file with samples information like:
```csv
samplename,barcode,barcode2,project,lane
sample1,1,,projectA,1
sample2,2,,projectA,1
sample1,1,,projectA,2
sample3,2,,projectB,2
sample3,3,,projectB,1
sample2,3,,projectA,2
```

Then you can run mergegi:
```bash
mergegi --samplesheet samplesheet.csv --input-directory mgi_raw_data --output-directory merge_data --paired
```
