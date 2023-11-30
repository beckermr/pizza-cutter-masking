from .constants import (
    NSIDE, NSIDE_COVERAGE,
)


def geom_to_map(geom_list, nside, use_bool=False):
    """
    Create a healsparse map from the input list of geometry primitives

    Parameters
    ----------
    geom_list: [geom]
        E.g. a list of Circle or Polygon
    nside : `int`
        Healpix nside of the map.
    use_bool : `boolean`, optional
        Use a boolean bit-packed mask?

    Returns
    -------
    hmap: healsparse.HealSparseMap
        Has the nside set in constants.py
    """
    import healsparse
    import numpy as np
    from tqdm import tqdm

    if nside is None:
        nside = NSIDE

    if use_bool:
        dtype = bool
        bit_packed = True
        sentinel = False
    else:
        dtype = np.int16
        bit_packed = False
        sentinel = 0

    hmap = healsparse.HealSparseMap.make_empty(
        nside_coverage=NSIDE_COVERAGE,
        nside_sparse=nside,
        dtype=dtype,
        sentinel=sentinel,
        bit_packed=bit_packed,
    )

    for g in tqdm(geom_list):
        pixels = g.get_pixels(nside=nside)
        if use_bool:
            hmap[pixels] = True
        else:
            hmap[pixels] |= g.value

    return hmap
