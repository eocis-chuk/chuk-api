import copy
import json
import xarray as xr
import numpy as np

class CHUKMETA:

    @staticmethod
    def decode4json(o):
        if isinstance(o,dict):
            for key in o:
                o[key] = CHUKMETA.decode4json(o[key])
            return o
        elif isinstance(o,list):
            for idx in range(len(o)):
                o[idx] = CHUKMETA.decode4json(o[idx])
            return o
        elif isinstance(o,np.float32):
            return float(o)
        elif isinstance(o,np.int32) or isinstance(o,np.int16) or isinstance(o,np.int8):
            return int(o)
        elif isinstance(o,np.ndarray):
            return CHUKMETA.decode4json(o.tolist())
        else:
            return o

    @staticmethod
    def to_json(ds):
        variable_metadata = {}
        for v in ds.variables:
            da = ds[v]
            variable_metadata[v] = copy.deepcopy(da.attrs)
        metadata = {}
        metadata["__variables__"] = variable_metadata
        metadata["__dataset__"] = copy.deepcopy(ds.attrs)
        return CHUKMETA.decode4json(metadata)

    @staticmethod
    def check(self, ds):
        pass # TODO check for missing or invalid CF/CHUK metadata


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-path", help="path to netcdf4 file from which metadata is to be extracted",
                        default="/home/dev/data/regrid/sst/2022/02/02/20220202120000-C3S-L4_GHRSST-SSTdepth-OSTIA-GLOB_ICDR3.0-v02.0-fv01.0.nc")
    parser.add_argument("--to-path", help="path to json file to which metadata is to be written", default="output.json")
    args = parser.parse_args()
    ds = xr.open_dataset(args.from_path)
    o = CHUKMETA.to_json(ds)
    with open(args.to_path,"w") as f:
        f.write(json.dumps(o))

