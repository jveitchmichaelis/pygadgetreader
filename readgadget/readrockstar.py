from .modules.common import *
import numpy as np
import os
from .modules.rs_structs import getRSformat

class RockstarFile(object):
    
    def __init__(self,binfile,data,galaxies,debug):
        self.galaxies = galaxies
        self.binfile  = binfile
        self.debug    = debug
        self.header()

        self.halos()
        if data == 'particles':
            self.particles()
        self.f.close()
        
    def header(self):
        f = open(self.binfile,'rb')
        f.seek(8*3 + 4*10,1)
        self.num_halos     = np.fromfile(f,dtype=np.int64,count=1)[0]
        self.num_particles = np.fromfile(f,dtype=np.int64,count=1)[0]
        #print self.num_halos
        f.seek(4 + 4 + 8,1)
        self.format_revision = np.fromfile(f,dtype=np.int32,count=1)[0]
        if self.debug: print('found HALO_FORMAT_REVISION %d (header)' % self.format_revision)
        bytes_left = 256 - f.tell()
        f.seek(bytes_left,1)
        self.f = f

        self.halostruct = getRSformat(self)
    
    def halos(self):
        #print 'reading %d halos (%d)' % (self.num_halos,self.galaxies)
        self.halodata = np.fromfile(self.f,dtype=self.halostruct,count=self.num_halos)
        
    def particles(self):
        self.particle_IDs     = np.zeros(self.num_particles,dtype=np.int64)
        self.particle_IDs.fill(-1)

        self.particle_haloIDs = np.zeros(self.num_particles,dtype=np.int64)
        self.particle_haloIDs.fill(-1)

        nparts = 0
        for i in range(0,self.num_halos):
            hid   = self.halodata[i]['id']
            num_p = self.halodata[i]['num_p']
            #print '%d %d' % (i,num_p)
            pids  = np.fromfile(self.f,dtype=np.int64,count=num_p)
            
            self.particle_IDs[nparts:nparts+num_p]     = pids
            self.particle_haloIDs[nparts:nparts+num_p] = hid
            nparts += num_p
        #print 'complete'

def compileReturnArray(RS,data):
    """compile data from RS binary and return requested value"""
    arr = []
    singleval = False

    ## return particle ID data
    if data == 'particles':
        npart = 0
        for i in range(0,len(RS)):
            npart += len(RS[i].particle_IDs)

        arr   = np.zeros((npart,2),dtype=np.int64)
        npart = 0
        for i in range(0,len(RS)):
            n = len(RS[i].particle_IDs)
            arr[npart:npart+n,0] = RS[i].particle_IDs
            arr[npart:npart+n,1] = RS[i].particle_haloIDs
            npart += n

        return arr

    ## return halo struct data
    if data in RS[0].halostruct.names:
        singleval = True
        if RS[0].debug: print('%s found in halodata' % data)

    nhalos = 0
    for i in range(0,len(RS)):
        nhalos += RS[i].num_halos
        if singleval:
            arr.extend(RS[i].halodata[data])
        else:
            arr.extend(RS[i].halodata)

    #print nhalos,len(arr)
    return np.asarray(arr)
    

def readrockstargalaxies(binfile,data,**kwargs):
    if 'galaxies' in kwargs: del kwargs['galaxies']
    arr = readrockstar(binfile,data,galaxies=1,**kwargs)
    return arr

def readrockstar(binfile,data,**kwargs):
    """read rockstar binary file

    Parameters
    ----------
    binfile : string
        path to rockstar binary file.  Do NOT include file extention or leading number
    data : string
        requested data, see readme for details

    Examples
    --------
    >>> halo_mass = readrockstar('/Users/bob/halos_020','m')
    >>> halo_mass
    array([  7.25643648e+08,   5.70148608e+08,   3.97376288e+08,
         3.66277274e+09,   1.99379231e+10,   5.01039648e+08,
         ...,
         1.58950515e+09,   2.10782208e+09,   8.41401088e+09,
         4.14653504e+08], dtype=float32)
    """
    galaxies = 0
    if 'galaxies' in kwargs and kwargs['galaxies']==1:
        galaxies = 1

    debug = 0
    if 'debug' in kwargs and kwargs['debug']==1:
        debug = 1

    RS_DATA = []
    for j in range(0,5000):
        b = '%s.%d.bin' % (binfile,j)
        if os.path.isfile(b):
            if debug: print('reading %s' % b)
            RS_DATA.append(RockstarFile(b,data,galaxies,debug))
        else:
            break

    arr = compileReturnArray(RS_DATA,data)
    return arr
