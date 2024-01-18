# PYODIM

A simple ODIM H5 (Opera Data Information Model - Hierarchical Data Format 
version 5) radar reader in Python. It outputs the radar date in an xarray 
Dataset. The goal is to be as barebone as possible while providing an xarray, 
so that it can easily scale up (production) or just a very lean reader for 
quicklooks into the data.

## Example

```python

import pyodim

filename = "/path/to/radar/file.h5"
rset = pyodim.read_odim(filename, lazy_load=True)  # Lazy load does not load the data in memory to save time if you are interested in only a specific sweep
radar = rset[0].compute()  # All sweeps are in a list (elevation ascending), so the 1st item of the list is the bottom sweep.
print(radar)
```

This code will output the radar data for the first sweep (lowest elevation 
scan) in the radar file as an xarray Dataset, for example:

```python
<xarray.Dataset>
Dimensions:     (azimuth: 360, range: 1283, elevation: 1, time: 360)
Coordinates:
  * range       (range) float32 125.0 375.0 625.0 ... 3.204e+05 3.206e+05
  * azimuth     (azimuth) float32 0.01111 1.011 2.011 ... 357.0 358.0 359.0
  * elevation   (elevation) float32 0.5
  * time        (time) datetime64[ns] 2024-01-16T02:49:29.337047353 ... 2024-...
Data variables: (12/17)
    DBZH        (azimuth, range) float64 nan nan nan nan nan ... nan nan nan nan
    SNRH        (azimuth, range) float64 nan nan nan nan nan ... nan nan nan nan    
    VRADH       (azimuth, range) float64 nan nan nan nan nan ... nan nan nan nan
    WRADH       (azimuth, range) float64 nan nan nan nan nan ... nan nan nan nan
    KDP         (azimuth, range) float64 nan nan nan nan nan ... nan nan nan nan
    ...          ...
    x           (azimuth, range) float32 0.02424 0.07271 ... -5.595e+03
    y           (azimuth, range) float32 125.0 375.0 ... 3.203e+05 3.206e+05
    z           (azimuth, range) float32 45.09 47.27 ... 2.84e+03 2.842e+03
    longitude   (azimuth, range) float32 144.8 144.8 144.8 ... 144.7 144.7 144.7
    latitude    (azimuth, range) float32 -37.85 -37.85 -37.85 ... -34.97 -34.96
Attributes: (12/15)
    Conventions:  ODIM_H5/V2_4
    latitude:     -37.85200119018555
    longitude:    144.75199890136722
    height:       44.0
    date:         2024-01-16T02:45:21
    object:       PVOL
    ...           ...
    beamwV:       1.0
    wavelength:   10.489999771118164
    NI:           36.5052
    highprf:      696.0
    start_time:   20240116_024928
    end_time:     20240116_024958
```

PYODIM reads the ODIM radar data and metadata. It also provides some quality of 
life feature like automatically creating the x, y, z and latitude/longitude 
coordinates for all radar gates (using the azimuthal equidistant - `aeqd` - projection). By 
default it uses `dask.delayed` to *lazily* load the data, meaning that it will 
not actually load all the sweeps in memory, as for many applications we often 
don't need all the radar sweeps. Instead, by calling the `.compute()` method 
like in the example above, PYODIM will only read and load in memory the sweep 
that you want, saving time. If you want to read all the sweeps at once in a 
list, then just set `lazy_load=False`.

## Dependencies

Mandatory:
- [numpy][1]
- [xarray][2]
- [pyproj][3]
- [dask][4]

And optionally (it will automatically populate the fields metadata using pyart 
if available): 
- [Py-ART][5] 

[1]: http://www.scipy.org/
[2]: http://numba.pydata.org
[3]: https://pypi.org/project/pyproj/
[4]: https://www.dask.org/
[5]: https://github.com/ARM-DOE/pyart