def apply_masks(ra, dec, footprint=None, mask=None, metadetect=None):
    """
    Get the indices that are within the footprint and not masked by the mask.
    Optionally check the metadetect mask as well

    Parameters
    ----------
    ra: number/array
        The right ascension in degrees
    dec: number/array
        The decliiatioj in degrees
    footprint: HealSparseMap, optional
        The healsparse map for the footprint
    mask: HealSparseMap, optional
        The healsparse map for the mask
    metadetect: HealSparseMap, optional
        The optional healsparse map for the metadetect footprint

    Returns
    -------
    keep: array
        Indices for objects in the footprint(s) and not masked
    """
    import numpy as np

    logic = np.ones(ra.size, dtype=bool)

    if not any((footprint, mask, metadetect)):
        raise RuntimeError('send at least one footprint or mask')

    if footprint is not None:
        footprint_ok = footprint.get_values_pos(
            ra, dec, lonlat=True, valid_mask=True,
        )
        logic &= footprint_ok

    if mask is not None:
        mask_vals = mask.get_values_pos(ra, dec, lonlat=True)
        logic &= (mask_vals == 0)

    if metadetect is not None:
        mdet_ok = metadetect.get_values_pos(
            ra, dec, lonlat=True, valid_mask=True,
        )
        logic &= mdet_ok

    keep, = np.where(logic)
    return keep
