import os
from glob import glob
from setuptools import setup, find_packages

__version__ = None

pth = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "pizza_cutter_masking",
    "version.py"
)
with open(pth, 'r') as fp:
    exec(fp.read())

scripts = glob('bin/*')
scripts = [s for s in scripts if '~' not in s]

setup(
    name="pizza-cutter-masking",
    author="Erin Sheldon, Matt Becker",
    url="https://github.com/beckermr/pizza-cutter-masking",
    description="make healsparse maps for DES Y6 pizza cutter/metadetect",
    packages=find_packages(),
    scripts=scripts,
    version=__version__,
)
