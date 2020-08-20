## FOR GADGET TYPE 1 BINARY FILES ##

import sys
import numpy as np
from .common import METALFACTOR
from .names import headerTypes,GasProps,GasStarProps


def skip(f):
    skipval = np.fromfile(f,dtype=np.uint32,count=1)
    return skipval[0]

def errorcheck(s1,s2,block):
    if s1!=s2:
        print('issue with before/after skips - block %s >> %d vs %d' % (block,s1,s2))
        sys.exit()

def skipblocks(f,h,val):
    """Skip to desired block!"""
    def skiptypes(ptypes,block,multiplier=1):
        """Skip an entire block of given type"""
        if ptypes == -1:
            ptypes = [0,1,2,3,4,5]
        if isinstance(ptypes,int):
            ptypes = [ptypes]
        nparts = np.sum(h.npartThisFile[ptypes])
        if nparts == 0:
            return

        dataType = h.dataType            

        s1 = skip(f)
        ## account for possible LONG IDs
        if block == 'pid':
            ntot = np.sum(h.npartThisFile)
            if s1 / (ntot * 4) == 1:
                dataType = np.uint32
            elif s1 / (ntot * 8) == 1:
                dataType = np.uint64
            
        for i in ptypes:
            f.seek(np.dtype(dataType).itemsize * multiplier * h.npartThisFile[i],1)
        s2 = skip(f)
        errorcheck(s1,s2,block)
            
    def skipmasses():
        """Skip mass block if it exists"""
        mb_exists = 0
        for i in range(0,len(h.npartThisFile)):
            if h.massTable[i] == 0 and h.npartThisFile[i] > 0:
                mb_exists = 1
                break
        if mb_exists:
            s1 = skip(f)
            for i in range(0,len(h.npartThisFile)):
                if h.massTable[i] == 0 and h.npartThisFile[i] > 0:
                    f.seek(np.dtype(h.dataType).itemsize * h.npartThisFile[i],1)
            s2 = skip(f)
            errorcheck(s1,s2,'mass')

    
    for key,items in h.BLOCKORDER.items():
        if val == key: 
            if h.debug:
                print('returning for key %s' % key)
            return

        if val == 'metalarray' and key == 'metallicity': return

        multi = 1
        if key == 'pos' or key == 'vel':
            multi = 3
        if key == 'metallicity' or key == 'metalarray':
            multi = h.flag_metals

        if h.debug: print('skipping %s' % key)
        if key == 'mass':
            skipmasses()
        elif len(items) == 1:
            skiptypes(items[0],key,multiplier=multi)
        elif len(items) > 1:
            if h.header_vals[headerTypes[items[1]]]:
                skiptypes(items[0],key,multiplier=multi)
    return    


def gadget_readposvel(f,h,ptype):
    skip1 = skip(f)
    for i in range(0,ptype):
        f.seek(np.dtype(h.dataType).itemsize*3*h.npartThisFile[i],1)
    posvel = np.fromfile(f,dtype=h.dataType,count=h.npartThisFile[ptype]*3)
    for i in range(ptype+1,len(h.npartThisFile)):
        f.seek(np.dtype(h.dataType).itemsize*3*h.npartThisFile[i],1)
    skip2 = skip(f)
    errorcheck(skip1,skip2,'posvel')
    
    posvel = posvel.reshape(h.npartThisFile[ptype],3)
    return posvel*h.convert

def gadget_readpid(f,h,ptype):
    skip1 = skip(f)
    ntot  = np.sum(h.npartThisFile)
    if skip1 / (4 * ntot) == 1:
        PIDdtype = np.uint32
    elif skip1 / (8 * ntot) == 1:
        PIDdtype = np.uint64
    else:
        print('err, could not determine PID data type! =/')
        sys.exit()

    for i in range(0,ptype):
        f.seek(np.dtype(PIDdtype).itemsize * h.npartThisFile[i],1)
    pid = np.fromfile(f,dtype=PIDdtype,count=h.npartThisFile[ptype])
    for i in range(ptype+1,len(h.npartThisFile)):
        f.seek(np.dtype(PIDdtype).itemsize * h.npartThisFile[i],1)
    skip2 = skip(f)
    errorcheck(skip1,skip2,'pids')
    return pid

def gadget_readmass(f,h,ptype):
    mb_exists = 0
    for i in range(0,len(h.npartThisFile)):
        if h.massTable[i] == 0 and h.npartThisFile[i] > 0:
            mb_exists = 1
            break

    if mb_exists:
        skip1 = skip(f)
        for i in range(0,ptype):
            if h.massTable[i] == 0 and h.npartThisFile[i] > 0:
                f.seek(np.dtype(h.dataType).itemsize * h.npartThisFile[i],1)
                
        if h.massTable[ptype] > 0:
            mass = np.zeros(h.npartThisFile[ptype],dtype=h.dataType)
            mass.fill(h.massTable[ptype])
        elif h.massTable[ptype] == 0 and h.npartThisFile[ptype] > 0:
            mass = np.fromfile(f,dtype=h.dataType,count=h.npartThisFile[ptype])

        for i in range(ptype+1,len(h.npartThisFile)):
            if h.massTable[i] == 0 and h.npartThisFile[i] > 0:
                f.seek(np.dtype(h.dataType).itemsize * h.npartThisFile[i],1)

        skip2 = skip(f)
        errorcheck(skip1,skip2,'mass')
        return mass*h.convert
        #return mass.astype(np.float64)*h.convert
    else:
        mass = np.zeros(h.npartThisFile[ptype],dtype=h.dataType)
        mass.fill(h.massTable[ptype])
        return mass

