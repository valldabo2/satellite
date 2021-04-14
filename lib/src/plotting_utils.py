import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon
import geopy.distance
from PIL import Image
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from skimage.util import view_as_blocks
from skimage.transform import rescale
from skimage.io import imsave

def plot_image(image, factor=1.0, clip_range=None, figsize=(15, 15), **kwargs):
    """
    Utility function for plotting RGB images.
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    if clip_range is not None:
        ax.imshow(np.clip(image * factor, *clip_range), **kwargs)
    else:
        ax.imshow(image * factor, **kwargs)
    ax.set_xticks([])
    ax.set_yticks([])

    return fig


def parse_polygon_coordinates(api_footprint_response: str):
    """Returns a Shapely Polygon object from the API response"""
    pg_coordinates = []
    for str_coordinates in api_footprint_response[9:].split(","):
        str_lat, str_long = str_coordinates.split(" ")
        long = float(str_long[:10])
        lat = float(str_lat[:10])
        pg_coordinates.append((long, lat))

    polygon = Polygon(pg_coordinates)
    return polygon


def find_polygon_boundaries(pg: Polygon):
    width = geopy.distance.geodesic(
        (pg.bounds[1], pg.bounds[0]), (pg.bounds[1], pg.bounds[2])
    ).kilometers
    height = geopy.distance.geodesic(
        (pg.bounds[1], pg.bounds[0]), (pg.bounds[3], pg.bounds[0])
    ).kilometers

    return (width, height)


def slice_giant_image(giant_image_path, height, width):
    im = Image.open(giant_image_path)
    giant_image = np.array(im)

    cut_images = []

    h_chunk = int(giant_image.shape[0] / height)
    w_chunk = int(giant_image.shape[1] / width)
    for h in range(int(height)):
        for w in range(int(width)):
            image_cut = giant_image[
                h_chunk * h : h_chunk * (h + 1), w_chunk * w : w_chunk * (w + 1), :
            ]
            cut_images.append(image_cut)

    # plt.imshow(cut_images[20])
    return cut_images


def cut_tile_blocks(tile_data, cut_factor = 10):
    shape = (tile_data.shape[0] // cut_factor, tile_data.shape[1] // cut_factor, 3)
    return view_as_blocks(tile_data, block_shape=(shape)).reshape(-1, *shape)


def scale_image(image_data, rescale_coeff=0.2332, factor=5/2e4):
    return (np.clip(rescale(image_data, scale=rescale_coeff, preserve_range=True, multichannel=True) * factor, 0, 1) * 255).astype(np.uint8)


def save_cuts(blocks, filepath, tile_name):
    Path(filepath).mkdir(exist_ok=True)
    for i, block in enumerate(blocks):
        scaled = scale_image(block)
        imsave(f'{filepath}/{tile_name}_block_{i}.jpg', scaled, check_contrast=False)


def cut_and_save(filepath, tile_data, tile_name):
    blocks = cut_tile_blocks(tile_data)
    print(f'Saving {len(blocks)} jpg images into {filepath} folder')
    save_cuts(blocks, filepath, tile_name)
