# chuk-api

Python API for working with CHUK datasets

## Installation

This package depends on rioxarray:

```
conda create -n chuk_api_env python=3.10
conda activate chuk_api_env
conda install rioxarray
conda install netcdf4
```

Clone this repo and run:

```
pip install .
```

Download CHUK grid reference file

```
wget https://gws-access.jasmin.ac.uk/public/nceo_uor/eocis-chuk/EOCIS-CHUK-GRID-100M-v0.4.nc
```

## Usage

### Create a CHUK dataset

```python
import xarray as xr
import numpy as np
from eocis_chuk_api.chuk_dataset_utils import CHUKDataSetUtils
utils = CHUKDataSetUtils("EOCIS-CHUK-GRID-100M-v0.4.nc") # downloaded as described above
chuk_ds = utils.create_new_dataset(
     title="My CHUK dataset",
     institution = "EOCIS CHUK",
     version = "1.0",
     convention = "CF-1.10",
     summary = "Shows estimates of the squirrel population in each CHUK grid cell",
     license = "Creative Commons Licence by attribution (https://creativecommons.org/licenses/by/4.0/)",
     history = "Developed from the squirrel population dataset",
     comment = "This is a made up example",
     creator_url = "https:///www.example.com",
     creator_name = "Institute of Squirrel Studies",
     creator_email = "enquiries@squirrel-studies.org.uk",
     creator_processing_institution = "Institute of Squirrel Studies")
# create an array to hold the data
population_data = np.zeros(utils.get_grid_shape())
# populate the data

# attach the data
chuk_ds["squirrel_population"] = xr.DataArray(population_data,dims=("y","x"), attrs={
   "long_name":"estimated_squirrel_population"
})

# save the dataset
utils.save(chuk_ds, "EOCIS-CHUK-SQUIRRELPOPULATION-100M-v0.1.nc")
```

### Export a CHUK variable from NetCDF4 to geotiff

```python
from eocis_chuk_api.chuk_dataset_utils import CHUKDataSetUtils

utils = CHUKDataSetUtils("EOCIS-CHUK-GRID-100M-v0.4.nc") # downloaded as described above
ds = utils.load("EOCIS-CHUK-SQUIRRELPOPULATION-100M-v0.1.nc")
utils.save_as_geotif(ds, "squirrel_population", "EOCIS-CHUK-SQUIRRELPOPULATION-100M-v0.1.tif")
```

### Check a dataset against the reference grid

```python
from eocis_chuk_api.chuk_dataset_utils import CHUKDataSetUtils

utils = CHUKDataSetUtils("EOCIS-CHUK-GRID-100M-v0.4.nc") # downloaded as described above
ds = utils.load("EOCIS-CHUK-SQUIRRELPOPULATION-100M-v0.1.nc")
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
* Check metadata (provisional)
* Export CHUK data to geotiff, preserving metadata


