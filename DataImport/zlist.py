#!usr/bin/env python
# -*- coding: utf-8 -*-
# =================================================
# File Name: zlist.py
# Author: Wang Yang
# mail: wangyang23@mail.sysu.edu.cn
# Created  Time: 2016-07-29 03:24:40 PM
# Modified Time: 2016-08-11 16:36:28
# =================================================


import numpy as np
import os


class Zlist:
    """
    store the a, z, look back year for snapshots
    """

    def __init__(self, fname):
        if os.path.isfile(fname):
            index, self.z, self.a, self.t, = np.loadtxt(fname, skiprows=1,
                                                        unpack=True)
        else:
            print("File %s does not exist" % (fname))
            pass

    def __len__(self):
        return len(self.t)

if __name__ == '__main__':
    zt = Zlist('../zlist')
    # print zt.a
    # print zt.z
    # print zt.t
