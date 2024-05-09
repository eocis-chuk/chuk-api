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

import os
import argparse
import requests

import xarray as xr

from eocis_chuk_api import CHUKDataSetUtils


def main():

    parser = argparse.ArgumentParser(description="download_grid.py: a utility for downloading the CHUK grid from JASMIN")

    parser.add_argument("output_path", help="path to output the downloaded CHUK netcdf4 file")
    parser.add_argument("--resolution", choices=[100,1000], type=int, help="resolution in metres for the grid file, must be either 100 or 1000", default=100)

    args = parser.parse_args()

    if args.resolution not in [100,1000]:
        print(f"Invalid value {args.resolution} for --resolution, please specify 100 or 1000")

    filename = f"EOCIS-CHUK-GRID-{args.resolution}M-v1.0.nc"

    if not os.path.exists(args.output_path):
        url = "https://gws-access.jasmin.ac.uk/public/nceo_uor/eocis-chuk/"+filename
        r = requests.get(url, allow_redirects=True)
        if r.ok:
            with open(args.output_path,"wb") as f:
                f.write(r.content)
        else:
            print(f"Failed to fetch URL from {url}")
    else:
        print(f"File {args.output_path} already exists")

if __name__ == '__main__':
    main()


