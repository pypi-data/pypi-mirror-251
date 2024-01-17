from pathlib import Path
from setuptools import setup, find_packages
from typing import List

def get_install_requires(filepath=None):
    if filepath is None:
        filepath = "./"
    """Returns requirements.txt parsed to a list"""
    fname = Path(filepath).parent / 'requirements.txt'
    targets = []
    if fname.exists():
        with open(fname, 'r') as f:
            targets = f.read().splitlines()
    return targets

def get_links():
    return [
        #"git+https://github.com/bacelii/machine_learning_tools.git"
    ]
    
    


def get_long_description(filepath='README.md'):
    try:
        import pypandoc
    except:
        raise Exception("Need to install pypandoc (and if havent done so install apt-get install pandoc)")
        
    long_description = pypandoc.convert_file(filepath, 'rst')        
    return long_description


setup(
    name='datasci_stdlib_tools', # the name of the package, which can be different than the folder when using pip instal
    version='1.0.1',
    description='Utility functions for commonly used data science packages (numpy, pandas, etc) and generic python utility functions',
    
    #long_description = Path("README.md").read_text()
    #long_description_content_type="something crazy",
    long_description=get_long_description(),
    project_urls={
        'Source':"https://github.com/reimerlab/datasci_tools",
        'Documentation':"https://reimerlab.github.io/datasci_tools/",
    },
    author='Brendan Celii',
    author_email='brendanacelii@gmail.com',
    packages=find_packages(),  #teslls what packages to be included for the install
    install_requires=get_install_requires(), #external packages as dependencies
    dependency_links = get_links(),
    # if wanted to install with the extra requirements use pip install -e ".[interactive]"
    extras_require={
        #'interactive': ['matplotlib>=2.2.0', 'jupyter'],
    },
    
    # if have a python script that wants to be run from the command line
    entry_points={
        #'console_scripts': ['pipeline_download=Applications.Eleox_Data_Fetch.Eleox_Data_Fetcher_vp1:main']
    },
    scripts=[],
    
)

