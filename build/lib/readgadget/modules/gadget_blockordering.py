from collections import OrderedDict

#############################################
## for gadget type-1 binary block ordering ##
#############################################
## you can easily add your own block ordering!  
# duplicate one of the below, then modify it to
# match your sims.  Don't forget to add yours
# to the dict BLOCKORDERING.
#
# Format of block ordering looks like this:
#
# (BlockName, [ParticleTypes,FlagsToCheck])
#
# -> BlockName : string
#    must be equal to those in dataTypes value
#    (value!!, not key, see below)
# -> ParticleTypes : integer list
#    defines what types of particles have this block
#    -1 means ALL particles
# -> FlagsToCheck : string
#    which flags (if any) to check that determine if block
#    is present
#############################################

## sets the default ordering
DEFAULT_BLOCKORDERING = 'romeel'

## Romeel's block ordering
BLOCKORDERING0 = OrderedDict([
    ('pos' ,[-1]),
    ('vel' ,[-1]),
    ('pid' ,[-1]),
    ('mass',[-1]),
    ('u'   ,[0]),
    ('rho' ,[0]),
    ('ne'  ,[0]),
    ('nh'  ,[0]),
    ('hsml',[0]),
    ('sfr' ,[0]),
    ('delaytime',  [0,'flag_delaytime']),
    ('fh2'  ,      [ 0,'flag_fh2']),
    ('sigma',      [ 0,'flag_fh2']),
    ('age' ,       [ 4,'flag_age']),
    ('metallicity',[[0,4],'flag_metals']),
    ('tmax',       [[0,4],'flag_tmax']),
    ('nspawn',     [[0,4]]),
    ('pot',        [-1,'flag_potential'])
])

## Ben's block ordering
BLOCKORDERING2 = OrderedDict([
    ('pos' ,[-1]),
    ('vel' ,[-1]),
    ('pid' ,[-1]),
    ('mass',[-1]),
    ('pot' ,[-1]),
    ('u'   ,[0]),
    ('rho' ,[0]),
    ('ne'  ,[0]),
    ('nh'  ,[0]),
    ('hsml',[0]),
    ('sfr' ,[0]),
    ('delaytime',  [0,'flag_delaytime']),
    ('fh2'  ,      [ 0,'flag_fh2']),
    ('sigma',      [ 0,'flag_fh2']),
    ('age' ,       [ 4,'flag_age']),
    ('metallicity',[[0,4],'flag_metals']),
    ('tmax',       [[0,4],'flag_tmax']),
    ('nspawn',     [[0,4]]),
])

## Ken's block ordering
BLOCKORDERING1 = OrderedDict([
    ('pos' ,[-1]),
    ('vel' ,[-1]),
    ('pid' ,[-1]),
    ('mass',[-1]),
    ('u'   ,[0]),
    ('rho' ,[0]),
    ('ne'  ,[0]),
    ('nh'  ,[0]),
    ('hsml',[0]),
    ('sfr' ,[0]),
    ('age' ,       [ 4,'flag_age']),
    ('metallicity',[[0,4],'flag_metals']),
    ('fh2'  ,      [ 0,'flag_fh2']),
    ('sigma',      [ 0,'flag_fh2']),
    ('pot',        [-1,'flag_potential'])
])

## NAME THE BLOCK ORDERINGS ##
BLOCKORDERING = {'romeel':BLOCKORDERING0,
                 'ken'   :BLOCKORDERING1,
                 'ben'   :BLOCKORDERING2}
