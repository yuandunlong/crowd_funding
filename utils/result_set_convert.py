#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: yuandunlong
# @Date:   2015-09-25 23:32:58
# @Last Modified by:   yuandunlong
# @Last Modified time: 2015-09-25 23:33:43


def models_2_arr(models):
    arr=[]
    for model in models:
        arr.append(model.as_map())
    return arr