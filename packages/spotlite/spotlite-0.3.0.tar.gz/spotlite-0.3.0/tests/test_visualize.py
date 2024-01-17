import unittest
from unittest.mock import patch, MagicMock
from spotlite.tile import TileManager  # Replace 'visualize' with the actual name of your Python file if different
import geopandas as gpd
from shapely.geometry import Polygon, Point, box

class TestVisualizer(unittest.TestCase):

    def setUp(self):
        self.visualizer = TileManager()


if __name__ == '__main__':
    unittest.main()
