# chuk-api

Python API for working with CHUK datasets

## Installation

This package depends on rioxarray:

```
conda create -n chuk_api_env python=3.10
conda activate chuk_api_env
conda install rioxarray
conda install netcdf4
pip install .
```

Download CHUK grid reference file

```
wget https://gws-access.jasmin.ac.uk/public/nceo_uor/eocis-chuk/EOCIS-CHUK-GRID-100M-v0.4.nc
```

## Usage

### Export a CHUK variable from NetCDF4 to geotiff

```python
from eocis_chuk_api.chuk_dataset_utils import CHUKDataSetUtils

utils = CHUKDataSetUtils("EOCIS-CHUK-GRID-100M-v0.4.nc") # downloaded as described above
ds = utils.load("my_chuk_dataset.nc")
utils.save_as_geotif(ds, "my_variable", "my_variable.tif")
```

### Check a dataset against the reference grid

```python
from eocis_chuk_api.chuk_dataset_utils import CHUKDataSetUtils

utils = CHUKDataSetUtils("EOCIS-CHUK-GRID-100M-v0.4.nc") # downloaded as described above
ds = utils.load("my_chuk_dataset.nc")
try:
    utils.check(ds)
except Exception as ex:
    print(ex)
```

## Objectives

* Use xarray datasets and data arrays as the underlying way to input and output data
* Provide the CHUK grid (100m, EPSG:27700) as a reference and a template for creating data
* Allow data providers to create and append to (in time) CHUK datasets
* Check that data providers have supplied the correct metadata
* Allow data users to retrieve data (optionally, specifying a spatial and temporal extent)
* Provide an abstraction over the underlying persistent storage format
  * netcdf4 filesystem driver will be provided as a reference
  * precision controlled by the data writer
  * chunking can be managed by the API to try to support timeseries extraction
* Provide documentation and code examples

## Currently Supported functionality

* Load from netcdf4
* Check dimensions against reference grid
* Export CHUK data to geotiff, preserving metadata


