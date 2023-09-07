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

class CHUKIO:

    def __init__(self, chuk_grid_path=None):
        self.chuk_grid_ds = xr.open_dataset(chuk_grid_path) if chuk_grid_path else None

    def check_grid_loaded(self):
        if self.chuk_grid_ds is None:
            raise Exception("Please initialise CHUK API with path to CHUK grid")

    def check_path(self, path):
        if not path.endswith(".nc"):
            raise Exception("Currently only netcdf4 files (filenames ending in .nc) are supported")

    def load(self, from_path, with_latlon=False, with_latlon_bnds=False):
        self.check_path(from_path)
        ds = xr.open_dataset(from_path)
        ds = self.adjust_latlon(ds, with_latlon, with_latlon_bnds)
        return ds

    def adjust_latlon(self, ds, with_latlon, with_latlon_bnds):
        if not with_latlon:
            for variable in ["lat", "lon"]:
                if variable in ds:
                    del ds[variable]

        if not with_latlon_bnds:
            for variable in ["lat_bnds", "lon_bnds"]:
                if variable in ds:
                    del ds[variable]

        if with_latlon and ("lat" not in ds or "lon" not in ds):
            self.check_grid_loaded()
            ds["lon"] = self.chuk_grid_ds["lon"]
            ds["lat"] = self.chuk_grid_ds["lat"]

        if with_latlon and ("lat_bnds" not in ds or "lon_bnds" not in ds):
            self.check_grid_loaded()
            ds["lon_bnds"] = self.chuk_grid_ds["lon_bnds"]
            ds["lat_bnds"] = self.chuk_grid_ds["lat_bnds"]

        return ds

    def save(self, ds, to_path, with_latlon=False, with_latlon_bnds=False):
        ds = self.adjust_latlon(ds, with_latlon, with_latlon_bnds)
        ds.to_netcdf(to_path) # TODO, encodings
