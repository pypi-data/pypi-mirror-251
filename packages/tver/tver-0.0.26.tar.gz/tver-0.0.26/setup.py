from io import open
from setuptools import setup

version = '0.0.26'

setup(
    name = 'tver',
    version=version,

    author='tak0ysebe',
    author_email='ffmarkov@yandex.ru',

    license='Free' ,

    include_package_data=True,  # Include data files specified in MANIFEST.in
    
    package_data={
        '': ['pic/*.png'],  # Include all PNG files in the 'pic' directory
    },
    
    packages= ['tver']
)
