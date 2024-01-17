'''



Purpose: To help automatically create a 




'''
from pathlib import Path
from setuptools import setup, find_packages
from typing import List

def get_links():
    return [
        #"datasci_tools @ git+https://github.com/bacelii/datasci_tools.git'"
    ]

def get_install_requires(filepath=None):
    if filepath is None:
        filepath = "./"
    """Returns requirements.txt parsed to a list"""
    fname = Path(filepath).parent / 'requirements.txt'
    targets = []
    if fname.exists():
        with open(fname, 'r') as f:
            targets = f.read().splitlines()
            
    targets += get_links()
    return targets

def get_long_description(filepath='README.md'):
    try:
        import pypandoc
        long_description = pypandoc.convert_file(filepath, 'rst') 
    except:
        print("\n\n\n****Need to install pypandoc (and if havent done so install apt-get install pandoc) to make long description clean****\n\n\n")
        
        long_description = Path("README.md").read_text()
        
    return long_description



setup_py_str = """

setup(
    name='[name]', # the name of the package, which can be different than the folder when using pip instal
    version='[version]',
    description='[description]',
    long_description=get_long_description(),
    #long_description_content_type = 'text/markdown',
    url='[url]',
    author='[author]',
    author_email='[author_email]',
    packages=find_packages(),  #teslls what packages to be included for the install
    install_requires=get_install_requires(), #external packages as dependencies
    # dependency_links = get_links(),
    # if wanted to install with the extra requirements use pip install -e ".[interactive]"
    extras_require={
        #'interactive': ['matplotlib>=2.2.0', 'jupyter'],
    },
    
    # if have a python script that wants to be run from the command line
    entry_points={
        #'console_scripts': ['pipeline_download=Applications.Eleox_Data_Fetch.Eleox_Data_Fetcher_vp1:main']
    },
    scripts=[], 
    #python_requires=">=3.8",
    # project_urls={
    #     'Source':"https://github.com/reimerlab/datasci_tools",
    #     'Documentation':"https://reimerlab.github.io/datasci_tools/",
    # },
    
    # these are tags you can use to search for 
    #classifiers=[
    #   
    #]
    
    # for optional requirements and would install using pip install packagename[key]
    #extras_require={
    #  key:[list of packages],
    #}
)

"""

def setup_py_str_generator(
    name,
    version = "1.0.0",
    author = "Brendan Celii",
    author_email = "brendanacelii@gmail.com",
    description = "",
    output_path = None,
    import_list = (
        "from pathlib import Path",
        "from setuptools import setup, find_packages",
        "from typing import List" ,
    ),
    url = "None",
    ):
    
    replace_dict = {
        "[name]":name,
        "[version]":version,
        "[author]":author,
        "[author_email]":author_email,
        "[description]":description,
        "[url]":url,
    }
    
    data =  str(setup_py_str)    
    for t,r in replace_dict.items():
        data = data.replace(t,r)
        
    data = (
        "\n".join(import_list)  + "\n"
        + "\n" + iu.function_code_as_str(get_install_requires)
        + "\n" + iu.function_code_as_str(get_links)
        + "\n" + iu.function_code_as_str(get_long_description)
        + "\n" + data
    )
    
    if output_path:
        filu.write_file(output_path,data=data,replace = True)
    
    return data
    


#--- from datasci_tools ---
from . import file_utils as filu
from . import inspect_utils as iu
