# -*- coding: utf-8 -*-
import datetime

import numpy as np
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
import xarray
from .chuk_metadata import CHUKMetadata


class CHUKDataSetUtils:
    """Provide utility functions for working with CHUK datasets, based on xarray data structures.

    This class helps users to work with CHUK datasets, providing support for creating and converting data and metadata

    Examples:

        >>> import xarray as xr
        >>> import numpy as np
        >>> from eocis_chuk_api import CHUKDataSetUtils
        >>> utils = CHUKDataSetUtils("EOCIS-CHUK-GRID-100M-v1.0.nc")
        >>> chuk_ds = utils.create_new_dataset(
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
        >>> # create an array to hold the data
        >>> population_data = np.zeros(utils.get_grid_shape())
        >>> # populate the data
        >>> population_data[...] = ...
        >>> # attach the data
        >>> chuk_ds["squirrel_population"] = xr.DataArray(population_data,dims=("y","x"), attrs={
            "long_name":"estimated_squirrel_population",
            "coordinates": "lat lon",
            "grid_mapping": "crsOSGB"
        })
        >>> # save the dataset
        >>> utils.save(chuk_ds, "EOCIS-CHUK-L4-SQUIRRELPOP-MERGED-20231204-v0.1.nc")

    """

    def __init__(self, chuk_grid_path: str):
        """
        Initialise an instance with the path to the CHUK grid file

        Args:
            chuk_grid_path: path to a grid file

        Notes:
            grid files can be obtained from https://gws-access.jasmin.ac.uk/public/nceo_uor/eocis-chuk/

        Examples:
            >>> from eocis_chuk_api import CHUKDataSetUtils
            >>> utils = CHUKDataSetUtils("EOCIS-CHUK-GRID-100M-v0.4.nc")
        """
        self.chuk_grid_ds = xr.open_dataset(chuk_grid_path)
        self.grid_resolution = int(self.chuk_grid_ds.x.data[1]) - int(self.chuk_grid_ds.x.data[0])

    def get_grid_latlons(self) -> (xarray.DataArray, xarray.DataArray):
        """
        Obtain the chuk grid lats/lons

        Returns:
            2-tuple containing xarray.DataArray objects (lats,lons)
        """
        return (self.chuk_grid_ds.lat, self.chuk_grid_ds.lon)

    def get_grid_shape(self) -> (int, int):
        """
        Obtain the chuk grid shape (y,x)

        Returns:
            2-tuple containing the grid (height, width)
        """
        return self.chuk_grid_ds.lat.shape

    def create_filename(self, project: str, processing_level: str, product_type: str, product_string: str,
                        datetime: str, version: str, additional_segregator: str = None, suffix: str = ".nc") -> str:
        """
        Create an EOCIS standards compliant filename

        Args:
            project: the EOCIS project string (see the appropriate standards doc)
            processing_level: specify the processing level in (L0, L1A, L1B, L1C, L2, L2P, L3, L3U, L3C, L3S, L4, IND)
            product_type: standardised term to describe the main product type in te dataset, see standards doc
            product_string: descriptive name chosen from the team, should not contain hyphens, can contain underscores
            datetime: date and optionally time, format YYYY[MM[DD[HH[MM[SS]]]]]
            version: File version number one or more digits followed by an optional "." and another one or more digits
            additional_segregator: an optional extra segregator, to be used if otherwise different data sets
                                   would generate the same filename
            suffix: the file suffix, including the "."

        Returns:
            Formatted filename
        """
        segregator = "" if additional_segregator is None else "-" + additional_segregator
        return f"EOCIS-{project}-{processing_level}-{product_type}-{product_string}{segregator}-{datetime}-fv{version}{suffix}"

    def create_new_dataset(self,
                           title: str = "",
                           include_lon_lat: bool = False,
                           institution: str = "EOCIS CHUK",
                           source: str = "",
                           history: str = "",
                           references: str = "",
                           tracking_id: str = "",
                           Conventions: str = "CF-1.10",
                           product_version: str = "",
                           format_version: str = "",
                           summary: str = "",
                           keywords: str = "",
                           id: str = "",
                           naming_authority: str = "",
                           keywords_vocabulary: str = "",
                           cdm_data_type: str = "",
                           comment: str = "",
                           date_created: str = "",
                           creator_name: str = "",
                           creator_url: str = "",
                           creator_email: str = "",
                           project: str = "Earth Observation Climate Information Service (EOCIS)",
                           geospatial_lat_min: str = "47.089",
                           geospatial_lat_max: str = "61.133",
                           geospatial_lon_min: str = "-15.374",
                           geospatial_lon_max: str = "4.750",
                           geospatial_vertical_min: str = "0",
                           geospatial_vertical_max: str = "0",
                           time_coverage_start: str = "",
                           time_coverage_end: str = "",
                           time_coverage_duration: str = "",
                           time_coverage_resolution: str = "",
                           standard_name_vocabulary: str = "",
                           license: str = "Creative Commons Attribution 4.0 International (CC-BY 4.0 license)",
                           platform: str = "",
                           sensor: str = "",
                           spatial_resolution: str = "100m",
                           geospatial_lat_units: str = "degrees_north",
                           geospatial_lon_units: str = "degrees_east",
                           geospatial_lon_resolution: str = "0.0009",
                           geospatial_lat_resolution: str = "0.00086",
                           key_variables: str = "",
                           acknowledgement: str = "Funded by UK EOCIS. Use of these data should acknowledge EOCIS",
                           publisher_url: str = "https://eocis.org",
                           publisher_name: str = "EOCIS",
                           publisher_email: str = "EOCIS@reading.ac.uk",
                           **other_attributes: dict) -> xarray.Dataset:
        """
        Create a new CHUK dataset with expected global attributes.

        Args:
            include_lon_lat: True if lon and lat 2d variables should be included
            title: a title for the dataset
            institution: Succinct description of the dataset
            source: Comma separated list of original data sources (+DOIs if available)
            history: Processing history of the dataset
            references: References to algorithm, ATBD, technical note describing dataset
            tracking_id: A UUID (Universal Unique Identifier) value
            Conventions: The CF Version e.g. CF-1.10
            product_version: The product version of this data file
            format_version: The EOCIS data format used e.g. “EOCIS Data Standards v1.x”
            summary: A paragraph describing the dataset
            keywords: A comma separated list of key words and phrases
            id: see naming_authority
            naming_authority: The combination of the naming authority and the id should be a globally unique identifier for the dataset
            keywords_vocabulary: If you are following a guideline for the words/phrases in your “keywords” attribute, put the name of that guideline here
            cdm_data_type: The THREDDS data type appropriate for this dataset
            comment: Miscellaneous information about the data
            date_created: The date on which the data was created
            creator_name: The person/organisation that created the data
            creator_url: A URL for the person/organisation that created the data
            creator_email: Contact email address for the person/organisation that created the data
            project: The scientific project that produced the data: “Earth Observation Climate Information Service (EOCIS)”
            geospatial_lat_min: Decimal degrees north, range -90 to +90
            geospatial_lat_max: Decimal degrees north, range -90 to +90
            geospatial_lon_min: Decimal degrees east, range -180 to +180
            geospatial_lon_max: Decimal degrees east, range -180 to +180
            geospatial_vertical_min: Assumed to be in metres above ground unless geospatial_vertical_units attribute defined otherwise
            geospatial_vertical_max: Assumed to be in metres above ground unless geospatial_vertical_units attribute defined otherwise
            time_coverage_start: Format yyyymmddThhmmssZ
            time_coverage_end: Format yyyymmddThhmmssZ
            time_coverage_duration: Should be an ISO8601 duration string, for example P1D
            time_coverage_resolution: Should be an ISO8601 duration string. For L2 data on the original satellite sampling it is acceptable to use 'satellite_orbit_frequency'
            standard_name_vocabulary: The name of the controlled vocabulary from which variable standard names are taken e.g. ‘CF Standard Name Table v82’
            license: Describe the restrictions to data access and distribution
            platform: Satellite name e.g. Sentinel-5. Separate lists by commas and use angled brackets for a platform series, e.g. ‘Envisat, NOAA-<12,14,16,17,18>, Metop-A’. The platform names used should follow the naming in the CCI controlled vocabulary
            sensor: Sensor name e.g. AATSR. Separate lists by commas.  The platform names used should follow the naming in the CCI controlled vocabulary
            spatial_resolution: A free-text string describing the approximate resolution of the product. For example, “1.1km at nadir”. This is intended to provide a useful indication to the user, so if more than one resolution is relevant e.g. the grid resolution and the data resolution, then both can be included.
            geospatial_lat_units: Geospatial latitude units used
            geospatial_lon_units: Geospatial longitude units used
            geospatial_lon_resolution: Geospatial latitude resolution used
            geospatial_lat_resolution: Geospatial longitude resolution used
            key_variables: A comma separated list of the key primary variables in the file i.e. those that have been scientifically validated.
            acknowledgement: Acknowledge funding sources and/or contributors
            other_attributes: any other attributes to include

        Returns:
            An xarray.Dataset object
        """

        attrs = {}
        self.__extend_attrs(attrs, "title", title, required=True)
        self.__extend_attrs(attrs, "institution", institution, required=True)
        self.__extend_attrs(attrs, "source", source)
        self.__extend_attrs(attrs, "history", history)
        self.__extend_attrs(attrs, "references", references)
        self.__extend_attrs(attrs, "tracking_id", tracking_id, required=True),
        self.__extend_attrs(attrs, "Conventions", Conventions)
        self.__extend_attrs(attrs, "product_version", product_version, required=True)
        self.__extend_attrs(attrs, "format_version", format_version)
        self.__extend_attrs(attrs, "summary", summary)
        self.__extend_attrs(attrs, "keywords", keywords)
        self.__extend_attrs(attrs, "id", id),
        self.__extend_attrs(attrs, "naming_authority", naming_authority),
        self.__extend_attrs(attrs, "keywords_vocabulary", keywords_vocabulary, required=False),
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
        # copy the grid definition from the grid file
        copyvars = ["x", "y", "x_bnds", "y_bnds", "crsOSGB"]
        if include_lon_lat:
            copyvars += ["lon", "lat"]
        for copyvar in copyvars:
            ds[copyvar] = self.chuk_grid_ds[copyvar]

        ds = ds.rio.write_crs("EPSG:27700", grid_mapping_name="crsOSGB")

        return ds

    def add_variable(self, to_dataset: xr.Dataset, data: np.array, variable_name: str, standard_name: str = None,
                     long_name: str = None, units: str = None, source: str = None, **other_attrs:dict):
        """
        Add a new variable to a dataset.  The dataset is updated in-place.

        Args:
            to_dataset: The xarray.Dataset to which the variable will be added
            data: a numpy array containing the data, organised by (y,x), (time,y,x) or (y,x,time)
            variable_name: the name of the variable to be added to the dataset
            standard_name: CF standard name (if appropriate)
            long_name:  A longer descriptive name of the variable
            units: units from UDUNITS
            other_attrs: dictionary containing other attributes to add to the new variable

        Raises:
            ValueError: if the data parameter does not match the expected shape
        """
        expected_shape = self.get_grid_shape()
        if len(data.shape) == 2:
            dims = ("y", "x")
            if data.shape != expected_shape:
                raise ValueError("Bad data shape, expecting: " + str(expected_shape) + " was: " + str(data.shape))
        else:
            if data.shape[1:] == expected_shape:
                dims = ("time", "y", "x")
            elif data.shape[1:] == expected_shape:
                dims = ("y", "x", "time")

        attrs = {
            "grid_mapping": "crsOSGB"
        }
        if standard_name is not None:
            attrs["standard_name"] = standard_name
        if long_name is not None:
            attrs["long_name"] = long_name
        if source is not None:
            attrs["source"] = source
        if units is not None:
            attrs["units"] = units
        attrs.update(other_attrs)

        to_dataset[variable_name] = xr.DataArray(data=data, dims=dims, attrs=attrs)

    def load(self, from_path: str, add_latlon: bool = False, add_latlon_bnds: bool = False) -> xarray.Dataset:
        """
        Load a CHUK dataset from file and return a dataset

        Args:
            from_path: path to a NetCDF4 file
            add_latlon: add lon and lat 2D arrays to the dataset
            add_latlon_bnds: add lon_bnds and lat_bnds 2D arrays to the dataset

        Returns:
            A dataset containing the loaded CHUK data
        """
        ds = xr.open_dataset(from_path, decode_coords="all")

        self.extend_latlon(ds, add_latlon=add_latlon, add_latlon_bnds=add_latlon_bnds)

        return ds

    def save(self, ds: xarray.Dataset, to_path: str, add_latlon: bool = False, add_latlon_bnds: bool = False,
             x_chunk_size: int = 1000, y_chunk_size: int = 1000,
             time_chunk_size: int = 1, custom_encodings: dict = {}, override_encodings: dict={}):
        """
        Save a CHUK dataset to file, applying the standard chunking and compression

        Args:
            ds: an xarray dataset containing CHUK data
            to_path: path to a NetCDF4 file
            add_latlon: add lon and lat 2D arrays to the dataset
            add_latlon_bnds: add lon_bnds and lat_bnds 2D arrays to the dataset
            x_chunk_size: size of chunking in the x-dimension
            y_chunk_size: size of chunking in the x-dimension
            time_chunk_size: size of chunking in the time dimension
            custom_encodings: dictionary mapping from variable names to a custom encoding to use by xarray
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

                    if v in override_encodings:
                        for (name,value) in override_encodings[v].items():
                            if value is None:
                                if name in encodings:
                                    del encodings[v][name]
                            else:
                                encodings[v][name] = value

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

        self.extend_latlon(ds, add_latlon=add_latlon, add_latlon_bnds=add_latlon_bnds)


        # ds = ds.rio.write_crs("EPSG:27700",grid_mapping_name="crsOSGB")

        ds.to_netcdf(to_path, encoding=encodings)

    def extend_latlon(self, ds, add_latlon=False, add_latlon_bnds=False):
        if add_latlon:
            self.add_latlon(ds)

        if add_latlon_bnds:
            self.add_latlon_bnds(ds)

        if add_latlon:
            for v in ["lat", "lon"]:
                # remove bounds if no such variable exists
                bounds = ds[v].attrs.get("bounds",None)
                if bounds and bounds not in ds.variables:
                    del ds[v].attrs["bounds"]

    def check(self, ds: xarray.Dataset) -> ([(str, str)], [(str, str)]):
        """
        Check a dataset against CHUK format, returning details of any problems found

        Args:
            ds: the xarray.Dataset to check

        Returns:
            2-tuple (warnings, errors) containing lists of (code,detail) tuples
        """

        # perform metadata checks
        warnings, errors = CHUKMetadata.check(ds)

        # check the dimensions are correct, compared to the grid
        for v in ["x", "y"]:
            actual_shape = ds[v].shape
            expected_shape = self.chuk_grid_ds[v].shape
            if actual_shape != expected_shape:
                errors.append(("bad_shape", (v, actual_shape, expected_shape)))

        return warnings, errors

    @staticmethod
    def sample(ds: xarray.Dataset, to_resolution: int) -> xarray.Dataset:
        """
        Create a lower resolution sample of a CHUK dataset

        Args:
            ds: the xarray.Dataset containing CHUK data to sample
            to_resolution: the resolution for the sampled output, must be a multiple of 100

        Returns:
            A dataset containing the sampled data
        """
        if to_resolution % 100 != 0:
            raise ValueError(f"Error - resolution requested ({to_resolution}) is not a multiple of 100")
        sample_step = int(to_resolution / 100)
        return ds.isel(x=slice(0, -1, sample_step), y=slice(0, -1, sample_step))

    def add_latlon(self, ds: xarray.Dataset):
        """
        Add lat and lon 2D arrays from the reference grid

        Args:
            ds: the dataset to mondify in-place
        """
        ds["lon"] = self.chuk_grid_ds["lon"]
        ds["lat"] = self.chuk_grid_ds["lat"]

    def add_latlon_bnds(self, ds: xarray.Dataset):
        """
        Add lat and lon 2D bounds from the reference grid

        Args:
           ds: the dataset to mondify in-place
        """
        ds["lon_bnds"] = self.chuk_grid_ds["lon_bnds"]
        ds["lat_bnds"] = self.chuk_grid_ds["lat_bnds"]

    @staticmethod
    def save_as_geotif(ds: xarray.Dataset, variable_name: str, to_path: str):
        """
        Save a CHUK dataset to a geotiff

        Args:
            ds: the CHUK dataset
            variable_name: the name of the variable to save from the dataset
            to_path: the path to save the geotiff file to
        """
        ds_crs = ds.rio.write_crs("EPSG:27700")
        if "grid_mapping" in ds_crs[variable_name].attrs:
            # this seems to cause a problem, why?
            del ds_crs[variable_name].attrs["grid_mapping"]
        tags = CHUKMetadata.to_json(ds_crs, variable_name)
        ds_crs[variable_name].rio.to_raster(to_path, tags=tags, driver="COG")

    def __extend_attrs(self, attrs, key, value, required=None):
        if required and value == "" or value is None:
            raise ValueError(f"attribute {key} is required")
        else:
            if value == "" or value is None:
                return
            attrs[key] = value
