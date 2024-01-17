from setuptools import setup, find_packages
from pathlib import Path

VERSION = '2.0'
DESCRIPTION = 'Simple library to calculate golden ratio'

this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / 'README.md').read_text()

# Setting up
setup(
    name="gold33423322",
    version=VERSION,
    author="SabillillahX",
    author_email="<sabillillahxtkj@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url='https://github.com/SabillillahX/pipi.git',
    packages=find_packages(),
    license='MIT',
    install_requires=[],
    keywords=['golden_ratio', 'golden'],
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
)