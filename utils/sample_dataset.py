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
import argparse

from eocis_chuk_api import CHUKDataSetUtils


def main():

    parser = argparse.ArgumentParser(description="sample_dataset.py: a utility for creating a lower resolution sample of a CHUK dataset")

    parser.add_argument("input_path", help="path to input CHUK netcdf4 file")
    parser.add_argument("output_path", help="path to output (sampled) CHUK netcdf4 file")
    parser.add_argument("resolution", type=int, help="resolution in metres for the sampled file, must be a multiple of 100")

    args = parser.parse_args()

    ds_in = xr.open_dataset(args.input_path)
    ds_out = CHUKDataSetUtils.sample(ds_in,args.resolution)
    ds_out.to_netcdf(args.output_path)


if __name__ == '__main__':
    main()

