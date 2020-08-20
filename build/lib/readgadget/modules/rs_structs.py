import numpy as np
import sys

## ROCKSTAR ##
halostruct1 = np.dtype([('id',np.int64),
                        ('pos',np.float32,(6,)),
                        ('corevel',np.float32,(3,)),
                        ('bulkvel',np.float32,(3,)),
                        ('m',np.float32),
                        ('r',np.float32),
                        ('child_r',np.float32),
                        ('vmax_r',np.float32),
                        ('mgrav',np.float32),
                        ('vmax',np.float32),
                        ('rvmax',np.float32),
                        ('rs',np.float32),
                        ('klypin_rs',np.float32),
                        ('vrms',np.float32),
                        ('J',np.float32,(3,)),
                        ('energy',np.float32),
                        ('spin',np.float32),
                        ('alt_m',np.float32,(4,)),
                        ('Xoff',np.float32),
                        ('Voff',np.float32),
                        ('b_to_a',np.float32),
                        ('c_to_a',np.float32),
                        ('A',np.float32,(3,)),
                        ('b_to_a2',np.float32),
                        ('c_to_a2',np.float32),
                        ('A2',np.float32,(3,)),
                        ('bullock_spin',np.float32),
                        ('kin_to_pot',np.float32),
                        ('m_pe_b',np.float32),
                        ('m_pe_d',np.float32),
                        ('dummy1',np.float32),              ## ALIGNMENT
                        ('num_p',np.int64),
                        ('num_child_particles',np.int64),
                        ('p_start',np.int64),
                        ('desc',np.int64),
                        ('flags',np.int64),
                        ('n_core',np.int64),
                        ('dummy2',np.float32),              ## ALIGNMENT
                        ('min_pos_err',np.float32),
                        ('min_vel_err',np.float32),
                        ('min_bulkvel_err',np.float32)
                    ])

halostruct2 = np.dtype([('id',np.int64),
                        ('pos',np.float32,(6,)),
                        ('corevel',np.float32,(3,)),
                        ('bulkvel',np.float32,(3,)),
                        ('m',np.float32),
                        ('r',np.float32),
                        ('child_r',np.float32),
                        ('vmax_r',np.float32),
                        ('mgrav',np.float32),
                        ('vmax',np.float32),
                        ('rvmax',np.float32),
                        ('rs',np.float32),
                        ('klypin_rs',np.float32),
                        ('vrms',np.float32),
                        ('J',np.float32,(3,)),
                        ('energy',np.float32),
                        ('spin',np.float32),
                        ('alt_m',np.float32,(4,)),
                        ('Xoff',np.float32),
                        ('Voff',np.float32),
                        ('b_to_a',np.float32),
                        ('c_to_a',np.float32),
                        ('A',np.float32,(3,)),
                        ('b_to_a2',np.float32),
                        ('c_to_a2',np.float32),
                        ('A2',np.float32,(3,)),
                        ('bullock_spin',np.float32),
                        ('kin_to_pot',np.float32),
                        ('m_pe_b',np.float32),
                        ('m_pe_d',np.float32),
                        ('halfmass_radius',np.float32),
                        #('dummy1',np.float32),              ## ALIGNMENT
                        ('num_p',np.int64),
                        ('num_child_particles',np.int64),
                        ('p_start',np.int64),
                        ('desc',np.int64),
                        ('flags',np.int64),
                        ('n_core',np.int64),
                        ('dummy2',np.float32),              ## ALIGNMENT
                        ('min_pos_err',np.float32),
                        ('min_vel_err',np.float32),
                        ('min_bulkvel_err',np.float32)
                    ])

## ROCKSTAR-GALAXIES ##
halogalaxystruct1 = np.dtype([('id',np.int64),
                              ('pos',np.float32,(6,)),
                              ('corevel',np.float32,(3,)),
                              ('bulkvel',np.float32,(3,)),
                              ('m',np.float32),
                              ('r',np.float32),
                              ('child_r',np.float32),
                              ('vmax_r',np.float32),
                              ('mgrav',np.float32),
                              ('vmax',np.float32),
                              ('rvmax',np.float32),
                              ('rs',np.float32),
                              ('klypin_rs',np.float32),
                              ('vrms',np.float32),
                              ('J',np.float32,(3,)),
                              ('energy',np.float32),
                              ('spin',np.float32),
                              ('alt_m',np.float32,(4,)),
                              ('Xoff',np.float32),
                              ('Voff',np.float32),
                              ('b_to_a',np.float32),
                              ('c_to_a',np.float32),
                              ('A',np.float32,(3,)),
                              ('b_to_a2',np.float32),
                              ('c_to_a2',np.float32),
                              ('A2',np.float32,(3,)),
                              ('bullock_spin',np.float32),
                              ('kin_to_pot',np.float32),
                              ('m_pe_b',np.float32),
                              ('m_pe_d',np.float32),
                              ('dummy1',np.float32),              ## ALIGNMENT
                              ('num_p',np.int64),
                              ('num_child_particles',np.int64),
                              ('p_start',np.int64),
                              ('desc',np.int64),
                              ('flags',np.int64),
                              ('n_core',np.int64),
                              ('dummy2',np.float32),              ## ALIGNMENT
                              ('min_pos_err',np.float32),
                              ('min_vel_err',np.float32),
                              ('min_bulkvel_err',np.float32),
                              ('type',np.int32),
                              ('sm',np.float32),
                              ('gas',np.float32),
                              ('bh',np.float32),
                              ('peak_density',np.float32),
                              ('av_density',np.float32),
                          ])


def getRSformat(obj):

    if obj.galaxies == 0:
        if obj.format_revision == 0:
            print('OUTDATED ROCKSTAR, PLEASE UPDATE!')
            sys.exit()

        elif obj.format_revision == 1:
            if obj.debug: print('returning halostruct1')
            return halostruct1

        elif obj.format_revision == 2:
            if obj.debug: print('returning halostruct2')
            return halostruct2
            
        else:
            print('found HALO_FORMAT_REVISION=%d, if this is >2 email me!' % 
                  obj.format_revision)
            sys.exit()

    elif obj.galaxies == 1:
        if obj.format_revision == 0:
            print('OUTDATED ROCKSTAR-GALAXIES, PLEASE UPDATE!')
            sys.exit()

        elif obj.format_revision == 1:
            if obj.debug: print('returning halogalaxystruct1')
            return halogalaxystruct1

        else:
            print('found HALO_FORMAT_REVISION=%d, if this is >1 email me!' % 
                  obj.format_revision)
            sys.exit()
