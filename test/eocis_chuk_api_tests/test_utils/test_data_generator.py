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

import numpy as np
import xarray as xr
import uuid

class TestDataGenerator:

    def __init__(self, chuk_dataset_utils):
        self.chuk_dataset_utils = chuk_dataset_utils

    def create_distances(self, utils, from_lat, from_lon):
        """
        Return a test CHUK dataset containing distances from a central point, in km

        :param utils: CHUKDatasetUtils instance
        :param from_lat: central point latitude
        :param from_lon: central point longitude

        :return: xarray.Dataset
        """
        lats, lons = self.chuk_dataset_utils.get_grid_latlons()

        # based on haversine example
        # https://gist.github.com/rochacbruno/2883505
        radius = 6371  # km

        dlat = np.radians(lats - from_lat)
        dlon = np.radians(lons - from_lon)
        a = np.sin(dlat / 2) * np.sin(dlat / 2) + np.cos(np.radians(lats)) \
            * np.cos(np.radians(from_lat)) * np.sin(dlon / 2) * np.sin(dlon / 2)
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        dists = radius * c * 1000

        ds = utils.create_new_dataset(title="Distance to the GB Centroid",
          product_version="1.0",
                            summary="The distance in km using the haversine formula to each CHUK grid location from the centroid of Great Britain",
                            tracking_id=str(uuid.uuid4()))

        ds["distances"] = xr.DataArray(dists, dims=("y", "x"), attrs={
            "long_name": "distance to Great British centroid",
            "units": "m",
            "comment": "calculated using the haversine formula",
            "coordinates": "lat lon",
            "grid_mapping": "crsOSGB"
        })
        return ds
