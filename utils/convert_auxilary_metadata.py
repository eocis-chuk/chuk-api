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
from eocis_chuk_api.chuk_dataset_utils import CHUKDataSetUtils
import argparse
from os.path import split, join
import os

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
    "d1.1-land_water.nc": {
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
    }
}

per_file_product_types = {
    "d1.1-land_water.nc": "LANDWATER",
    "d1.2-countries.nc": "COUNTRY",
    "d1.3-counties.nc": "COUNTY",
    "d1.4-parishes.nc": "PARISH",
    "d1.5-postcodes.nc": "POSTCODE",
    "d1.6-nhs_boundaries.nc": "HEALTH",
    "d1.7-fire_boundaries.nc": "FIRERESCUE",
    "d1.8-land_cover.nc": "LANDCOVER"
}

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
    "summary=": "summary",
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

def convert(input_folder, input_filename, grid_path, output_folder):
    print(f"Processing input file {input_filename}")
    path = os.path.join(input_folder, input_filename)

    ds = xr.open_dataset(path)

    # compile a list of variables
    key_variables = []
    for vname in ds.variables:
        if vname not in ["crsOSGB", "lat", "lon", "x", "y"]:
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

    product_type = per_file_product_types[input_filename]
    history = ds.attrs.get("history", "")
    if history:
        history += ", "
    history += "reprocessed with metadata standardisation from " + input_filename
    mapped_attrs["history"] = history

    mapped_attrs["source"] = ds.attrs.get("source", input_filename)
    mapped_attrs["key_variables"] = ds.attrs.get("key_variables", ",".join(key_variables))

    chuk_ds = utils.create_new_dataset(
        **mapped_attrs
    )

    custom_encodings = {}
    for vname in ds.variables:
        if vname not in ["lat", "lon", "x", "y"]:
            print(f"\tCopying variable {vname}")
            attrs = attrs = ds[vname].attrs
            # if "grid_mapping" in attrs:
            #    del attrs["grid_mapping"]
            chuk_ds[vname] = xr.DataArray(ds[vname].data, dims=ds[vname].dims, attrs=attrs)
            if vname.endswith("str"):
                # apply a custom encoding for these string variables, chunking causes problems
                custom_encodings[vname] = { "zlib": True, "complevel": 5 }
    version = ds.attrs["version"]

    output_filename = f"EOCIS-AUXILARY-L4-{product_type}-MERGED-2023-fv{version}.nc"

    utils.save(chuk_ds, join(output_folder, output_filename), custom_encodings=custom_encodings)
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
            print(ex)

if __name__ == '__main__':
    main()

