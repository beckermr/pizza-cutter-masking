select
    g.ra, g.dec, g.phot_g_mean_mag
from
    gaia_dr2 g
where exists
    (
      select
          1
      from
          carnero.Y6A2_FOOTPRINT_GRIZ_N2_V2 f
      where
          f.hpix_4096=g.hpix_4096
          and f.frac_det_griz > 0.
    );


