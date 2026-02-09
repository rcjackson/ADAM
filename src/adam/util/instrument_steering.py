import numpy as np
import logging
from adam.io import RadarImage
from scipy.ndimage import center_of_mass, label

def azimuth_point(instrument_lon, instrument_lat, 
                  radar_image: RadarImage, index=None,
                  area_threshold=20):
    """
    Calculate the azimuth angle from the radar instrument to each pixel in the radar image.

    Parameters
    ----------
    instrument_lat: float
        Latitude of the radar instrument in degrees.
    instrument_lon: float
        Longitude of the radar instrument in degrees.
    radar_image: RadarImage
        The RadarImage object containing the radar data and metadata.
    index: int, optional
        If the radar image contains multiple time frames, specify the index of the frame to use. If None, use the first frame.
    area_threshold: int
        The minimum continuous area in pixels for lake breeze segments. This helps
        remove false positive speckles that are identified by the model.

    Returns
    -------
    deg_angle: float
       Azimuth angle in degrees from the radar instrument to the center of the largest lake breeze region.
    lat_center: float
       Latitude of the center of the largest lake breeze region.
    lon_center: float
       Longitude of the center of the largest lake breeze region.
    """
    # Convert lat/lon to radians
    if index is None:
        mask = radar_image[0]
    else:
        mask = radar_image[index]
    
    lats = radar_image.grid_lat
    lons = radar_image.grid_lon
    lat_index = np.argmin(np.abs(lats - instrument_lat))
    lon_index = np.argmin(np.abs(lons - instrument_lon))
    labels, num_features = label(mask)
    area_threshold = 20
    largest_area = -99999
    mask = mask.T
    for i in range(num_features):
        area = mask[labels == i].sum()
        if area > largest_area:
            largest_area = area
        if area < area_threshold:
            mask[labels == i] = 0

    center = center_of_mass(mask)
    num_y = len(radar_image.grid_y)
    num_x = len(radar_image.grid_x)
    center_x = radar_image.grid_x[int(center[1])]
    center_y = radar_image.grid_y[int(center[0])]
    logging.info(f"Center of mass: {center}, Center lat/lon: {center_y}, {center_x}")
    instrument_x = radar_image.grid_x[lon_index]
    instrument_y = radar_image.grid_y[lat_index]
    logging.info(f"Instrument lat/lon: {instrument_y}, {instrument_x}")
    angle = np.arctan2((center_x - instrument_x), (center_y - instrument_y))
    deg_angle = np.rad2deg(angle)
    deg_angle = (deg_angle + 360) % 360

    # Get the distance from the instrument to the nearest point in the lake breeze region
    x, y = np.meshgrid(radar_image.grid_x, radar_image.grid_y)
    dist = np.sqrt((x - instrument_x)**2 + (y - instrument_y)**2)
    dist = dist[mask == 1]
    dist = np.min(dist)
    return deg_angle, lats[int(center[0])], lons[int(center[1])], dist


    