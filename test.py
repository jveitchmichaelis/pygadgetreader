import sys
sys.path.insert(0,'../')

#from readgadget import *
from pygadgetreader import *
from pylab import *
import numpy as np

DB     = 1
UNITS  = 1
SINGLE = 0
SUP    = 0
NTH    = 1

G1  = 0
G1M = 0
G2  = 1
G2M = 0
H5  = 0
H5M = 0


bd = '/Users/bob/RAID5/Research/FILETYPES'

pygro = {'units':UNITS,'debug':DB,'single':SINGLE,'suppress':SUP,'nth':NTH}

## G1
if G1:
    print('')
    print('GADGET TYPE 1')
    snap = '%s/gadget/g1/snap_N128L16_037' % bd
    z    = readhead(snap,'redshift')
    h    = readhead(snap,'header')
    gpid = readsnap(snap,'pid','gas',**pygro)
    rho  = readsnap(snap,'rho','gas',**pygro)
    u    = readsnap(snap,'u','gas',**pygro)
    fig=figure()
    plot(np.log10(rho),np.log10(u),'o',ms=1)
    title(r'GadgetType1')


# G1 MULTI
if G1M:
    print('')
    print('GADGET TYPE 1-MULTI')
    snap = '%s/gadget/g1/multi/snap_N64L10_006' % bd
    npart = readhead(snap,'npartThis')
    rho = readsnap(snap,'rho','gas',**pygro)
    u   = readsnap(snap,'u','gas',**pygro)
    print(len(rho))
    fig=figure()
    plot(np.log10(rho),np.log10(u),'o',ms=1)
    title(r'GadgetType1-Multi')

## G2
if G2:
    print('')
    print('GADGET TYPE 2')
    snap = '%s/gadget/g2/snap_lowres_030' % bd
    #rho = readsnap(snap,'RH','gas',units=UNITS,debug=DB)
    rho = readsnap(snap,'rho','gas',**pygro)
    u   = readsnap(snap,'u','gas',**pygro)
    #m   = readsnap(snap,'mass','gas',units=UNITS,debug=DB)
    pot = readsnap(snap,'ABVC','gas',**pygro)
    fig=figure()
    plot(np.log10(rho),np.log10(u),'o',ms=1)
    title(r'GadgetType2')

# G2 MULTI
if G2M:
    print('')
    print('GADGET TYPE 2-MULTI')
    snap = '%s/gadget/g2/multi/snap_lowres_030' % bd
    rho = readsnap(snap,'rho','gas',**pygro)
    u   = readsnap(snap,'u','gas',**pygro)
    fig=figure()
    plot(np.log10(rho),np.log10(u),'o',ms=1)
    title(r'GadgetType2-Multi')

## HDF5
if H5:
    print('')
    print('HDF5')
    snap = '%s/hdf5/snap_N128L16_037' % bd
    rho = readsnap(snap,'rho','gas',**pygro)
    u   = readsnap(snap,'u','gas',**pygro)
    fig=figure()
    plot(np.log10(rho),np.log10(u),'o',ms=1)
    title(r'HDF5')


# HDF5 multi
if H5M:
    print('')
    print('HDF5 MULTI')
    snap = '%s/hdf5/multi/snap_N128L16_037' % bd
    for i in range(0,4):
        print(readhead('%s.%d.hdf5' % (snap,i),'npartThisFile'))
    rho = readsnap(snap,'rho','gas',**pygro)
    u   = readsnap(snap,'u','gas',**pygro)
    fig=figure()
    plot(np.log10(rho),np.log10(u),'o',ms=1)
    title(r'HDF5-Multi')


show()
sys.exit()
