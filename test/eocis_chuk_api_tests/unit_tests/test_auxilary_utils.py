
import unittest

import unittest
import os
import uuid
import numpy as np

from eocis_chuk_api import CHUKAuxilaryUtils, CHUKDataSetUtils
from eocis_chuk_api_tests.test_utils.test_data_generator import TestDataGenerator
from eocis_chuk_api_tests.test_utils.test_utils import download_test_file


class TestTiffExport(unittest.TestCase):

    def test1(self):
        grid_path = download_test_file(TestDataGenerator.get_tmp_folder(),"EOCIS-CHUK-GRID-1000M-TEST-v0.4.nc")
        utils = CHUKDataSetUtils(grid_path)

        maxst_local_path = download_test_file(TestDataGenerator.get_tmp_folder(),"EOCIS-CHUK-L4-LST-LANDSAT_MAXST-1KM-2022-fv0.1.nc")
        landcover_local_path = download_test_file(TestDataGenerator.get_tmp_folder(),"EOCIS-AUXILARY-L4-LANDCOVER-MERGED-2023-1KM-fv1.0.nc")

        max_ds = utils.load(maxst_local_path)

        landcover_woodland_mask = CHUKAuxilaryUtils.create_mask(landcover_local_path,"land_cover",mask_values="*woodland")

        landcover_freshwater_mask = CHUKAuxilaryUtils.create_mask(landcover_local_path, "land_cover",
                                                                mask_values="Freshwater")
        print(landcover_woodland_mask.get_all_mask_values())
        print(landcover_woodland_mask.get_selected_mask_values())
        landcover_urban_mask = CHUKAuxilaryUtils.create_mask(landcover_local_path, "land_cover",mask_values=["Urban","Suburban"])

        landcover_woodland_area_sq_km = landcover_woodland_mask.count()
        landcover_built_area_sq_km = landcover_urban_mask.count()
        landcover_freshwater_area_sq_km = landcover_freshwater_mask.count()

        print(f"Woodland sq km={landcover_woodland_area_sq_km}")
        print(f"Built sq km={landcover_built_area_sq_km}")
        print(f"Freshwater sq km={landcover_freshwater_area_sq_km}")

        ds = utils.create_new_dataset(title="My Mask",
                                      product_version="1.0",
                                      summary="A mask",
                                      tracking_id=str(uuid.uuid4()))

        utils.add_variable(ds, data=landcover_urban_mask.to_array().data, variable_name="urban_or_suburban")
        utils.save(ds,"urban_mask.nc")

        mean_woodland_max_temps = float(max_ds["ST"].where(landcover_woodland_mask.to_array(),np.nan).mean(skipna=True))
        mean_urban_max_temps = float(max_ds["ST"].where(landcover_urban_mask.to_array(), np.nan).mean(skipna=True))
        mean_freshwater_max_temps = float(max_ds["ST"].where(landcover_freshwater_mask.to_array(), np.nan).mean(skipna=True))

        print(f"Woodland mean max temp={mean_woodland_max_temps}")
        print(f"Built mean max temp={mean_urban_max_temps}")
        print(f"Freshwater mean max temp={mean_freshwater_max_temps}")


