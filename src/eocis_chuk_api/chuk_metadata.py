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


class CHUKMetadata:
    expected_dataset_metadata_keys = {
        "title",
        "institution",
        "product_version",
        "Conventions",
        "summary",
        "license",
        "history",
        "references",
        "tracking_id",
        "Conventions",
        "product_version",
        "format_version",
        "summary",
        "keywords",
        "id",
        "naming_authority",
        "comment",
        "date_created",
        "creator_url",
        "creator_name",
        "creator_email",
        "project",
        "geospatial_lat_min",
        "geospatial_lat_max",
        "geospatial_lon_min",
        "geospatial_lon_max",
        "geospatial_vertical_min",
        "geospatial_vertical_max",
        "time_coverage_start",
        "time_coverage_end",
        "time_coverage_duration",
        "time_coverage_resolution",
        "platform",
        "sensor",
        "spatial_resolution",
        "geospatial_lat_units",
        "geospatial_lon_units",
        "geospatial_lat_resolution",
        "geospatial_lon_resolution",
        "key_variables"
    }

    @staticmethod
    def __decode4json(o):
        if isinstance(o, dict):
            for key in o:
                o[key] = CHUKMetadata.__decode4json(o[key])
            return o
        elif isinstance(o, list):
            for idx in range(len(o)):
                o[idx] = CHUKMetadata.__decode4json(o[idx])
            return o
        elif isinstance(o, np.float32):
            return float(o)
        elif isinstance(o, np.int32) or isinstance(o, np.int16) or isinstance(o, np.int8):
            return int(o)
        elif isinstance(o, np.ndarray):
            return CHUKMetadata.__decode4json(o.tolist())
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
        return CHUKMetadata.__decode4json(metadata)

    @staticmethod
    def check(ds):
        warnings = []
        errors = []
        for key in CHUKMetadata.expected_dataset_metadata_keys:
            if key not in ds.attrs:
                warnings.append(("missing_global_attribute", key))

        return warnings, errors
