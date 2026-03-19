import numpy as np
import os

def test_make_scan_file():
    from adam.triggering.halo_lidar import make_scan_file
    from adam.testing import TEST_RHI_FILE, TEST_PPI_FILE
    elevations = [0, 90]
    azimuths = [90]
    out_file_name = 'test_scan_rhi.txt'
    make_scan_file(elevations, azimuths, el_speed=2, out_file_name=out_file_name)
    
    with open(out_file_name, 'r') as f:
        lines = f.readlines()
    with open(TEST_RHI_FILE, 'r') as f:
        expected_lines = f.readlines()

    assert len(lines) == len(expected_lines)
    for i, (line, expected_line) in enumerate(zip(lines, expected_lines)):
        assert line == expected_line, f"Line {i} does not match expected output.\nGot: {line}\nExpected: {expected_line}"

    elevations = [0, 5, 10]
    azimuths = [90, 180]    
    out_file_name = 'test_scan_ppi.txt'
    make_scan_file(elevations, azimuths, el_speed=2, out_file_name=out_file_name)
    
    with open(out_file_name, 'r') as f:
        lines = f.readlines()
    with open(TEST_PPI_FILE, 'r') as f:
        expected_lines = f.readlines()

    assert len(lines) == len(expected_lines)
    for i, (line, expected_line) in enumerate(zip(lines, expected_lines)):
        assert line == expected_line, f"Line {i} does not match expected output.\nGot: {line}\nExpected: {expected_line}"

def test_send_scan():
    from adam.triggering.halo_lidar import send_scan
    from adam.testing import TEST_RHI_FILE
    from adam.testing.fake_lidar import FakeSSHClient
    lidar_ip_addr = None
    lidar_uname = None
    lidar_pwd = None
    in_file_name = TEST_RHI_FILE
    out_file_name = 'test_rhi_scan.txt'
    out_file_name2 = 'test_rhi_scan_copy.txt'
    with FakeSSHClient() as client:
        send_scan(in_file_name, lidar_ip_addr, lidar_uname, lidar_pwd, out_file_name=out_file_name,
                  client=client)
        with open(client.sftp.files[0], 'r') as f:
            lines = f.readlines()
        with open(TEST_RHI_FILE, 'r') as f:
            expected_lines = f.readlines()
        assert len(lines) == len(expected_lines)
        for i, (line, expected_line) in enumerate(zip(lines, expected_lines)):
            assert line == expected_line, f"Line {i} does not match expected output.\nGot: {line}\nExpected: {expected_line}"

def test_trigger_lidar_ppis_from_mask():
    import torch
    import adam
    torch.manual_seed(42)
    rad_scan = adam.io.preprocess_radar_image('KLOT', '2025-07-15T18:00:00')
    rad_scan = adam.model.infer_lake_breeze(
        rad_scan, model_name='lakebreeze_best_model_fcn_resnet50')
    result = adam.triggering.trigger_lidar_ppis_from_mask(rad_scan, 41.70101404798476, -87.99577278662817,
                                                  None, None, None, elevations=[0, 5, 10], az_width=30.,  
                                                  out_file_name='test_scan_ppi_lakebreeze.txt', dyn_csm=False)
    assert result is False, "Expected the scan to not be triggered due to distance from lidar to lake breeze region being greater than max_distance."

    rad_scan = adam.io.preprocess_radar_image('KLOT', '2025-04-24T20:03:23')
    rad_scan = adam.model.infer_lake_breeze(
        rad_scan, model_name='lakebreeze_model_fcn_resnet50_no_augmentation')
    with adam.testing.FakeSSHClient() as client:
        result = adam.triggering.trigger_lidar_ppis_from_mask(
            rad_scan, 41.70101404798476, -87.99577278662817,
            None, None, None, elevations=[0, 5, 10], az_width=30., 
            out_file_name='test_scan_ppi_lakebreeze_close.txt', dyn_csm=False, client=client)
        assert result is True, "Expected the scan to be triggered since the distance from lidar to lake breeze region is less than max_distance."
        client.sftp.get(client.sftp.files[0], 'test_scan_ppi_lakebreeze_close_copy.txt')
        with open('test_scan_ppi_lakebreeze_close_copy.txt', 'r') as f:
            lines = f.readlines()
        with open(adam.testing.TEST_PPI_TRIGGERED_SCAN, 'r') as f:
            expected_lines = f.readlines()
        assert len(lines) == len(expected_lines)
        for i, (line, expected_line) in enumerate(zip(lines, expected_lines)):
            assert line == expected_line, f"Line {i} does not match expected output.\nGot: {line}\nExpected: {expected_line}"
    os.remove('test_scan_ppi_lakebreeze_close_copy.txt')
    os.remove('test_scan_ppi_lakebreeze_close.txt')
    os.remove('test_scan_ppi.txt')

def test_trigger_lidar_rhi_from_mask():
    import torch
    import adam
    torch.manual_seed(42)
    rad_scan = adam.io.preprocess_radar_image('KLOT', '2025-07-15T18:00:00')
    rad_scan = adam.model.infer_lake_breeze(
        rad_scan, model_name='lakebreeze_best_model_fcn_resnet50')
    result = adam.triggering.trigger_lidar_rhi_from_mask(rad_scan, 41.70101404798476, -87.99577278662817,
                                                  None, None, None, elevations=[0, 45],   
                                                  out_file_name='test_scan_rhi_lakebreeze.txt', dyn_csm=False)
    assert result is False, "Expected the scan to not be triggered due to distance from lidar to lake breeze region being greater than max_distance."
    rad_scan = adam.io.preprocess_radar_image('KLOT', '2025-04-24T20:03:23')
    rad_scan = adam.model.infer_lake_breeze(
        rad_scan, model_name='lakebreeze_model_fcn_resnet50_no_augmentation')
    with adam.testing.FakeSSHClient() as client:
        result = adam.triggering.trigger_lidar_rhi_from_mask(rad_scan, 41.70101404798476, -87.99577278662817,
                                                  None, None, None, elevations=[0, 45],   
                                                  out_file_name='test_scan_rhi_lakebreeze.txt', dyn_csm=False, client=client)
        assert result is True, "Expected the scan to be triggered since the distance from lidar to lake breeze region" \
             " is less than max_distance."
        client.sftp.get(client.sftp.files[0], 'test_scan_rhi_lakebreeze_copy.txt')
        with open('test_scan_rhi_lakebreeze_copy.txt', 'r') as f:
            lines = f.readlines()
        with open(adam.testing.TEST_RHI_TRIGGERED_SCAN, 'r') as f:
            expected_lines = f.readlines()
        assert len(lines) == len(expected_lines)
        for i, (line, expected_line) in enumerate(zip(lines, expected_lines)):
            assert line == expected_line, f"Line {i} does not match expected output.\nGot: {line}\nExpected: {expected_line}"
    os.remove('test_scan_rhi_lakebreeze_copy.txt')
    os.remove('test_scan_rhi_lakebreeze.txt')
    os.remove('test_scan_rhi.txt')
