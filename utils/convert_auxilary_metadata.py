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

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="path to file to convert", default="/home/dev/Projects/CHUK/d1.8-land_cover.nc")
    parser.add_argument("--output-folder", help="folder to output converted file", default=".")
    parser.add_argument("--grid-path", help="CHUK grid file", default="/home/dev/Projects/CHUK/EOCIS-CHUK-GRID-100M-v0.4.nc")

    args = parser.parse_args()
    path = args.input
    output_folder = args.output_folder
    grid_path = args.grid_path

    input_filename = split(path)[-1]

    ds = xr.open_dataset(path)

    # compile a list of variables
    key_variables = []
    for vname in ds.variables:
        if vname not in ["crsOSGB", "lat", "lon", "x", "y"]:
            # include only 2D or higher variables
            if len(ds[vname].shape) > 1:
                key_variables.append(vname)

    utils = CHUKDataSetUtils(grid_path)

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
        "key_variables": ",".join(key_variables)
    }

    per_file_attributes = {
        "d1.8-land_cover.nc": {
            "source": "UKCEH 25m land cover"
        }
    }

    per_file_product_types = {
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
        "id": "uuid",
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

    product_type=per_file_product_types[input_filename]

    chuk_ds = utils.create_new_dataset(
        **mapped_attrs
    )

    for vname in ds.variables:
        if vname not in ["lat", "lon", "x", "y"]:
            print(f"Copying variable {vname}")
            attrs = attrs=ds[vname].attrs
            # if "grid_mapping" in attrs:
            #    del attrs["grid_mapping"]
            chuk_ds[vname] = xr.DataArray(ds[vname].data,dims=ds[vname].dims,attrs=attrs)


    version = ds.attrs["version"]

    filename = f"EOCIS-AUXILARY-L4-{product_type}-MERGED-2023-fv{version}.nc"
    tiff_filename = f"EOCIS-AUXILARY-L4-{product_type}-MERGED-2023-fv{version}.tiff"

    utils.save(chuk_ds,join(output_folder,filename))
    utils.save_as_geotif(chuk_ds,"land_cover",join(output_folder,tiff_filename))

    # ds = xr.open_dataset(filename)
    # print(ds)
    # ds = ds.drop_vars("crsOSGB: x y crsWGS84: lat lon")
    # print(ds)

    # ds.to_netcdf(join(output_folder,filename))


if __name__ == '__main__':
    main()

