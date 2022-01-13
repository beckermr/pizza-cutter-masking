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
        footprint_vals = footprint.get_values_pos(ra, dec, lonlat=True)
        logic &= (footprint_vals == 1)

    if mask is not None:
        mask_vals = mask.get_values_pos(ra, dec, lonlat=True)
        logic &= (mask_vals == 0)

    if metadetect is not None:
        mdet_vals = metadetect.get_values_pos(ra, dec, lonlat=True)
        logic &= (mdet_vals == 1)

    keep, = np.where(logic)
    return keep
