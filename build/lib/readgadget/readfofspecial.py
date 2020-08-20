from .modules.common import *
import numpy as np
import os

class Group(object):
    def __init__(self,npart,index):
        self.index = index
        self.npart_total = npart

def readfofspecial(catdir,snapnum,groupIndex,**kwargs):
    """Read and return info from FOFSpecial catalogues.

    Parameters
    ----------
    catdir : string
        path to your FOF catalogues
    snapnum : int
        snapnum you are interested in
    groupIndex : int
        which group to return info for? (-1 for all)
    
    Notes
    -----
    returns a Group class
    """

    GROUPS = []

    ## group catelog
    f = open('%s/fof_special_catalogue_%03d' % (catdir,snapnum),'rb')
    ngroups = np.fromfile(f,dtype=np.int32,count=1)[0]
    for i in range(0,ngroups):
        nparts = np.fromfile(f,dtype=np.uint32,count=1)[0]
        GROUPS.append(Group(nparts,i))
    for i in range(0,ngroups):
        cumnum = np.fromfile(f,dtype=np.uint32,count=1)[0]
        GROUPS[i].cumcount = cumnum
    for i in range(0,ngroups):
        grp_mass = np.fromfile(f,dtype=np.float32,count=1)[0]
        GROUPS[i].mass = grp_mass
    for i in range(0,ngroups):
        cmpos = np.fromfile(f,dtype=np.float32,count=3)
        GROUPS[i].cm = cmpos
    for i in range(0,ngroups):
        ngas  = np.fromfile(f,dtype=np.uint32,count=1)[0]
        ndm   = np.fromfile(f,dtype=np.uint32,count=1)[0]
        nstar = np.fromfile(f,dtype=np.uint32,count=1)[0]
        GROUPS[i].ngas  = ngas
        GROUPS[i].ndm   = ndm
        GROUPS[i].nstar = nstar
    for i in range(0,ngroups):
        gmass  = np.fromfile(f,dtype=np.float32,count=1)[0]
        dmmass = np.fromfile(f,dtype=np.float32,count=1)[0]
        smass  = np.fromfile(f,dtype=np.float32,count=1)[0]
        GROUPS[i].gmass  = gmass
        GROUPS[i].dmmass = dmmass
        GROUPS[i].smass  = smass
    f.close()

    ## index list
    f = open('%s/fof_special_indexlist_%03d' % (catdir,snapnum),'rb')
    nindexes  = np.fromfile(f,dtype=np.uint32,count=1)[0]
    indexList = np.fromfile(f,dtype=np.uint32,count=nindexes)
    f.close()

    if groupIndex == -1:
        groupIndex = range(0,ngroups)

    if isinstance(groupIndex,int):
        grp = GROUPS[groupIndex]
        grp.indexes = np.zeros(grp.npart_total,dtype=np.uint32)
        for j in range(0,grp.npart_total):
            grp.indexes[j] = indexList[grp.cumcount + j] - 1
        return grp
        
    elif isinstance(groupIndex,list):
        grps = []
        for i in range(0,len(groupIndex)):
            grp = GROUPS[groupIndex[i]]
            grps.append(grp)
            
            grp.indexes = np.zeros(grp.npart_total,dtype=np.uint32)
            for j in range(0,grp.npart_total):
                grp.indexes[j] = indexList[grp.cumcount + j] - 1
        return grps
            
