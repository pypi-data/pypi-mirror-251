from setuptools import setup, find_packages
from pathlib import Path

VERSION = '4.0'
DESCRIPTION = 'Simple library to calculate golden ratio'

this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / 'README.md').read_text()

# Setting up
setup(
    name="gold33423308",
    version=VERSION,
    author="Aliza",
    author_email="<faizata00@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    license='MIT',
    install_requires=[],
    keywords=['golden_ratio', 'golden'],
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
)