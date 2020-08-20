import numpy as np
import os,sys
from . import common as c
from . import gadget_blockordering as gbo
import struct


class Header(object):
    def __init__(self,snap, filenum, *args):
        self.snap_passed = snap
        self.filenum     = filenum
        self.args        = args[0]

        self.setVars()
        fileType = self.detectFileType()
        if self.debug:
            print('detected file type %s' % fileType)

        if fileType == 'gadget':  
            self.read_gadget_header()
            if not hasattr(self,'BLOCKORDER'):
                self.BLOCKORDER = gbo.BLOCKORDERING[gbo.DEFAULT_BLOCKORDERING]
        elif fileType == 'hdf5':  self.read_hdf5_header()
        elif fileType == 'tipsy': self.read_tipsy_header()

        for i in range(0,5):
            if self.npartTotalHW[i] > 0:
                self.npartTotal[i] += (self.npartTotalHW[i] << 32)

        self.calcRhoCrit()

        ## assign dictionary
        self.header_vals = {'npartThisFile':self.npartThisFile,
                            'npartTotal':self.npartTotal,
                            'npartTotalHW':self.npartTotalHW,
                            'ngas':self.npartTotal[0],'ndm':self.npartTotal[1],
                            'ndisk':self.npartTotal[2],'nbulge':self.npartTotal[3],
                            'nstar':self.npartTotal[4],'nbndry':self.npartTotal[5],
                            'massTable':self.massTable,
                            'time':self.time,
                            'nfiles':self.nfiles,
                            'redshift':self.redshift,
                            'boxsize':self.boxsize,
                            'O0':self.Omega0,
                            'Ol':self.OmegaLambda,
                            'h':self.HubbleParam,
                            'flag_cooling':self.flag_cool,
                            'flag_sfr':self.flag_sfr,
                            'flag_fb':self.flag_fb,
                            'flag_fh2':self.flag_fH2,
                            'flag_age':self.flag_age,
                            'flag_metals':self.flag_metals,
                            'flag_potential':self.flag_potential,
                            'flag_delaytime':self.flag_delaytime,
                            'flag_tmax':self.flag_tmax,
                            'rhocrit':self.rhocrit}

    def calcRhoCrit(self):
        H0  = self.HubbleParam * 100.
        Hz  = H0 * np.sqrt(self.OmegaLambda + self.Omega0 * (1.+self.redshift)**3)
        Hz /= 3.08567758e19  ## 1/s
        G   = 6.674e-8       ## cm^3/g/s^2

        self.rhocrit = 3. * Hz**2 / (8. * np.pi * G)

    def setVars(self):
        ## nth particle ##
        self.nth = 1
        if 'nth' in self.args and self.args['nth'] > 1:
            self.nth = self.args['nth']

        ## single file read?  ignore multi-part ##
        self.singleFile = False
        if 'single' in self.args and self.args['single'] == 1:
            self.singleFile = True

        ## debug? ##
        self.debug = False
        if 'debug' in self.args and self.args['debug'] == 1:
            self.debug = True

        ## unit conversions? ##
        self.units = False
        if 'units' in self.args and self.args['units'] == 1:
            self.units = True
        
        ## allow for different block ordering on the fly ##
        if 'blockordering' in self.args:
            self.BLOCKORDER = gbo.BLOCKORDERING[self.args['blockordering']]

        ## supress output? ##
        self.suppress = False
        if( ('supress_output' in self.args and self.args['supress_output'] == 1) or
            ('suppress_output' in self.args and self.args['suppress_output'] == 1) or
            ('suppress' in self.args and self.args['suppress'] == 1) ):
            self.suppress = True

        ## return double array? ##
        self.double = False
        if 'double' in self.args and self.args['double'] == 1:
            self.double = True

        self.UnitMass_in_g = c.UnitMass_in_g
        self.UnitLength_in_cm = c.UnitLength_in_cm
        self.UnitVelocity_in_cm_per_s = c.UnitVelocity_in_cm_per_s        
        
        if 'UnitMass_in_g' in self.args:
            self.UnitMass_in_g = self.args['UnitMass_in_g']
        if 'UnitLength_in_cm' in self.args:
            self.UnitLength_in_cm = self.args['UnitLength_in_cm']
        if 'UnitVelocity_in_cm_per_s' in self.args:
            self.UnitVelocity_in_cm_per_s = self.args['UnitVelocity_in_cm_per_s']



    def detectFileType(self):
        snap  = self.snap_passed
        fn    = self.filenum
        FTYPE = None

        ## only for reading single (from multi-part)
        if self.singleFile:
            if '.hdf5' in snap:
                FTYPE = 'hdf5'
            elif '.bin' in snap:
                FTYPE = 'tipsy'
            else:
                FTYPE = 'gadget'
            self.snap = snap
            return FTYPE

        ## strip extensions
        if '.0.hdf5' in snap:
            snap = snap[:-7]
        elif '.hdf5' in snap:
            snap = snap[:-5]
        elif '.bin' in snap:
            snap = snap[:-4]
        elif snap[-2:] == '.0':
            snap = snap[:-2]            

        ## detect file type ##

        # gadget
        if os.path.isfile(snap):
            FTYPE = 'gadget'
            self.snap = snap
        elif os.path.isfile('%s.%d' % (snap,fn)):
            FTYPE = 'gadget'
            self.snap = '%s.%d' % (snap,fn)

        # hdf5
        elif os.path.isfile('%s.hdf5' % snap):
            FTYPE = 'hdf5'
            self.snap = '%s.hdf5' % snap
        elif os.path.isfile('%s.%d.hdf5' % (snap,fn)):
            FTYPE = 'hdf5'
            self.snap = '%s.%d.hdf5' % (snap,fn)
            
        # tipsy
        elif os.path.isfile('%s.bin' % snap):
            FTYPE = 'tipsy'
            self.snap = '%s.bin' % snap

        else:
            print('Could not determine file type by extension!')
            sys.exit()

        return FTYPE

    def read_gadget_header(self):
        from . import gadget1 as g
        f = open(self.snap,'rb')
        self.f = f

        ## test for type 2 ##
        if np.fromfile(f,dtype=np.uint32,count=1)[0] == 8:
            NAME = struct.unpack('4s',f.read(4))[0]
            np.fromfile(f,dtype=np.uint32,count=1)
            np.fromfile(f,dtype=np.uint32,count=1)
            self.fileType = 'gadget2'
        else:
            f.seek(0)
            self.fileType = 'gadget1'

        skip1 = g.skip(f)
        self.npartThisFile = np.fromfile(f,dtype=np.uint32,count=6)
        self.massTable     = np.fromfile(f,dtype=np.float64,count=6)
        self.time          = np.fromfile(f,dtype=np.float64,count=1)[0]
        self.redshift      = np.fromfile(f,dtype=np.float64,count=1)[0]
        self.flag_sfr      = np.fromfile(f,dtype=np.int32,count=1)[0]
        self.flag_fb       = np.fromfile(f,dtype=np.int32,count=1)[0]
        self.npartTotal    = np.fromfile(f,dtype=np.uint32,count=6)
        self.flag_cool     = np.fromfile(f,dtype=np.int32,count=1)[0]
        self.nfiles        = np.fromfile(f,dtype=np.int32,count=1)[0]
        self.boxsize       = np.fromfile(f,dtype=np.float64,count=1)[0]
        self.Omega0        = np.fromfile(f,dtype=np.float64,count=1)[0]
        self.OmegaLambda   = np.fromfile(f,dtype=np.float64,count=1)[0]
        self.HubbleParam   = np.fromfile(f,dtype=np.float64,count=1)[0]
        self.flag_age      = np.fromfile(f,dtype=np.int32,count=1)[0]
        self.flag_metals   = np.fromfile(f,dtype=np.int32,count=1)[0]
        self.npartTotalHW  = np.fromfile(f,dtype=np.uint32,count=6)
        self.flag_entropy         = np.fromfile(f,dtype=np.int32,count=1)[0]
        self.flag_doubleprecision = np.fromfile(f,dtype=np.int32,count=1)[0]
        self.flag_potential       = np.fromfile(f,dtype=np.int32,count=1)[0]
        self.flag_fH2             = np.fromfile(f,dtype=np.int32,count=1)[0]
        self.flag_tmax            = np.fromfile(f,dtype=np.int32,count=1)[0]
        self.flag_delaytime       = np.fromfile(f,dtype=np.int32,count=1)[0]
        bl = 256
        if self.fileType == 'gadget2':
            bl += 4 + 4 + 4 + 4
        bytes_left = bl + 4 - f.tell()
        f.seek(bytes_left,1)
        skip2 = g.skip(f)
        g.errorcheck(skip1,skip2,'header')

        ## determine data type ##
        if self.fileType == 'gadget2':
            f.seek(4 + 4 + 4 + 4,1)
        nbytes = np.fromfile(f,dtype=np.uint32,count=1)[0]
        ntot   = np.sum(self.npartThisFile)
        if nbytes / (ntot * 4 * 3) == 1:
            self.dataType = np.float32
        elif nbytes / (ntot * 8 * 3) == 1:
            self.dataType = np.float64
        else:
            print('could not determine data type!')
            sys.exit()
        f.seek(-4,1)
        if self.fileType == 'gadget2':
            f.seek(-16,1)

        return

    def read_hdf5_header(self):
        self.fileType = 'hdf5'
        import h5py as h5py
        f = h5py.File(self.snap,'r')
        self.f = f

        hd = f['Header']
        ha = hd.attrs

        self.npartThisFile = ha['NumPart_ThisFile']
        self.massTable     = ha['MassTable']
        self.time          = ha['Time']
        self.redshift      = ha['Redshift']
        self.flag_sfr      = ha['Flag_Sfr']
        self.flag_fb       = ha['Flag_Feedback']
        self.npartTotal    = ha['NumPart_Total']
        self.flag_cool     = ha['Flag_Cooling']
        self.nfiles        = ha['NumFilesPerSnapshot']
        self.boxsize       = ha['BoxSize']
        self.Omega0        = ha['Omega0']
        self.OmegaLambda   = ha['OmegaLambda']
        self.HubbleParam   = ha['HubbleParam']
        self.flag_age      = ha['Flag_StellarAge']
        self.flag_metals   = ha['Flag_Metals']
        self.npartTotalHW  = ha['NumPart_Total_HighWord']

        if 'PartType0/Potential' in f:
            self.flag_potential   = 1
        else:
            self.flag_potential   = 0
        if 'PartType0/FractionH2' in f:
            self.flag_fH2         = 1
        else:
            self.flag_fH2         = 0
        if 'PartType0/TemperatureMax' in f:
            self.flag_tmax        = 1
        else:
            self.flag_tmax        = 0
        if 'PartType0/DelayTime' in f:
            self.flag_delaytime   = 1
        else:
            self.flag_delaytime   = 0

        return

    def read_tipsy_header(self):
        self.fileType = 'tipsy'
        f = open(self.snap,'rb')
        self.f    = f
        self.time = np.fromfile(f,dtype=np.float64,count=1)[0]
        ntotal    = np.fromfile(f,dtype=np.int32,count=1)[0]
        ndim      = np.fromfile(f,dtype=np.int32,count=1)[0]
        ngas      = np.fromfile(f,dtype=np.int32,count=1)[0]
        ndark     = np.fromfile(f,dtype=np.int32,count=1)[0]
        nstar     = np.fromfile(f,dtype=np.int32,count=1)[0]
        alignment = np.fromfile(f,dtype=np.float32,count=1)
        
        self.npartThisFile = [ngas,ndark,0,0,nstar,0]
        self.npartTotal    = [ngas,ndark,0,0,nstar,0]
        self.massTable     = [0.,0.,0.,0.,0.,0.]
        self.redshift      = 1.0 / self.time - 1.0
        self.flag_sfr      = 1
        self.flag_fb       = 1
        self.flag_cool     = 1
        self.nfiles        = 1
        self.boxsize       = 0.0
        self.Omega0        = 0.0
        self.OmegaLambda   = 0.0
        self.HubbleParam   = 0.0
        self.flag_age      = 1
        self.flag_metals   = 1
        self.npartTotalHW  = [0,0,0,0,0,0]
        self.flag_entropy  = 0
        self.flag_doubleprecision = 0
        self.flag_potential = 1
        self.flag_fH2    = 0
        self.flag_tmax   = 1
        self.flag_delaytime = 1

        return
