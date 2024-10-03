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
from eocis_chuk_api import CHUKDataSetUtils
import argparse
from os.path import split, join
import os
import numpy as np
import datetime

cf_standard_names = set()
cf_standard_names_path = os.path.join(os.path.split(__file__)[0],"cf_standard_names_v82.txt")

with open(cf_standard_names_path) as f:
    for line in f.readlines():
        cf_standard_names.add(line.strip())

cf_standard_names.remove("region") # region should be removed as non-standard regions are supplied

comment = "Technical documentation describing how this data can be found in the accompanying technical documentation, which should have been provided with this data. A copy of the technical documentation can be found at https://eocis.org/portal/documents/IEA-EOCISAuxfiles-TR_Additional_v8.pdf"

constants = {
    "geospatial_lat_min": "47.08929443",
    "geospatial_lat_max": "61.13276672",
    "geospatial_lon_min": "-15.37353897",
    "geospatial_lon_max": "61.13276672",
    "geospatial_lat_units": "degrees_north",
    "geospatial_lon_units": "degrees_east",
    "geospatial_lon_resolution": "0.00153",
    "geospatial_lat_resolution": "0.00090",
    "geospatial_vertical_min": "0.0",
    "geospatial_vertical_max": "0.0",
    "project": "Earth Observation Climate Information Service (EOCIS)",
    "naming_authority": "uk.ac.stfc",
    "format_version": "EOCIS Data Standards v0.1, EOCIS CHUK Data Standards v0.1",
    "cdm_type": "grid",
    "standard_name_vocabulary": "CF Standard Name Table v82"
}

per_file_attributes = {
    "d1.1-land-water.nc": {
        "source": "UKCEH 10m land cover",
        "keywords": "Land, Water, River, Lake"
    },
    "d1.2-countries.nc": {
        "source": "UK Office for National Statistics (ONS)",
        "keywords": "Countries"
    },
    "d1.3-counties.nc": {
        "source": "UK Office for National Statistics (ONS)",
        "keywords": "UK Counties, UK Unitary Authorities"
    },
    "d1.4-parishes.nc": {
        "source": "UK Office for National Statistics (ONS)",
        "keywords": "UK Parishes"
    },
    "d1.5-postcodes.nc": {
        "source": "Doogal Archive",
        "keywords": "UK Postcodes"
    },
    "d1.6-nhs_boundaries.nc": {
        "source": "UK Office for National Statistics (ONS)",
        "keywords": "UK NHS Health Regions"
    },
    "d1.7-fire_boundaries.nc": {
        "source": "UK Office for National Statistics (ONS)",
        "keywords": "UK NHS Health Regions"
    },
    "d1.8-land_cover.nc": {
        "source": "UKCEH 25m land cover",
        "keywords": "Land Cover"
    },
    "d1.10-built_area.nc": {
        "source": "UKCEH 10m land cover",
        "keywords": "Land Cover"
    },
    "d1.11-power.nc": {
        "source": "OpenStreetMap",
        "keywords": "Land Cover, Power"
    },
    "d1.11-road-rail.nc": {
        "source": "OrdnanceSurvey, Open Data Northern Ireland, OpenStreetMap",
        "keywords": "Land Cover, Road, Rail"
    },
    "d1.12-elevation.nc": {
        "source": "Copernicus Global 30m DEM",
        "keywords": "Elevation, DEM, topography"
    },
    "d1.13-qualifications.nc": {
        "source": "UK Government, Office for National Statistics, Scottish Government, Northern Ireland Statistics and Research Agency, Scotland's Census",
        "keywords": "Educational Attainment"
    }
}

per_file_product_types = {
    "d1.1-land-water.nc": ("LANDWATER",2023),
    "d1.2-countries.nc": ("COUNTRY",2023),
    "d1.3-counties.nc": ("COUNTY",2023),
    "d1.4-parishes.nc": ("PARISH",2023),
    "d1.5-postcodes.nc": ("POSTCODE",2023),
    "d1.6-nhs_boundaries.nc": ("HEALTH",2023),
    "d1.7-fire_boundaries.nc": ("FIRERESCUE",2023),
    "d1.8-land_cover.nc": ("LANDCOVER",2023),
    "d1.10-built_area.nc": ("BUILTAREA",2023),
    "d1.11-power.nc": ("POWER",2023),
    "d1.11-road-rail.nc": ("ROADRAIL",2023),
    "d1.12-elevation.nc": ("ELEVATION",2023),
    "d1.13-qualifications.nc": ("QUALIFICATIONS",2023)
}

