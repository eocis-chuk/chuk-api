# chuk-api

Python API for working with CHUK datasets

Requirements

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
