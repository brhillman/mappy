#!/usr/bin/env python3
import numpy, xarray

def apply_map(d_native, row, col, wgt):
    d_remap = numpy.zeros(max(row).values)
    for k in range(len(wgt)):
        d_remap[row[k]-1] = d_remap[row[k]-1] + d_native[col[k]-1] * wgt[k]
    return d_remap

def main(vname, mapfile, inputfile, outputfile):

    # Read inputs
    ds_map = xarray.open_dataset(mapfile)
    ds_in  = xarray.open_dataset(inputfile).isel(time=0)
    wgt = ds_map['S']
    row = ds_map['row']
    col = ds_map['col']
    d_native = ds_in[vname]

    # Read coordinate variables
    lat = ds_map['yc_b']
    lon = ds_map['xc_b']

    # Apply map
    d_remap = xarray.DataArray(apply_map(d_native, row, col, wgt), dims=lat.dims)

    # Save to output file
    xarray.Dataset({vname: d_remap, 'lat': lat, 'lon': lon}).to_netcdf(outputfile)

if __name__ == '__main__':
    import plac; plac.call(main)
