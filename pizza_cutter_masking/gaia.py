from .constants import (
    GAIA_VAL, GAIA_RADIUS_FAC, GAIA_MINRAD_ARCSEC, GAIA_MAX_GMAG,
    GAIA_POLY_COEFFS,
)


def make_gaia_geom(fname):
    """
    make a healsparse geometry primitives for gaia stars

    Parameters
    ----------
    fname: str
        Path to the catalog

    Returns
    -------
    list of geometry primitives, in this case all are Circles
    """

    import numpy as np
    import fitsio
    import healsparse
    from tqdm import tqdm

    data = fitsio.read(fname, lower=True)

    ply = np.poly1d(GAIA_POLY_COEFFS)

    circles = []
    for objdata in tqdm(data):
        if objdata['phot_g_mean_mag'] > GAIA_MAX_GMAG:
            continue

        log10_radius_arcsec = ply(objdata['phot_g_mean_mag'])
        radius_arcsec = 10**log10_radius_arcsec * GAIA_RADIUS_FAC
        if radius_arcsec < GAIA_MINRAD_ARCSEC:
            radius_arcsec = GAIA_MINRAD_ARCSEC

        radius_degrees = radius_arcsec / 3600

        circle = healsparse.geom.Circle(
            ra=objdata['ra'],
            dec=objdata['dec'],
            radius=radius_degrees,
            value=GAIA_VAL,
        )
        circles.append(circle)

    return circles
