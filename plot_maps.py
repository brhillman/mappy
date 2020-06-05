#!/usr/bin/env python3
import xarray
from matplotlib import pyplot
from cartopy import crs

def main(varname, outputfile, *inputfiles, **kwargs):
    figure, axes = pyplot.subplots(1, len(inputfiles), figsize=(15, 5))
    for icase, inputfile in enumerate(inputfiles):
        ds = xarray.open_dataset(inputfile)
        data = ds[varname].squeeze()
        lon = ds['lon']
        lat = ds['lat']
        
        ax = figure.add_axes(axes[icase])
        pl = ax.tripcolor(lon, lat, data)

    figure.savefig(outputfile, bbox_inches='tight')

if __name__ == '__main__':
    import plac; plac.call(main)
