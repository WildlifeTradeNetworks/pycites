# pycites
`pycites` is a package to download and interact with the [CITES Trade Database](https://trade.cites.org/) using Python. [citesdb](https://github.com/ropensci/citesdb) exists for R users to load and analzyes this data, so we wanted a way to do the same!

Currently very much a work in progress.  This only allows uses to download CITES trade data and load it as a `pandas` DataFrame.

## Installation
`pip install pycites`

## Roadmap
- [ ] Release a CSV to make it easier for users to download and load data
- [ ] Experiement with other data formats for better memory usage of data (currently pretty high)
- [ ] Include metadata and other useful information, like `citesdb`
- [ ] Add additional functionality for analysis (time series and network analyses), and integrate with other data sources (such as World Bank)
- [ ] Setup CI and testing
