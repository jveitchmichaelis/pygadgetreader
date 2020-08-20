import numpy as np
from .common import METALFACTOR
import sys

NMETALS = 4

gasstruct  = np.dtype([('mass',np.float32),
                       ('pos',np.float32,(3,)),
                       ('vel',np.float32,(3,)),
                       ('rho',np.float32),
                       ('u',np.float32),
                       ('hsml',np.float32),
                       ('metallicity',np.float32),
                       ('pot',np.float32)])
dmstruct   = np.dtype([('mass',np.float32),
                       ('pos',np.float32,(3,)),
                       ('vel',np.float32,(3,)),
                       ('hsml',np.float32),
                       ('pot',np.float32)])
starstruct = np.dtype([('mass',np.float32),
                       ('pos',np.float32,(3,)),
                       ('vel',np.float32,(3,)),
                       ('metallicity',np.float32),
                       ('age',np.float32),
                       ('hsml',np.float32),
                       ('pot',np.float32)])

auxgasstruct   = np.dtype([('metalarray',np.float32,(NMETALS,)),
                           ('sfr',np.float32),
                           ('tmax',np.float32),
                           ('delaytime',np.float32),
                           ('ne',np.float32),
                           ('nh',np.float32),
                           ('nspawn',np.int32)])
auxstarstruct  = np.dtype([('metalarray',np.float32,(NMETALS,)),
                           ('age',np.float32),
                           ('tmax',np.float32),
                           ('nspawn',np.int32)])

def tipsy_binread(f,h,ptype):
    """read tipsy binfile"""
    if ptype == 0:
        data = np.fromfile(f,dtype=gasstruct,count=h.npartThisFile[0])
    elif ptype == 1:
        f.seek((4*6 + 4*3 + 4*3) * h.npartThisFile[0],1)
        data = np.fromfile(f,dtype=dmstruct,count=h.npartThisFile[1])
    elif ptype == 4:
        f.seek((4*6 + 4*3 + 4*3) * h.npartThisFile[0],1)
        f.seek((4*3 + 4*3 + 4*3) * h.npartThisFile[1],1)
        data = np.fromfile(f,dtype=starstruct,count=h.npartThisFile[4])
    return data[:][h.reading]

def tipsy_auxread(f,h,ptype):
    """read tipsy aux file"""
    if ptype == 0:
        data = np.fromfile(f,dtype=auxgasstruct,count=h.npartThisFile[0])
    elif ptype == 4:
        f.seek((4*NMETALS + 6*4) * h.npartThisFile[0],1)
        data = np.fromfile(f,dtype=auxstarstruct,count=h.npartThisFile[4])
    return data[:][h.reading]


def tipsy_pids(f,h,ptype):
    """read tipsy particle IDs"""
    if ptype == 0:
        pids = np.fromfile(f,dtype=np.int32,count=h.npartThisFile[0])
    elif ptype == 1:
        f.seek(4 * h.npartThisFile[0],1)
        pids = np.fromfile(f,dtype=np.int32,count=h.npartThisFile[1])
    elif ptype == 4:
        f.seek(4*h.npartThisFile[0] + 4*h.npartThisFile[1],1)
        pids = np.fromfile(f,dtype=np.int32,count=h.npartThisFile[4])
    return pids

def tipsy_read(f,h,ptype):
    """controls which tispy file we read from"""

    ## idnum file
    if h.reading=='pid':
        h.f.close()
        h.f = open('%s.idnum' % h.snap_passed, 'rb')
        f = h.f
        arr = tipsy_pids(f,h,ptype)
        
    ## aux file
    elif (h.reading=='metalarray' or h.reading=='sfr' or 
          h.reading=='tmax' or h.reading=='delaytime' or
          h.reading=='ne' or h.reading=='nh' or h.reading=='nspawn'):
        h.f.close()
        h.f = open('%s.aux' % h.snap_passed, 'rb')
        f = h.f
        arr = tipsy_auxread(f,h,ptype)
        
    ## bin file
    else:
        arr = tipsy_binread(f,h,ptype)
    
    return arr
