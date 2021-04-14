from lib.src.data_fetch.sentinel_utils import SentinelUtils
from lib.src.data_fetch.data_download import download_tiles

if __name__ == "__main__":
    list_of_tiles = [
        # {"tile_name": "10SEH", "date": ("20200928", "20200930")},
        {'tile_name': '10SFG', 'date': ('20200627', '20200629')},
        # {"tile_name": "10TDK", "date": ("20201004", "20201009")},
        # {"tile_name": "10TDL", "date": ("20200928", "20200930")},
    ]

    user = "utsavjha"
    password = "abcdefgh"

    data_dir_path = SentinelUtils.create_directory(dir_name="data")
    plots_dir_path = SentinelUtils.create_directory(dir_name="data/plots")

    download_tiles(list_of_tiles, data_dir_path, user, password, nfilter=None)
