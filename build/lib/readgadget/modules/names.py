## default particle types
pTypes = {0:0,1:1,2:2,3:3,4:4,5:5,
          'gas':0,'dm':1,'disk':2,'bulge':3,'stars':4,'bndry':5}
# account for different names
pTypes['star'] = 4

pNames = {0:'GAS  ',
          1:'DM   ',
          2:'DISK ',
          3:'BULGE',
          4:'STAR ',
          5:'BNDRY'}

## default header returns (corresponds to h.header_vals[KEY])
headerTypes = {'npartThisFile':'npartThisFile',
               'npartTotal':'npartTotal',
               'ngas':'ngas',
               'ndm':'ndm',
               'ndisk':'ndisk',
               'nbulge':'nbulge',
               'nstar':'nstar',
               'nbndry':'nbndry',
               'massTable':'massTable',
               'time':'time',
               'nfiles':'nfiles',
               'redshift':'redshift',
               'boxsize':'boxsize',
               'O0':'O0',
               'Ol':'Ol',
               'h':'h',
               'flag_sfr':'flag_sfr',
               'flag_cooling':'flag_cooling',
               'flag_sfr':'flag_sfr',
               'flag_fb':'flag_fb',
               'flag_fh2':'flag_fh2',
               'flag_age':'flag_age',
               'flag_metals':'flag_metals',
               'flag_delaytime':'flag_delaytime',
               'flag_tmax':'flag_tmax',
               'flag_potential':'flag_potential',
               'rhocrit':'rhocrit'}
# account for different names
headerTypes['mass']          = 'massTable'
headerTypes['num_files']     = 'nfiles'
headerTypes['nstars']        = 'nstar'
headerTypes['gascount']      = 'ngas'
headerTypes['dmcount']       = 'ndm'
headerTypes['diskcount']     = 'ndisk'
headerTypes['bulgecount']    = 'nbulge'
headerTypes['bndrycount']    = 'nbndry'
headerTypes['starcount']     = 'nstar'
headerTypes['a']             = 'time'
headerTypes['z']             = 'redshift'
headerTypes['box']           = 'boxsize'
headerTypes['Omega0']        = 'O0'
headerTypes['OmegaLambda']   = 'Ol'
headerTypes['hubble']        = 'h'
headerTypes['flag_feedback'] = 'flag_fb'
headerTypes['f_sfr']         = 'flag_sfr'
headerTypes['f_fb']          = 'flag_fb'
headerTypes['f_cooling']     = 'flag_cooling'
headerTypes['f_age']         = 'flag_age'
headerTypes['f_fh2']         = 'flag_fh2'
headerTypes['f_metals']      = 'flag_metals'
headerTypes['npartThis']     = 'npartThisFile'
headerTypes['nparts']        = 'npartTotal'
headerTypes['npart']         = 'npartTotal'
headerTypes['rhoc']          = 'rhocrit'
headerTypes['header']        = ' '
headerTypes['Header']        = ' '


## default data types
# the VALUE here is the important part
dataTypes = {'pos':'pos',
             'vel':'vel',
             'pid':'pid',
             'mass':'mass',
             'u':'u',
             'rho':'rho',
             'ne':'ne',
             'nh':'nh',
             'hsml':'hsml',
             'sfr':'sfr',
             'delaytime':'delaytime',
             'fh2':'fh2',
             'sigma':'sigma',
             'age':'age',
             'z':'metallicity',
             'zarray':'metalarray',
             'tmax':'tmax',
             'nspawn':'nspawn',
             'pot':'pot'}
# account for different names
dataTypes['positions']  = 'pos'
dataTypes['vels']       = 'vel'
dataTypes['velocity']   = 'vel'
dataTypes['velocities'] = 'vel'
dataTypes['fH2']        = 'fh2'
dataTypes['FH2']        = 'fh2'
dataTypes['metals']     = 'metalarray'

## values used for output logging
dataNames = {'pos':'Positions',
             'vel':'Velocities',
             'pid':'Particle IDs',
             'mass':'Mass',
             'u':'Internal Energy',
             'rho':'Density',
             'ne':'Electron Abundance',
             'nh':'Neutral Hydrogen Density',
             'hsml':'Smoothing Length',
             'sfr':'Star Formation Rate',
             'delaytime':'Delay Time',
             'fh2':'Fractional H2 abundance',
             'sigma':'Surface Density',
             'age':'Stellar Age',
             'metallicity':'Metallicity',
             'metalarray':'Metal Array',
             'tmax':'Maximum Temperature',
             'nspawn':'Number of Stars Spawned',
             'pot':'Potential'}
dataDefaultUnits = {'sfr':'[Msun/yr]'}
dataUnits = {'vel':'[km/s, peculiar]',
             'mass':'[Msun/h]',
             'u':'[Kelvin]',
             'rho':'[h^2 g/cm^3, physical]',
             'sfr':'[Msun/yr]',
             'sigma':'[h g/cm^2, physical]'}


## properties that redirect to readgasprops()
GasProps     = ['u','rho','ne','nh','hsml','sfr',
                'delaytime','fh2','sigma']
GasStarProps = ['tmax','nspawn']
