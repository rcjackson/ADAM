"""
TEMPORARY DIAGNOSTIC -- delete once the test_adaptive_scanning regression is understood.

Reproduces the exact sequence of `tests/test_adaptive_scanning.py::
test_trigger_lidar_ppis_from_mask` and reports the intermediate quantities the
test never shows: the mask size, the derived azimuth, and above all the
distance that the assertion actually turns on.

The test asserts a hard binary threshold::

    dist > max_distance (5000 m)  ->  scan not triggered

so knowing whether `dist` lands near 5000 or nowhere near it decides whether
this is a boundary-sensitivity problem or something larger.

Run it twice against different pyproj versions to attribute any movement.
"""

import sys

import numpy as np
import torch

import adam
from adam.util import azimuth_point

# ATMOS, matching the coordinates the tests use.
LIDAR_LAT = 41.70101404798476
LIDAR_LON = -87.99577278662817
MAX_DISTANCE = 5000.0

# (scan time, model, what the test expects of the trigger)
CASES = [
    ('2025-07-15T18:00:00', 'lakebreeze_best_model_fcn_resnet50', False),
    ('2025-04-24T20:03:23', 'lakebreeze_model_fcn_resnet50_no_augmentation', True),
]


def versions():
    import matplotlib
    import pyproj
    mods = {'torch': torch.__version__, 'pyproj': pyproj.__version__,
            'PROJ': pyproj.proj_version_str, 'matplotlib': matplotlib.__version__}
    try:
        import cartopy
        mods['cartopy'] = cartopy.__version__
    except Exception:
        pass
    try:
        import pyart
        mods['pyart'] = pyart.__version__
    except Exception:
        pass
    return '  '.join(f'{k}={v}' for k, v in mods.items())


def main():
    print('=' * 78)
    print('TRIGGER DIAGNOSTIC')
    print(versions())
    print('=' * 78)

    # Mirror the test exactly: one seed, then both inferences in order, so the
    # RNG state entering the second inference matches the test's.
    torch.manual_seed(42)

    for scan_time, model_name, expected_trigger in CASES:
        print(f'\n--- {scan_time}  |  {model_name}')
        print(f'    test expects trigger={expected_trigger} '
              f'(i.e. dist {"<" if expected_trigger else ">"} {MAX_DISTANCE:.0f} m)')
        try:
            scan = adam.io.preprocess_radar_image('KLOT', scan_time)
            scan = adam.model.infer_lake_breeze(scan, model_name=model_name)
            mask = scan.lakebreeze_mask
            n = int(np.asarray(mask).sum())
            print(f'    mask pixels      : {n}')
            if n == 0:
                print('    mask is EMPTY -> azimuth_point cannot produce a centroid')
                continue
            angle, lat, lon, dist = azimuth_point(LIDAR_LON, LIDAR_LAT, scan)
            actual = bool(dist <= MAX_DISTANCE)
            margin = dist - MAX_DISTANCE
            print(f'    centroid lat/lon : {lat:.5f}, {lon:.5f}')
            print(f'    azimuth          : {angle:.3f} deg')
            print(f'    dist             : {dist:.1f} m')
            print(f'    margin vs 5000   : {margin:+.1f} m '
                  f'({"INSIDE" if actual else "OUTSIDE"} threshold)')
            print(f'    would trigger    : {actual}   '
                  f'{"MATCHES test" if actual == expected_trigger else "*** CONTRADICTS test ***"}')
        except Exception as exc:  # keep going so we see every case
            print(f'    RAISED {type(exc).__name__}: {exc}')

    print('\n' + '=' * 78)
    return 0


if __name__ == '__main__':
    sys.exit(main())
