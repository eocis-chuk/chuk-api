from eocis_chuk_api.chuk_dataset_utils import CHUKDataSetUtils

if __name__ == '__main__':
    cds = CHUKDataSetUtils("../../EOCIS-CHUK-GRID-1000M-v0.4.nc")
    ds = cds.load("../../EOCIS-CHUK-GRID-1000M-v0.4.nc")
    cds.save_as_geotif(ds, "lon", "../../1000m.tif")