def gadget_readgasprop(f,h):
    skip1   = skip(f)
    gasprop = np.fromfile(f,dtype=h.dataType,count=h.npartThisFile[0])
    skip2   = skip(f)
    errorcheck(skip1,skip2,'gasprop')

    ## read in Ne for temp calc
    if h.units and h.reading == 'u':
        skip1 = skip(f)
        f.seek(np.dtype(h.dataType).itemsize * h.npartThisFile[0],1)
        skip2 = skip(f)
        errorcheck(skip1,skip2,'rho for Temp')
        
        skip1 = skip(f)
        ne    = np.fromfile(f,dtype=h.dataType,count=h.npartThisFile[0])
        skip2 = skip(f)
        errorcheck(skip1,skip2,'ne for Temp')

        from . import common as common
        h.convert = common.getTfactor(ne,h)

    return gasprop*h.convert

def gadget_readgasstarprop(f,h,ptype):
    skip1 = skip(f)
    if ptype == 4:
        f.seek(np.dtype(h.dataType).itemsize * h.npartThisFile[0],1)
    gasstarprop = np.fromfile(f,dtype=h.dataType,count=h.npartThisFile[ptype])
    if ptype == 0:
        f.seek(np.dtype(h.dataType).itemsize * h.npartThisFile[4],1)
    skip2 = skip(f)
    errorcheck(skip1,skip2,'gas-star prop')
    return gasstarprop*h.convert

def gadget_readmetals(f,h,ptype,single=1):
    skip1 = skip(f)
    if ptype == 4:
        f.seek(np.dtype(h.dataType).itemsize * h.flag_metals * h.npartThisFile[0],1)
    metals = np.fromfile(f,dtype=h.dataType,count=h.flag_metals * h.npartThisFile[ptype])
    if ptype == 0:
        f.seek(np.dtype(h.dataType).itemsize * h.flag_metals * h.npartThisFile[4],1)
    skip2 = skip(f)
    errorcheck(skip1,skip2,'metals')

    if single and h.flag_metals > 1:
        newZ   = np.zeros(h.npartThisFile[ptype],dtype=h.dataType)
        metals = metals.reshape(h.npartThisFile[ptype],h.flag_metals)
        for i in range(0,h.npartThisFile[ptype]):
            tmpz = 0.0
            for k in range(0,h.flag_metals):
                tmpz += metals[i,k]
            newZ[i] = tmpz * METALFACTOR
        metals = newZ
        newZ   = None
    elif h.flag_metals > 1:
        metals = metals.reshape(h.npartThisFile[ptype],h.flag_metals)

    return metals

def gadget_readpotentials(f,h,ptype):
    skip1 = skip(f)
    for i in range(0,ptype):
        f.seek(np.dtype(h.dataType).itemsize * h.npartThisFile[i],1)
    potentials = np.fromfile(f,dtype=h.dataType,count=h.npartThisFile[ptype])
    for i in range(ptype+1,len(h.npartThisFile)):
        f.seek(np.dtype(h.dataType).itemsize * h.npartThisFile[i],1)
    skip2 = skip(f)
    errorcheck(skip1,skip2,'potentials')

    return potentials

def gadget_readage(f,h):
    skip1 = skip(f)
    age   = np.fromfile(f,dtype=h.dataType,count=h.npartThisFile[4])
    skip2 = skip(f)
    errorcheck(skip1,skip2,'age')

    return age



def gadget_read(f,h,p,d):
    """Main driver for reading gadget binaries"""

    skipblocks(f,h,d)

    if h.reading == 'pos' or h.reading == 'vel':
        arr = gadget_readposvel(f,h,p)
    elif h.reading == 'pid':
        arr = gadget_readpid(f,h,p)
    elif h.reading == 'mass':
        arr = gadget_readmass(f,h,p)
    elif h.reading in GasProps:
        if p != 0: 
            print('WARNING!! you requested ParticleType%d for %s, returning GAS instead' 
                  % (p,h.reading))
        arr = gadget_readgasprop(f,h)
    elif h.reading in GasStarProps:
        arr = gadget_readgasstarprop(f,h,p)
    elif h.reading == 'metallicity':
        arr = gadget_readmetals(f,h,p)
    elif h.reading == 'metalarray':
        arr = gadget_readmetals(f,h,p,single=0)
    elif h.reading == 'pot':
        arr = gadget_readpotentials(f,h,p)
    elif h.reading == 'age':
        arr = gadget_readage(f,h)
    else:
        print('no clue what to read =(')
        arr = np.zeros(0)
    
    return arr
