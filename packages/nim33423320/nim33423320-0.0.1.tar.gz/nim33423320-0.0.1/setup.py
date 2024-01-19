from setuptools import setup, find_packages
from pathlib import Path

VERSION = '0.0.1'
DESCRIPTION = 'Golden Ratio'

this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / 'README.md').read_text()

setup(
    name="nim33423320",
    version=VERSION,
    author="rizalfarhann",
    author_email="rizalfarhannanda@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url='https://github.com/rizalfarhan',
    packages=find_packages(),
    license='MIT',
    install_requires=[],
    keywords=['Hello'],
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
)