import numpy as np
import fitsio

infile = 'HyperLeda_meandata_B16_18.csv'
outfile = 'HyperLeda_meandata_B16_18.fits.gz'


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
