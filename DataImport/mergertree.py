#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =================================================
# File Name: PostProcessing.py
# Author: Wang Yang
# mail: wangyang23@mail.sysu.edu.cn
# Created  Time: 2016-07-29 10:54:36 AM
# Modified Time: 2016-08-09 15:58:39
# =================================================

import struct
import os
import numpy as np
import zlist
import re


class MergerTree:
    """
    Import the data for merger tree and related processing methods
    self.tree[s][m][n] = id of pro of nth progenitor of halo m in snap s
    m starts with 1
    n strats with 0
    """

    def __init__(self, path, filetype='default', keyword='', maxsnap=0,
                 filez=None):
        """
        Args:
            path: merger tree file or
                  a directory containing all merger tree files for snapshots
            type: the type of merger tree
            keywords: ext of merger tree file
            maxsnap: snaps ranges for 0 to maxsnap. if maxsnap == 0, it will
                     be detected automatically(be careful)
            filez: a list for matching the snapshot number to a,z,t
        """
        if filez is not None:
            self.z = zlist.Zlist(filez)

        if os.path.exists(path):
            # merger trees in one file
            if os.path.isfile(path):
                if maxsnap == 0:
                    maxsnap = self._get_maxsnap(path, filetype=filetype)
                self.tree = [[] for i in range(maxsnap+1)]
                if filetype == 'ahf':
                    self._read_history_ahf(path)
            # merger trees in different files for different snapshots
            if os.path.isdir(path):
                pa = []
                for dirpath, dirnames, filenames in os.walk(path):
                    for flist in filenames:
                        if flist[-(len(keyword)):] == keyword:
                            pa.append(os.path.join(dirpath, flist))
                # determine the max snapshots number
                if maxsnap == 0:
                    maxsnap = self._get_maxsnap(pa, filetype=filetype)
                self.tree = [[] for i in range(maxsnap+1)]
                for i in range(len(pa)):
                    # add read history function for other type in the
                    # following 'if' block
                    if filetype == 'default':
                        self._read_history_gadget(pa[i])
                    elif filetype == 'compact':
                        self._read_history_compact(pa[i])
                    else:
                        print "Unknow file type "+filetype
        else:
            print("File/Dir %s does not exist" % (path))

    def load_z(self, filez):
        self.z = zlist.Zlist(filez)

    def __setitem__(self, key, value):
        self.tree[key] = value

    def __getitem__(self, key):
        return self.tree[key]

    def __str__(self):
        # s = '\n'
        # for i in range(len(self.tree)):
            # if len(self.tree[i]) > 1:
                # s.join('snap %d :' % (i))
                # s.join(str(self.tree[i]))
                # break
        # s = s.join('\n... ...\nsnap %d : ' % (len(self.tree)+1))
        s = (str(self.tree[-1][1]))
        # s = s.join('... ...')
        # s = s.join(str(self.tree[-1][-1]))
        return s

    def __len__(self):
        return len(self.tree)

    def _get_maxsnap(self, path, filetype='default'):
        if filetype == 'default' or \
           filetype == 'compact':
            s = []
            for i in range(len(path)):
                s.append(self._get_snap(path[i], filetype=filetype))
            return max(s)
        elif filetype == 'ahf':
            offset = 1000000000000
            s = []
            f = open(path, 'r')
            data = f.readlines()
            for line in data[3:10]:
                snap = int(line.strip().split()[0])/offset
                s.append(snap)
            for line in data[-10:-2]:
                snap = int(line.strip().split()[0])/offset
                s.append(snap)
            return max(s)
        else:
            print "Unknow file type "+filetype

    def _get_snap(self, filename, filetype='default'):
        if filetype == 'compact':
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
        elif filetype == 'default':
            pass

    def _read_history_gadget(self, fname):
        """
        halo id starts with 1
        for simple history file
        Nsub: Halo number of this snap
        Nsub_pre: Total progenitor number
        ProCount: progenitor number of every halo
        ProFirst: first progenitor of every halo
        ProList:  full list of progentiors
        """
        # get snap No. from file name
        snap = int(fname[-3:])
        # read files
        f = open(fname, 'rb')
        Nsub, Nsub_pre = struct.unpack('ii', f.read(8))
        ProCount = np.array([0])
        ProFirst = np.array([0])
        ProList = np.array([0])
        x = np.fromfile(f, dtype=np.int32, count=Nsub, sep="")
        ProCount = np.append(ProCount, x)
        x = np.fromfile(f, dtype=np.int32, count=Nsub, sep="")
        ProFirst = np.append(ProFirst, x)
        x = np.fromfile(f, dtype=np.int32, count=Nsub_pre, sep="")
        ProList = np.append(ProList, x)
        f.close()
        # building trees
        self.tree[snap] = [[]]*(Nsub+1)
        for j in range(Nsub+1):
            subid = ProFirst[j]
            pro = [subid]
            for k in range(ProCount[j]-1):
                subid = ProList[subid]
                pro.append(subid)
            if len(pro) == 1 and pro[0] == 0:
                pro[0] = -1
            self.tree[snap][j] = pro

    def _read_history_ahf(self, fname):
        offset = 1000000000000
        for b in self.tree:
            b.append([-1])
        with open(fname, 'r') as f:
            data = f.readlines()
        Nhalo = int(data[2].strip().split()[0])
        tag = 3
        for i in range(Nhalo):
            element = data[tag].strip().split()
            snap = int(element[0]) / offset
            hid = int(element[0]) % offset
            pronum = int(element[1])
            tag += 1
            pro = []
            for j in range(pronum):
                element2 = data[tag].strip().split()
                pro.append(int(element2[0]) % offset)
                tag += 1
            if len(pro) == 0:
                pro.append(-1)
            if hid > len(self[snap])-1:
                inc = hid - len(self.tree[snap])+1
                arr = [[0] for k in range(inc)]
                self.tree[snap].extend(arr)
            self.tree[snap][hid] = pro

    def _read_history_compact(self, fname):
        # import pdb
        # pdb.set_trace()
        snap = self._get_snap(fname, filetype='compact')
        for b in self.tree:
            b.append([-1])
        with open(fname, 'r') as f:
            data = f.readlines()
        tag = 2
        while tag < len(data):
            element = data[tag].strip().split()
            hid = int(element[0])
            pronum = int(element[2])
            tag += 1
            pro = []
            for j in range(pronum):
                element2 = data[tag].strip().split()
                pro.append(int(element2[1]))
                tag += 1
            if len(pro) == 0:
                pro.append(-1)
            if hid > len(self[snap])-1:
                inc = hid - len(self.tree[snap])+1
                arr = [[-1] for k in range(inc)]
                self.tree[snap].extend(arr)
            self.tree[snap][hid] = pro


if __name__ == '__main__':
    fn1 = '/home/wangyang/Project_Sysu/DATA/Dark512/CatalogueSpringel/History/'
    tree = MergerTree(fn1, maxsnap=0)
