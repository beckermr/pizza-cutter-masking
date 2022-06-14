from .constants import (
    NSIDE, NSIDE_COVERAGE,
)


def geom_to_map(geom_list):
    """
    Create a healsparse map from the input list of geometry primitives

    Parameters
    ----------
    geom_list: [geom]
        E.g. a list of Circle or Polygon

    Returns
    -------
    hmap: healsparse.HealSparseMap
        Has the nside set in constants.py
    """
    import healsparse
    import numpy as np

    hmap = healsparse.HealSparseMap.make_empty(
        nside_coverage=NSIDE_COVERAGE,
        nside_sparse=NSIDE,
        dtype=np.int16,
        sentinel=0,
    )
    healsparse.realize_geom(geom_list, hmap)
    return hmap