per_file_variable_attributes = {
    "d1.12-elevation.nc": {
        "elevation": {
            "units": "m"
        }
    },
    "d1.11-road-rail.nc": {
        "roads": {
            "flag_masks": np.array([1,2,4], dtype="int8")
        }
    },
    "d1.10-built_area.nc": {
        "urban_area": {
            "units": "1"
        },
        "suburban_area": {
            "units": "1"
        }
    }

}

per_file_variable_encodings = {
    "d1.11-power.nc": {
        "powerline": {
            "dtype": "byte",
            "_FillValue": -1
        }
    },
    "d1.11-road-rail.nc": {
        "roads": {
            "dtype": "byte",
            "_FillValue": -1
        },
        "railways": {
            "dtype": "byte",
            "_FillValue": -1
        }
    }
}

def fix_flag_meanings(da):
    old = da.attrs["flag_meanings"]
    new = ""
    for ch in old:
        if (ch >= 'a' and ch <= 'z') or (ch >= 'A' and ch <= "Z") or (ch >= '0' and ch <= '9') or ch in [' ','_','-',"+",".","@"]:
            new += ch
        else:
            new += '_'
    da.attrs["flag_meanings"] = new
    return da

per_file_variable_transforms = {
    "d1.13-qualifications.nc": {
        "area_code": lambda da: da.astype(np.int16)
    },
    "d1.1-land-water.nc": {
        "landwater": lambda da: da.astype(np.int8),
        "rivers": lambda da: da.astype(np.int8)
    },
    "d1.3-counties.nc": {
        "county": lambda da: fix_flag_meanings(da)
    },
    "d1.4-parishes.nc": {
        "parish": lambda da: fix_flag_meanings(da)
    },
    "d1.6-nhs_boundaries.nc": {
        "icb": lambda da: fix_flag_meanings(da)
    },
    "d1.7-fire_boundaries.nc": {
        "fire_boundary": lambda da: fix_flag_meanings(da)
    },
    "d1.8-land_cover.nc": {
        "land_cover": lambda da: da.astype(np.int8)
    }
}

per_file_transforms = {

}

def add_time(ds, year, with_bounds):
    time_attrs = {'units': 'days since 1970-01-01', 'calendar': 'proleptic_gregorian', 'long_name': 'time'}

    if with_bounds:
        time_attrs['bounds'] = 'time_bnds'

    ref_dt = datetime.datetime(1970, 1, 1)
    mid_dt = datetime.datetime(year, 7, 1)
    ds["time"] = xr.DataArray(np.array([(mid_dt - ref_dt).days], dtype=float), dims=("time",), attrs=time_attrs)
    if with_bounds:
        start_dt = datetime.datetime(year, 1, 1, 0, 0, 0)
        end_dt = datetime.datetime(year, 12, 31, 23, 59, 59)
        ds["time_bnds"] = xr.DataArray(np.array([[(start_dt - ref_dt).days,(end_dt - ref_dt).days]], dtype=float), dims=("time","nv"))
        ds.attrs["time_coverage_duration"] = "P1Y"
        ds.attrs["time_coverage_resolution"] = "P1Y"
        ds.attrs["time_coverage_start"] = start_dt.strftime("%Y%m%dT%H:%M:%SZ")
        ds.attrs["time_coverage_end"] = end_dt.strftime("%Y%m%dT%H:%M:%SZ")

def create_lccs_transform(year):
    def transform(ds):
        add_time(ds, year, with_bounds=True)
        ds["lccs_class"] = ds["lccs_class"].expand_dims("time")
        return ds
    return transform

def create_socioeconomic_itl3_transform(year):
    def transform(ds):
        ds = ds.rename_dims({"t":"time"})
        add_time(ds, year, with_bounds=True)
        return ds
    return transform

