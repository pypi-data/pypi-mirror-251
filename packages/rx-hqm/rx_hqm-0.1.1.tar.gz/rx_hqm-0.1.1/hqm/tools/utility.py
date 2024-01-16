import os
import json
import uproot
import pickle
import zfit
from importlib.resources import files
from logzero import logger as log


def get_lumi(year):
    lumi = {
        "2011": 1.0,
        "2012": 2.0,
        "2015": 0.3,
        "2016": 1.6,
        "2017": 1.7,
        "2018": 2.1,
    }
    return lumi[year]


def get_shape(dataset, trigger, func, *, parameter_name_prefix="", pdf_name=""):
    if dataset in ["2017", "2018"]:
        return_value = func(
            year=dataset, trigger=trigger, parameter_name_prefix=parameter_name_prefix, pdf_name=pdf_name
        )
    else:
        if dataset == "r1":
            years = ["2011", "2012"]
        elif dataset == "r2p1":
            years = ["2015", "2016"]
        else:
            log.error(f'Invalid dataset: {dataset}')
            raise

        values = [
            func(year=year, trigger=trigger, parameter_name_prefix=parameter_name_prefix, pdf_name=pdf_name)
            for year in years
        ]
        lumis = [get_lumi(year) for year in years]
        frac = lumis[0] / sum(lumis)

        if isinstance(values[0], tuple):
            pdfs = [value[0] for value in values]
            constraints = values[0][1]
            constraints.update(values[1][1])
            pdf = zfit.pdf.SumPDF(pdfs, fracs=[frac], name=f"{pdf_name}_{dataset}_{trigger}")
            return_value = (pdf, constraints)
        else:
            pdfs = values
            pdf = zfit.pdf.SumPDF(pdfs, fracs=[frac], name=f"{pdf_name}_{dataset}_{trigger}")
            return_value = pdf

    return return_value


def get_project_root() -> str:
    file_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = file_dir.removesuffix("hqm/tools")
    return project_root


def dump_json(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=4)


def load_json(path):
    with open(path, "r") as f:
        obj = json.load(f)
    return obj


def dump_pickle(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(obj, f)


def load_pickle(path):
    with open(path, "rb") as f:
        obj = pickle.load(f)
    return obj


def read_root(path, tree_name):
    # read root file and return awkward array
    if not os.path.isfile(path):
        raise FileNotFoundError(f"{path} is not found.")

    with uproot.open(path) as f:
        events = f[tree_name]
        data_array = events.arrays()
    return data_array


def cache_json(json_file_name):
    json_path = files("hqm_data").joinpath(json_file_name)

    def decorator(func):
        def inner():
            if os.path.isfile(json_path):
                return load_json(json_path)
            else:
                obj = func()
                dump_json(obj, json_path)
                return obj

        return inner

    return decorator
