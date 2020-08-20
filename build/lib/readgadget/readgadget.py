from .modules.common import *
from .modules.names import *
from .modules import header as HEAD
from .modules import gadget1 as gadget1
from .modules import gadget2 as gadget2
from .modules import tipsy as tipsy
from .modules import hdf5 as hdf5
import numpy as np
import sys

def readhead(snap,data,**kwargs):
    """Read and return desired header info
    
    Parameters
    ----------
    snap : string
        path to your snapshot EXCLUDING file extension (if any)
    data : string
        requested header information.  see readme for details.

    Notes
    -----
    If your snapshot happens to have a file extension, do NOT pass it to pyGadgetReader.  
    It will attempt to automatically detect your file type

    Examples
    --------
    >>> h = readhead('/Users/bob/snap_020','h')
    >>> h
    0.7
    """
    h = HEAD.Header(snap,0,kwargs)
    h.f.close()
    pollHeaderOptions(h,data)
    if data == 'header' or data == 'Header':
        return h.header_vals
    return h.header_vals[headerTypes[data]]

def readheader(snap,data,**kwargs):
    """Read and return desired header info
    
    Parameters
    ----------
    snap : string
        path to your snapshot EXCLUDING file extension (if any)
    data : string
        requested header information.  see readme for details.

    Notes
    -----
    If your snapshot happens to have a file extension, do NOT pass it to pyGadgetReader.  
    It will attempt to automatically detect your file type

    Examples
    --------
    >>> h = readheader('/Users/bob/snap_020','h')
    >>> h
    0.7
    """
    return readhead(snap,data,**kwargs)


def readsnap(snap,data,ptype,**kwargs):
    """Read and return desired snapshot data
    
    Parameters
    ----------
    snap : string
        path to your snapshot EXCLUDING file extension (if any)
    data : string
        requested data type.  see readme for details.
    ptype : string or int
        particle type requested.  Can be of type string, or integers 0-5
    
    Notes
    -----
    If your snapshot happens to have a file extension, do NOT pass it to pyGadgetReader.  
    It will attempt to automatically detect your file type

    Examples
    --------
    >>> pos  = readsnap('/Users/bob/snap_020','pos','gas')
    >>> pos
    array([[ 7160.86572266,  6508.62304688,  5901.06054688],
       [ 7161.45166016,  6585.53466797,  5931.87451172],
       ...,
       [ 7512.12158203,  7690.34179688,  8516.99902344]])
    """
    h   = HEAD.Header(snap,0,kwargs)
    d,p = pollOptions(h,kwargs,data,ptype)
    h.reading = d

    #print 'reading %s.%s' % (snap,h.extension)

    f = h.f
    initUnits(h)
    
    #print 'reading %d files...' % (h.nfiles)

    for i in range(0,h.nfiles):
        if i > 0:
            h = HEAD.Header(snap,i,kwargs)
            f = h.f
            h.reading = d
            initUnits(h)

        if h.npartThisFile[p] == 0:
            if h.nfiles > 1:
                continue
            print('no %s particles present!' % pNames[p])
            sys.exit()

        if h.fileType == 'hdf5':
            arr = hdf5.hdf5_read(f,h,p)
        elif h.fileType == 'tipsy':
            arr = tipsy.tipsy_read(f,h,p)
        elif h.fileType == 'gadget1':
            arr = gadget1.gadget_read(f,h,p,d)
        elif h.fileType == 'gadget2':
            arr = gadget2.gadget_type2_read(f,h,p)

        f.close()

        ## return nth value
        if h.nth > 1:
            arr = arr[0::h.nth]

        ## put arrays together
        if i > 0:
            if len(arr) > 0:
                return_arr = np.concatenate((return_arr,arr))
        else:
            return_arr = arr
            gadgetPrinter(h,d,p)
            if h.nth > 1 and not h.suppress:
                print('selecting every %d particles' % h.nth)

        ## if requesting a single file, break out of loop
        if h.singleFile:
            break

    if h.double and h.reading != 'pid' and h.reading != 'ParticleIDs':
        return_arr = return_arr.astype(np.float64)
                                    
    return return_arr


