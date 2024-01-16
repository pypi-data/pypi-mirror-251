import xarray as xr
import numpy as np


def composite(
    data: (xr.DataArray | xr.Dataset),
    events: list[dict],
    relative_coords: dict,
    interpolate: bool = False,
) -> xr.DataArray | xr.Dataset:
    """Create a composite of events from a dataset or dataarray.add()

    Parameters
    ----------
    data : xr.DataArray  |  xr.Dataset
        Input data.
    events : list[dict]
        List of events, each event is a dictionary with keys that correspond to the dimensions of the data.
    relative_coords : dict
        For each coordinate that should center around the event, provide a list of relative coordinates,
        e.g. given a dimension "x" with values ``[0, 1, 2, 3, 4, 5]``,
        relative_coords = ``dict(x=[-1, 0, 1])`` would result in a composite with values at ``[-1, 0, 1]`` relative to the event
    interpolate : bool, optional
        If False, use xarray's .sel() method to select datapoints. If True, use xarray's .interp() method to interpolate. Defaults to False.

    Returns
    -------
    xr.DataArray | xr.Dataset
        Output data with dimensions "event" and "rel_<dim>" for each dimension that is a relative coordinate.


    Examples
    --------
    >>> # sample dataset with dimensions (n, m, x, y)
    >>> n = 8
    >>> m = 10
    >>> x = 100
    >>> y = 200

    >>> # Create the sample data array
    >>> data = np.random.rand(n, m, x, y)
    >>> coords = {'n': np.arange(n), 'm': np.arange(m), 'x': np.arange(x), 'y': np.arange(y)}
    >>> data = xr.DataArray(data, coords=coords, dims=['n', 'm', 'x', 'y'])
    <xarray.DataArray (n: 8, m: 10, x: 100, y: 200)>
    Coordinates:
    * n        (n) int64 0 1 2 3 4 5 6 7
    * m        (m) int64 0 1 2 3 4 5 6 7 8 9
    * x        (x) int64 0 1 2 3 4 5 6 7 8 9 10 ... 90 91 92 93 94 95 96 97 98 99
    * y        (y) int64 0 1 2 3 4 5 6 7 8 ... 191 192 193 194 195 196 197 198 199

    >>> # sample events
    >>> events = [
    ...     {'n': 0, 'm': 0, 'x': 11, 'y': 22},
    ...     {'n': 0, 'm': 0, 'x': 22, 'y': 33},
    ...     {'n': 1, 'm': 1, 'x': 33, 'y': 44},
    ...     {'n': 1, 'm': 3, 'x': 44, 'y': 55},
    ...     {'n': 2, 'm': 5, 'x': 55, 'y': 66},
    ...     {'n': 3, 'm': 7, 'x': 77, 'y': 77},
    ... ]

    >>> composite(data, events, relative_coords=dict(x=np.arange(-5, 6), y=np.arange(-5, 6)))
    <xarray.DataArray (event: 6, rel_x: 11, rel_y: 11)>
    Coordinates:
        n        (event) int64 0 0 1 1 2 3
        m        (event) int64 0 0 1 3 5 7
        x        (event, rel_x) int64 6 7 8 9 10 11 12 13 ... 76 77 78 79 80 81 82
        y        (event, rel_y) int64 17 18 19 20 21 22 23 ... 76 77 78 79 80 81 82
    * event    (event) int64 0 1 2 3 4 5
    * rel_x    (rel_x) int64 -5 -4 -3 -2 -1 0 1 2 3 4 5
    * rel_y    (rel_y) int64 -5 -4 -3 -2 -1 0 1 2 3 4 5


    Notes
    -----
    If the relative coordinates lead to selection of coordinates that are not present in the input data, use ``interpolate=True`` to interpolate the data (result will be NaN where no data is present).
    """
    n_events = len(events)
    event_indices = np.arange(n_events)

    # iterate all dimensions and define DataArray that stores their coordinates relative to dimension "event"
    all_dims = events[0].keys()
    event_coords = {}
    for d in all_dims:
        event_coords[d] = xr.DataArray(
            [e[d] for e in events], coords=dict(event=event_indices), dims=["event"]
        )

    # iterate relative coordinates and define DataArray that stores their relative grid
    sel_rel_coords = {}
    for coord_name, rel_coords in relative_coords.items():
        rel_coord_name = "rel_" + coord_name
        rel_coords_dataarray = xr.DataArray(
            rel_coords, coords={rel_coord_name: rel_coords}, dims=rel_coord_name
        )
        sel_rel_coords[coord_name] = event_coords[coord_name] + rel_coords_dataarray

    # for all dimensions that are not relative, select the event coordinate, for all dimensions that are relative, select the relative coordinate
    sel_non_rel_coords = {
        k: event_coords[k] for k in event_coords.keys() - relative_coords.keys()
    }
    # either select or interpolate
    if interpolate:
        return data.interp(**sel_non_rel_coords, **sel_rel_coords)
    else:
        # ensure that all coordinate labels are present in the data
        data_reindexed = data.reindex(
            {k: np.unique(v) for k, v in sel_rel_coords.items()}
        )
        return data_reindexed.sel(**sel_non_rel_coords, **sel_rel_coords)
