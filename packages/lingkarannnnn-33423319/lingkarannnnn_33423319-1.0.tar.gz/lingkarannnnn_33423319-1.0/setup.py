from setuptools import setup, find_packages
from pathlib import Path

VERSION = '1.0'
DESCRIPTION = 'luas'

this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / 'README.md').read_text()

# Setting up
setup(
    name="lingkarannnnn_33423319",
    version=VERSION,
    author="iqbal",
    author_email="<rafiiqbal2407@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url='https://github.com/iqbull2244/goldenn.git',
    packages=find_packages(),
    license='MIT',
    install_requires=[],
    keywords=['golden_ratio', 'golden'],
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
)

