from setuptools import setup, find_packages
from pathlib import Path

VERSION = '1.0'
DESCRIPTION = 'hitung luas lingkaran'

this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / 'README.md').read_text()

# Setting up
setup(
    name="lingkar33423319",
    version=VERSION,
    author="iqbal",
    author_email="<rafiiqbal2407@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url='https://github.com/iqbull2244/lingkaran.git',
    packages=find_packages(),
    license='MIT',
    install_requires=[],
    keywords=['lingkaran', 'luas'],
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
)
