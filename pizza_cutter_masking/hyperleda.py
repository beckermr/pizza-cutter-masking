from .constants import (
    HYPERLEDA_VAL,
    # HYPERLEDA_RADIUS_FAC,
)
# from .maps import geom_to_map


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
    import fitsio

    print('reading hyperleda:', fname)
    data = fitsio.read(fname, lower=True)

    circles = []
    for objdata in tqdm(data):
        bmag = objdata['bt']
        ra = objdata['ra']
        dec = objdata['dec']

        # keep a superset of the DES area
        if between(dec, -75, 10) and (
            between(ra, 0, 120) or
            between(ra, 295, 360)
        ):

            radius = get_hyperleda_radius(bmag)
            if radius > 0:

                circle = healsparse.geom.Circle(
                    ra=ra,
                    dec=dec,
                    radius=radius,
                    value=HYPERLEDA_VAL,
                )
                circles.append(circle)

    return circles


def get_hyperleda_radius(bmag):
    """
    Get the hyperleda radius in degrees

    Parameters
    ----------
    bmag: float
        The magnitude in B

    Returns
    -------
    radius in degrees
    """
    slope = -0.00824
    offset = 0.147
    return offset + slope * bmag


def convert_hyperleda_to_fits():
    import numpy as np
    import fitsio

    infile = 'hyperLeda_B16_18.csv'
    outfile = 'hyperLeda_B16_18.fits.gz'

    data = []
    namelen = -1
    typelen = -1

    print('reading from:', infile)
    with open(infile) as fobj:
        for line in fobj:
            if line[0] == '#':
                continue
            ls = line.split(',')
            if ls[0] == 'pgc':
                continue

            d = {}
            d['pgc'] = int(ls[0])
            d['objname'] = ls[1]
            d['objtype'] = ls[2]
            d['ra'] = float(ls[3])
            d['dec'] = float(ls[4])
            d['bt'] = float(ls[5])
            d['bterr'] = float(ls[6])

            namelen = max(namelen, len(d['objname']))
            typelen = max(typelen, len(d['objtype']))
            data.append(d)

    dt = [
        ('pgc', 'i4'),
        ('objname', f'U{namelen}'),
        ('objtype', f'U{typelen}'),
        ('ra', 'f8'),
        ('dec', 'f8'),
        ('bt', 'f4'),
        ('bterr', 'f4'),
    ]

    outdata = np.zeros(len(data), dtype=dt)
    for od, d in zip(outdata, data):
        for n in od.dtype.names:
            od[n] = d[n]

    print('writing:', outfile)
    fitsio.write(outfile, outdata, clobber=True)


def fit_hyperleda_radius_relation():
    import numpy as np
    import fitsio
    import esutil as eu
    from espy import fitting

    import matplotlib.pyplot as mplt

    data = fitsio.read('leda_ra_dec_radii.fits', lower=True)

    bs = eu.stat.Binner(data['bt'], data['rad_avoid'])
    bs.dohist(min=15, max=17, nperbin=550, rev=True)

    w, = np.where(bs['hist'] > 0)
    lf = fitting.fit_line(bs['xmean'][w], bs['ymean'][w])

    print(lf)
    res = lf.get_result()
    slope = res['pars'][0]
    offset = res['pars'][1]

    fig, ax = mplt.subplots()

    ax.set(
        xlabel='B',
        ylabel='radius [degrees]',
    )
    ax.errorbar(
        bs['xmean'][w], bs['ymean'][w], bs['yerr'][w], ls='', marker='o',
    )

    xvals = np.linspace(bs['xmean'][w[0]], 18)
    yvals = offset + slope * xvals

    ax.plot(xvals, yvals)

    mplt.savefig('fit-hleda-radius.pdf')


# def make_hyperleda_map(
#     fname,
#     output,
# ):
#     """
#     make and write a healsparse map for hyperleda, trimming to the DES area
#
#     Parameters
#     ----------
#     fname: str
#         Path to the catalog
#     output: str
#         Output file path
#     """
#     circles = make_hyperleda_geom(fname)
#     hmap = geom_to_map(circles)
#     print('writing:', output)
#     hmap.write(output, clobber=True)
#
#
# def _read_hyperleda_catalog(fname):
#     import numpy as np
#     import fitsio
#     import esutil as eu
#
#     data = fitsio.read(fname, lower=True)
#
#     # logd25 is log(radius/0.1 arcmin)
#
#     w, = np.where(np.isfinite(data['logd25']))
#     data = data[w]
#
#     diameter_arcmin = 0.1 * 10**data['logd25']
#     # diameter_arcmin = 0.1 * np.exp(data['logd25'])
#
#     radius_degrees = (diameter_arcmin / 2) / 60
#
#     dt = [('radius_degrees', 'f8')]
#     output = eu.numpy_util.add_fields(data, dt)
#
#     output['radius_degrees'] = radius_degrees
#
#     return output
