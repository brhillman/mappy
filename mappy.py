#!/usr/bin/env python3
import numpy, xarray, scipy.sparse

def apply_map_slow(d_native, row, col, wgt):
    d_remap = numpy.zeros(max(row).values)
    for k in range(len(wgt)):
        d_remap[row[k]-1] = d_remap[row[k]-1] + d_native[col[k]-1] * wgt[k]
    return d_remap

def apply_map(d_native, row, col, wgt, shape_out=None):
    # Load weights into a scipy sparse COO matrix
    weights = scipy.sparse.coo_matrix((wgt.values, (row.values-1, col.values-1)))
    # Apply weights
    d_remap = weights.dot(d_native)
    # Reshape
    if shape_out is not None:
        d_remap = d_remap.reshape(shape_out)
    # Return remapped, reshaped array
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
    d_remap = apply_map(d_native, row, col, wgt)

    # Create a DataArray with coordinate data
    d_remap_da = xarray.DataArray(
        d_remap,
        dims=lat.dims,
    )

    # Save to output file
    xarray.Dataset({vname: d_remap_da, 'lat': lat, 'lon': lon}).to_netcdf(outputfile)

if __name__ == '__main__':
    import plac; plac.call(main)
