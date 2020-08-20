import numpy as np
import sys
from .names import *

METALFACTOR = 0.0189/0.0147
H_MASSFRAC  = 0.76
BOLTZMANN   = 1.3806e-16
PROTONMASS  = 1.6726e-24
GAMMA       = 5.0 / 3.0

UnitLength_in_cm         = 3.085678e21
UnitMass_in_g            = 1.989e43
UnitVelocity_in_cm_per_s = 1.0e5


RecognizedOptions = ['units',
                     'hdf5',
                     'tipsy',
                     'single',
                     'suppress',
                     'suppress_output',
                     'supress_output',
                     'blockordering',
                     'debug',
                     'double',
                     'nth']
def pollOptions(h,KWARGS,data,ptype):
    """warn user if option is unrecognized"""
    for key,items in KWARGS.items():
        if key not in RecognizedOptions:
            print('WARNING!! option not recognized: %s' % key)

    d = data
    p = ptype

    kill = 0
    if data not in dataTypes:
        if h.fileType != 'hdf5' and h.fileType != 'gadget2':
          print('ERROR! %s not a recognized data request' % data)
          kill = 1
        if h.fileType == 'gadget2':
            if len(d) < 4:
                d += ' '*(4-len(d))
            elif len(d) > 4:
                d = d[0:4]
    else:
        d = dataTypes[d]

    if ptype not in pTypes:
        print('ERROR! %s not a recognized particle type' % ptype)
        kill = 1
    else:
        p = pTypes[p]

    if kill:
        sys.exit()

    return d,p

def pollHeaderOptions(h,data):
    """make sure we're returning proper header value"""
    if data not in headerTypes:
        print('ERROR! %s not a recognized header value' % data)
        sys.exit()

def initUnits(h):
    """initialize conversion factors"""
    convert = 1.0

    if h.units and h.fileType != 'tipsy':
        if h.reading == 'rho':
            if h.boxsize > 0. and h.OmegaLambda > 0:
                convert = ((1.0 + h.redshift)**3 * 
                           h.UnitMass_in_g / h.UnitLength_in_cm**3)
            else:
                convert = h.UnitMass_in_g / h.UnitLength_in_cm**3
        elif h.reading == 'vel':
            if h.boxsize > 0. and h.Ol > 0:
                convert = np.sqrt(h.time)
        elif h.reading == 'sigma':
            convert = h.UnitMass_in_g / h.UnitLength_in_cm**2
        elif h.reading == 'u':
            h.UnitTime_in_s = h.UnitLength_in_cm / h.UnitVelocity_in_cm_per_s
            h.UnitEnergy_in_cgs = (h.UnitMass_in_g * h.UnitLength_in_cm**2 / 
                                   h.UnitTime_in_s**2)
        elif h.reading == 'mass':
            convert = h.UnitMass_in_g/1.989e33
        
    if h.reading == 'pid':
        convert = 1
    h.convert = convert


def getTfactor(Ne,h):
    """calculate temperature conversion factor including Ne"""
    MeanWeight = (4.0 / (3.0 * H_MASSFRAC + 1.0 + 4.0 * H_MASSFRAC * Ne) * 
                  PROTONMASS)
    conversion = (MeanWeight / BOLTZMANN * (GAMMA - 1.0) * 
                  h.UnitEnergy_in_cgs / h.UnitMass_in_g)
    return conversion
def getTfactorNoNe():
    """calculate temperature conversion factor withOUT Ne"""
    conversion = (GAMMA-1.0) * (PROTONMASS/BOLTZMANN) * 1.0e5**2
    return conversion

def gadgetPrinter(h,d,p):

    printer = ''

    if d not in dataNames and (h.fileType == 'hdf5' or h.fileType == 'gadget2'):
        printer = 'Returning %s %s' % (pNames[p],d)
    else:
        printer = 'Returning %s %s' % (pNames[p],dataNames[d])

        if h.units:
            if d in dataUnits:
                if d == 'u':
                    printer = 'Returning %s Temperature %s' % (pNames[p],dataUnits[d])
                else:
                    printer = '%s %s' % (printer, dataUnits[d])
            else:
                if d in dataDefaultUnits:
                    printer = '%s %s' % (printer,dataDefaultUnits[d])
                else:
                    printer = '%s in code units' % printer
    if h.suppress:
        return
    else:
        print(printer)
