from .constants import FOREGROUND_MINRAD_ARCSEC, FOREGROUND_RADIUS_FAC


def make_foreground_geom(fname):
    """
    make a healsparse geometry primitives for the foreground objects (type
    Circle)

    Parameters
    ----------
    fname: str
        Path to the catalog

    Returns
    -------
    list of geometry primitives, in this case all are Circles
    """

    import fitsio
    import healsparse
    from tqdm import tqdm

    data = fitsio.read(fname, lower=True)

    minrad_degrees = FOREGROUND_MINRAD_ARCSEC / 3600

    circles = []
    for objdata in tqdm(data):
        radius_degrees = objdata['rad_avoid'] * FOREGROUND_RADIUS_FAC
        if radius_degrees < minrad_degrees:
            radius_degrees = minrad_degrees

        circle = healsparse.geom.Circle(
            ra=objdata['ra'],
            dec=objdata['dec'],
            radius=radius_degrees,
            # the value is stored as float in the table/file
            value=int(objdata['mask_bit']),
        )
        circles.append(circle)

    return circles
