#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: yuandunlong
# @Date:   2015-09-10 22:16:29
# @Last Modified by:   yuandunlong
# @Last Modified time: 2015-09-10 22:22:13
import string
import random
def random_digits(length):
    return string.join(random.sample(string.digits, length)).replace(" ","")