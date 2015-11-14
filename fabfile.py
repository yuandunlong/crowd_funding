#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: yuandunlong
# @Date:   2015-11-07 13:47:35
# @Last Modified by:   yuandunlong
# @Last Modified time: 2015-11-07 14:02:23
from fabric.api import local,cd,run,hosts,env
env.hosts=['ydl@www.leychina.com']

env.password='yuandunlong'

def deploy():
    print 'remote deploy'
    with cd('~/crowd_funding'):
        run('git pull')
        run('./uswgi_server.sh restart')

def migrate():
    print "remote db migrate"
    with cd('~/crowd_funding'):
        run('git pull')
        run('./uswgi_server.sh stop')
        run('python manager.py db migrate')
        run('python manager.py db upgrade')
        run('./uswgi_server.sh start')
