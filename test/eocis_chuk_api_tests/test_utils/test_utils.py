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


import os.path
import xarray

from eocis_chuk_api import CHUKDataSetUtils

def download_test_file(to_local_folder, filename):
    local_path = os.path.join(to_local_folder, filename)

    if not os.path.exists(local_path):
        import requests
        r = requests.get("https://gws-access.jasmin.ac.uk/public/nceo_uor/eocis-chuk/test_files/"+filename, allow_redirects=True)
        with open(local_path,"wb") as f:
            f.write(r.content)

    return local_path



