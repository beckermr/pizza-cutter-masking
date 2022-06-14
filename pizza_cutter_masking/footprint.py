from .constants import NSIDE_COVERAGE, FOOTPRINT_VAL


def convert_to_healsparse():
    import healsparse as hsp
    import fitsio

    nside = 4096

    infile = f'footprint-{nside}.fits.gz'
    outfile = f'footprint-hsmap{nside}.fits'

    print('reading original footprint:', infile)
    data = fitsio.read(infile, lower=True)

    hsp_map = hsp.HealSparseMap.make_empty(
        nside_coverage=NSIDE_COVERAGE,
        nside_sparse=nside,
        dtype='i2',
    )
    hsp_map[data['hpix_4096']] = FOOTPRINT_VAL

    print('writing:', outfile)
    hsp_map.write(outfile, clobber=True)
