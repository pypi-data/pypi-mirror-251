import unittest
import numpy as np
import xarray as xr
from xevent import composite


class TestComposite(unittest.TestCase):
    def setUp(self):
        # sample dataset with dimensions (n, m, x, y)
        n = 8
        m = 10
        x = 100
        y = 200

        # Create the sample data array
        data = np.random.rand(n, m, x, y)
        coords = {
            "n": np.arange(n),
            "m": np.arange(m),
            "x": np.arange(x),
            "y": np.arange(y),
        }
        data = xr.DataArray(data, coords=coords, dims=["n", "m", "x", "y"])

        # sample events
        events = [
            {"n": 0, "m": 0, "x": 11, "y": 22},
            {"n": 0, "m": 0, "x": 22, "y": 33},
            {"n": 1, "m": 1, "x": 33, "y": 44},
            {"n": 1, "m": 3, "x": 44, "y": 55},
            {"n": 2, "m": 5, "x": 55, "y": 66},
            {"n": 3, "m": 7, "x": 77, "y": 77},
        ]
        self.data = data
        self.events = events

    def test_composite_no_interpolation(self):
        # Test composite without interpolation
        relative_coords = {"x": np.arange(-5, 6), "y": np.arange(-5, 6)}

        print(self.data)
        result = composite(self.data, self.events, relative_coords, interpolate=False)
        print(result)
        self.assertIsInstance(result, xr.DataArray)
        self.assertEqual(result.dims, ("event", "rel_x", "rel_y"))

    def test_composite_with_interpolation(self):
        pass

    def test_composite_missing_coord_labels(self):
        relative_coords = {"x": np.arange(-100, 100), "y": np.arange(-5, 6)}
        result = composite(self.data, self.events, relative_coords, interpolate=False)
        print(result)


if __name__ == "__main__":
    unittest.main()
