# chuk-api

Python API for working with CHUK datasets built on (xarray)[https://xarray.dev/]

CHUK datasets provide Earth Observation-derived climate data and relevant auxilary data for the UK at 100m resolution, developed for the (EOCIS Project)[https://eocis.org]

The file format for storing CHUK data is NetCDF4.

## Objectives

* Consumer API
  * Create masked based on queries - for example *create a mask for all cells containing power lines in Wales*
  * Designed to be used with CHUK datasets describing UK administrative boundaries, infrastructure, demographic data, due to be released soon.
* Producer API
  * Assist with creation and maintenance of CHUK data files
  
## Installation

Installation into a miniforge enviromnent is suggested.  See [https://github.com/conda-forge/miniforge](https://github.com/conda-forge/miniforge) for installing miniforge.


```
mamba create -n chuk_api_env python=3.10
mamba activate chuk_api_env
mamba install rioxarray netcdf4 requests cfchecker
```

Clone this repo and run:

```
pip install .
```

Download CHUK grid reference file (latest version is v1.0):

```
wget https://gws-access.jasmin.ac.uk/public/nceo_uor/eocis-chuk/EOCIS-CHUK-GRID-100M-v1.0.nc
```

## Links to Resources

CHUK data files will be available from:

https://gws-access.jasmin.ac.uk/public/nceo_uor/eocis-chuk/

Full API documentation:

https://eocis-chuk.github.io/chuk-api/

CHUK Data Standards Document:

[Download CHUK Data Standards Document (latest version v1.1)](docs_src/EOCIS_CHUK_data_standards_v1.1.pdf)

## Usage

### Create a CHUK dataset

```python
import xarray as xr
import numpy as np
from eocis_chuk_api import CHUKDataSetUtils
utils = CHUKDataSetUtils("EOCIS-CHUK-GRID-100M-v1.0.nc") # downloaded as described above
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
     creator_name = "Institute of Biological Studies")
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

### Export a CHUK variable from a NetCDF4 dataset to geotiff

```python
from eocis_chuk_api import CHUKDataSetUtils

utils = CHUKDataSetUtils("EOCIS-CHUK-GRID-100M-v1.0.nc") # downloaded as described above
ds = utils.load("EOCIS-CHUK-L4-SQUIRRELPOP-MERGED-20231204-v0.1.nc")
utils.save_as_geotif(ds, "squirrel_population", "EOCIS-CHUK-L4-SQUIRRELPOP-MERGED-20231204-v0.1.TIF")
```

### Check a dataset against the reference grid

```python
from eocis_chuk_api import CHUKDataSetUtils

utils = CHUKDataSetUtils("EOCIS-CHUK-GRID-100M-v1.0.nc") # downloaded as described above
ds = utils.load("EOCIS-CHUK-SQUIRRELPOPULATION-100M-v0.1.nc")
(warnings, errors) = utils.check(ds)
```

### Create a boolean mask from a CHUK Auxilary file

```python
from eocis_chuk_api import CHUKAuxilaryUtils

# build a mask with all pixels containing power lines or substations, whatever the voltage
substation_mask = CHUKAuxilaryUtils.create_mask("d1.11-power.nc", "powerline", mask_values="*kV")
powerline_mask = CHUKAuxilaryUtils.create_mask("d1.11-power.nc", "powerline", mask_values="*kV")
combined_mask = CHUKAuxilaryUtils.combine_masks_or(powerline_mask, substation_mask)
print(combined_mask.count(),combined_mask.fraction())
bool_array = combined_mask.to_array()
```




