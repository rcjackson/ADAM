import boto3
import pyart
import numpy as np
import cmweather
import matplotlib.pyplot as plt
import torch

from datetime import datetime, timedelta 
from botocore import UNSIGNED
from torchvision.io import decode_image
from torchvision import transforms

class RadarImage(object):
    """
    This class contains the basic data for predicting the lake-breeze front location
    from radar. It includes parameters for storing the radar data for later analysis
    in Py-ART and for inference in the lake-breeze prediction model.
    """
    pyart_object = None
    lat_range = None
    lon_range = None
    datetime = None
    grid_lat = None
    grid_lon = None
    pytorch_image = None
    lakebreeze_mask = None

def preprocess_radar_image(radar, datetime=None, lat_range=(41.1280, 42.5680),
                           lon_range=(-88.7176, -87.2873))
    """
    This module will preprocess the NEXRAD radar data for inference into the lake-breeze
    prediction model of ADAM.

    Parameters
    ----------
    radar: str
        The 4-letter code for the radar to obtain the scan from. For Chicago, use KLOT.
    datetime: ISO-format datestring
        The date/time string in ISO format for the radar scan. If None, then ADAM will
        get the latest scan.
    lat_range: 2-tuple of floats
        The minimum and maximum latitude of the domain in degrees. Default is a centered
        domain around the KLOT Chicago area radar.
    lon_range: 2-tuple of floats
        The minimum and maximum longitude of the domain in degrees. Default is a centered
        domain around the KLOT Chicago area radar.

    Returns
    -------
    image: :code:`adam.io.RadarImage`
        The :code:`RadarImage` object containing the radar scan, pre-processed image,
        and grid.
    """
    if inp_time is None:
        right_now = datetime.utcnow()
    else:
        right_now = inp_time
    yesterday = right_now - timedelta(days=1)
    year = right_now.year
    month = right_now.month
    day = right_now.day

    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    bucket_name = 'noaa-nexrad-level2'
    radar = "KLOT"
    prefix = f'{year}/{month:02d}/{day:02d}/{radar}'
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    file_list = [x['Key'] for x in response['Contents']]
    
    # Find yesterday's scans
    prefix = f'{yesterday.year}/{yesterday.month:02d}/{yesterday.day:02d}/{radar}'
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    file_list = file_list + [x['Key'] for x in response['Contents']]
    out_path = os.path.join(out_path, f'{year}/{year}{month:02d}{day}/')
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    time_list = []
    for filepath in file_list:
        name = filepath.split("/")[-1]
        if name[-3:] == "MDM":
            time_list.append(
                datetime.strptime(name, f"{radar}%Y%m%d_%H%M%S_V06_MDM"))
        else:
            time_list.append(
                datetime.strptime(name, f"{radar}%Y%m%d_%H%M%S_V06"))

    time_list = np.array(time_list)
    cur_time = time_list[np.argmin(np.abs(time_list - right_now))]
    path = "s3://noaa-nexrad-level2/" + file_list[np.argmin(np.abs(time_list - right_now))]
    cur_radar = pyart.io.read_nexrad_archive(path)

    disp = pyart.graph.RadarMapDisplay(cur_radar)
    fig, ax = plt.subplots(1, 1, figsize=(256/150, 256/150),
            subplot_kw=dict(projection=ccrs.PlateCarree(), frameon=False))

    disp.plot_ppi_map('reflectivity', sweep=1, min_lon=lon_range[0],
            ax=ax, max_lon=lon_range[1], min_lat=lat_range[0], max_lat=lat_range[1],
            embellish=False, vmin=-20, vmax=60, cmap='HomeyerRainbow',
            add_grid_lines=False, colorbar_flag=False, title_flag=False)
    ax.set_axis_off()
    fig.tight_layout(pad=0, w_pad=0, h_pad=0)
    fig.savefig('temp.png', dpi=150)
    plt.close(fig)
    # Transform image
    image = decode_image('temp.png')
    image = image[:3, :, :].float()
    transform = transforms.Compose([
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
    image = torch.stack([transform(image)])
    lats = np.linspace(lat_range[1], lat_range[0], image.shape[1])
    lons = np.linspace(lon_range[0], lon_range[1], image.shape[0])
    os.remove('temp.png')

    rad_image = RadarImage()
    rad_image.pytorch_image = image
    rad_image.lat_range = lat_range
    rad_image.lon_range = lon_range
    rad_image.pyart_object = cur_radar
    rad_image.grid_lat = lats
    rad_image.grid_lon = lons

    return rad_image