

def mask_lmc(hmap):
    import numpy as np
    from pizza_cutter_masking.constants import (
        LMC_RA_RANGE, LMC_DEC_RANGE,
    )
    vpix, ra, dec = hmap.valid_pixels_pos(return_pixels=True)
    bad, = np.where(
        (ra > LMC_RA_RANGE[0])
        & (ra < LMC_RA_RANGE[1])
        & (dec > LMC_DEC_RANGE[0])
        & (dec < LMC_DEC_RANGE[1])
    )

    hmap[vpix[bad]] = hmap._sentinel
