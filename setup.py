from setuptools import setup, find_packages
import os

CONFIG_DIR = os.path.join(os.path.expanduser("~"), '.bkm')

setup(
    name='bkm',
    version='0.1',
    license = "MIT",
    author = "Willem van der Jagt",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        bkm=bkm.bkm:cli
    '''
)