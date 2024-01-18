#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import absolute_import, division, print_function

from os import makedirs, remove, rename
from os.path import basename, dirname, exists, isdir, join
from urllib.request import urlopen

import numpy as np
from netCDF4 import Dataset
from osgeo import gdal

"""
Read global surface water from https://global-surface-water.appspot.com/

Example:
    GSW().get(lat, lon)
"""


def url_tile(tile_name):
    return "https://storage.googleapis.com/global-surface-water/downloads/occurrence/occurrence_{}.tif".format(
        tile_name
    )


def fetch_gsw_tile(tile_name, directory, verbose=True):
    """
    Read remote file and returns its content

    https://storage.googleapis.com/global-surface-water/downloads/occurrence/occurrence_180W_80N.tif
    """
    url = url_tile(tile_name)

    if verbose:
        print("Downloading", url)
    #    with tempfile.NamedTemporaryFile() as t:
    #        # download the tile
    #        with urlopen(url) as response:
    #            raw_data = response.read()
    #
    #        # write to temporary
    #        with open(t.name, 'wb') as fp:
    #            fp.write(raw_data)

    resp = urlopen(url)
    respHtml = resp.read()
    binfile = open(join(directory, basename(url)), "wb")
    binfile.write(respHtml)
    binfile.close()

    # read geotiff data
    ds = gdal.Open(join(directory, basename(url)))
    data = ds.ReadAsArray()
    ds = None
    data[data == 255] = 100  # fill invalid data (assume water)
    remove(join(directory, basename(url)))
    return data


def aggregate(A, agg=1):
    if agg == 1:
        return A

    data = None
    for i in range(agg):
        for j in range(agg):
            acc = A[i::agg, j::agg]
            if data is None:
                data = acc.astype("f")
            else:
                data += acc

    return (data / (agg * agg)).astype(A.dtype)


def write_nc(filename, var, data, attrs={}):
    root = Dataset(filename + ".tmp", "w")
    root.createDimension("width", data.shape[1])
    root.createDimension("height", data.shape[0])
    var = root.createVariable(
        var,
        data.dtype,
        ["height", "width"],
        zlib=True,
    )
    var[:] = data
    # set attributes
    root.setncatts(attrs)
    root.close()

    # move to final
    rename(filename + ".tmp", filename)


def read_nc(filename, var):
    root = Dataset(filename)
    data = root.variables[var][:]
    root.close()
    return data


def get_gsw_tile(tile_name, directory="landmask_gsw", agg=1, verbose=True):
    assert agg > 0
    assert (agg & (agg - 1)) == 0, "Agg must be a power of 2"

    filename = join(directory, "occurrence_{}_{}.nc".format(tile_name, agg))
    if not exists(filename):
        write_nc(
            filename,
            "occurrence",
            aggregate(fetch_gsw_tile(tile_name, directory, verbose=verbose), agg=agg),
            {
                "aggregation factor": str(agg),
                "source_file": url_tile(tile_name),
            },
        )

    return filename


def read_gsw_tile(tile_name, directory="landmask_gsw", agg=1, verbose=True):
    """
    Read one tile from local data or downloads it

    agg: aggregate by agg x agg (agg = 1, 2, 4, 8, etc)
    """
    filename = get_gsw_tile(tile_name, directory=directory, agg=agg, verbose=verbose)

    return read_nc(filename, "occurrence")


def get_sw(lat, lon, directory="landmask_gsw", agg=1):
    """
    Reads JRC Global Surface Water data from (lat, lon) in water percentage
    """
    if not exists(directory):
        raise IOError(
            "Data directory for GSW data (global surface water) does not exist: mkdir -p {}".format(
                directory
            )
        )

    sw = np.zeros(lat.shape, dtype="float32")

    # determine the required tiles
    ilatlon = (
        100 * (9 + np.floor(np.array(lat) / 10).astype("int"))
        + 18
        + np.floor(np.array(lon) / 10).astype("int")
    )

    tids = set(ilatlon.ravel())
    for i, tid in enumerate(tids):
        ilat = ((tid // 100 - 9) + 1) * 10
        ilon = (tid % 100 - 18) * 10

        tile_name = "{}{}_{}{}".format(
            abs(ilon),
            {True: "E", False: "W"}[ilon >= 0],
            abs(ilat),
            {True: "N", False: "S"}[ilat >= 0],
        )

        # check is data is available
        if (ilat > 80) or (ilat < -50):
            continue

        data = read_gsw_tile(tile_name, directory=directory, agg=agg)
        n = data.shape[0]
        assert data.shape == (n, n)

        # fills for the current tile
        ok = ilatlon == tid

        ilat_ = ((ilat - np.array(lat)[ok]) * (n - 1) / 10).astype("int")
        ilon_ = ((np.array(lon)[ok] - ilon) * (n - 1) / 10).astype("int")

        sw[ok] = data[(ilat_, ilon_)]

    return sw


class GSW(object):
    def __init__(self, directory="landmask_gsw", on_error=0.0, threshold=90.0, agg=1):
        """
        Global surface water interface

        GSW().get(lat, lon)

        agg: aggregation factor (a power of 2)
             original resolution of GSW is about 55M at equator
             reduce this resolution by agg x agg to approximately match the sensor resolution
        """
        current_path = dirname(__file__)
        self.directory = join(current_path, directory)
        self.on_error = on_error
        self.threshold = threshold
        self.agg = agg
        if not isdir(self.directory):
            makedirs(self.directory)

    def get(self, lat, lon):
        """
        Returns land occurrence for coordinates lat, lon (arrays) as a boolean array
        (water percentage lower than threshold)
        """
        data = get_sw(lat, lon, directory=self.directory, agg=self.agg)

        return data < self.threshold


if __name__ == "__main__":
    lat = np.array([38])
    lon = np.array([122])
    gsw = GSW().get(lat, lon)
    print(gsw)
