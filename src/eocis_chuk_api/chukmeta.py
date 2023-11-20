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

import copy
import numpy as np

class CHUKMETA:

    @staticmethod
    def __decode4json(o):
        if isinstance(o,dict):
            for key in o:
                o[key] = CHUKMETA.__decode4json(o[key])
            return o
        elif isinstance(o,list):
            for idx in range(len(o)):
                o[idx] = CHUKMETA.__decode4json(o[idx])
            return o
        elif isinstance(o,np.float32):
            return float(o)
        elif isinstance(o,np.int32) or isinstance(o,np.int16) or isinstance(o,np.int8):
            return int(o)
        elif isinstance(o,np.ndarray):
            return CHUKMETA.__decode4json(o.tolist())
        else:
            return o

    @staticmethod
    def to_json(ds, for_variable):
        variable_metadata = {}
        da = ds[for_variable]
        variable_metadata[for_variable] = copy.deepcopy(da.attrs)
        metadata = {}
        metadata["__variable__"] = variable_metadata
        metadata["__dataset__"] = copy.deepcopy(ds.attrs)
        return CHUKMETA.__decode4json(metadata)

    @staticmethod
    def check(ds):
        pass # TODO check for missing or invalid CF/CHUK metadata


