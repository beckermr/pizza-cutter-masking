

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

    circles = []
    for objdata in tqdm(data):
        circle = healsparse.geom.Circle(
            ra=objdata['ra'],
            dec=objdata['dec'],
            radius=objdata['rad_avoid'],
            # the value is stored as float in the table/file
            value=int(objdata['mask_bit']),
        )
        circles.append(circle)

    return circles
