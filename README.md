# pycites
`pycites` is a package to download and interact with the [CITES Trade Database](https://trade.cites.org/) using Python. [citesdb](https://github.com/ropensci/citesdb) exists for R users to load and analzyes this data, so we wanted a way to do the same!

Currently very much a work in progress.  Currently only downloads and loads data.

## Installation
`pip install pycites`

## Usage instructions
To download the CITES Trade Database and load into a dataframe, run the following in a Jupyter notebook or Python shell:
```python
import pycites

pycites.get_data()
df = pycites.load_data()
```
This will download and extract the zip file from the CITES website, do some basic data validation (e.g. drop rows with missing or incorrect Years), and combine the data into a single compressed CSV file.  This uses a decent amount of memory, so may cause issues on a machines with low resource.

## Roadmap
- [ ] Release a CSV to make it easier for users to download and load data
- [ ] Experiement with other data formats for better memory usage of data (currently pretty high)
- [ ] Add a CLI for downloading data
- [ ] Include metadata and other useful information, like `citesdb`
- [ ] Add additional functionality for analysis (time series and network analyses), and integrate with other data sources (such as World Bank)
- [ ] Setup CI and testing
