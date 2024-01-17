import pathlib
from typing import Dict, List
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '1.0'
PACKAGE_NAME = 'altair_easeviz'
AUTHOR = 'Miguel Huayllas'
AUTHOR_EMAIL = 'mhuaylch10@alumnes.ub.edu'
URL = 'https://miguelub.github.io/altair-easeviz/'
SOURCE ='https://github.com/MiguelUB/altair-easeviz'

LICENSE = 'MIT'  # Tipo de licencia
DESCRIPTION = 'Accesible themes and functions to create accessible graph for Altair'
LONG_DESCRIPTION = (HERE / "README.md").read_text(
    encoding='utf-8')
LONG_DESC_TYPE = "text/markdown"


ENTRY_POINTS: Dict[str, List[str]] = {
    "altair.vegalite.v5.theme": [
        "accessible_theme = altair_easeviz.themes:accessible_theme",
        "dark_accessible_theme = altair_easeviz.themes:dark_accessible_theme",
        "filler_pattern_theme = altair_easeviz.themes:filler_pattern_theme",
        "print_theme = altair_easeviz.themes:print_friendly_theme",
    ],
}
DEPENDENCIES: List[str] = ["altair==5.*", "typing-extensions>=4.0, <5", "jinja2==3.*", "pyRserve>=1.0"]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    source=SOURCE,
    install_requires=DEPENDENCIES,
    entry_points=ENTRY_POINTS,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)
