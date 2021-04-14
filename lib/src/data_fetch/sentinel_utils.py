import os
import shutil
from collections import OrderedDict
from glob import glob
from pathlib import Path

import rasterio

from lib.src.plotting_utils import *
import pandas as pd
import subprocess
BANDWIDTHS_TO_EXTRACT = OrderedDict({"red": "B04", "green": "B03", "blue": "B02"})


class SentinelUtils:
    @staticmethod
    def create_directory(dir_name="data"):
        abspath_to_create = os.path.join(os.path.abspath(os.path.curdir), dir_name)
        os.makedirs(name=abspath_to_create, exist_ok=True)
        return os.path.abspath(abspath_to_create)

    @staticmethod
    def unarchive_zip(file_path):
        unarchive_dir = file_path.parent
        shutil.unpack_archive(file_path, unarchive_dir)
        # os.remove(file_path)

    @staticmethod
    def get_data_from_image(bandwidth, files):
        print("files:{}".format(files))
        data_file = [bf for bf in files if bandwidth in bf][0]
        if data_file:
            data_array = rasterio.open(data_file).read(1)
            return data_array
        else:
            return None

    @staticmethod
    def save_originals(file_path, output_folder, tile_title, keep, delete_unused):
        Path(file_path).mkdir(exist_ok=True)
        band_files = glob(str(Path(f'{file_path}.SAFE/GRANULE/*/IMG_DATA/*.jp2')))
        to_move = [file for file in band_files if any(file.endswith(f'{band}.jp2') for band in keep)]
        for file in to_move:
            Path(file).replace(Path(f'{output_folder}/{tile_title}/{Path(file).name}'))
        if delete_unused:
            shutil.rmtree(Path(f'{file_path}.SAFE'))

    @staticmethod
    def extract_bandwidth_data_from_zip(
            zip_path, file_extraction_pattern="/GRANULE/*/IMG_DATA/*.jp2"
    ):
        data_folder = str(zip_path).replace(".zip", ".SAFE")

        bandwidth_files_to_be_extracted = glob(data_folder + file_extraction_pattern)

        results = []

        for color, wavelength_code in BANDWIDTHS_TO_EXTRACT.items():
            print("Extracting {0}, Code: {1}".format(color, wavelength_code))
            data = SentinelUtils.get_data_from_image(
                bandwidth=wavelength_code, files=bandwidth_files_to_be_extracted
            )
            # print("data: {}".format(data))
            results.append(data)
        return np.dstack(results)

    @staticmethod
    def plot_and_save_image(plot_path, figure_data):
        fig = plot_image(figure_data, factor=5 / 2e4, clip_range=(0, 1))

        fig.savefig(plot_path)

    @staticmethod
    def extract_zip_files(downloaded_products, output_folder):
        filename = [
            downloaded_products[0][k]["title"] for k in downloaded_products[0].keys()
        ][0]
        polygon_coordinates = [
            downloaded_products[0][item]["footprint"]
            for item in downloaded_products[0].keys()
        ][0]

        zip_file_path = Path(f"{output_folder}/{filename}.zip")
        SentinelUtils.unarchive_zip(zip_file_path)

        bandwidth_data = SentinelUtils.extract_bandwidth_data_from_zip(zip_file_path)

        plot_save_path = os.path.join(output_folder, "plots", filename + ".png")

        SentinelUtils.plot_and_save_image(plot_save_path, bandwidth_data)

        pg = parse_polygon_coordinates(polygon_coordinates)
        w, h = find_polygon_boundaries(pg)
        slice_giant_image(plot_save_path, height=h, width=w)

    @staticmethod
    def process_products(products, output_folder, delete_unused):
        print(f'Downloaded {len(products)} tiles, extracting and combining data')
        layers = []
        for tile in products.itertuples():
            layers.append(SentinelUtils.extract_data_from_tile(tile, output_folder, delete_unused))
        return pd.DataFrame.from_records(layers, columns=['rgb', 'b12'], index=products.index)


    @staticmethod
    def run_bash_script(input_folder, tile):
        # tmp = 'lib/src/data/S2B_MSIL1C_20200628T184919_N0209_R113_T10SFG_20200628T220923.SAFE/GRANULE/L1C_T10SFG_A017299_20200628T185809/IMG_DATA'
        folder_with_jp2_images = os.path.join(input_folder, tile.title + '.SAFE')
        output_dir = os.path.join(folder_with_jp2_images, 'jpg_image')
        print("starting Bash Script")
        # subprocess.call(f"s2Converter.sh -w 10980 -i {folder_with_jp2_images} ")
        os.system(f"lib/src/data_fetch/s2Converter.sh -w 10980 -o {output_dir} -i {folder_with_jp2_images}")
        print("ending Bash Script")


    @staticmethod
    def extract_data_from_tile(tile, output_folder, delete_unused):
        file_path = Path(f'{output_folder}/{tile.title}.zip')
        SentinelUtils.unarchive_zip(file_path)

        # run bash now
        SentinelUtils.run_bash_script(input_folder=output_folder, tile=tile)
        rgb, b12 = extract_and_combine(file_path)

        plot_save_path = os.path.join(output_folder, "plots", tile.title + ".png")
        SentinelUtils.plot_and_save_image(plot_save_path, bandwidth_data)

        pg = parse_polygon_coordinates(polygon_coordinates)
        w, h = find_polygon_boundaries(pg)


        cut_and_save(file_path, rgb, tile.title)

        SentinelUtils.save_originals(file_path, output_folder, tile.title, ['B04', 'B03', 'B02', 'B12'], delete_unused)
        return rgb, b12
