from .constants import (
    HYPERLEDA_VAL, HYPERLEDA_RADIUS_FAC,
)
from .maps import geom_to_map


def make_hyperleda_geom(fname):
    """
    make a healsparse geometry primitives for hyperleda (type Circle), trimming
    to the DES area

    Parameters
    ----------
    fname: str
        Path to the catalog

    Returns
    -------
    list of geometry primitives, in this case all are Circles
    """

    import healsparse
    from tqdm import tqdm
    from esutil.numpy_util import between

    data = _read_hyperleda_catalog(fname)

    circles = []
    for objdata in tqdm(data):
        ra = objdata['raj2000']
        dec = objdata['dej2000']

        # skip objects in LMC area with huge radii
        if between(ra, 73, 89) and between(dec, -72, -67.6):
            continue

        if between(ra, 9.5, 17.5) and between(dec, -74, -71):
            continue

        # otherwise keep a superset of the DES area
        if between(dec, -75, 10) and (
            between(ra, 0, 120) or
            between(ra, 295, 360)
        ):

            circle = healsparse.geom.Circle(
                ra=objdata['raj2000'],
                dec=objdata['dej2000'],
                radius=objdata['radius_degrees'] * HYPERLEDA_RADIUS_FAC,
                value=HYPERLEDA_VAL,
            )
            circles.append(circle)

    return circles


def make_hyperleda_map(
    fname,
    output,
):
    """
    make and write a healsparse map for hyperleda, trimming to the DES area

    Parameters
    ----------
    fname: str
        Path to the catalog
    output: str
        Output file path
    """
    circles = make_hyperleda_geom(fname)
    hmap = geom_to_map(circles)
    print('writing:', output)
    hmap.write(output, clobber=True)


def _read_hyperleda_catalog(fname):
    import numpy as np
    import fitsio
    import esutil as eu

    data = fitsio.read(fname, lower=True)

    # logd25 is log(radius/0.1 arcmin)

    w, = np.where(np.isfinite(data['logd25']))
    data = data[w]

    diameter_arcmin = 0.1 * 10**data['logd25']
    # diameter_arcmin = 0.1 * np.exp(data['logd25'])

    radius_degrees = (diameter_arcmin / 2) / 60

    dt = [('radius_degrees', 'f8')]
    output = eu.numpy_util.add_fields(data, dt)

    output['radius_degrees'] = radius_degrees

    return output
