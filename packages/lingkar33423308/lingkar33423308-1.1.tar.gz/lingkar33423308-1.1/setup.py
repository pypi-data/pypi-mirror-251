from setuptools import setup, find_packages
from pathlib import Path

VERSION = '1.1'
DESCRIPTION = 'Menghitung luas lingkaran'

this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / 'README.md').read_text()

# Setting up
setup(
    name="lingkar33423308",
    version=VERSION,
    author="Aliza",
    author_email="<faizata00@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    license='MIT',
    install_requires=[],
    keywords=['luas', 'lingkaran'],
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
)