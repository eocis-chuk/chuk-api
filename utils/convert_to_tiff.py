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

import argparse

from eocis_chuk_api import CHUKDataSetUtils


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="path to CHUK format netcdf4 file")
    parser.add_argument("variable_name", help="name of variable")
    parser.add_argument("grid_path",help="path to EOCIS CHUK grid file")
    parser.add_argument("output_path", help="path to output TIFF file")

    args = parser.parse_args()

    dsu = CHUKDataSetUtils(args.grid_path)
    ds = dsu.load(args.input_path)
    dsu.save_as_geotif(ds,args.variable_name,args.output_path)


if __name__ == '__main__':
    main()