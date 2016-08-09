#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =================================================
# File Name: __init__.py
# Author: Wang Yang
# mail: wangyang23@mail.sysu.edu.cn
# Created  Time: 2016-07-29 08:48:50 PM
# Modified Time: 2016-08-03 9:05:03
# =================================================

def AllData(inputfile):
    from .database import AllData
    return AllData(inputfile)
