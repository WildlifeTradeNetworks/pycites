# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.5.0
#   kernelspec:
#     display_name: 'Python 3.8.3 64-bit (''pycites'': conda)'
#     language: python
#     name: python38364bitpycitesconda301c197b92604ee8a3a0bec38518af4f
# ---

# %%
from glob import glob
import hashlib
from pathlib import Path
import zipfile

from appdirs import user_cache_dir, user_data_dir
import pandas as pd
import requests
from tqdm import tqdm

# currently unused:
# import janitor
# import pyarrow
# from pyarrow import csv
# import pyarrow.feather as feather
# import pyarrow.parquet as pq

# %%
def get_zip_filename():
    with requests.head(cites_url) as r:
        zip_file = (
            r.headers.get("Content-Disposition", default_filename)
            .split("filename=")[-1]
            .strip('"')
        )  # has weird header, which contains filename
    return zip_file


# %%
def checksum(filename, hash_factory=hashlib.md5, chunk_num_blocks=128):
    """ https://stackoverflow.com/a/4213255 """
    h = hash_factory()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_num_blocks * h.block_size), b""):
            h.update(chunk)
    return h.hexdigest()


# %%
def download_cites_trade_zip(zip_file):
    """
    https://stackoverflow.com/a/39217788
    https://stackoverflow.com/a/37573701
    """
    cachedir = zip_file.parent
    cachedir.mkdir(parents=True, exist_ok=True)
    print(
        f"Downloading CITES Trade database zip file from {cites_url} to {zip_file} ..."
    )
    with requests.get(cites_url, stream=True) as r:
        local_filename = cachedir / zip_file
        content_length = int(r.headers.get("content-length", 0))
        total_size = content_length if content_length > 0 else None
        block_size = 1024
        with tqdm(total=total_size, unit="B", unit_scale=True, unit_divisor=1024) as t:
            with open(local_filename, "wb") as f:
                for data in r.iter_content(block_size):
                    t.update(len(data))
                    f.write(data)
    #                     shutil.copyfileobj(r.raw, f)
    #                     t.update()


# %%
def extract_files(zip_file, cleanup=False):
    dest = zip_file.parent  # TODO: make a subdir to contain this?
    print(f"Extracting CITES Trade database zip file {zip_file} to {dest} ...")
    # dest.mkdir(parents=True, exist_ok=True)  # no longer necessary because already exists
    with zipfile.ZipFile(zip_file, "r") as zip_file:
        for file in tqdm(
            iterable=zip_file.namelist(), total=len(zip_file.namelist()), unit="files"
        ):
            zip_file.extract(member=file, path=dest)
    if cleanup:
        zip_file.unlink()


# %%
def combine_csv(csv_dir, cleanup=False):
    datasets = []
    files = list(csv_dir.glob("*.csv"))
    print(f"Reading in CITES Trade database CSV files from {csv_dir} ...")
    for f in tqdm(iterable=files, total=len(files), unit="files"):
        d = pd.read_csv(f, low_memory=False)
        # make sure Year and Quantiy values are numeric (int and float, respectively)
        # drop rows that are missing Year
        # ensure Year is between 1970 and 2020
        d = d[pd.to_numeric(d["Year"], errors="coerce").notnull()]
        d = d.dropna(subset=["Year"])
        d["Year"] = d["Year"].astype(int)
        d["Quantity"] = pd.to_numeric(d["Quantity"], errors="coerce")
        d["Quantity"] = d["Quantity"].astype(float)
        d = d[d["Year"] > 1970]
        d = d[d["Year"] < 2020]
        datasets.append(d)
    print("Combining CSV files into a single DataFrame...")
    df = pd.concat(datasets)
    print("Sorting and re-indexing DataFrame...")
    df = df.sort_values(
        by=[
            "Year",
            "Taxon",
            "Order",
            "Family",
            "Genus",
            "Term",
            "Importer",
            "Exporter",
            "Appendix",
        ]
    )
    df = df.reset_index(drop=True)
    if cleanup:
        for f in files:
            f.unlink()
    return df


# %%
# default locations
cites_url = "https://trade.cites.org/cites_trade/download_db"
default_filename = "trade_database.zip"

cachedir = Path(user_cache_dir("pycites", "ltirrell"))
datadir = Path(user_data_dir("pycites", "ltirrell"))
zip_file = cachedir / get_zip_filename()
csv_file = datadir / zip_file.name.replace("zip", "csv.gz")

# checksums for v2019.2
# known_zip_md5 = "3d774b109c3ebf3594cf0fd4c20c1d1b"
# known_csv_md5 = "920614bc5a9219849b1626a653d5ea64"
# checksums for v2020.1, latest
known_zip_md5 = "d64d99182bdfb3696f6ce91687ccdd81"
known_csv_md5 = "417b1cc7be04a7328e654fc74098d205"

# column dtypes (not currently used)
column_types = {
    "Year": "int",
    "Appendix": "string",
    "Taxon": "string",
    "Class": "string",
    "Order": "string",
    "Family": "string",
    "Genus": "string",
    "Term": "string",
    "Quantity": "float",
    "Unit": "string",
    "Importer": "string",
    "Exporter": "string",
    "Origin": "string",
    "Purpose": "string",
    "Source": "string",
    "Reporter.type": "string",
    "Import.permit.RandomID": "string",
    "Export.permit.RandomID": "string",
    "Origin.permit.RandomID": "string",
}


# %%
def get_data(zip_file=zip_file, csv_file=csv_file, force_update=True, cleanup=False):
    # TODO: cleanup
    if not zip_file.exists() or force_update:
        download_cites_trade_zip(zip_file)
    zip_md5 = checksum(zip_file)
    if zip_md5 != known_zip_md5:
        raise ValueError(
            f"md5 sum of zip file ({zip_md5}) does not match known value: {known_zip_md5}"
        )
    extract_files(zip_file, cleanup=cleanup)
    df = combine_csv(zip_file.parent, cleanup)
    print(f"Saving combined CITES Trade database CSV files to {csv_file} ...")
    df.to_csv(csv_file, index=False)
    return csv_file


# %%
def load_data(csv_file=csv_file, update=False, update_kwargs=None):
    if update:
        if update_kwargs is not None:
            get_data(**update_kwargs)
        else:
            get_data()

    if not csv_file.exists():
        raise FileNotFoundError(f"The file {csv_file} does not exist! Run `pycites.get_data() to download")

    csv_md5 = checksum(csv_file)
    if csv_md5 != known_csv_md5:
        raise ValueError(
            f"md5 sum of zip file ({csv_md5}) does not match known value: {known_csv_md5}"
        )

    df = pd.read_csv(csv_file)
    return df


# %%
