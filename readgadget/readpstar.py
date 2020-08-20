from .modules.common import *
import numpy as np
import os

class Group(object):
    def __init__(self,npart,index):
        self.index = index
        self.npart_total = npart

def readpstar(catdir,snapnum,groupIndex,**kwargs):
    """Read and return info from P-Star catalogues.

    Parameters
    ----------
    catdir : string
        path to your PSTAR catalogues
    snapnum : int
        snapnum you are interested in
    groupIndex : int
        which group to return info for? (-1 for all)
    
    Notes
    -----
    returns a Group class
    """

    GROUPS = []

    fcat   = open('%s/catalogue_%03d' % (catdir,snapnum),'rb')
    fprop  = open('%s/properties_%03d' % (catdir,snapnum),'rb')
    fpos   = open('%s/pos_%03d' % (catdir,snapnum),'rb')
    fptype = open('%s/type_%03d' % (catdir,snapnum),'rb')
    findex = open('%s/index_%03d' % (catdir,snapnum),'rb')
    
    ngroups  = np.fromfile(fcat,dtype=np.uint32,count=1)[0]
    nparttot = np.fromfile(fpos,dtype=np.uint32,count=1)[0]
    fprop.seek(4,1)
    fptype.seek(4,1)
    findex.seek(4,1)

    for i in range(0,ngroups):
        gpids = []
        spids = []
        stypes = []
        pids  = []

        nparts = np.fromfile(fcat,dtype=np.uint32,count=1)[0]
        offset = np.fromfile(fcat,dtype=np.uint32,count=1)[0]
        for j in range(0,nparts):
            ppos  = np.fromfile(fpos,dtype=np.float32,count=3)
            ptype = np.fromfile(fptype,dtype=np.uint32,count=1)[0]
            pid   = np.fromfile(findex,dtype=np.uint32,count=1)[0]
            if ptype == 0:
                gpids.append(pid)
            elif ptype == 4:
                spids.append(pid)
                stypes.append(ptype)
                
        pmstars = np.fromfile(fprop,dtype=np.float32,count=1)[0]
        mags    = np.fromfile(fprop,dtype=np.float32,count=4)
        pcm     = np.fromfile(fprop,dtype=np.float32,count=3)
        pmsfr   = np.fromfile(fprop,dtype=np.float32,count=1)[0]
        pmgas   = np.fromfile(fprop,dtype=np.float32,count=1)[0]
        pmmetals= np.fromfile(fprop,dtype=np.float32,count=1)[0]
        pmgmetals=np.fromfile(fprop,dtype=np.float32,count=1)[0]

        GROUPS.append(Group(nparts,i))
        GROUPS[i].mstar = pmstars
        GROUPS[i].mgas  = pmgas
        GROUPS[i].cm    = pcm
        GROUPS[i].metals= pmmetals
        GROUPS[i].gmetals=pmgmetals
        GROUPS[i].gpids = gpids
        GROUPS[i].spids = spids
        GROUPS[i].stypes = stypes

    fcat.close()
    fprop.close()
    fpos.close()
    fptype.close()
    findex.close()

    if groupIndex == -1:
        groupIndex = range(0,ngroups)

    if isinstance(groupIndex,int):
        grp = GROUPS[groupIndex]
        return grp
        
    elif isinstance(groupIndex,list):
        grps = []
        for i in range(0,len(groupIndex)):
            grp = GROUPS[groupIndex[i]]
            grps.append(grp)

        return grps

    """
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
    """
