import unittest
from unittest.mock import patch, MagicMock
from spotlite.search import Searcher  # Replace 'search' with the actual name of your Python file if different
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

class TestSearcher(unittest.TestCase):

    def setUp(self):
        self.searcher = Searcher(key_id="dummy_id", key_secret="dummy_secret")

    def test_date_range_chunks(self):
        # Create an instance of the Searcher class
        searcher = Searcher()

        # Define test data
        start_date = "2023-01-01"
        end_date = "2023-02-01"
        chunk_size_days = 14

        # Call the method under test
        chunks = list(searcher._date_range_chunks(start_date, end_date, chunk_size_days))

        # Expected number of chunks
        expected_num_chunks = 2

        # Assertions
        self.assertEqual(len(chunks), expected_num_chunks)
        self.assertEqual(chunks[0], ("2023-01-01", "2023-01-15"))
        self.assertEqual(chunks[1], ("2023-01-15", "2023-02-01"))



if __name__ == '__main__':
    unittest.main()
