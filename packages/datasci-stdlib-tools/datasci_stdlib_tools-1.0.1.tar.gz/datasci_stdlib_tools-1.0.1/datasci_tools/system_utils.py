'''



How to get a reference to the current module

#import sys
current_module = sys.modules[__name__]



'''
from contextlib import contextmanager
from os import devnull
from contextlib import contextmanager,redirect_stderr,redirect_stdout
from pathlib import Path
from zipfile import ZipFile
import _pickle as cPickle
import bz2
import bz2, os
import contextlib
import copy
import logging
from . import numpy_dep as np
import os
import pickle
import shutil
import signal
import subprocess
import sys
import sys, os
import time
import warnings, os, os

# # ************ warning this will disable all printing until turned off *************
# # Disable
# def blockPrint():
#     sys.stdout = open(os.devnull, 'w')

# # Restore
# def enablePrint():
#     sys.stdout = sys.__stdout__
# # ************ warning this will disable all printing until turned off *************

    
    
#better way of turning off printing: 
#import os, sys


class HiddenPrints:
    """
    Example of how to use: 
    with HiddenPrints():
        print("This will not be printed")

    print("This will be printed as before")
    
    """
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
    
#import warnings
#import logging, sys
def ignore_warnings():
    """
    This will ignore warnings but not the meshlab warnings
    
    """
    warnings.filterwarnings('ignore')
    logging.disable(sys.maxsize)
    
suppress_warnings = ignore_warnings
turn_off_warnings = ignore_warnings
    


#from os import devnull
#from datasci_tools import tqdm_utils as tqu
#from datasci_tools.tqdm_utils import tqdm
#import copy

@contextmanager
def suppress_stdout_stderr(suppress_tqdm=True):
    """
    Purpose: Will suppress all print outs
    and pinky warning messages:
    --> will now suppress the output of all the widgets like tqdm outputs
    if suppress_tqdm = True
    
    Ex: How to suppress warning messages in Poisson
    from neurd import soma_extraction_utils as sm
with su.suppress_stdout_stderr():
    sm.soma_volume_ratio(my_neuron.concept_network.nodes["S0"]["data"].mesh)
    
    
    A context manager that redirects stdout and stderr to devnull
    Example of how to use: 
    import sys

    def rogue_function():
        print('spam to stdout')
        print('important warning', file=sys.stderr)
        1 + 'a'
        return 42

    with suppress_stdout_stderr():
        rogue_function()
    
    
    """
    #will supress the warnings:
    ignore_warnings()
    
    
    #get the original setting of the tqdm.disable
    if suppress_tqdm:
        original_tqdm = copy.copy(tqdm.disable)
        tqu.turn_off_tqdm()
    
    
    with open(devnull, 'w') as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)
            
    if not original_tqdm:
        tqu.turn_on_tqdm()
            
    
            


"""
#for creating a conditional with statement around some code (to suppress outputs)


Example: (used in neuron init)
if minimal_output:
            print("Processing Neuorn in minimal output mode...please wait")

with su.suppress_stdout_stderr() if minimal_output else su.dummy_context_mgr():
    #do the block of node

"""
class dummy_context_mgr():
    def __enter__(self):
        return None
    def __exit__(self, exc_type, exc_value, traceback):
        return False

#import contextlib

@contextlib.contextmanager
def dummy_context_mgr():

    yield None
    
    

# How to save and load objects
"""
*** Warning *****
The way you import a class can affect whether it was picklable or not

Example: 

---Way that works---: 

su = reload(su)

#from meshAfterParty.neuron import Neuron
another_neuron = Neuron(new_neuron)
su.save_object(another_neuron,"inhibitory_saved_neuron")

---Way that doesn't work---
su = reload(su)

#from neurd import neuron
another_neuron = neuron.Neuron(new_neuron)
su.save_object(another_neuron,"inhibitory_saved_neuron")

"""
#from pathlib import Path
#import pickle
def save_object(obj, filename,return_size=False):
    """
    Purpose: to save a pickled object of a neuron
    
    ** Warning ** do not reload the module of the 
    object you are compressing before compression
    or else it will not work***
    
    """
    if type(filename) == type(Path()):
        filename = str(filename.absolute())
    if filename[-4:] != ".pkl":
        filename += ".pkl"
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
    print(f"Saved object at {Path(filename).absolute()}")
    
    file_size = get_file_size(filename)/1000000
    print(f"File size is {file_size} MB")
    
    try:
        meshu.clear_all_mesh_cache_in_nested_data_struct(obj)
    except Exception as e:
        print(e)
    
    if return_size:
        return file_size
    
#import pickle5 as pickle5
def load_object(filename):
    if type(filename) == type(Path()):
        filename = str(filename.absolute())
    else:
        if filename[-4:] != ".pkl":
            filename += ".pkl"
            
    
    with open(filename, 'rb') as input:
        retrieved_obj = pickle.load(input)
#     except:
#         with open(filename, "rb") as fh:
#             data = pickle5.load(fh)
    return retrieved_obj


load_pkl = load_object



