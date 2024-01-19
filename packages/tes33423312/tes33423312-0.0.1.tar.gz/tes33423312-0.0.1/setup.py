from setuptools import setup, find_packages
from pathlib import Path

VERSION = '0.0.1'
DESCRIPTION = 'tes33423312'

this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / 'README.md').read_text()

# Setting up
setup(
    name="tes33423312",
    version=VERSION,
    author=" ",
    author_email=" ",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=' ',
    packages=find_packages(),
    license='MIT',
    install_requires=[],
    keywords=['luas', 'lingkaran'],
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
)