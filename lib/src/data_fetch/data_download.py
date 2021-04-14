import fnmatch
import os

from sentinelsat import SentinelAPI

from data_fetch.sentinel_utils import SentinelUtils
import pandas as pd

def make_filter(pattern):
    def node_filter(node_info, include_pattern=pattern):
        return (
            True
            if fnmatch.fnmatch(node_info["node_path"].lower(), include_pattern)
            else False
        )

    return node_filter

def query_and_download(tile, api, cols, output_folder):
    print(f'Download tile name: {tile["tile_name"]} for {tile["date"][0]}, {tile["date"][1]}')
    name = tile['tile_name']
    date = tile['date']
    products = api.query(date=date, tileid=name, platformname='Sentinel-2', producttype='S2MSI1C')

    downloaded_products = api.download_all(products, directory_path=output_folder, n_concurrent_dl=5)

    return pd.DataFrame([
        [v[col] for col in cols] for (_, v) in downloaded_products[0].items()
    ], columns=cols).set_index('id')


def download_tiles(list_of_tiles, output_folder, user, password, nfilter="*B??.jp2"):
    if nfilter:
        nodefilter = make_filter(nfilter)

    api = SentinelAPI(user, password, "https://scihub.copernicus.eu/dhus")

    if os.path.exists(output_folder):
        cols = ['id', 'title', 'date', 'footprint', 'url', 'path']
        results = []
        for tile in list_of_tiles:
            downloaded_products = query_and_download(tile, api, cols, output_folder)
            layers_df = SentinelUtils.process_products(downloaded_products, output_folder, delete_unused=True)
            tiles_df = pd.concat([downloaded_products, layers_df], axis=1)
            results.append(tiles_df)
            # SentinelUtils.extract_zip_files(downloaded_products, output_folder)
