"""
TEMPORARY DIAGNOSTIC -- delete with scripts/diagnose_trigger.py.

Dumps the actual model input tensor so it can be compared across pyproj/PROJ
versions. This measures the thing that matters -- the 256x256 image the network
sees -- rather than modelling cartopy's internals and hoping the model is right.

    python scripts/diagnose_render.py out.npy          # dump
    python scripts/diagnose_render.py a.npy b.npy      # compare two dumps
"""

import sys

import numpy as np

SCAN_TIME = '2025-04-24T20:03:23'   # the case whose assertion flips


def dump(path):
    import pyproj

    import adam
    print(f'pyproj {pyproj.__version__} / PROJ {pyproj.proj_version_str}')
    scan = adam.io.preprocess_radar_image('KLOT', SCAN_TIME)
    arr = scan.pytorch_image.detach().numpy()
    np.save(path, arr)
    print(f'saved {path}  shape={arr.shape}  '
          f'min={arr.min():.3f} max={arr.max():.3f} mean={arr.mean():.3f}')


def best_shift(a, b, radius=8):
    """Integer (dy, dx) shift of `b` that best matches `a`, by brute force SSD."""
    best, best_d = None, np.inf
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            bs = np.roll(np.roll(b, dy, axis=0), dx, axis=1)
            c = max(abs(dy), abs(dx))
            inner_a = a[c:a.shape[0] - c or None, c:a.shape[1] - c or None]
            inner_b = bs[c:bs.shape[0] - c or None, c:bs.shape[1] - c or None]
            d = float(np.mean((inner_a - inner_b) ** 2))
            if d < best_d:
                best_d, best = d, (dy, dx)
    return best, best_d


def compare(pa, pb):
    a = np.load(pa)[0]
    b = np.load(pb)[0]
    diff = np.abs(a - b)
    print(f'shape {a.shape}')
    print(f'max |diff|   = {diff.max():.3f}')
    print(f'mean |diff|  = {diff.mean():.3f}')
    frac = float((diff > 1.0).mean())
    print(f'pixels differing by >1.0 : {frac * 100:.2f}%')
    ga, gb = a.mean(axis=0), b.mean(axis=0)     # grey, channel-averaged
    (dy, dx), resid = best_shift(ga, gb)
    base = float(np.mean((ga - gb) ** 2))
    print(f'\nbest integer alignment of B onto A: dy={dy:+d} px, dx={dx:+d} px')
    print(f'  SSD at zero shift = {base:.3f}')
    print(f'  SSD at best shift = {resid:.3f}')
    if (dy, dx) == (0, 0):
        print('  -> no net translation; difference is not a rigid shift')
    else:
        print(f'  -> images are offset by roughly ({dy}, {dx}) pixels')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        dump(sys.argv[1])
    elif len(sys.argv) == 3:
        compare(sys.argv[1], sys.argv[2])
    else:
        print(__doc__)
        sys.exit(2)
