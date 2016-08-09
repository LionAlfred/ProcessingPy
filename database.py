#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =================================================
# File Name: database.py
# Author: Wang Yang
# mail: wangyang23@mail.sysu.edu.cn
# Created  Time: 2016-07-29 08:40:48 PM
# Modified Time: 2016-08-04 8:47:01
# =================================================


import DataImport as di
import pdb
from multiprocessing import Pool


class AllData:

    def __init__(self, inputfile):
        self.path = {}
        with open(inputfile) as f:
            for line in f.readlines():
                temp = line.split()
                self.path[temp[0].strip()] = temp[1].strip()

    def import_zlist(self, fname):
        self.zlist = di.Zlist(fname)

    def import_halo(self, filez):
        self.halo = di.Halo(filez=filez)

    def import_halo_prop(self, fname):
        pass

    def import_halo_env(self, fname):
        pass

    def import_tree(self, fname, filetype='default', keyword='', maxsnap=0,
                    filez=None):
        self.tree = di.MergerTree(fname, filetype=filetype, keyword=keyword,
                                  maxsnap=maxsnap, filez=filez)

    def get_tree_size(self, snap, haloid):
        try:
            len(self.zlist)
        except NameError:
            print "Please initalize the time list first"
            exit(0)
        try:
            len(self.tree)
        except NameError:
            print "Please initalize the tree first"
        pdb.set_trace()
        stack = []
        stack.append((snap, haloid))
        _size = 0.0
        while(len(stack) != 0):
            print 'stack len', len(stack)
            print _size
            _tag, _id = stack.pop()
            print _tag, _id
            if _id < len(self.tree[_tag][0]):
                if self.tree[_tag][_id][0] >= 0:
                    _size += len(self.tree[_tag][_id]) * \
                        abs(self.zlist.t[_tag] - self.zlist.t[_tag-1])
                for pro in self.tree[_tag][_id]:
                    if pro >= 0:
                        stack.append((_tag-1, pro))
        return _size / self.get_tree_len(snap, haloid)

    def get_tree_len(self, snap, haloid):
        try:
            len(self.zlist)
        except AttributeError:
            print "Please initalize the time list first"
        try:
            len(self.tree)
        except AttributeError:
            print "Please initalize the tree first"
        _time = 0.0
        mainpro = haloid
        for tag in range(snap, 0, -1):
            if mainpro >= len(self.tree[tag]):
                _time += abs(self.zlist.t[tag] - self.zlist.t[tag-1])
                break
            else:
                mainpro = self.tree[tag][mainpro][0]
                if mainpro >= 0:
                    _time += abs(self.zlist.t[tag] - self.zlist.t[tag-1])
                elif mainpro < 0:
                    break
        return _time

    def get_tree_len_all(self):
        maxsnap = len(self.tree) - 1
        nhalo = len(self.tree[-1])
        arr_len = [self.get_tree_len(maxsnap, i) for i in range(nhalo)]
        return arr_len

    def get_tree_size_all(self):
        maxsnap = len(self.tree) - 1
        nhalo = len(self.tree[-1])
        arr_size = [self.get_tree_size(maxsnap, i) for i in range(nhalo)]
        return arr_size

    def get_tree(self, haloid):
        maxsnap = len(self.tree) - 1
        nhalo = len(self.tree[-1])
        if haloid > nhalo or haloid < 1:
            print "in valid halo id"
        else:
            arr_id = [0 for i in range(maxsnap+1)]
            tag_snap = maxsnap
            tag_id = haloid
            for i in range(maxsnap+1):
                arr_id[tag_snap] = tag_id
                if self.tree[tag_snap][tag_id][0] is not 0:
                    tag_id = self.tree[tag_snap][tag_id][0]
                    tag_snap = tag_snap - 1
                else:
                    break
        return arr_id


if __name__ == '__main__':
    fn2 = '/home/wangyang/Project_Sysu\
           /DATA/Dark512/HBT/Sub/anal/protableHBT/HBTTree'
    fn1 = '/home/wangyang/Project_Sysu/DATA/Dark512/CatalogueSpringel/History/'
    data = AllData()
    data.import_tree(fn1)
