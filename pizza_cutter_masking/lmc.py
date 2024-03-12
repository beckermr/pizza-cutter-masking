

def mask_lmc(hmap):
    import hpgeom as hpg
    from pizza_cutter_masking.constants import (
        LMC_RA_RANGE, LMC_DEC_RANGE,
    )

    lmc_ranges = hpg.query_box(
        hmap.nside_sparse,
        LMC_RA_RANGE[0],
        LMC_RA_RANGE[1],
        LMC_DEC_RANGE[0],
        LMC_DEC_RANGE[1],
        return_pixel_ranges=True,
    )

    hmap[lmc_ranges] = None
