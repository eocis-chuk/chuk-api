# -*- coding: utf-8 -*-

#     API for managing EOCIS-CHUK data
#
#     Copyright (C) 2023  EOCIS and National Centre for Earth Observation (NCEO)
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import xarray as xr

# geotiff support via rioxarray is optional
rioxarray_support = False
try:
    import rioxarray as rio
    rioxarray_support = True
except Exception as ex:
    pass

from chukmeta import CHUKMETA

class CHUKDataSetUtils:

    def __init__(self, chuk_grid_path):
        """
        Initialise with the path to the CHUK grid file

        :param chuk_grid_path: path to a grid file

        :notes: grid files can be obtained from https://gws-access.jasmin.ac.uk/public/nceo_uor/eocis-chuk/
        """
        self.chuk_grid_ds = xr.open_dataset(chuk_grid_path)

    def load(self, from_path, add_latlon=False, add_latlon_bnds=False):
        """
        Load a CHUK dataset from file and return an xarray dataset

        :param from_path: path to a NetCDF4 file
        :param add_latlon: add lon and lat 2D arrays to the dataset
        :param add_latlon_bnds: add lon_bnds and lat_bnds 2D arrays to the dataset
        :return: an xarray.Dataset object
        """
        ds = xr.open_dataset(from_path, decode_coords="all")

        self.check(ds)

        if add_latlon:
            ds = self.add_latlon(ds)

        if add_latlon_bnds:
            ds = self.add_latlon_bnds(ds)

        return ds

    def check(self, ds):
        """
        Check a dataset against CHUK format

        :param ds: the xarray.Dataset to check

        :raises: Exception if any checks fail
        """
        # check the dimensions are correct, compared to the grid
        for v in ["x","y"]:
            actual_shape = ds[v].shape
            expected_shape = self.chuk_grid_ds[v].shape
            if actual_shape != expected_shape:
                raise Exception(f"variable {v} shape ({actual_shape}) is different to expected x dimension shape ({expected_shape})")

        # perform metadata checks
        CHUKMETA.check(ds)

    def add_latlon(self, ds):
        """
        Add lat and lon 2D arrays from the reference grid

        :param ds: the xarray.Dataset to extend
        """
        ds["lon"] = self.chuk_grid_ds["lon"]
        ds["lat"] = self.chuk_grid_ds["lat"]


    def add_latlon_bnds(self,ds):
        """
        Add lat and lon 2D bounds from the reference grid

        :param ds: the xarray.Dataset to extend
        """
        ds["lon_bnds"] = self.chuk_grid_ds["lon_bnds"]
        ds["lat_bnds"] = self.chuk_grid_ds["lat_bnds"]


    def save_as_geotif(self, ds, variable_name, to_path):
        """
        Save a CHUK dataset to a geotiff

        :param ds: the CHUK dataset
        :param variable_name: the name of the variable to save from the dataset
        :param to_path: the path to save the geotiff file to
        """
        if not rioxarray_support:
            raise Exception("rioxarray is not available, CHUKdataSet.save_as_geotiff will not be available")
        if ds.rio.crs is None:
            # this is important if the dataset is later exported
            ds = ds.rio.write_crs("EPSG:27700")
        tags = CHUKMETA.to_json(ds, variable_name)
        ds[variable_name].rio.to_raster(to_path, tags=tags)



