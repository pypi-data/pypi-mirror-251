
import scipy.io as io

def loadmat(filepath):
    return io.loadmat(filepath)


#from datasci_tools import matlab_utils as matu




from . import matlab_utils as matu