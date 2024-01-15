from io import open
from setuptools import setup

version = '0.0.27'

setup(
    name = 'tver',
    version=version,

    author='tak0ysebe',
    author_email='ffmarkov@yandex.ru',

    license='Free' ,

    include_package_data=True,  # Include data files specified in MANIFEST.in
    
    package_data={
        '': ['pic/*.jpeg'],  # Include all PNG files in the 'pic' directory
    },
    
    packages= ['tver']
)
