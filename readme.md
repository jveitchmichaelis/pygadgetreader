# pyGadgetReader
Author: Robert Thompson

E-Mail: rthompsonj@gmail.com

If you use this code for your work please cite [[ascl:1411.001](http://ascl.net/1411.001)]

---

# Contents
* [Summary](#markdown-header-summary)
* [Requirements](#markdown-header-requirements)
* [Obtaining and Updating](#markdown-header-obtaining-and-updating)
* [Customization](#markdown-header-customization)
* [Installation](#markdown-header-installation)
* [Usage](#markdown-header-usage)
	 * [readheader()](#markdown-header-readheader)
	 * [readsnap()](#markdown-header-readsnap) 
	 * [readrockstar()](#markdown-header-readrockstar) 
	 * [readrockstargalaxies()](#markdown-header-readrockstargalaxies)
	 * [readfofspecial()](#markdown-header-readfofspecial)
	 * [readpstar()](#markdown-header-readpstar)
* [Tips](#markdown-header-tips)

---
## Summary
Do you *love* running simulations but *hate* fighting with the different flavors of output?  If so, you've come to the right place!  `pyGadgetReader` is designed to take the headache out of reading your `GADGET` simulation data; it plays the role of interpreter between the binary snapshot & `python`.  The module currently supports the following data types:

- **Gadget** types 1 & 2 binaries (single/multi-part)
- **HDF5** outputs (single/multi-part)
- **TIPSY** binaries (bin/aux)

`pyGadgetReader` attempts to detect which file format is is dealing with so you don't have to!  It does however, assume that the different formats have unique file extensions (*none*,`.hdf5`,& `.bin`).  

`pyGadgetReader` also supports the following non-GADGET files:

- **Rockstar** binary outputs
- **Rockstar-Galaxies** binary outputs
- **FoF Special** catalogue & indexlist binaries
- **P-StarGroupFinder** data files

---
## Requirements
* python >= 2.7.x
* numpy >= 1.7.x
* h5py

---
## Obtaining and Updating
The easiest way to download the code and stay up to date is to clone a version from [bitbucket](https://bitbucket.org/rthompson/pygadgetreader) to your local computer via Mercurial (hg):
~~~Bash
> hg clone https://bitbucket.org/rthompson/pygadgetreader
~~~

To update all you need to do is:
~~~Bash
> hg pull
> hg up
(reinstall)
~~~

---
## Customization
Before building the module, there are a few customizations you *may* want to tinker with.  The first two variables can be found in *`readgadget/modules/common.py`*, while the third is located in *`readgadget/modules/gadget_blockordering.py`*.

1. **UNITS:**  The code currently assumes that your **default** `Gadget` length units are `kpc/h`, mass units are 10^(10)`Msun/h`, and velocity units are `km/s`.  This can be changed by modifying the *`UnitLength_in_cm`*, *`UnitMass_in_g`*, and *`UnitVelocity_in_cm_per_s`* respectively in `readgadget/modules/common.py`.  This can optionally be altered on a per-call basis by passing new values through as an option to the `readsnap()` function. (*note: has NO impact on TIPSY files as of now*)

2. **METALFACTOR:**  If your metal field contains multiple species `(flag_metals > 1)`, this factor is multiplied to their sum to determine the particle's overall metallicity (default is 0.0189/0.0147 for historical reasons).

3. **BLOCKORDERING:** When dealing with `Gadget` **type-1 binaries**, the block-ordering can be a pain in the neck.  Custom fields can be added the snapshot causing all of your previous readers to start returning bad data; not anymore!  I've tried to design a system where the user can easily customize their block ordering.  `pyGadgetReader` currently has 2 default options - `BLOCKORDERING0` and `BLOCKORDERING1`.  The default is set via the `DEFAULT_BLOCKORDERING` variable, which is used in conjunction with the `BLOCKORDERING` dictionary defined farther down in the file.  This can be changed by editing `readgadget/modules/gadget_blockordering.py`.

    If you require a custom block ordering, use one of the already present block orderings as a template.  The first step is creating a new `OrderedDict` named something along the lines of `BLOCKORDERING3`.  Each entry in the `OrderedDict` represents a data block, and must contain both a *KEY* and a *VALUE*.  Once your new block ordering is defined, you should add it to the `BLOCKORDERING` dictionary with an appropriate name.  You can also set it as default via the `DEFAULT_BLOCKORDERING` variable if you so wish.

    **KEY:** This is the name of the block - it MUST be present as a value in the `dataTypes` dictionary defined in `readgadget/modules/names.py`.

    **VALUE:** This is a list that contains 2 important pieces of information: 1) what particles this block is present for, and 2) should the code first check for a specific header flag?

	Below are two examples.  The first represents the 'pos' block (which is present in the `dataTypes` dictionary).  The second entry is a list telling the code what particle types have this block, where -1 meaning ALL particle types.  The second represents the 'metallicity' data block; here we have a list of [0,4] telling the code that this block is present for particle types 0 (gas) & 4 (stars), and to check the `flag_metals` flag before attempting a read.  You can omit the flag checker if you know for certain the data block exists.

~~~python
('pos',[-1]),
('metallicity',[[0,4],'flag_metals']),
~~~

---
## Installation
Once the code is downloaded there are two methods of installation depending on your access rights.  If you have write access to your python distribution, then the preferred method is to execute the following commands:

~~~Bash
	> python setup.py build     ## this builds the module
	> python setup.py install   ## this installs the module, may require sudo
~~~

If you do *not* have write access to your python install, we need to modify your environment variable `PYTHONPATH` to point to the pyGadgetReader directory.  Add these two lines to your `.bashrc/.bash_profile` (or respective shell file):

~~~Bash
PYTHONPATH=/path/to/pygadgetreader:$PYTHONPATH
export PYTHONPATH
~~~

****
#### NOTE for uninstalling previous versions:
If you had previously installed my `C` version of `pyGadgetReader` you should *remove* it before trying to use the code as there may be some naming conflicts.  First you need to find out *where* python, a point in the general direction is typing `which python` in your terminal, this will return your installation directory.  Next you need to locate your `site-packages` directory which is usually under python's `lib` directory.  Once there you are looking for anything in the form of `readgadget.so`, once this is found remove it.

---
## Usage
**IMPORTANT:** When using `pyGadgetReader`, **try NOT to include** the snapshot extension or number prefix (for multi-part).  As an example, if your snapshot is named `'snap_N128L16_005.0.hdf5'`, you would only pass `'snap_N128L16_005'` to the below functions.  If the code detects `.hdf5`, `.bin`, or `.0` in the snapname it will attempt to strip the extension.

To gain access to the following functions, place this at the top of your python script:

~~~python
from pygadgetreader import *
~~~

---
## readheader()
This function reads in the header and returns values of interest.  The values it can read in are as follows:

	 time	       - scale factor of the snapshot
	 redshift      - redshift of the snapshot
	 boxsize       - boxsize if present (typically in kpc/h)
	 O0	       	   - Omega_0 (Omega_dm+Omega_b)
	 Ol	       	   - Omega_Lambda
	 h	       	   - hubble parameter
	 gascount      - total # of gas   particles [type 0]
	 dmcount       - total # of DM    particles [type 1]
	 diskcount     - total # of disk  particles [type 2]
	 bulgecount    - total # of bulge particles [type 3]
	 starcount     - total # of star  particles [type 4]
	 bndrycount    - total # of bndry particles [type 5]
	 f_sfr	       - Star Formation Rate flag	 0=off 1=on
	 f_fb	       - Feedback flag	     		 0=off 1=on
	 f_cooling     - Cooling flag			 	 0=off 1=on 
	 f_age	       - Stellar Age tracking flag	 0=off 1=on
	 f_metals      - Metal tracking flag  		 0=off 1=on

	 npartTotal    - list of particle counts (including HighWord)
	 header		   - returns the entire header as a dictionary
	 
 	 npartThisFile - list of particle counts in a single file
	                 (you MUST pass the full snapshot name for this one, 
	                  otherwise it will return data from file .0)

**DEFINITION:**

		readheader(a,b,debug=0,single=0)

		Parameters
	   	----------
	   	a : string
	   	    Input file
		b : string
		    Requested data type (from above list)

		Optional
		--------
		debug: output debugging info

		Returns
		-------
		float, double, int, list, array, dict (depending on request)

		Examples
		--------
		>>> readheader('snap_001','redshift')
			2.3499995966280447

		>>> readheader('snap_005','npartTotal')
			array([  53921,   54480,       0,       0,    3510, 2090342], dtype=uint32)
		
		>>> readheader('snap_006','header')
			{'O0': 0.29999999999999999,
			 'Ol': 0.69999999999999996,
 			 'boxsize': 16000.0,
			 'h': 0.69999999999999996,
 			 'massTable': array([ 0.,  0.00172772,  0.,  0.,  0., 0.01626092]),
			  ...,
			 'time': 0.29850749862971743}

---
## readsnap()
This function does the heavy lifting.  It reads data blocks from the snapshot and returns the requested data for a a specified particle type.

**SUPPORTED DATA BLOCKS:**
          
	  ---------------------
	  -  STANDARD BLOCKS  -
  	  ---------------------
	   pos	       - (all)         Position data
	   vel	       - (all)         Velocity data code units
	   pid	       - (all)         Particle ids
	   mass	       - (all)         Particle masses
	   u	       - (gas)         Internal energy
	   rho	       - (gas)         Density
	   ne	       - (gas)         Number density of free electrons
	   nh	       - (gas)         Number density of neutral hydrogen
	   hsml	       - (gas)         Smoothing length of SPH particles
	   sfr	       - (gas)         Star formation rate in Msun/year
	   age	       - (stars)       Formation time of stellar particles
 	   z	       - (gas & stars) Metallicty of gas/star particles (returns total Z)
	   pot   	   - (all)         Potential of particles (if present in output)

	  ---------------------
	  -  CUSTOM  BLOCKS   -
  	  ---------------------
	   delaytime   - (gas)         DelayTime (>0 member of wind)
	   fH2	       - (gas)         Fractional Abundance of molecular hydrogen
	   Sigma       - (gas)         Approximate surface density	   
	   tmax        - (gas & stars) Maximum temp
	   nspawn      - (gas & stars) Number of star particles spawned
	   zarray      - (gas & stars) NMETALS array [C,O,Si,Fe]


**SUPPORTED PARTICLE TYPES:**

	   gas	       - Type0: Gas
	   dm	       - Type1: Dark Matter
	   disk	       - Type2: Disk particles
	   bulge       - Type3: Bulge particles
	   star        - Type4: Star particles
	   bndry       - Type5: Boundary particles
	   

**DEFINITION:**

        readsnap(a,b,c,units=0,debug=0,suppress=0,
		    		   double=0,nth=1,single=0,
			    	   blockordering='romeel',
				       UnitLength_in_cm = 3.085678e21,
					   UnitMass_in_g = 1.989e43,
					   UnitVelocity_in_cm_per_s = 1.0e5)

		Parameters
		----------
		a : string
			Input File
		b : string
			Requested data block (from supported data blocks above)
		c : string, int
			Requested particle type (from supported particle types above)
		
		Optional
		--------
		     debug: Shows debug information
          suppress: if set to 1 no output is printed to the command line
            double: returns a double array rather than float
 	           nth: only returns the nth particle (useful for random sampling)
 	        single: returns data from 1 part of a multi-part snapshot
 	                (in this case you MUST pass the full snapshot name)
	 blockordering: allows for the user to specify which block ordering to use
					(only valid for Gadget type-1 binaries)

		     units: Can either be 0 for code units or 1 physical:
		     		 rho: g/cm^3 (physical if boxsize>0 and OmegaLambda>0)
		     	 	 vel: km/s   (peculiar if boxsize>0 and OmegaLambda>0)
		     		   u: Kelvin
		     		mass: g
					(returned units do NOT include little h, 
					 that still needs to be divided out)

			  
		Returns
		-------
		numpy array
			  
		Examples
		--------
		>>> readsnap('snap_001','pos','dm')
			array([[ 7160.68994141,  6526.55810547,  5950.74707031],
		   		   [ 7097.95166016,  6589.15966797,  5958.44677734],
   					...,
			       [ 7929.03466797,  7870.52783203,  8016.08447266]], dtype=float32)

		>>> readsnap('snap_005','rho',0,units=1)
			array([  1.60686842e-09,   3.20981991e-10,   1.59671165e-10, ...,
      				 4.05850381e-10,   7.22671034e-10,   1.10464858e-11], dtype=float32)
      				 

**NOTE** for `HDF5` and `Gadget-Type2` files: *you can pass arbitrary block requests in for `b` above, this allows you to pull custom data blocks out without having to alter the source. As an example:*

	# hdf5
    >>> readsnap('snap_036','ArtificialViscosity',0)
        array([ 0.2,  0.2,  0.2, ...,  0.2, 0.2,  0.21387598], dtype=float32)
        
    # gadget type-2 binary (limited to 4 characters)
    >>> readsnap('snap_036','ABVC',0)
        array([ 0.38793027,  0.48951781,  0.37891224, ...,  0.2301995], dtype=float32)

---
## readrockstar()
This function reads `Rockstar` binary data.  **Current supported return data types:**

	   	halos		- All halo data
	   	particles 	- particle IDs & respective halo membership

		pos
		corevel
		bulkvel
		m
		r
		child_r
		vmax_r
		mgrav
		vrmax
		rvmax
		rs
		klypin_rs
		vrms
		J
		energy
		spin
		alt_m
		Xoff
		Voff
		b_to_a
		c_to_a
		A
		b_to_a2
		c_to_a2
		A2
		bullock_spin
		kin_to_pot
		m_pe_b
		m_pe_d
		halfmass_radius (only avail with recent versions)
		num_p
		num_child_particles
		p_start
		desc
		flags
		n_core
		min_pos_err
		min_vel_err
		min_bulkvel_err

**DEFINITION:**

		readrockstar(a,b,debug=0,galaxies=0)

		Parameters
		----------
		a : string
		    Input binary file. Do NOT include the number or .bin extensions!!
		b : string
			Data block you are interested in (see above list)
					  
		Optional
		--------
		     debug: Shows debug information
		  galaxies: Invokes the RS-Galaxies reader if = 1
					    
		Returns
		-------
		array, dict
		
		Examples
		--------
		## returns all halo data
		>>> readrockstar('halos_037','halos')
			array([ (0, [7.364242076873779, 6.997755527496338, 7.268182754516602, 19.809770584106445,...
		
		## only returns halo position data
		>>> readrockstar('halos_037','pos')
			array([[   7.36424208,    6.99775553,    7.26818275,   19.80977058,
          			-2.92877913,  -95.81005859],...

		## returns particle data	
		## [i,0]=particle ID, [i,1]=halo ID
		>>> readrockstar('halos_037','particles')			
			array([[ 62336,      0],
			       [ 63438,      0],
	       			...,
			       [105530,    103]])

---
## readrockstargalaxies()
Identical usage as `readrockstar()`, except only to be used on `Rockstar-Galaxies` binary files.

---
## readfofspecial()
This function reads `FoF_Special` binary outputs (indexlists & catalogues).  It returns a `Group` object, or a list of `Group` objects, all of which have **three** attributes:

	 index         - group index
	 npart_total   - total number of group particles
	 indexes       - indexes of all particles belonging to group

**DEFINITION:**

    	  readfofspecial(a,b,c)

	      Parameters
	      ----------
	      a : string
	      	  Group catalogue directory
		  b : int
	   	      Snapshot number
	   	  c : int, list
	   	  	  halo or halos of interest

		  Returns
		  -------
	      group object, list of group objects
	      
	      Examples
	      --------
	      ## returns a single 'Group' object for halo 10
	      >>> readfofspecial('/path/to/catalogues', 12, 10)
	      
	      ## returns a list of 'Group' objects for halos 10, 11, & 32
	      >>> readfofspecial('/path/to/catalogues', 12, [10,11,32])
	      
		  ## returns a list of 'Group' objects for all halos
		  >>> readfofspecial('/path/to/catalogues', 12, -1)
		  
		  ## sample data access ##
		  >>> halo10 = readfofspecial('/path/to/catalogues', 12, 10)
		  >>> print halo10.index
		      10
		      
   		  >>> halos  = readfofspecial('/path/to/catalogues', 12, -1)
		  >>> pcount = [s.npart_total for s in halos]

---
## readpstar()
This function reads `P-StarGroupFinder` binary outputs (indexlists & catalogues).  It returns a `Group` object, or a list of `Group` objects, all of which have **eleven** attributes:

	 index         - group index
	 npart_total   - total number of group particles
	 indexes       - indexes of all particles belonging to group
	 mstar         - stellar mass
	 mgas          - gas mass
	 cm            - center of mass
	 metals        - star metallicity
	 gmetals       - gas metallicity
	 gpids         - list of gas PIDs
	 spids		   - list of star PIDs
	 stypes		   - 

**DEFINITION:**
	
		  readpstar(a,b,c)

	      Parameters
	      ----------
	      a : string
	      	  Group catalogue directory
	      b : int
	      	  Snapshot number
	      c : int, list
	      	  Galaxy, or list of galaxy indexes
	      
	      Returns
	      -------
	      group object, list of group objects
	      
	      Examples
	      --------
	      ## returns a single 'Group' object for galaxy 10
	      >>> readpstar('/path/to/catalogues', 12, 10)
	      
     	  ## returns a list of 'Group' objects for galaxies 10,11, & 32
	      >>> readpstar('/path/to/catalogues', 12, [10,11,32])
	      
	      ## returns a list of 'Group' objects for all galaxies
	      >>> readpstar('/path/to/catalogues', 12, -1)
	      
	      ## sample data access ##
		  >>> gal10 = readpstar('/path/to/catalogues', 12, 10)
		  >>> print gal10.index
		      10
		      
		  >>> galaxies = readpstar('/path/to/catalogues', 12, -1)
		  >>> masses   = [s.mstar for s in galaxies]

---
## TIPS
If you plan on doing multiple reads in a single script, you can pass a common set of options via a dictionary.  As an example:

~~~python
from pygadgetreader import *

snap  = 'snap_N128L16_036'
pygro = {'debug':1, 'units':1, 'UnitMass_in_g':1.989e33}
rho   = readsnap(snap, 'rho', 0, **pygro)
temp  = readsnap(snap, 'u',   0, **pygro)
~~~
This convinient form means that if you need to change the variables passed to each `readsnap()` call you only have to alter the `pygro` dictionary.

****
If you have any comments or suggestions feel free to contact me.  Enjoy!

    Robert Thompson
    rthompsonj@gmail.com