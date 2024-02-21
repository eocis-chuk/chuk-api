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
import fnmatch


class BaseMask:

    def or_mask(self, *others):
        return CHUKAuxilaryDataCombinedMask(self, *others, operator="or")

    def and_mask(self, *others):
        return CHUKAuxilaryDataCombinedMask(self, *others, operator="and")

    def not_mask(self):
        return CHUKAuxilaryDataCombinedMask(self, operator="not")

    def count(self):
        return int(self.to_array().sum())

    def fraction(self):
        m = self.to_array()
        count = 1
        for d in m.shape:
            count *= d
        return int(m.sum()) / count


class CHUKAuxilaryDataMask(BaseMask):

    def __init__(self, dataset_name, variable_name):
        self.dataset_name = dataset_name
        self.variable_name = variable_name
        self.da = xr.open_dataset(dataset_name)[variable_name]
        meanings = self.da.attrs["flag_meanings"].split(" ")
        values = self.da.attrs["flag_values"]
        self.value_lookup = {}
        for (meaning, value) in zip(meanings, values):
            self.value_lookup[meaning] = value
        self.mask_values = []
        self.cached_result = None

    def get_all_mask_values(self) -> list[str]:
        """
        Get a list of all the values in this mask

        Returns:
             a list of values in this mask
        """
        return list(self.value_lookup.keys())

    def get_selected_mask_values(self):
        keys = []
        for mask_value in self.mask_values:
            keys += self.__get_matching_keys(mask_value)
        return keys

    def add_mask_value(self, mask_value):
        matching_keys = self.__get_matching_keys(mask_value)
        if len(matching_keys) == 0:
            raise ValueError(f"Value {mask_value} does not match any values {','.join(self.value_lookup.keys())}")
        self.cached_result = None
        self.mask_values.append(mask_value)
        return matching_keys

    def to_array(self):
        if self.cached_result is None:
            filter_keys = []
            for mask_value in self.mask_values:
                filter_keys += self.__get_matching_keys(mask_value)
            filter_values = [self.value_lookup[key] for key in filter_keys]
            self.cached_result = xr.where(self.da.isin(filter_values), 1, 0)
        return self.cached_result

    def __get_matching_keys(self, value_or_pattern):
        if value_or_pattern in self.value_lookup:
            return [value_or_pattern]
        matches = []
        for key in self.value_lookup:
            if fnmatch.fnmatch(key, value_or_pattern):
                matches.append(key)
        return matches


class CHUKAuxilaryDataCombinedMask(BaseMask):

    def __init__(self, *masks, operator="or"):
        self.input_masks = masks
        self.operator = operator

    def to_array(self):
        if self.operator == "not":
            m = self.input_masks[0]()
            return xr.where(m == 1, 0, 1)
        stacked = xr.concat([m() for m in self.input_masks], "layer")
        if self.operator == "or":
            return stacked.max("layer")
        elif self.operator == "and":
            return stacked.min("layer")


class CHUKAuxilaryUtils:

    @staticmethod
    def create_mask(dataset_path:str, variable:str, mask_values:[str,list[str]]) -> CHUKAuxilaryDataMask:
        """
        Create a mask

        Args:
            dataset_path: path to the netcdf file containing the auxilary data to use
            variable: the variable in the file to use in the mask
            mask_values: a string or list of strings

        Returns:
            A mask
        """
        mask = CHUKAuxilaryDataMask(dataset_path, variable)
        if isinstance(mask_values, str):
            mask_values = [mask_values]
        for mask_value in mask_values:
            mask.add_mask_value(mask_value)
        return mask

    @staticmethod
    def combine_masks_and(masks):
        return masks[0].and_mask(*masks[1:])

    @staticmethod
    def combine_masks_or(masks):
        return masks[0].or_mask(*masks[1:])

    @staticmethod
    def not_mask(mask):
        return mask.not_mask()
