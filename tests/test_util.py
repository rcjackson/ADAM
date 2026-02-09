import pytest 
import adam
import torch
import numpy as np

def test_instrument_steering():
    torch.manual_seed(42)
    rad_scan = adam.io.preprocess_radar_image('KLOT', '2025-04-24T20:03:23')
    rad_scan = adam.model.infer_lake_breeze(
        rad_scan, model_name='lakebreeze_model_fcn_resnet50_no_augmentation')
    angle, lat, lon, dist = adam.util.azimuth_point(-87.99577278662817, 41.70101404798476, rad_scan)
    np.testing.assert_almost_equal(angle, 224.61, decimal=0)
    np.testing.assert_almost_equal(lat, 41.68, decimal=2)
    np.testing.assert_almost_equal(lon, -88.01, decimal=2)
    np.testing.assert_almost_equal(dist, 0, decimal=2)