# pizza-cutter-masking
mask making codes for pizza-cutter

Examples
--------
```bash
# make the foregound/gaia/des stars/hyperleda mask
pcm-make-mask \
    --hyperleda hyperleda_B16_18.fits.gz \
    --foreground foreground-v2.fits \
    --gaia gaia.fits \
    --des-stars gold_2_0_r_lt_21_summary.fit \
    --output hleda-foreground-v2-gaia-des-stars-hsmap16384.fits

# make the combined map from the metadetect healsparse files
pcm-make-mdet-mask \
    --flist $(find /gpfs02/astro/workarea/beckermr/des-y6-analysis/2022_04_21_run_mdet_final_v2/data_final_nogcut/ -name "*.hs") \
    --output mdet-16384-v1.fits

# combine all masks
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
