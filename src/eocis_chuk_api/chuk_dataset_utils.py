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
                           title="",
                           include_lon_lat=True,
                           institution="EOCIS CHUK",
                           source="",
                           history="",
                           references="",
                           tracking_id="",
                           Conventions="CF-1.10",
                           product_version="",
                           format_version="",
                           summary="",
                           keywords="",
                           id="",
                           naming_aithority = "",
                           keywords_vocabulary = "",
                           cdm_data_type = "",
                           comment = "",
                           date_created = "",
                           creator_name = "",
                           creator_url = "",
                           creator_email = "",
                           project = "Earth Observation Climate Information Service (EOCIS)",
                           geospatial_lat_min = "",
                           geospatial_lat_max = "",
                           geospatial_lon_min="",
                           geospatial_lon_max="",
                           geospatial_vertical_min="",
                           geospatial_vertical_max="",
                           time_coverage_start="",
                           time_coverage_end="",
                           time_coverage_duration="",
                           time_coverage_resolution="",
                           standard_name_vocabulary="",
                           license="",
                           platform="",
                           sensor="",
                           spatial_resolution="",
                           geospatial_lat_units="",
                           geospatial_lon_units="",
                           geospatial_lon_resolution="",
                           geospatial_lat_resolution="",
                           key_variables="",
                           acknowledgement="Funded by UK EOCIS. Use of these data should acknowledge EOCIS",
                           publisher_url = "https://eocis.org",
                           publisher_name = "EOCIS",
                           publisher_email = "EOCIS@reading.ac.uk",
                           **other_attributes):
        """
        Create a new CHUK dataset with expected global attributes.

        :param include_lon_lat: True if lon and lat 2d variables should be included
        :param title: a title for the dataset
        :param institution: Succinct description of the dataset
        :param source: Comma separated list of original data sources (+DOIs if available)
        :param history: Processing history of the dataset
        :param references: References to algorithm, ATBD, technical note describing dataset
        :param tracking_id: A UUID (Universal Unique Identifier) value
        :param Conventions: The CF Version e.g. CF-1.10
        :param product_version: The product version of this data file
        :param format_version: The EOCIS data format used e.g. “EOCIS Data Standards v1.x”
        :param summary: A paragraph describing the dataset
        :param keywords: A comma separated list of key words and phrases
        :param id: see naming_authority
        :param naming_authority: The combination of the naming authority and the id should be a globally unique identifier for the dataset
        :param keywords_vocabulary: If you are following a guideline for the words/phrases in your “keywords” attribute, put the name of that guideline here
        :param cdm_data_type: The THREDDS data type appropriate for this dataset
        :param comment: Miscellaneous information about the data
        :param date_created: The date on which the data was created
        :param creator_name: The person/organisation that created the data
        :param creator_url: A URL for the person/organisation that created the data
        :param creator_email: Contact email address for the person/organisation that created the data
        :param project: The scientific project that produced the data: “Earth Observation Climate Information Service (EOCIS)”
        :param geospatial_lat_min: Decimal degrees north, range -90 to +90
        :param geospatial_lat_max: Decimal degrees north, range -90 to +90
        :param geospatial_lon_min: Decimal degrees east, range -180 to +180
        :param geospatial_lon_max: Decimal degrees east, range -180 to +180
        :param geospatial_vertical_min: Assumed to be in metres above ground unless geospatial_vertical_units attribute defined otherwise
        :param geospatial_vertical_max: Assumed to be in metres above ground unless geospatial_vertical_units attribute defined otherwise
        :param time_coverage_start: Format yyyymmddThhmmssZ
        :param time_coverage_end: Format yyyymmddThhmmssZ
        :param time_coverage_duration: Should be an ISO8601 duration string
        :param time_coverage_resolution: Should be an ISO8601 duration string. For L2 data on the original satellite sampling it is acceptable to use 'satellite_orbit_frequency'
        :param standard_name_vocabulary: The name of the controlled vocabulary from which variable standard names are taken e.g. ‘CF Standard Name Table v82’
        :param license: Describe the restrictions to data access and distribution
        :param platform: Satellite name e.g. Sentinel-5. Separate lists by commas and use angled brackets for a platform series, e.g. ‘Envisat, NOAA-<12,14,16,17,18>, Metop-A’. The platform names used should follow the naming in the CCI controlled vocabulary
        :param sensor: Sensor name e.g. AATSR. Separate lists by commas.  The platform names used should follow the naming in the CCI controlled vocabulary
        :param spatial_resolution: A free-text string describing the approximate resolution of the product. For example, “1.1km at nadir”. This is intended to provide a useful indication to the user, so if more than one resolution is relevant e.g. the grid resolution and the data resolution, then both can be included.
        :param geospatial_lat_units: Geospatial latitude units used
        :param geospatial_lon_units: Geospatial longitude units used
        :param geospatial_lon_resolution: Geospatial latitude resolution used
        :param geospatial_lat_resolution: Geospatial longitude resolution used
        :param key_variables: A comma separated list of the key primary variables in the file i.e. those that have been scientifically validated.
        :param acknowledgement: Acknowledge funding sources and/or contributors
        :param other_attributes: any other attributes to include

        :return: an xarray.Dataset object
        """

        attrs = {}
        self.__extend_attrs(attrs, "title", title, required=True)
        self.__extend_attrs(attrs,"institution",institution, required=True)
        self.__extend_attrs(attrs, "source", source)
        self.__extend_attrs(attrs, "history", history)
        self.__extend_attrs(attrs, "references", references)
        self.__extend_attrs(attrs, "tracking_id", tracking_id, required=True),
        self.__extend_attrs(attrs, "Conventions", Conventions)
        self.__extend_attrs(attrs, "product_version",product_version, required=True)
        self.__extend_attrs(attrs, "format_version",format_version)
        self.__extend_attrs(attrs, "summary",summary)
        self.__extend_attrs(attrs, "keywords",keywords)
        self.__extend_attrs(attrs, "id",id),
        self.__extend_attrs(attrs, "naming_aithority", naming_aithority),
        self.__extend_attrs(attrs, "keywords_vocabulary",keywords_vocabulary),
        self.__extend_attrs(attrs, "cdm_data_type", cdm_data_type),
        self.__extend_attrs(attrs, "comment", comment),
        self.__extend_attrs(attrs, "date_created", date_created),
        self.__extend_attrs(attrs, "creator_name", creator_name),
        self.__extend_attrs(attrs, "creator_url", creator_url),
        self.__extend_attrs(attrs, "creator_email", creator_email),
        self.__extend_attrs(attrs, "project", project),
        self.__extend_attrs(attrs, "geospatial_lat_min", geospatial_lat_min),
        self.__extend_attrs(attrs, "geospatial_lat_max", geospatial_lat_max),
        self.__extend_attrs(attrs, "geospatial_lon_min", geospatial_lon_min),
        self.__extend_attrs(attrs, "geospatial_lon_max", geospatial_lon_max),
        self.__extend_attrs(attrs, "geospatial_vertical_min", geospatial_vertical_min),
        self.__extend_attrs(attrs, "geospatial_vertical_max", geospatial_vertical_max),
        self.__extend_attrs(attrs, "time_coverage_start", time_coverage_start),
        self.__extend_attrs(attrs, "time_coverage_end", time_coverage_end),
        self.__extend_attrs(attrs, "time_coverage_duration", time_coverage_duration),
        self.__extend_attrs(attrs, "time_coverage_resolution", time_coverage_resolution),
        self.__extend_attrs(attrs, "standard_name_vocabulary", standard_name_vocabulary),
        self.__extend_attrs(attrs, "license", license),
        self.__extend_attrs(attrs, "platform", platform),
        self.__extend_attrs(attrs, "sensor", sensor),
        self.__extend_attrs(attrs, "spatial_resolution", spatial_resolution),
        self.__extend_attrs(attrs, "geospatial_lat_units", geospatial_lat_units),
        self.__extend_attrs(attrs, "geospatial_lon_units", geospatial_lon_units),
        self.__extend_attrs(attrs, "geospatial_lon_resolution", geospatial_lon_resolution),
        self.__extend_attrs(attrs, "geospatial_lat_resolution", geospatial_lat_resolution),
        self.__extend_attrs(attrs, "key_variables", key_variables)
        self.__extend_attrs(attrs, "acknowledgement", acknowledgement)
        self.__extend_attrs(attrs, "publisher_name", publisher_name),
        self.__extend_attrs(attrs, "publisher_url", publisher_url),
        self.__extend_attrs(attrs, "publisher_email", publisher_email),

        attrs.update(other_attributes)
        ds = xr.Dataset(attrs=attrs)
        # copy the lat/lon bounds
        copyvars = ["x", "y", "crsOSGB"]
        if include_lon_lat:
            copyvars += ["lon", "lat"]
        for copyvar in copyvars:
            ds[copyvar] = self.chuk_grid_ds[copyvar]

        ds = ds.rio.write_crs("EPSG:27700")
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


    def save(self, ds, to_path, add_latlon=False, add_latlon_bnds=False, x_chunk_size=200, y_chunk_size=200,
             time_chunk_size=1, custom_encodings={}):
        """
        Save a CHUK dataset to file, applying the standard chunking and compression

        :param ds: an xarray dataset containing CHUK data
        :param to_path: path to a NetCDF4 file
        :param add_latlon: add lon and lat 2D arrays to the dataset
        :param add_latlon_bnds: add lon_bnds and lat_bnds 2D arrays to the dataset
        :param x_chunk_size: size of chunking in the x-dimension
        :param y_chunk_size: size of chunking in the x-dimension
        :param time_chunk_size: size of chunking in the time dimension
        :param custom_encodings: dictionary mapping from variable names to a custom encoding to use
        :return: an xarray.Dataset object
        """

        encodings = {}

        for v in ds.variables:
            if custom_encodings and v in custom_encodings:
                encodings[v] = custom_encodings[v]
            else:
                dims = ds[v].dims
                if "x" in dims and "y" in dims:

                    encodings[v] = {
                        "zlib": True,
                        "complevel": 5
                    }

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
                    encodings[v]["chunksizes"] = chunk_sizes

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



    def __extend_attrs(self, attrs, key, value, required=False):
        if required and not value:
            raise ValueError(f"attribute {key} is required")
        else:
            if value:
                attrs[key] = value
