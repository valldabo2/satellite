import fnmatch
import os
from pathlib import Path

from sentinelsat import SentinelAPI

from data_fetch.sentinel_utils import SentinelUtils


def make_filter(pattern):
    def node_filter(node_info, include_pattern=pattern):
        return (
            True
            if fnmatch.fnmatch(node_info["node_path"].lower(), include_pattern)
            else False
        )

    return node_filter


def download_tiles(list_of_tiles, output_folder, user, password, nfilter="*B??.jp2"):
    if nfilter:
        nodefilter = make_filter(nfilter)

    api = SentinelAPI(user, password, "https://scihub.copernicus.eu/dhus")

    if os.path.exists(output_folder):
        for tile in list_of_tiles:
            print(
                f'Download tile name: {tile["tile_name"]} for {tile["date"][0]}, {tile["date"][1]}, with filter {nfilter}'
            )
            name = tile["tile_name"]
            date = tile["date"]
            products = api.query(
                date=date,
                tileid=name,
                platformname="Sentinel-2",
                producttype="S2MSI1C"
            )
            if nfilter:
                downloaded_products = api.download_all(
                    products,
                    directory_path=output_folder,
                    n_concurrent_dl=5,
                    nodefilter=nodefilter,
                )
            else:
                downloaded_products = api.download_all(
                    products, directory_path=output_folder, n_concurrent_dl=5
                )

            SentinelUtils.extract_zip_files(downloaded_products, output_folder)
