# chuk-api

Python API for working with CHUK datasets

## Objectives

* Producer API
  * Assist with creation of CHUK data files
* Consumer API
  * Create masked based on queries - eg create mask for all pixels containing power lines in Wales
  * This will be based on datasets created for the CHUK project by the IEA

## Currently Supported functionality (Producer API)

* Load from netcdf4
* Check dimensions against reference grid
* Check metadata (provisional)
* Export CHUK data to geotiff, preserving metadata

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

## Links to Resources

CHUK data files will be available from:

https://gws-access.jasmin.ac.uk/public/nceo_uor/eocis-chuk/

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
   "long_name":"estimated_squirrel_population",
   "coordinates": "lat lon",
    "grid_mapping": "crsOSGB"
})

# save the dataset
utils.save(chuk_ds, "EOCIS-CHUK-L4-SQUIRRELPOP-MERGED-20231204-v0.1.nc")
```

### Export a CHUK variable from NetCDF4 to geotiff

```python
from eocis_chuk_api.chuk_dataset_utils import CHUKDataSetUtils

utils = CHUKDataSetUtils("EOCIS-CHUK-GRID-100M-v0.4.nc") # downloaded as described above
ds = utils.load("EOCIS-CHUK-L4-SQUIRRELPOP-MERGED-20231204-v0.1.nc")
utils.save_as_geotif(ds, "squirrel_population", "EOCIS-CHUK-L4-SQUIRRELPOP-MERGED-20231204-v0.1.TIF")
```

### Check a dataset against the reference grid

```python
from eocis_chuk_api.chuk_dataset_utils import CHUKDataSetUtils

utils = CHUKDataSetUtils("EOCIS-CHUK-GRID-100M-v0.4.nc") # downloaded as described above
ds = utils.load("EOCIS-CHUK-SQUIRRELPOPULATION-100M-v0.1.nc")
(warnings, errors) = utils.check(ds)
```