#--------------- Less memory pickling options -----------------
# Pickle a file and then compress it into a file with extension 
#import bz2
#import _pickle as cPickle
def compressed_pickle(obj,filename,return_size=False,verbose=False,
                     return_filepath=False,
                     folder = None):
    """
    compressed_pickle(data,'example_cp') 
    """
    if folder is not None:
        filename = Path(folder) / Path(filename)
    
    if type(filename) == type(Path()):
        filename = str(filename.absolute())
    if filename[-5:] != ".pbz2":
        filename += ".pbz2"
 
    with bz2.BZ2File(filename, 'w') as f: 
        cPickle.dump(obj, f)
        
    file_size = get_file_size(filename)/1000000
    
    if verbose:
        print(f"Saved object at {Path(filename).absolute()}")
        print(f"File size is {file_size} MB")
    
    if return_size:
        return file_size

    if return_filepath:
        return str(Path(filename).absolute())

# Load any compressed pickle file
def decompress_pickle(filename):
    """
    Example: 
    data = decompress_pickle('example_cp.pbz2') 
    """
    if type(filename) == type(Path()):
        filename = str(filename.absolute())
    if filename[-5:] != ".pbz2":
        filename += ".pbz2"
        
    data = bz2.BZ2File(filename, 'rb')
    data = cPickle.load(data)
    return data


#import os
def get_file_size(filepath,MB=False):
    curr_size = os.path.getsize(filepath)
    if MB:
        return curr_size/1000000
    else:
        return curr_size


# ----------- How to make copies -------------- #
#import shutil

#import os
#from pathlib import Path

def is_path_obj(obj):
    return isinstance(obj,Path)

def copy_file(source,destination):
    if is_path_obj(source):
        source = str(source.absolute())
    if is_path_obj(destination):
        destination = str(destination.absolute())
    shutil.copy(source,destination)


def copy_file_and_create_shell_script(original_file,num_copies,new_dir=False):
    """
    Example: 
    copy_file_and_create_shell_script("BaylorSegmentCentroid.py",5,new_dir=False)
    """
    if new_dir:
        if not os.path.exists("copies"):
            os.makedirs("copies")
        folder = "./copies"
    else:
        folder = "./"
    print(f"Using folder {folder}")
    #create the new files
    new_file_names = []
    for i in range(0,num_copies):
        # Copy the file in same folder with different name
        new_name = str(i) + "_" + str(original_file)
        shutil.copy(original_file,folder +"/" + str(new_name))
        
        new_file_names.append(new_name)

    #write the shell script
    f = open(folder + "/run_multiple_" + str(original_file) + ".sh", "w")
    f.write("#!/bin/bash")
    f.write("\n")
    for file_name in new_file_names:
        f.write("python3 " + str(file_name) + " &")
        f.write("\n")
    f.close()
    
    
#import signal
#from contextlib import contextmanager

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    """
    How to do call it
    try:
        with su.time_limit(10):
            long_function_call()
    except su.TimeoutException as e:
        print("Timed out!")
    
    
    """
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        
        
#from pathlib import Path
def filter_folder_for_substring(path,substring_query):
    """
    PUrpose: To filter a directory for certain files
    using regex expressions
    
    Ex: This replaces the need for this
    decomp_path = Path("/mnt/dj-stor01/platinum/minnie65/02/decomposition/")
    files = list(decomp_path.glob("*axon_v7.pbz2"))
    files
    
    """
    path = Path(path)
    files = list(path.glob(substring_query))
    return 

# ---------------- 10/19 ---------------------
#import subprocess
def bash_command(command,split_by_line = False):
    file_outputs = subprocess.check_output(command.split())
    if split_by_line:
        return_value = file_outputs.splitlines()
        return [b.decode("utf-8") for b in return_value ]
    else:
        return file_outputs.decode("utf-8")
    
    
    
#--------------- 2/1 Saving off zipped files -------------
#from zipfile import ZipFile
#import time
#from . import numpy_dep as np

def zip_write_from_file_paths(
    zip_file_path,
    file_paths,
    verbose = True,
    calculate_size_diff = False,
    save_directory_structure = False,
    ):
    """
    Purpose: To Create a zip file from 
    a list of file directories
    """

    zipObj = ZipFile(zip_file_path, 'w')

    original_size = []
    st = time.time()
    for f in tqdm(file_paths):

        if "str" not in str(type(f)):
            f = str(f.absolute())

        if calculate_size_diff:
            original_size.append(su.get_file_size(f,MB = True))
        if save_directory_structure:
            zipObj.write(f)
        else:
            zipObj.write(f,arcname=Path(f).name)
    zipObj.close()


    if verbose:
        if calculate_size_diff:
            print(f"Original Size before zip = {np.sum(original_size)}")
        print(f"Total zip size: {su.get_file_size(zip_file_path,MB = True)}")
        print(f"Total time = {time.time() - st}")
        
    return zip_file_path

def zip_extract(
    path_to_zip_file,
    directory_to_extract_to,
    verbose = False,
    ):

    st = time.time()
    with ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(directory_to_extract_to)

    if verbose:
        print(f"Time for unzipping = {time.time() - st}")


def environment_variables():
    return os.environ

#import shutil
def rm_dir(directory,ignore_errors = False):
    shutil.rmtree(directory, ignore_errors=ignore_errors)
    

    


#from datasci_tools import system_utils as su






#--- from datasci_tools ---
from . import tqdm_utils as tqu
from .tqdm_utils import tqdm
from . import mesh_utils as meshu

from . import system_utils as su