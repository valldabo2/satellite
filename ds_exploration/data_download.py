import shutil
import rasterio
import fnmatch
import os
from pathlib import Path
from glob import glob
import numpy as np
from ds_exploration.plotting_utils import plot_image

os.chdir('../sentinelsat/')
from sentinelsat import SentinelAPI
from sentinelsat import SentinelProductsAPI
os.chdir('../notebooks/')

def make_filter(pattern):
    def node_filter(node_info, include_pattern=pattern):
        return True if fnmatch.fnmatch(node_info["node_path"].lower(), include_pattern) else False
    return node_filter

def unarchive_download(file_path):
    unarchive_dir = file_path.parent
    shutil.unpack_archive(file_path, unarchive_dir)
    os.remove(file_path)

def extract_and_combine(zip_file_path):
    data_path = str(zip_file_path).replace(".zip", ".SAFE")
    band_files = glob(data_path + "/GRANULE/*/IMG_DATA/*.jp2")

    def get_band_array(band, band_files):
        band_file = [bf for bf in band_files if band in bf][0]
        array = rasterio.open(band_file).read(1)
        return array

    red = get_band_array("B04", band_files)
    green = get_band_array("B03", band_files)
    blue = get_band_array("B02", band_files)
    return np.dstack([red, green, blue])

def download_tiles(list_of_tiles,
                   output_folder,
                   user,
                   password,
                   nfilter='*B??.jp2'
                  ):
    if nfilter:
        nodefilter=make_filter(nfilter)
        api = SentinelProductsAPI(user, password, 'https://scihub.copernicus.eu/dhus')
    else:
        api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')
    
    try:
        os.mkdir(output_folder)
    except:
        pass
    
    for tile in list_of_tiles:
        print(f'Download tile name: {tile["tile_name"]} for {tile["date"][0]}, {tile["date"][1]}, with filter {nfilter}')
        name = tile['tile_name']
        date = tile['date']
        products = api.query(
            date=date, tileid=name,
            platformname='Sentinel-2', producttype='S2MSI1C'
        )
        if nfilter:
            downloaded_products = api.download_all(products, directory_path=output_folder, n_concurrent_dl=5, nodefilter=nodefilter)
        else:
            downloaded_products = api.download_all(products, directory_path=output_folder, n_concurrent_dl=5)
        
        print(downloaded_products)
        filename = [downloaded_products[0][k]['title'] for k in downloaded_products[0].keys()][0]
        zip_file_path = Path(f"{output_folder}/{filename}.zip")
        unarchive_download(zip_file_path)
        
        rgb = extract_and_combine(zip_file_path)
        print(rgb.shape)
        plot_image(rgb, factor=5/2e4, clip_range=(0,1))
