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

import unittest
import os
import uuid

from eocis_chuk_api import CHUKDataSetUtils
from eocis_chuk_api_tests.test_utils.test_data_generator import TestDataGenerator
from eocis_chuk_api_tests.test_utils.test_utils import download_test_file


class TestTiffExport(unittest.TestCase):

    def test1(self):
        grid_path = download_test_file(TestDataGenerator.get_tmp_folder(), "EOCIS-CHUK-GRID-1000M-v1.0.nc")
        utils = CHUKDataSetUtils(grid_path)

        gen = TestDataGenerator(utils)
        # Whitendale Hanging Stones is the centroid of Great Britain
        # https://www.ordnancesurvey.co.uk/blog/where-is-the-centre-of-great-britain

        ds = utils.create_new_dataset(title="Distance to the GB Centroid",
                                      product_version="1.0",
                                      summary="The distance in km using the haversine formula to each CHUK grid location from the centroid of Great Britain",
                                      tracking_id=str(uuid.uuid4()))

        dists = gen.create_distances(54.0025, -2.5449)
        utils.add_variable(ds, variable_name="distances",
                           data=dists,
                           long_name="distance to Great British centroid",
                           units="km",
                           comment="calculated using the haversine formula")


        filename = utils.create_filename("CHUK", processing_level="L4", product_type="TEST", product_string="UNITTEST",
                                         datetime="2024", version="1.0", suffix=".tif")

        tmp_folder = TestDataGenerator.get_tmp_folder()
        utils.save_as_geotif(ds,"distances",os.path.join(tmp_folder,filename))


