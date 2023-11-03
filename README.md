# pizza-cutter-masking
mask making codes for pizza-cutter

Examples making masks
---------------------
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

Running for High Resolution on a big memory machine
===================================================
dir=/nfs/slac/des/fs1/g/sims/esheldon/hsfiles
pcm-make-mdet-mask --use-bool --nside 131072 --flist $(find $dir -name "*.hs" | sort) --output metadetect-v10_mdetcat_consolidated_healsparse-mask.parquet.hs --use-parquet

fintermediate=hleda-foreground-gaia-des-stars-hsmap131k-v1.parquet
pcm-make-mask \
    --nside 131072 \
    --hyperleda hyperleda_B16_18.fits.gz \
    --foreground foreground-v2.fits \
    --gaia gaia.fits \
    --des-stars gold_2_0_r_lt_21_summary.fit \
    --output $fintermediate \
    --use-parquet

fmdet=y6-combined-hleda-gaiafull-des-stars-hsmap131k-mdet-v1.parquet
pcm-make-combined \
    --use-bool \
    --nside 131072 \
    --mask $fintermediate \
    --footprint footprint-hsmap4096.fits \
    --metadetect metadetect-v10_mdetcat_consolidated_healsparse-mask.parquet.hs \
    --output $fmdet \
    --use-parquet

pcm-make-fracdet \
    --nside 16384 \
    --combined y6-combined-hleda-gaiafull-des-stars-hsmap131k-mdet-v1.parquet \
    --output y6-combined-hleda-gaiafull-des-stars-hsmap131k-mdet-v1-fracdet-16k.hsp

pcm-make-fracdet \
    --nside 4096 \
    --combined y6-combined-hleda-gaiafull-des-stars-hsmap131k-mdet-v1.parquet \
    --output y6-combined-hleda-gaiafull-des-stars-hsmap131k-mdet-v1-fracdet-4k.hsp
