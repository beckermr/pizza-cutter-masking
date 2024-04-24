# pizza-cutter-masking
mask making codes for pizza-cutter

Making High Resolution mask
============================

This requires a moderately high memory machine.  Using bit-packed boolean masks
from healsparse 1.8 (along with a memory leak fixed in hpgeom 1.1.1) means that
even a moderate memory machine (18 Gb peak usage) can run these at high
resolution.

These were the commands used:

```bash
dir=/nfs/slac/des/fs1/g/sims/esheldon/hsfiles
mdmask=metadetect-v10_mdetcat_consolidated_healsparse-mask.hsp
pcm-make-mdet-mask \
    --use-bool \
    --nside 131072 \
    --flist $(find $dir -name "*.hs" | sort) \
    --output $mdmask

fintermediate=hleda-foreground-gaia-des-stars-hsmap131k-v1.hsp
pcm-make-mask \
    --nside 131072 \
    --hyperleda hyperleda_B16_18.fits.gz \
    --foreground foreground-v2.fits \
    --gaia gaia.fits \
    --des-stars gold_2_0_r_lt_21_summary.fit \
    --output $fintermediate \
    --use-bool

fmdet=y6-combined-hleda-gaiafull-des-stars-hsmap131k-mdet-v2.hsp
pcm-make-combined \
    --use-bool \
    --nside 131072 \
    --mask $fintermediate \
    --metadetect $mdmask \
    --output $fmdet

pcm-make-fracdet \
    --nside 16384 \
    --combined $fmdet \
    --output y6-combined-hleda-gaiafull-des-stars-hsmap131k-mdet-v2-fracdet-16k.hsp

pcm-make-fracdet \
    --nside 4096 \
    --combined $fmdet \
    --output y6-combined-hleda-gaiafull-des-stars-hsmap131k-mdet-v2-fracdet-4k.hsp

pcm-add-extra-masks \
    --extra-mask-config-json scripts/hleda_extra_mask_config_v1.json \
    --input-mask y6-combined-hleda-gaiafull-des-stars-hsmap131k-mdet-v2.hsp \
    --output-mask y6-combined-hleda-gaiafull-des-stars-hsmap131k-mdet-extra-masks-v2.hsp \
    --output-masked-pixels y6-extra-masks-pixels-v2-16k.hsp
```

Examples applying masks
```python
import healsparse as hsp

hmap = hsp.HealSparseMap.read('y6-combined-hleda-gaiafull-des-stars-hsmap16384-mdet-v2.fits')

# the map has value 1 for "good" pixels.  But it is simpler
# use the valid_mask check for positions
ok = metadetect.get_values_pos(ra, dec, lonlat=True, valid_mask=True)
fig, ax = mplt.subplots()
ax.scatter(ra, dec, c='black')
ax.scatter(ra[ok], dec[ok], c='red')
mplt.show()
```

Other Examples making masks
----------------------------
```bash
# make the foregound/gaia/des stars/hyperleda mask
# this mask has value zero for "good" pixels
#   vals = metadetect_mask.get_values_pos(ra, dec, lonlat=True)
#   mask_ok = (vals == 0)
pcm-make-mask \
    --hyperleda hyperleda_B16_18.fits.gz \
    --foreground foreground-v2.fits \
    --gaia gaia.fits \
    --des-stars gold_2_0_r_lt_21_summary.fit \
    --output hleda-foreground-v2-gaia-des-stars-hsmap16384.fits

# make the combined map from the metadetect healsparse files
# good pixels can be check for valid_mask=True
# mdet_ok = metadetect_mask.get_values_pos(ra, dec, lonlat=True, valid_mask=True)
pcm-make-mdet-mask \
    --flist $(find /gpfs02/astro/workarea/beckermr/des-y6-analysis/2022_04_21_run_mdet_final_v2/data_final_nogcut/ -name "*.hs") \
    --output mdet-16384-v1.fits

# combine all masks including the footprint mask, for example the one here
# https://cdcvs.fnal.gov/redmine/projects/des-y6/wiki/Y6A2_Gold_footprint
# good values in the combined mask can be found using a valid_mask check,
# see section below on applying masks
pcm-make-combined \
    --mask hleda-foreground-v2-gaia-des-stars-hsmap16384.fits \
    --footprint footprint-hsmap4096.fits \
    --metadetect mdet-16384-v1.fits \
    --output y6-combined-hleda-gaiafull-des-stars-hsmap16384-mdet-v2.fits

# combine without metadetect
pcm-make-combined \
    --mask hleda-foreground-v2-gaia-des-stars-hsmap16384.fits \
    --footprint footprint-hsmap4096.fits \
    --output y6-combined-hleda-gaiafull-des-stars-hsmap16384-nomdet-v2.fits

# visualize the map
pcm-plot-mask y6-combined-hleda-gaiafull-des-stars-hsmap16384-nomdet-v2.fits
```
