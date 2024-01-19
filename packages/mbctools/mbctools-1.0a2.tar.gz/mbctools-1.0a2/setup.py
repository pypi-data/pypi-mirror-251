import re
from setuptools import setup, find_packages


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('mbctools/mbctools.py').read(),
    re.M
    ).group(1)

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name='mbctools',
    version=version,    
    description='mbctools: A User-Friendly Metabarcoding and Cross-Platform Pipeline for Analyzing Multiple Amplicon Sequencing Data across a Large Diversity of Organisms',
    long_description = long_descr,
    long_description_content_type="text/markdown",
    url='https://github.com/GuilhemSempere/mbctools/blob/dev/mbctools.py',
    author='Christian Barnabe, Guilhem Sempere, Vincent Manzanilla, Etienne Waleckx', 
    author_email='guilhem.sempere@cirad.fr',
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "mbctools = mbctools.__main__:main"
        ]
    },
)