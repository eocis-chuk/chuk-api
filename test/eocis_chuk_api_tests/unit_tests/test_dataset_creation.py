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

from eocis_chuk_api.chuk_dataset_utils import CHUKDataSetUtils
from eocis_chuk_api_tests.test_utils.test_data_generator import TestDataGenerator
folder = os.path.split(__file__)[0]
grid_path = os.path.join(folder,"..","..","..","EOCIS-CHUK-GRID-1000M-v0.4.nc")

class TestDatasetCreation(unittest.TestCase):

    def test1(self):
        utils = CHUKDataSetUtils(grid_path)
        gen = TestDataGenerator(utils)
        # Whitendale Hanging Stones is the centroid of Great Britain
        # https://www.ordnancesurvey.co.uk/blog/where-is-the-centre-of-great-britain
        ds = gen.create_distances(utils, 54.0025,-2.5449) # up to 1000km
        warnings, errors = utils.check(ds)
        self.assertEqual(0,len(warnings))
        self.assertEqual(0, len(errors))
        utils.save(ds,"EOCIS-CHUK-L4-TEST-MERGED-20231204-fv0.1.nc")