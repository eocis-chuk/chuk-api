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

from eocis_chuk_api import CHUKAuxilaryUtils, CHUKDataSetUtils
from eocis_chuk_api_tests.test_utils.test_data_generator import TestDataGenerator
from eocis_chuk_api_tests.test_utils.test_utils import download_test_file
from eocis_chuk_api.chuk_auxilary_utils import Mask

class TestAuxSupport(unittest.TestCase):

    def test_usage(self):
        grid_path = download_test_file(TestDataGenerator.get_tmp_folder(),"EOCIS-CHUK-GRID-1000M-v1.0.nc")

        utils = CHUKDataSetUtils(grid_path)

        maxst_local_path = download_test_file(TestDataGenerator.get_tmp_folder(),"EOCIS-CHUK-L4-LST-LANDSAT_MAXST-1KM-2022-fv0.1.nc")
        landcover_local_path = download_test_file(TestDataGenerator.get_tmp_folder(),"EOCIS-AUXILARY-L4-LANDCOVER-MERGED-2023-1KM-fv1.0.nc")

        max_ds = utils.load(maxst_local_path)

        landcover_woodland_mask = CHUKAuxilaryUtils.create_mask(landcover_local_path,"land_cover",mask_values="*woodland")

        landcover_freshwater_mask = CHUKAuxilaryUtils.create_mask(landcover_local_path, "land_cover",
                                                                mask_values="Freshwater")

        self.assertEqual(['No_data', 'Deciduous_woodland', 'Coniferous_woodland', 'Arable', 'Improved_grassland', 'Neutral_grassland', 'Calcareous_grassland', 'Acid_grassland', 'Fen', 'Heather', 'Heather_grassland', 'Bog', 'Inland_rock', 'Saltwater', 'Freshwater', 'Supralittoral_rock', 'Supralittoral_sediment', 'Littoral_rock', 'Littoral_sediment', 'Saltmarsh', 'Urban', 'Suburban'],
                         landcover_woodland_mask.get_all_mask_values())
        self.assertEqual(['Deciduous_woodland', 'Coniferous_woodland'],landcover_woodland_mask.get_selected_mask_values())

        landcover_urban_mask = CHUKAuxilaryUtils.create_mask(landcover_local_path, "land_cover",mask_values=["Urban","Suburban"])

        landcover_woodland_area_sq_km = landcover_woodland_mask.count()
        landcover_built_area_sq_km = landcover_urban_mask.count()
        landcover_freshwater_area_sq_km = landcover_freshwater_mask.count()

        self.assertEqual(30905,landcover_woodland_area_sq_km)
        self.assertEqual(19435,landcover_built_area_sq_km)
        self.assertEqual(3160,landcover_freshwater_area_sq_km)

        ds = utils.create_new_dataset(title="My Mask",
                                      product_version="1.0",
                                      summary="A mask",
                                      tracking_id=str(uuid.uuid4()))

        urban_mask_path = os.path.join(TestDataGenerator.get_tmp_folder(),"urban_mask.nc")
        utils.add_variable(ds, data=landcover_urban_mask.to_array().data, variable_name="urban_or_suburban")
        utils.save(ds,urban_mask_path)

        mean_woodland_max_temps = float(max_ds["ST"].where(landcover_woodland_mask.to_array(),np.nan).mean(skipna=True))
        mean_urban_max_temps = float(max_ds["ST"].where(landcover_urban_mask.to_array(), np.nan).mean(skipna=True))
        mean_freshwater_max_temps = float(max_ds["ST"].where(landcover_freshwater_mask.to_array(), np.nan).mean(skipna=True))

        self.assertEqual(302, int(mean_woodland_max_temps))
        self.assertEqual(312,int(mean_urban_max_temps))
        self.assertEqual(298,int(mean_freshwater_max_temps))

    def test_mask_combinations(self):

        class MockMask(Mask):

            def __init__(self, data_array):
                self.data_array = data_array

            def to_array(self):
                return self.data_array

        mm1 = MockMask(xr.DataArray(np.array([[True,True],[False,False]]), dims=("y","x")))
        mm2 = MockMask(xr.DataArray(np.array([[True,False],[True,False]]), dims=("y", "x")))

        and_mask = CHUKAuxilaryUtils.combine_masks_and(mm1,mm2)
        print(and_mask.to_array())
        self.assertTrue(np.array_equal(and_mask.to_array().data,np.array([[True,False],[False,False]])))

        or_mask = CHUKAuxilaryUtils.combine_masks_or(mm1, mm2)
        print(or_mask.to_array())
        self.assertTrue(np.array_equal(or_mask.to_array().data,
                                       np.array([[True,True], [True,False]])))

        not_mask = CHUKAuxilaryUtils.not_mask(mm1)
        print(not_mask.to_array())
        self.assertTrue(np.array_equal(not_mask.to_array().data,np.array([[False,False],[True,True]])))
