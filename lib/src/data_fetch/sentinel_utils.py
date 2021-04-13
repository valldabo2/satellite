import os
import shutil
from collections import OrderedDict
from glob import glob
from pathlib import Path

import rasterio

from plotting_utils import *

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
        os.remove(file_path)

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