def create_socioeconomic_msoa_transform(year):
    def transform(ds):
        ds = ds.rename_dims({"t":"time"})
        add_time(ds, year, with_bounds=False)
        return ds
    return transform

for year in range(2001,2021):
    key = f"d1.9-lccs_{year:04d}.nc"
    per_file_product_types[key] = ("LANDCLASS",year)
    per_file_attributes[key] = {
        "keywords": "Land Cover",
        "source": "ESACCI Land Cover Classification System (https://cds.climate.copernicus.eu/cdsapp#!/dataset/satellite-land-cover?tab=overview)"
    }
    per_file_variable_transforms[key] = {
        "lccs_class": lambda da: da.astype(np.uint8)
    }
    per_file_transforms[key] = create_lccs_transform(year)


for year in range(1997,2022):
    key = f"d1.13-socioeconomic-itl3-{year:04d}.nc"
    per_file_variable_transforms[key] = {
        "itl3_code": lambda da: da.astype(np.int16)
    }
    per_file_variable_attributes[key] = {
        "pop_density": {
            "comment": "units are persons per square kilometre"
        }
    }
    per_file_product_types[key] = ("SOCIOECONOMIC_ITL3",year)
    per_file_attributes[key] = {
        "keywords": "household income, population, educational attainment",
        "source": "Office for National Statistics, Eurostat Population Database"
    }
    per_file_transforms[key] = create_socioeconomic_itl3_transform(year)


for year in [2014,2018,2020]:
    key = f"d1.13-socioeconomic-msoa-{year:04d}.nc"
    per_file_product_types[key] = ("SOCIOECONOMIC_MSOA",year)
    per_file_attributes[key] = {
        "keywords": "household income, population, educational attainment",
        "source": "Office for National Statistics, Eurostat Population Database, Scottish Government, Northern Ireland Statistics and Research Agency, Scotland's Census"
    }
    per_file_variable_attributes[key] = {
        "pop_density": {
            "comment": "units are persons per square kilometre"
        }
    }
    per_file_variable_transforms[key] = {
        "area_code": lambda da: da.astype(np.int16)
    }
    per_file_transforms[key] = create_socioeconomic_msoa_transform(year)


for key in per_file_attributes:
    per_file_attributes[key]["comment"] = comment

mapping = {
    "title": "title",
    "institution": "institution",
    "source": "",
    "history": "",
    "references": "comment",
    "tracking_id": "uuid",
    "Conventions": "Convention",
    "product_version": "version",
    "format_version": "",
    "summary": "summary",
    "keywords": "",
    "id": "id",
    "naming_aithority": "EOCIS CHUK",
    "keywords_vocabulary": "",
    "cdm_data_type": "",
    "comment": "comment",
    "date_created": "date_created",
    "creator_name": "creator_name",
    "creator_url": "creator_url",
    "creator_email": "creator_email",
    "time_coverage_start": "",
    "time_coverage_end": "",
    "time_coverage_duration": "",
    "time_coverage_resolution": "",
    "standard_name_vocabulary": "",
    "license": "license",
    "platform": "",
    "sensor": "",
    "spatial_resolution": "spatial_resolution",
    "publisher_name": "publisher_name",
    "publisher_email": "publisher_email",
    "publisher_url": "publisher_url",
    "acknowledgement": "acknowledgement"
}

attribute_processors = {
    "comment": lambda s: s.replace("https://eocis.org/","https://eocis.org/portal/documents/IEA-EOCISAuxfiles-TR_Additional_v8.pdf")
}

