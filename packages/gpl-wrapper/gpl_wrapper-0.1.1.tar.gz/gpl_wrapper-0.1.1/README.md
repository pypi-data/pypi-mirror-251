# gpl wrapper

[![PyPI - Version](https://img.shields.io/pypi/v/gpl-wrapper.svg)](https://pypi.org/project/gpl-wrapper)

-----


This is a wrapper to run the GRIDSS-PURPLE-LINX tool. The original nextflow pipeline is [here](https://github.com/umccr/gridss-purple-linx-nf). I have modified the docker image to make it compatible with our working environment. 

Additionally, hg38 for hmftools is harcoded for the "chr"-prefixed reference genome. So, we have added a previous step to reheader both bams and input vcfs so they also include the prefix. Our modified repo is [here](https://github.com/pbousquets/gridss-purple-linx-nf)


## Installation

```console
pip install gpl-wrapper
```

