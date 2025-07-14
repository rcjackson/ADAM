import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pyart

from ..io import RadarImage

def visualize_lake_breeze(radar_scan: RadarImage, **kwargs):

    lat_lines = kwargs.pop('lat_lines', default=[41.2, 41.4, 41.6, 41.8, 42, 42.2, 42.4])
    lon_lines = kwargs.pop('lon_lines', default=[-88.4, -88.2, -88, -87.8, -87.6])
    vmin = kwargs.pop('vmin', default=-30)
    vmax = kwargs.pop('vmax', default=60)
    sweep = kwargs.pop('sweep', default=0)

    disp = pyart.graph.RadarMapDisplay(cur_radar)
    if 'ax' not in kwargs.keys():
        fig, ax = plt.subplots(1, 1, figsize=(5, 5),
                subplot_kw=dict(projection=ccrs.PlateCarree()))
    else:
        ax = kwargs.pop('ax') 
    disp.plot_ppi_map('reflectivity', sweep=sweep, min_lon=radar_scan.lon_range[0],
        ax=ax, max_lon=radar_scan.lon_range[1], min_lat=radar_scan.lat_range[0], max_lat=radar_scan.lat_range[1],
        lat_lines=lat_lines, lon_lines=lon_lines, vmin=vmin, vmax=vmax, ax=ax, **kwargs)
    ax.coastlines()
    ax.add_feature(cfeature.STATES)
    ax.contour(radar_scan.grid_lon, radar_scan.grid_lat,
            radar_scan.lakebreeze_mask.T, levels=1)

    return ax


