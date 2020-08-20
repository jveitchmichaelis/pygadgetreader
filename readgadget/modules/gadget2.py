## FOR GADGET TYPE 2 BINARY FILES ##

import sys
import struct
import numpy as np
from . import gadget1 as g

TYPE2NAMES = {
    'pos':'POS ',
    'vel':'VEL ',
    'pid':'ID  ',
    'mass':'MASS',
    'u':'U   ',
    'rho':'RHO ',
    'ne':'NE  ',
    'nh':'NH  ',
    'hsml':'HSML',
    'sfr':'SFR',
    'metallicity':'Z   ',
    'pot':'POT ',
    'fh2':'fH2 ',
    'sigma':'Sigm',
    'age':'AGE '
}

def findBlock(f,h):
    RETURN = False

    blk1 = np.fromfile(f,dtype=np.uint32,count=1)
    if not blk1:
        return 2
    blk1 = blk1[0]
    NAME = struct.unpack('4s',f.read(4))[0]
    NAME = NAME.decode()
    sl   = np.fromfile(f,dtype=np.uint32,count=1)
    blk2 = np.fromfile(f,dtype=np.uint32,count=1)[0]
    g.errorcheck(blk1,blk2,'blk %s' % NAME)

    ## custom return
    if h.reading not in TYPE2NAMES:
        if NAME == h.reading:
            RETURN = True
    elif NAME == TYPE2NAMES[h.reading]:
        RETURN = True

    if RETURN:
        if h.debug: print('returning for block %s' % NAME)
        return 1
    else:
        if h.debug: print('skipping block %s' % NAME)

    s1 = np.fromfile(f,dtype=np.uint32,count=1)[0]
    f.seek(s1, 1)
    s2 = np.fromfile(f,dtype=np.uint32,count=1)[0]
    g.errorcheck(s1,s2,NAME)
    return 0

def gadget_general(f,h,ptype):
    skip1 = np.fromfile(f,dtype=np.uint32,count=1)[0]
    
    gOnly   = 0.
    sOnly   = 0.
    gsOnly  = 0.
    allPart = 0.

    if h.npartThisFile[0] > 0:
        gOnly   = skip1 / (np.dtype(h.dataType).itemsize * h.npartThisFile[0])
    if h.npartThisFile[4] > 0:
        sOnly   = skip1 / (np.dtype(h.dataType).itemsize * h.npartThisFile[4])
    if h.npartThisFile[0] > 0 or h.npartThisFile[4] > 0:
        gsOnly  = skip1 / (np.dtype(h.dataType).itemsize * h.npartThisFile[0] + 
                           np.dtype(h.dataType).itemsize * h.npartThisFile[4])
    allPart = skip1 / (np.dtype(h.dataType).itemsize * np.sum(h.npartThisFile)) 

    if gOnly == 1.0:
        if ptype != 0:
            print('block is only present for gas!')
            return
        vals = np.fromfile(f,dtype=h.dataType,count=h.npartThisFile[ptype])
    elif sOnly == 1.0:
        if ptype != 4:
            print('block is only present for stars!')
            return
        vals = np.fromfile(f,dtype=h.dataType,count=h.npartThisFile[ptype])
    elif gsOnly == 1.0:
        if ptype != 0 and ptype != 4:
            print('block is only present for gas & stars!')
            return
        if ptype == 4:
            f.seek(np.dtype(h.dataType).itemsize * h.npartThisFile[0],1)
        vals = np.fromfile(f,dtype=h.dataType,count=h.npartThisFile[ptype])
        if ptype == 0:
            f.seek(np.dtype(h.dataType).itemsize * h.npartThisFile[4],1)
    elif allPart == 1.0:
        for i in range(0,ptype):
            f.seek(np.dtype(h.dataType).itemsize * h.npartThisFile[i],1)
        vals = np.fromfile(f,dtype=h.dataType,count=h.npartThisFile[ptype])
        for i in range(ptype+1,len(h.npartThisFile)):
            f.seek(np.dtype(h.dataType).itemsize * h.npartThisFile[i],1)
        
    skip2 = np.fromfile(f,dtype=np.uint32,count=1)[0]
    g.errorcheck(skip1,skip2,"generic read")
    return vals
    
def gadget_type2_read(f,h,p):
    """Main driver for reading gadget type-2 binaries"""

    stat = 0
    while stat == 0:
        stat = findBlock(f,h)
        
    if stat == 2:
        print('end of file =/')
        print('scanning did not find block %s' % (h.reading))
        sys.exit()
    
    if h.reading == 'pos' or h.reading == 'vel':
        arr = g.gadget_readposvel(f,h,p)
    elif h.reading == 'pid':
        arr = g.gadget_readpid(f,h,p)
    elif h.reading == 'mass':
        arr = g.gadget_readmass(f,h,p)
    elif h.reading == 'metallicity':
        arr = g.gadget_readmetals(f,h,p,single=0)
    else:
        arr = gadget_general(f,h,p)
        
    return arr
