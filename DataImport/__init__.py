#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =================================================
# File Name: __init__.py
# Author: Wang Yang
# mail: wangyang23@mail.sysu.edu.cn
# Created  Time: 2016-07-29 03:23:10 PM
# Modified Time: 2016-08-02 22:44:26
# =================================================


def MergerTree(path, filetype='default', keyword='', maxsnap=0,
               filez=None):
    from .mergertree import MergerTree
    return MergerTree(path, filetype=filetype, keyword=keyword,
                      maxsnap=maxsnap, filez=filez)


def Particle(fname):
    from .particle import Particle
    return Particle


def Zlist(fname):
    from .zlist import Zlist
    return Zlist(fname)


def Halo(filez=None, maxsnap=200):
    from .halo import Halo
    return Halo(filez=filez, maxsnap=200)
