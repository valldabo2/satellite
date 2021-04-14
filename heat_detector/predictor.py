import numpy as np


class HeatPredictor(object):
    def predict(self, tiles, band_value_threshold=10_000, min_points=250, **kwargs):
        """
        :param tiles: list containing tiles data
        :param band_value_threshold: B12 value we consider "hot enough"
        :param min_points: minimum quantity of "hot enough" points to consider fire
        :return: boolean, fire or not
        """
        return [self._is_fire(t["B12"], band_value_threshold, min_points) for t in tiles]

    def _is_fire(self, b12, band_value_threshold=10_000, min_points=250):
        """
        :param b12: list containing the B12 band values
        :param band_value_threshold: B12 value we consider "hot enough"
        :param min_points: minimum quantity of "hot enough" points to consider fire
        :return: boolean, fire or not
        """
        return (np.array(b12).flatten() > band_value_threshold).sum() >= min_points
