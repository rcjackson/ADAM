#!/usr/bin/env python
import pytest
import adam
import torch
import numpy as np

"""Tests for `adam` package."""

# from adam import adam

def test_preprocess_radar_image():
    torch.manual_seed(42)
    rad_scan = adam.io.preprocess_radar_image('KLOT', '2025-07-15T18:00:00')
    assert rad_scan.pytorch_image.shape == torch.Size([1, 3, 256, 256])
    np.testing.assert_almost_equal(rad_scan.pytorch_image.sum().numpy(), 1.5452675e+08, -2)

def test_infer_fcn_resnet50():
    torch.manual_seed(42)
    rad_scan = adam.io.preprocess_radar_image('KLOT', '2025-07-15T18:00:00')
    rad_scan = adam.model.infer_lake_breeze(rad_scan, model_name='lakebreeze_best_model_fcn_resnet50')
    assert rad_scan.lakebreeze_mask.sum() == 714
    assert rad_scan.lakebreeze_mask.shape == (256, 256)

def test_infer_fcn_resnet50_no_augmentation():
    torch.manual_seed(42)
    rad_scan = adam.io.preprocess_radar_image('KLOT', '2025-07-15T18:00:00')
    rad_scan = adam.model.infer_lake_breeze(rad_scan, model_name='lakebreeze_model_fcn_resnet50_no_augmentation')
    assert rad_scan.lakebreeze_mask.sum() == 638
    assert rad_scan.lakebreeze_mask.shape == (256, 256)

def test_infer_fcn_resnet50_batch():
    torch.manual_seed(42)
    rad_scan1 = adam.io.preprocess_radar_image('KLOT', '2025-07-15T18:00:00')
    rad_scan2 = adam.io.preprocess_radar_image('KLOT', '2025-07-15T18:05:00')
    rad_scan = adam.model.infer_lake_breeze_batch(
        [rad_scan1, rad_scan2], model_name='lakebreeze_best_model_fcn_resnet50')
    assert len(rad_scan) == 2
    assert rad_scan[0].lakebreeze_mask.sum() == 676
    assert rad_scan[1].lakebreeze_mask.sum() == 732
    rad_scan = adam.model.infer_lake_breeze_batch(
        [rad_scan1, rad_scan2], model_name='lakebreeze_model_fcn_resnet50_no_augmentation')
    assert len(rad_scan) == 2
    assert rad_scan[0].lakebreeze_mask.sum() == 614
    assert rad_scan[1].lakebreeze_mask.sum() == 961