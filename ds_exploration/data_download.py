import shutil
import rasterio
import fnmatch
import os
from pathlib import Path
from glob import glob
import numpy as np
import pandas as pd

from sentinelsat import SentinelAPI
from ds_exploration.plotting_utils import cut_and_save


def make_filter(pattern):
    def node_filter(node_info, include_pattern=pattern):
        return True if fnmatch.fnmatch(node_info["node_path"].lower(), include_pattern) else False
    return node_filter


def unarchive_download(file_path):
    unarchive_dir = file_path.parent
    zip_file_path = Path(f'{file_path}.zip')
    shutil.unpack_archive(zip_file_path, unarchive_dir)
    os.remove(zip_file_path)


def extract_and_combine(file_path):
    data_path = Path(f'{file_path}.SAFE')
    band_files = glob(str(data_path) + "/GRANULE/*/IMG_DATA/*.jp2")

    def get_band_array(band, band_files):
        band_file = [bf for bf in band_files if band in bf][0]
        return rasterio.open(band_file).read(1)

    red, green, blue = [get_band_array(band, band_files) for band in ['B04', 'B03', 'B02']]
    b12 = get_band_array('B12', band_files)
    return (np.dstack([red, green, blue]), b12)


def save_originals(file_path, output_folder, tile_title, keep, delete_unused):
    Path(file_path).mkdir(exist_ok=True)
    band_files = glob(str(Path(f'{file_path}.SAFE/GRANULE/*/IMG_DATA/*.jp2')))
    to_move = [file for file in band_files if any(file.endswith(f'{band}.jp2') for band in keep)]
    for file in to_move:
        Path(file).replace(Path(f'{output_folder}/{tile_title}/{Path(file).name}'))
    if delete_unused:
        shutil.rmtree(Path(f'{file_path}.SAFE'))


def query_and_download(tile, api, cols, output_folder):
    print(f'Download tile name: {tile["tile_name"]} for {tile["date"][0]}, {tile["date"][1]}')
    name = tile['tile_name']
    date = tile['date']
    products = api.query(date=date, tileid=name, platformname='Sentinel-2', producttype='S2MSI1C')

    downloaded_products = api.download_all(products, directory_path=output_folder, n_concurrent_dl=5)

    return pd.DataFrame([
        [v[col] for col in cols] for (_, v) in downloaded_products[0].items()
    ], columns=cols).set_index('id')


def extract_data_from_tile(tile, output_folder, delete_unused):
    file_path = Path(f'{output_folder}/{tile.title}')
    unarchive_download(file_path)
    rgb, b12 = extract_and_combine(file_path)
    cut_and_save(file_path, rgb, tile.title)
    save_originals(file_path, output_folder, tile.title, ['B04', 'B03', 'B02', 'B12'], delete_unused)
    return rgb, b12

def process_products(products, output_folder, delete_unused):
    print(f'Downloaded {len(products)} tiles, extracting and combining data')
    layers = []
    for tile in products.itertuples():
        layers.append(extract_data_from_tile(tile, output_folder, delete_unused))
    return pd.DataFrame.from_records(layers, columns=['rgb', 'b12'], index=products.index)


def download_tiles(list_of_tiles,
                   output_folder,
                   user,
                   password,
                   delete_unused=True,
                  ):

    Path(output_folder).mkdir(exist_ok=True)
    
    api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')
    
    cols = ['id', 'title', 'date', 'footprint', 'url', 'quicklook_url', 'path']
    results = []
    for tile in list_of_tiles:
        products = query_and_download(tile, api, cols, output_folder)
        layers_df = process_products(products, output_folder, delete_unused)
        tiles_df = pd.concat([products, layers_df], axis=1)
        results.append(tiles_df)

    return pd.concat(results)
