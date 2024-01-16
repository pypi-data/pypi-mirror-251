from setuptools import setup, find_packages
from io import open

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='tvms',
    version='0.0.27',
    description='Aboubakar',
    long_description=open('README.txt').read()+'\n\n'+open('CHANGELOG.txt').read(),
    url='',
    author='Boo4kin',
    author_email='bkolyabi@gmail.com',
    classifiers=classifiers,
    license='MIT',
    keywords='test',
    include_package_data=True,  # Include data files specified in MANIFEST.in
    package_data={
        '': ['pic/*.jpeg'],  # Include all PNG files in the 'pic' directory
    },
    install_requiers=[''],
    packages= ['tvms']

)
