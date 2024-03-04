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

import abc

import xarray as xr
import numpy as np
import fnmatch


class Mask(abc.ABC):

    def __init__(self):
        """
        Abstract Base Class for masks, do not instantiate directly
        """
        pass

    def or_mask(self, *others:list["Mask"]) -> "Mask":
        """
        OR this mask with other masks

        Args:
            others: a list of masks to be OR'd with this mask
        Returns:
            a combined mask
        """
        return CHUKAuxilaryDataCombinedMask(self, *others, operator="or")

    def and_mask(self, *others:list["Mask"]) -> "Mask":
        """
        AND this mask with other masks

        Args:
            others: a list of masks to be AND'd with this mask
        Returns:
            a combined mask
        """
        return CHUKAuxilaryDataCombinedMask(self, *others, operator="and")


    def not_mask(self) -> "Mask":
        """
        Invert this mask

        Returns:
             a new mask that is the negation of this mask
        """
        return CHUKAuxilaryDataCombinedMask(self, operator="not")

    def count(self) -> int:
        """
        Count the number of True values in this mask

        Returns:
            the total number of True values
        """
        return int(self.to_array().sum())

    def fraction(self) -> float:
        """
        Calculate the fraction of values that are True in this mask

        Returns:
            the fraction of values that are True
        """
        m = self.to_array()
        count = 1
        for d in m.shape:
            count *= d
        return int(m.sum()) / count

    @abc.abstractmethod
    def to_array(self) -> xr.DataArray:
        """
        Convert this mask to an xarray.DataArray and return it

        Returns:
             an xarray.DataArray containing the mask values
        """
        pass # implemented in sub-classes


class CHUKAuxilaryDataMask(Mask):

    def __init__(self, dataset_name:str, variable_name:str, include_missing:bool=False):
        """
        Construct a mask associated with a particular dataset

        Args:
            dataset_name: the name of the dataset
            variable_name: the name of the variable in the dataset to use to construct the mask
            include_missing: whether to also include missing data values (eg NaN) in the mask
        """
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
        self.include_missing = include_missing

    def get_all_mask_values(self) -> list[str]:
        """
        Get a list of all the values that could be included in this mask

        Returns:
             a list of values
        """
        return list(self.value_lookup.keys())

    def get_selected_mask_values(self) -> list[str]:
        """
        Get a list of all the values that are included in this mask

        Returns:
             a list of values included in this mask
        """
        keys = []
        for mask_value in self.mask_values:
            keys += self.__get_matching_keys(mask_value)
        return keys

    def add_mask_value(self, mask_value: str):
        """
        Add a value to the mask

        Args:
            mask_value: the category value to include in the mask
        Throws:
            ValueError if the specified value is not a valid value for this mask
        """
        matching_keys = self.__get_matching_keys(mask_value)
        if len(matching_keys) == 0:
            raise ValueError(f"Value {mask_value} does not match any values {','.join(self.value_lookup.keys())}")
        self.cached_result = None
        self.mask_values.append(mask_value)
        return matching_keys

    def to_array(self) -> xr.DataArray:
        """
        Obtain the evaluated mask values
        Returns:
            an xarray DataArray object
        """
        if self.cached_result is None:
            filter_keys = []
            for mask_value in self.mask_values:
                filter_keys += self.__get_matching_keys(mask_value)
            filter_values = [self.value_lookup[key] for key in filter_keys]
            self.cached_result = xr.where(self.da.isin(filter_values), True, False)
            if self.include_missing:
                self.cached_result = xr.where(np.isnan(self.da),True,self.cached_result)
        return self.cached_result

    def __get_matching_keys(self, value_or_pattern):
        if value_or_pattern in self.value_lookup:
            return [value_or_pattern]
        matches = []
        for key in self.value_lookup:
            if fnmatch.fnmatch(key, value_or_pattern):
                matches.append(key)
        return matches


class CHUKAuxilaryDataCombinedMask(Mask):

    def __init__(self, *masks:list[Mask], operator:str="or"):
        """
        Create a mask derived from one or more other masks

        Args:
            masks: a list of one or more masks to be combined
            operator: the operator to use, should be "not", "or" or "and"

        Throws:
            ValueError for example if the list of masks is empty or operator is not one of "not","and","or"
        """
        if len(masks) == 0:
            raise ValueError("masks must be a non-empty list")
        if operator not in ("and","or","not"):
            raise ValueError('operator must be one of "and", "or" or "not"')
        if operator == "not" and len(masks) > 1:
            raise ValueError("only one mask can be supplied for the not operator")
        self.input_masks = masks
        self.operator = operator

    def to_array(self):

        if self.operator == "not":
            m = self.input_masks[0].to_array()
            return xr.where(m,False,True)

        stacked = xr.concat([m.to_array() for m in self.input_masks], "layer")

        if self.operator == "or":
            return stacked.any(dim="layer")
        elif self.operator == "and":
            return stacked.all(dim="layer")


class CHUKAuxilaryUtils:

    @staticmethod
    def create_mask(dataset_path:str, variable:str, mask_values:[str,list[str]], include_missing:bool=False) -> CHUKAuxilaryDataMask:
        """
        Create a mask

        Args:
            dataset_path: path to the netcdf file containing the auxilary data to use
            variable: the variable in the file to use in the mask
            mask_values: a string or list of strings
            include_missing: whether to include missing data values in the mask or not

        Returns:
            A mask object containing of True or False values for every cell
        """
        mask = CHUKAuxilaryDataMask(dataset_path, variable)
        if isinstance(mask_values, str):
            mask_values = [mask_values]
        for mask_value in mask_values:
            mask.add_mask_value(mask_value)
        return mask

    """
    Construct the logical AND of a list of masks
    
    Args:
        masks: the masks to combine
        
    Returns:
        Resulting mask
    """
    @staticmethod
    def combine_masks_and(*masks:list[Mask]):
        return masks[0].and_mask(*masks[1:])

    """
    Construct the logical OR of a list of masks

    Args:
        masks: the masks to combine

    Returns:
        Resulting mask
    """
    @staticmethod
    def combine_masks_or(*masks:list[Mask]):
        return masks[0].or_mask(*masks[1:])

    """
    Construct the logical NOT of a mask

    Args:
        masks: the masks to combine

    Returns:
        Resulting mask
    """
    @staticmethod
    def not_mask(mask:Mask):
        return mask.not_mask()
