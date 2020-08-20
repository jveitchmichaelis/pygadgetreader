import h5py as h5py
import numpy as np
from .common import METALFACTOR

HDF5_NAMES = {'pos':'Coordinates',
              'vel':'Velocities',
              'pid':'ParticleIDs',
              'mass':'Masses',
              'u':'InternalEnergy',
              'rho':'Density',
              'hsml':'SmoothingLength',
              'ne':'ElectronAbundance',
              'nh':'NeutralHydrogenAbundance',
              'sfr':'StarFormationRate',
              'metallicity':'Metallicity',
              'metalarray':'Metallicity',
              'age':'StellarFormationTime',
              'pot':'Potential',
              'fh2':'FractionH2',
              'sigma':'Sigma',
              'tmax':'TemperatureMax',
              'delaytime':'DelayTime',
              'nspawn':'NstarsSpawn'}


def hdf5_general(f,h,ptype):

    if ('PartType%d' % ptype) in f:
        if h.reading not in HDF5_NAMES:
            if h.reading in f['PartType%d' % ptype]:
                arr = f['PartType%d/%s' % (ptype,h.reading)]
            else:
                print('ERROR!  could not find "%s" in PartType%d' % (h.reading,ptype))
                arr = np.zeros(0,dtype=np.float32)

        elif HDF5_NAMES[h.reading] in f['PartType%d' % ptype]:
            if h.debug: print('reading PartType%d/%s' % (ptype,HDF5_NAMES[h.reading]))
            arr = f['PartType%d/%s' % (ptype,HDF5_NAMES[h.reading])]

        else:
            if h.debug: print('could not locate PartType%d/%s' % (ptype,HDF5_NAMES[h.reading]))
            arr = np.zeros(h.npartThisFile[ptype],dtype=np.float32)

        if h.units and h.reading == 'u':
            from . import common as common
            if HDF5_NAMES['ne'] not in f['PartType0']:
                print('WARNING! ElectronAbundance not found!  Temp estimate approximate')
                h.convert = common.getTfactorNoNe()
            else:
                ne = f['PartType0/%s' % (HDF5_NAMES['ne'])]
                h.convert = common.getTfactor(np.asarray(ne,dtype=np.float32),h)
                #h.convert = h.convert.astype(np.float32)
    else:
        if h.debug: print('coult not find PartType%d' % ptype)
        arr = np.zeros(0,dtype=np.float32)

    return np.asarray(arr)*h.convert


def hdf5_readmass(f,h,ptype):

    if ('PartType%d' % ptype) in f:
        ## check to see if mass block exists
        if HDF5_NAMES[h.reading] in f['PartType%d' % ptype]:
            arr = f['PartType%d/%s' % (ptype,HDF5_NAMES[h.reading])]
        else:
            if h.debug: print('could not locate PartType%d/%s' % (ptype,HDF5_NAMES[h.reading]))
            arr = np.zeros(h.npartThisFile[ptype],dtype=np.float32)
            arr.fill(h.massTable[ptype])
    else:
        if h.debug: print('coult not find PartType%d' % ptype)
        arr = np.zeros(0,dtype=np.float32)

    return np.asarray(arr)*h.convert


def hdf5_readmetals(f,h,ptype,single=1):
    
    if ('PartType%d' % ptype) in f:
        if HDF5_NAMES[h.reading] in f['PartType%d' % ptype]:
            metals = f['PartType%d/%s' % (ptype,HDF5_NAMES[h.reading])]
            if single and h.flag_metals == 11:  ## FROM GIZMO
                arr = metals[:,0]
            elif single and h.flag_metals > 1:
                arr = np.sum(metals,axis=1) * METALFACTOR
            else:
                arr = np.asarray(metals)
        else:
            if single:
                arr = np.zeros(h.npartThisFile[ptype],dtype=np.float32)
            else:
                arr = np.zeros((h.npartThisFile[ptype],h.flag_metals))
    else:
        if single:
            arr = np.zeros(0,dtype=np.float32)
        else:
            arr = np.zeros((0,h.flag_metals),dtype=np.float32)

    return arr


def hdf5_read(f,h,p):
    """Main driver for reading HDF5 files"""
    if h.reading == 'metallicity':
        arr = hdf5_readmetals(f,h,p)
    elif h.reading == 'metalarray':
        arr = hdf5_readmetals(f,h,p,single=0)
    elif h.reading == 'mass':
        arr = hdf5_readmass(f,h,p)
    else:
        arr = hdf5_general(f,h,p)

    return arr