def convert(input_folder, input_filename, grid_path, output_folder):
    print(f"Processing input file {input_filename}")

    (product_type, year) = per_file_product_types[input_filename]

    path = os.path.join(input_folder, input_filename)

    ds = xr.open_dataset(path)

    version = ds.attrs["version"]

    output_filename = f"EOCIS-CHUK_GEOSPATIAL_INFORMATION-L4-{product_type}-MERGED-{year:04d}-fv{version}.nc"

    if os.path.exists(os.path.join(output_folder, output_filename)):
        print(f"Output file {output_filename} already exists!  Skipping...")
        return

    # compile a list of variables
    key_variables = []
    for vname in ds.variables:
        if vname not in ["crsOSGB", "lat", "lon", "x", "y", "lat_bnds", "lon_bnds", "x_bnds", "y_bnds"]:
            # include only 2D or higher variables
            if len(ds[vname].shape) > 1:
                key_variables.append(vname)

    utils = CHUKDataSetUtils(grid_path)

    mapped_attrs = {}

    for (name, value) in constants.items():
        mapped_attrs[name] = value

    for (name, mapped_name) in mapping.items():
        if mapped_name and mapped_name in ds.attrs:
            mapped_attrs[name] = ds.attrs[mapped_name]

    if input_filename in per_file_attributes:
        for key in per_file_attributes[input_filename]:
            if key not in mapped_attrs:
                mapped_attrs[key] = per_file_attributes[input_filename][key]

    history = ds.attrs.get("history", "")
    if history:
        history += ", "
    history += "reprocessed with metadata standardisation from " + input_filename
    mapped_attrs["history"] = history

    mapped_attrs["source"] = ds.attrs.get("source", input_filename)
    mapped_attrs["key_variables"] = ds.attrs.get("key_variables", ",".join(key_variables))

    # perform requested extra processing on attributes
    kvs = [(k,v) for (k,v) in mapped_attrs.items()]
    for (k,v) in kvs:
        if k in attribute_processors:
            mapped_attrs[k] = attribute_processors[k](v)

    chuk_ds = utils.create_new_dataset(
        **mapped_attrs
    )

    custom_encodings = {}
    override_encodings = per_file_variable_encodings.get(input_filename,{})

    for vname in key_variables:
        print(f"\tCopying variable {vname}")
        attrs = ds[vname].attrs
        # check standard_name is valid
        if "standard_name" in attrs:
            standard_name = attrs["standard_name"]
            if standard_name not in cf_standard_names:
                # variable has an invalid standard name, remove it
                print(f"removing invalid standard_name {standard_name}")
                del attrs["standard_name"]
                # if long_name is not already present, use the invalid standard name
                if "long_name" not in attrs:
                    attrs["long_name"] = standard_name
        ds_dims = ds[vname].dims
        if "x" in ds_dims and "y" in ds_dims:
            attrs["grid_mapping"] = "crsOSGB: x y"

        if input_filename in per_file_variable_attributes:
            if vname in per_file_variable_attributes[input_filename]:
                for (name,value) in per_file_variable_attributes[input_filename][vname].items():
                    attrs[name] = value

        da = xr.DataArray(ds[vname].data, dims=ds[vname].dims, attrs=attrs)
        if input_filename in per_file_variable_transforms:
            if vname in per_file_variable_transforms[input_filename]:
                da = per_file_variable_transforms[input_filename][vname](da)

        chuk_ds[vname] = da
        if vname.endswith("str"):
            # apply a custom encoding for these string variables, chunking causes problems
            custom_encodings[vname] = { "zlib": True, "complevel": 5 }


    chuk_ds.attrs["Conventions"] = "CF-1.8"

    if input_filename in per_file_transforms:
        chuk_ds = per_file_transforms[input_filename](chuk_ds)

    utils.save(chuk_ds, join(output_folder, output_filename), add_latlon=True, custom_encodings=custom_encodings, override_encodings=override_encodings)
    print(f"Written output file {output_filename}")

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--input-folder", help="path to folder containing files to convert", required=True)
    parser.add_argument("--output-folder", help="folder to output converted file", default=".")
    parser.add_argument("--grid-path", help="CHUK grid file", required=True)

    args = parser.parse_args()
    input_folder = args.input_folder
    output_folder = args.output_folder

    os.makedirs(output_folder, exist_ok=True)
    grid_path = args.grid_path

    for input_filename in os.listdir(input_folder):
        if input_filename not in per_file_product_types:
            continue
        try:
            convert(input_folder, input_filename, grid_path, output_folder)
        except Exception as ex:
            print(f"Failed to convert {input_filename}: {str(ex)}")


if __name__ == '__main__':
    main()

