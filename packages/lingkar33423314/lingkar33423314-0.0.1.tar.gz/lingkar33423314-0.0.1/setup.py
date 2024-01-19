from setuptools import setup, find_packages
from pathlib import Path

VERSION = '0.0.1'
DESCRIPTION = 'Library Python sederhana untuk menghitung luas lingkaran.'

this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / 'README.md').read_text()

# Setting up
setup(
    name="lingkar33423314",
    version=VERSION,
    author="Hassan",
    author_email="<mhnzayyan@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url='',
    packages=find_packages(),
    license='MIT',
    install_requires=[],
    keywords=['luas','lingkaran'],
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
)
