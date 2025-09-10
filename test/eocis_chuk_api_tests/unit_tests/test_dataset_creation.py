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
import uuid
import os
import numpy as np
import xarray as xr

from eocis_chuk_api import CHUKDataSetUtils
from eocis_chuk_api_tests.test_utils.test_data_generator import TestDataGenerator
from eocis_chuk_api_tests.test_utils.test_utils import download_test_file

class TestDatasetCreation(unittest.TestCase):

    def test1(self):
        grid_path = download_test_file(TestDataGenerator.get_tmp_folder(), "EOCIS-CHUK-GRID-1000M-v1.0.nc")
        utils = CHUKDataSetUtils(grid_path)

        gen = TestDataGenerator(utils)
        # Whitendale Hanging Stones is the centroid of Great Britain
        # https://www.ordnancesurvey.co.uk/blog/where-is-the-centre-of-great-britain

        ds = utils.create_new_dataset(title="Distance to the GB Centroid",
                                      product_version="1.0",
                                      summary="The distance in km using the haversine formula to each CHUK grid location from the centroid of Great Britain",
                                      tracking_id=str(uuid.uuid4()),
                                      spatial_resolution="1km",
                                      format_version="EOCIS Data Standards v0.4",
                                      key_variables="distance",
                                      creator_email="EOCIS@reading.ac.uk",
                                      creator_name="EOCIS",
                                      creator_url="https://eocis.org",
                                      sensor="N/A",
                                      platform="N/A",
                                      history="Developed for eocis_chuk_api unit tests",
                                      time_coverage_start="20220630T000000Z",
                                      time_coverage_end="20220630T235959Z",
                                      time_coverage_duration="P1Y",
                                      time_coverage_resolution="P1Y",
                                      comment="For testing purposes only",
                                      references="there are no references",
                                      date_created="20220630T235959Z",
                                      keywords="test",
                                      id="TEST_DISTANCES",
                                      naming_authority="EOCIS")

        dists = gen.create_distances(54.0025, -2.5449)
        utils.add_variable(ds, variable_name="distances",
                           data=dists,
                           long_name="distance to Great British centroid",
                           units="km",
                           comment="calculated using the haversine formula")

        warnings, errors = utils.check(ds)
        self.assertEqual(0, len(warnings))
        self.assertEqual(0, len(errors))
        filename = utils.create_filename("CHUK",processing_level="L4",product_type="TEST", product_string="UNITTEST", datetime="2024", version="1.0")
        tmp_folder = TestDataGenerator.get_tmp_folder()
        utils.save(ds,os.path.join(tmp_folder,filename))

    def test_doc_example(self):
        grid_path = download_test_file(TestDataGenerator.get_tmp_folder(), "EOCIS-CHUK-GRID-100M-v1.0.nc")
        utils = CHUKDataSetUtils(grid_path)  # downloaded as described above
        chuk_ds = utils.create_new_dataset(
            title="My CHUK dataset",
            institution="EOCIS CHUK",
            Conventions="CF-1.10",
            tracking_id="12345678",
            product_version="1.0",
            summary="Shows estimates of the squirrel population in each CHUK grid cell",
            license="Creative Commons Licence by attribution (https://creativecommons.org/licenses/by/4.0/)",
            history="Developed from the squirrel population dataset",
            comment="This is a made up example",
            creator_url="https:///www.example.com",
            creator_name="Institute of Biological Studies")
        # create an array to hold the data
        population_data = np.zeros(utils.get_grid_shape())
        # populate the data

        # attach the data
        chuk_ds["squirrel_population"] = xr.DataArray(population_data, dims=("y", "x"), attrs={
            "long_name": "estimated_squirrel_population",
            "coordinates": "lat lon",
            "grid_mapping": "crsOSGB"
        })

        # save the dataset
        utils.save(chuk_ds, "EOCIS-CHUK-L4-SQUIRRELPOP-MERGED-20231204-v0.1.nc")