from io import open
from setuptools import setup

version = '0.0.1'

setup(
    name = 'terv',
    version=version,

    author='Boo4kin',
    author_email='bkolyabi@gmail.com',

    license='Free' ,

    include_package_data=True,  # Include data files specified in MANIFEST.in
    
    package_data={
        '': ['pic/*.png'],  # Include all PNG files in the 'pic' directory
    },
    
    packages= ['terv']
)

