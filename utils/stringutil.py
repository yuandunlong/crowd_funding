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


def uniqid(prefix='', more_entropy=False):
    m = time.time()
    uniqid = '%8x%05x' %(math.floor(m),(m-math.floor(m))*1000000)
    if more_entropy:
        valid_chars = list(set(string.hexdigits.lower()))
        entropy_string = ''
        for i in range(0,10,1):
            entropy_string += random.choice(valid_chars)
        uniqid = uniqid + entropy_string
    uniqid = prefix + uniqid
    return uniqid


def build_order_no():
    uiq=uniqid()
    arr=[]
    for i in range(6):
        arr.append(str(ord(uiq[7+i])))
    temp=''.join(arr)

    return (datetime.now().strftime('%Y%m%d')+temp[:8])    