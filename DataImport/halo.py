#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =================================================
# File Name: halo.py
# Author: Wang Yang
# mail: wangyang23@mail.sysu.edu.cn
# Created  Time: 2016-07-29 03:23:45 PM
# Modified Time: 2016-08-09 18:42:52
# =================================================


import pandas as pd
import numpy as np
import zlist
import re
import os


class Halo:
    """
    import all properties of halo catalogue
    """
    _title_ahf = ['haloid', 'hostid', 'nsub', 'mass',
                  'npart', 'cx', 'cy', 'cz',
                  'vx', 'vy', 'vz', 'r2sig', 'rmax',
                  'null14', 'null15', 'null16',
                  'vmax', 'vdisp', 'spin_p_x', 'spin_p_y', 'spin_p_z',
                  'spin_b_x', 'spin_b_y', 'spin_b_z',
                  'mvir_th', 'rvir_th', 'mvir_b200', 'rvir_b200',
                  'mvir_c200', 'rvir_c200', 'rhalf', 'msum',
                  'rc200sum', 'null34', 'null35', 'null36',
                  'null37', 'null38', 'null39', 'null40',
                  'null41', 'null42', 'null43']

    _title_compact = ['haloid', 'hostid', 'nsub', 'mass', 'npart',
                      'cx', 'cy', 'cz', 'vx', 'vy', 'vz',
                      'rvir', 'rmax', 'r2', 'mbp_offset', 'com_offset',
                      'vmax', 'v_esc', 'sig_v', 'lambda', 'lambdaE',
                      'lx', 'ly', 'lz', 'b', 'c',
                      'eax', 'eay', 'eaz', 'ebx', 'eby', 'ebz',
                      'ecx', 'ecy', 'ecz', 'ovdens', 'nbins',
                      'fMhires', 'Ekin', 'Epot', 'SurfP', 'Phi0',
                      'cNFW', 'n_gas', 'm_gas', 'lambda_gas',
                      'lambdaE_gas', 'lx_gas', 'ly_gas', 'lz_gas',
                      'b_gas', 'c_gas', 'eax_gas', 'eay_gas', 'eaz_gas',
                      'ebx_gas', 'eby_gas', 'ebz_gas',
                      'ecx_gas', 'ecy_gas', 'ecz_gas',
                      'Ekin_gas', 'Epot_gas', 'n_star', 'm_star',
                      'lambda_star', 'lambdaE_star',
                      'lx_star', 'ly_star', 'lz_star',
                      'b_star', 'c_star',
                      'eax_star', 'eay_star', 'eaz_star',
                      'ebx_star', 'eby_star', 'ebz_star',
                      'ecx_star', 'ecy_star', 'ecz_star',
                      'Ekin_star', 'Epot_star']

    _type_ahf = {'haloid': np.int64, 'hostid': np.int64, 'nsub': np.int32,
                 'npart': np.int64}

    _type_compact = {'haloid': np.int32, 'hostid': np.int32, 'nsub': np.int32,
                     'npart': np.int64}

    _default_col = ['haloid', 'hostid', 'mass', 'npart', 'cx', 'cy', 'cz',
                    'vx', 'vy', 'vz']

    def __init__(self, filez=None, maxsnap=200):
        self.halos = [{} for i in range(maxsnap)]
        if filez is not None:
            self.z = zlist.Zlist(filez)

    def _get_snap(self, filename):
        try:
            temp = re.findall(r'\d+\.+\d+', filename)[-1]
            tag = 0
            for i in range(len(self.z.z)):
                if round(self.z.z[i], 3) == float(temp):
                    tag = 1
                    return i
            if tag == 0:
                print filename
                print 'can\'t find snap for redshift ' + temp
                return None
        except NameError:
            print 'Please load zlist file first'

    def load_z(self, fname):
        self.z = zlist.Zlist(fname)

    def import_all_snap(self, path, keyword='halos',
                        col=_default_col,
                        ftype='compact'):
        if os.path.isdir(path):
            pa = []
            for dirpath, dirnames, filenames in os.walk(path):
                for flist in filenames:
                    if flist[-(len(keyword)):] == keyword:
                        pa.append(os.path.join(dirpath, flist))
            for flist in pa:
                self.import_one_snap(flist, col=col, ftype=ftype)
        else:
            print 'Path should be the directory of all halos files'

    def import_one_snap(self, filename,
                        col=_default_col,
                        ftype='compact'):
        if ftype == 'ahf':
            self.import_property_ahf(filename, col_used=col,
                                     col_title=self._title_ahf)
        elif ftype == 'compact':
            self.import_property_compact(filename, col_used=col,
                                         col_title=self._title_compact)

    def import_property_ahf(self, fname,
                            col_used=_default_col,
                            col_title=_title_ahf,
                            dtype=_type_ahf):
        """
        import halos properties of one snap, for ahf format
        """
        snap = self._get_snap(fname)
        if snap is None:
            print "check the zlist for matching first"
        else:
            print 'snap', snap
            self.halos[snap] = pd.read_csv(fname, delim_whitespace=True,
                                           header=None,
                                           comment='#',
                                           dtype=dtype,
                                           names=col_title,
                                           usecols=col_used)

    def import_property_compact(self, fname,
                                col_used=_default_col,
                                col_title=_title_compact,
                                dtype=_type_compact):
        """
        import halos properties of one snap, for ahf format
        """
        snap = self._get_snap(fname)
        if snap is None:
            print "check the zlist for matching first"
        else:
            print 'snap', snap
            self.halos[snap] = pd.read_csv(fname, delim_whitespace=True,
                                           header=None,
                                           comment='#',
                                           dtype=dtype,
                                           names=col_title,
                                           usecols=col_used)
