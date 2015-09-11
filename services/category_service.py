#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: yuandunlong
# @Date:   2015-09-11 15:49:42
# @Last Modified by:   yuandunlong
# @Last Modified time: 2015-09-11 15:53:22

from database.models import Category
def get_all_categories():
    cats= Category.query.all()

    return cats