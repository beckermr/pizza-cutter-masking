from .constants import DES_STARS_RADIUS_ARCSEC, DES_STARS_VAL


def make_des_stars_geom(fname):
    """
    make a healsparse geometry primitives for des stars

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
    w, = np.where(data['mash'] == 0)
    data = data[w]

    radius_degrees = DES_STARS_RADIUS_ARCSEC / 3600

    circles = []
    for objdata in tqdm(data):

        circle = healsparse.geom.Circle(
            ra=objdata['ra'],
            dec=objdata['dec'],
            radius=radius_degrees,
            value=DES_STARS_VAL,
        )
        circles.append(circle)

    return circles
