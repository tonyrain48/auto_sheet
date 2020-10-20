# -*- coding: utf-8 -*-
# Copyright (C) 2017 SWFE Limited.
#
# Created: Wed Jun 28  2017
#      by: Ruchuang Gao, 18818265578
#          gaoflaine@126.com
#
#
# WARNING! All changes made in this file will be lost!

'''
database_setup, Created on Jun, 2017
#version: 1.0
DB Manager
'''
import sys
import pandas as pd

from sqlalchemy import *

class connMySQL_Ali:
    def __init__(self, user='root', passwd='Swhy1234', host='rm-uf6558j60h2k43835o.mysql.rds.aliyuncs.com',
                 databasename='spdb'):
        try:
            # connect MySQL
            self.engine = create_engine(
                "mysql+mysqldb://{0}:{1}@{2}/{3}?charset=utf8".format(user, passwd, host, databasename))
        except:
            info = sys.exc_info()
            print info[0], ":", info[1]

class connMySQL_Xiaofeiji:
    def __init__(self, user='cyh', passwd='admin', host='192.168.91.188',
                 databasename='padb'):
        try:
            # connect MySQL
            self.engine = create_engine(
                "mysql+mysqldb://{0}:{1}@{2}/{3}?charset=utf8".format(user, passwd, host, databasename))
        except:
            info = sys.exc_info()
            print info[0], ":", info[1]

    def __del__(self):
        # disconnect
        self.engine.dispose()
