
import pathlib

from setuptools import setup

from pyumldiagrams import __version__

# The directory containing this file
HERE = pathlib.Path(__file__).parent

README  = (HERE / "README.md").read_text()
LICENSE = (HERE / 'LICENSE').read_text()

setup(
    name='pyumldiagrams',
    version=__version__,
    author='Humberto A. Sanchez II',
    author_email='humberto.a.sanchez.ii@gmail.com',
    maintainer='Humberto A. Sanchez II',
    maintainer_email='humberto.a.sanchez.ii@gmail.com',
    description='Draw UML diagrams in various formats',
    long_description = README,
    long_description_content_type='text/markdown',
    license=LICENSE,
    url='https://github.com/hasii2011/pyumldiagrams',
    packages=[
        'pyumldiagrams',
        'pyumldiagrams.image', 'pyumldiagrams.image.resources',
        'pyumldiagrams.pdf',   'pyumldiagrams.pdf.resources',
        'pyumldiagrams.xmlsupport'
    ],
    package_data={
        'pyumldiagrams':                 ['py.typed'],
        'pyumldiagrams.image.resources': ['py.typed'],
        'pyumldiagrams.image':           ['py.typed'],
        'pyumldiagrams.pdf':             ['py.typed'],
        'pyumldiagrams.pdf.resources':   ['py.typed'],
        'pyumldiagrams.xmlsupport':      ['py.typed'],
    },
    install_requires=['fpdf2==2.7.5', 'Pillow==10.0.1', 'untangle==1.2.1', 'codeallybasic>=1.1.0', 'codeallyadvanced>=1.1.0']
)
