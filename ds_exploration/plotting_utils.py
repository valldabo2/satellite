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
    _, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    if clip_range is not None:
        ax.imshow(np.clip(image * factor, *clip_range), **kwargs)
    else:
        ax.imshow(image * factor, **kwargs)
    ax.set_xticks([])
    ax.set_yticks([])
    return ax


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
