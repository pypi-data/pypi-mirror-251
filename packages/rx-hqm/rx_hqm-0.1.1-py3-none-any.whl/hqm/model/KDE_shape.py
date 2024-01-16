from hqm.tools.utility import get_project_root
from hqm.tools.utility import read_root
from hqm.tools.utility import cache_json
from hqm.tools.selection import selection
import zfit
import awkward as ak
import numpy as np


def get_KDE_shape(obs, kind, q2, bandwidth=10, year="2018", trigger="ETOS", pdf_name=""):
    json_file = f"KDE_{year}_{trigger}_{q2}_{kind}.json"

    @cache_json(json_file)
    def _get_data_array():
        if kind == "jpsi":
            kind_dir = "ctrl"
        else:
            kind_dir = kind
        data_path = get_project_root() + f"root_sample/v6/{kind_dir}/v10.21p2/{year}_{trigger}/{q2}_nomass.root"
        data_array = read_root(data_path, trigger)
        if trigger in ["ETOS", "MTOS"]:
            bdt_cmb = selection["ee"]["bdt_cmb"][trigger]
            bdt_prc = selection["ee"]["bdt_prc"][trigger]
        elif trigger in ["GTIS"]:
            bdt_cmb = selection["mm"]["bdt_cmb"][trigger]
            bdt_prc = selection["ee"]["bdt_prc"][trigger]
        else:
            raise

        bdt = bdt_cmb & bdt_prc
        data_array = bdt.apply(data_array)
        data_list = ak.to_numpy(data_array.B_M).tolist()
        return data_list

    data_list = _get_data_array()
    data_np = np.array(data_list)

    zdata = zfit.Data.from_numpy(obs, array=data_np)
    if bandwidth is None:
        shape = zfit.pdf.KDE1DimFFT(obs=obs, data=zdata, name=f"{pdf_name}_{year}_{trigger}")
    else:
        shape = zfit.pdf.KDE1DimFFT(obs=obs, data=zdata, name=f"{pdf_name}_{year}_{trigger}", bandwidth=bandwidth)

    return shape
