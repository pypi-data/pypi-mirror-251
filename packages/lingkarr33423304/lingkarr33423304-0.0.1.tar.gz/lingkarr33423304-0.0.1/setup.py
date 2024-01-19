from setuptools import setup, find_packages
from pathlib import Path

VERSION = '0.0.1'
DESCRIPTION = 'Luas Lingkaran'

this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / 'README.md').read_text()

# Setting up
setup(
    name="lingkarr33423304",
    version=VERSION,
    author="shaaa",
    author_email="<ayeshacha177@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url='',
    packages=find_packages(),
    license='MIT',
    install_requires=[],
    keywords=['Luas lingkaran'],
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
)
