import pytest 
import adam
import torch
import numpy as np

def test_instrument_steering():
    torch.manual_seed(42)
    rad_scan = adam.io.preprocess_radar_image('KLOT', '2025-07-15T18:00:00')
    rad_scan = adam.model.infer_lake_breeze(
        rad_scan, model_name='lakebreeze_best_model_fcn_resnet50')
    angle, lat, lon = adam.util.azimuth_point(-87.99577278662817, 41.70101404798476, rad_scan)
    np.testing.assert_almost_equal(angle, 150.8913299536037, decimal=0)
    np.testing.assert_almost_equal(lat, 41.963764705882355, decimal=0)
    np.testing.assert_almost_equal(lon, -87.75284862745099, decimal=0)