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
import uuid
import datetime

from .chuk_metadata import CHUKMetadata


class CHUKDataSetUtils:

    def __init__(self, chuk_grid_path):
        """
        Initialise with the path to the CHUK grid file

        :param chuk_grid_path: path to a grid file

        :notes: grid files can be obtained from https://gws-access.jasmin.ac.uk/public/nceo_uor/eocis-chuk/
        """
        self.chuk_grid_ds = xr.open_dataset(chuk_grid_path)
        self.grid_resolution = int(self.chuk_grid_ds.x.data[1]) - int(self.chuk_grid_ds.x.data[0])

    def get_grid_latlons(self):
        """
        Return the chuk grid lats/lons

        :return: 2-tuple containing xarray.DataArray objects (lats,lons)
        """
        return (self.chuk_grid_ds.lat, self.chuk_grid_ds.lon)

    def get_grid_shape(self):
        """
        Return the chuk grid shape (y,x)

        :return: 2-tuple containing the grid (height, width)
        """
        return self.chuk_grid_ds.lat.shape

    def create_new_dataset(self,
                           title="A CHUK dataset",
                           institution = "EOCIS CHUK",
                           version = "1.0",
                           Conventions = "CF-1.10",
                           summary = "A summary of this dataset",
                           license = "Creative Commons Licence by attribution (https://creativecommons.org/licenses/by/4.0/)",
                           history = "describe the history of this product",
                           comment = "a useful comment about this dataset",
                           creator_url = "the creator\'s web URL",
                           creator_name = "the creator\'s name",
                           creator_email = "general email address for creator NOT a named individual",
                           creator_processing_institution = "the creator\'s institution",
                           date_created = None,
                           id = None,
                           source = "",
                           references = "",
                           tracking_id = "",
                           product_version = "",
                           format_version = "",
                           keywords = "",
                           naming_authority = "",
                           keywords_vocabulary = "",
                           cdm_data_type = "",
                           project = "",
                           geospatial_lat_min = "",
                           geospatial_lat_max = "",
                           geospatial_lon_min = "",
                           geospatial_lon_max = "",
                           geospatial_vertical_min = "",
                           geospatial_vertical_max = "",
                           time_coverage_start = "",
                           time_coverage_end = "",
                           time_coverage_duration = "",
                           time_coverage_resolution = "",
                           standard_name_vocabulary = "",
                           platform = "",
                           sensor = "",
                           geospatial_lat_units = "",
                           geospatial_lon_units = "",
                           geospatial_lat_resolution = "",
                           geospatial_lon_resolution = "",
                           key_variables = "",
                           **other_attributes):
        """
        Create a new CHUK dataset using CF/CCI standard metadata

        :return: an xarray.Dataset object
        """
        date_created = date_created if date_created else datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        id = id if id else str(uuid.uuid4())
        attrs = {
            "title": title,
            "institution": institution,
            "version": version,
            "Conventions": Conventions,
            "summary": summary,
            "license": license,
            "history": history,
            "comment": comment,
            "creator_url": creator_url,
            "creator_name": creator_name,
            "creator_email": creator_email,
            "creator_processing_institution": creator_processing_institution,
            "publisher_url": "https://eocis.org",
            "publisher_name": "EOCIS",
            "publisher_email": "EOCIS@reading.ac.uk",
            "acknowledgement": "Funded by UK EOCIS. Use of these data should acknowledge EOCIS",
            "date_created": date_created,
            "creation_date": date_created,
            "id": id,
            "spatial_resolution": f"{self.grid_resolution}m",
            "source": source,
            "references": references,
            "tracking_id": tracking_id,
            "product_version": product_version,
            "format_version": format_version,
            "keywords": keywords,
            "naming_authority": naming_authority,
            "keywords_vocabulary": keywords_vocabulary,
            "cdm_data_type": cdm_data_type,
            "project": project,
            "geospatial_lat_min": geospatial_lat_min,
            "geospatial_lat_max": geospatial_lat_max,
            "geospatial_lon_min": geospatial_lon_min,
            "geospatial_lon_max": geospatial_lon_max,
            "geospatial_vertical_min": geospatial_vertical_min,
            "geospatial_vertical_max": geospatial_vertical_max,
            "time_coverage_start": time_coverage_start,
            "time_coverage_end": time_coverage_end,
            "time_coverage_duration": time_coverage_duration,
            "time_coverage_resolution": time_coverage_resolution,
            "standard_name_vocabulary": standard_name_vocabulary,
            "platform": platform,
            "sensor": sensor,
            "geospatial_lat_units": geospatial_lat_units,
            "geospatial_lon_units": geospatial_lon_units,
            "geospatial_lat_resolution": geospatial_lat_resolution,
            "geospatial_lon_resolution": geospatial_lon_resolution,
            "key_variables": key_variables
        }
        attrs.update(other_attributes)
        ds = xr.Dataset(attrs=attrs)
        return ds

    def load(self, from_path, add_latlon=False, add_latlon_bnds=False):
        """
        Load a CHUK dataset from file and return an xarray dataset

        :param from_path: path to a NetCDF4 file
        :param add_latlon: add lon and lat 2D arrays to the dataset
        :param add_latlon_bnds: add lon_bnds and lat_bnds 2D arrays to the dataset
        :return: an xarray.Dataset object
        """
        ds = xr.open_dataset(from_path, decode_coords="all")

        if add_latlon:
            ds = self.add_latlon(ds)

        if add_latlon_bnds:
            ds = self.add_latlon_bnds(ds)

        return ds

    def save(self, ds, to_path, add_latlon=False, add_latlon_bnds=False, x_chunk_size=400, y_chunk_size=400, time_chunk_size=1):
        """
        Save a CHUK dataset to file, applying the standard chunking and compression

        :param ds: an xarray dataset containing CHUK data
        :param to_path: path to a NetCDF4 file
        :param add_latlon: add lon and lat 2D arrays to the dataset
        :param add_latlon_bnds: add lon_bnds and lat_bnds 2D arrays to the dataset
        :param x_chunk_size: size of chunking in the x-dimension
        :param y_chunk_size: size of chunking in the x-dimension
        :param time_chunk_size: size of chunking in the time dimension
        :return: an xarray.Dataset object
        """

        encodings = {}

        for v in ds.variables:
            dims = ds[v].dims
            if "x" in dims and "y" in dims:
                chunk_sizes = []
                for d in dims:
                    if d == "y":
                        chunk_sizes.append(y_chunk_size)
                    elif d == "x":
                        chunk_sizes.append(x_chunk_size)
                    elif d == "time":
                        chunk_sizes.append(time_chunk_size)
                    else:
                        chunk_sizes.append(0)

                encodings[v] = {
                    "zlib": True,
                    "complevel": 5,
                    "chunksizes" : chunk_sizes
                }

        if add_latlon:
            ds = self.add_latlon(ds)

        if add_latlon_bnds:
            ds = self.add_latlon_bnds(ds)

        if ds.rio.crs is None:
            # this is important if the dataset is later exported
            ds = ds.rio.write_crs("EPSG:27700")

        ds.to_netcdf(to_path, encoding=encodings)

    def check(self, ds):
        """
        Check a dataset against CHUK format

        :param ds: the xarray.Dataset to check

        :returns: 2-tuple (warnings, errors) containing lists of (code,detail)
        """

        # perform metadata checks
        warnings, errors = CHUKMetadata.check(ds)

        # check the dimensions are correct, compared to the grid
        for v in ["x","y"]:
            actual_shape = ds[v].shape
            expected_shape = self.chuk_grid_ds[v].shape
            if actual_shape != expected_shape:
                errors.append(("bad_shape",(v,actual_shape,expected_shape)))

        return warnings, errors

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
        ds_crs = ds.rio.write_crs("EPSG:27700")
        del ds_crs[variable_name].attrs["grid_mapping"] # this seems to cause a problem, why?
        tags = CHUKMetadata.to_json(ds_crs, variable_name)
        ds_crs[variable_name].rio.to_raster(to_path, tags=tags)





