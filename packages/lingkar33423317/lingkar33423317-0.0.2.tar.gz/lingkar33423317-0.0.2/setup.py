from setuptools import setup, find_packages
from pathlib import Path

VERSION = '0.0.2'
DESCRIPTION = 'Simple library to calculate lingkaran'

this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / 'README.md').read_text()

# Setting up
setup(
    name="lingkar33423317",
    version=VERSION,
    author="nihlah",
    author_email="<mutiaranihlah@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url='',
    packages=find_packages(),
    license='MIT',
    install_requires=[],
    keywords=['lingkaran', 'luas_lingkaran', 'luas'],
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
)