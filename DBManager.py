#-*- coding: utf-8 -*-
# Copyright (C) 2016 SWFE Limited.
#
# Created: Fri Otc 05  2016
#      by: chenqiuxing, 18317010980
#          1078494347@qq.com, chenqiuxing@sjtu.edu.cn
#          
#
# WARNING! All changes made in this file will be lost!

'''
database_setup, Created on May, 2015
#version: 1.0

'''

import sys
import MySQLdb

from _config import MysqlConfig
from Model.globalInfo import GlobalInfo

class connMySQL:
    def __init__(self):
        try:
            infoObj = MysqlConfig()
            # connect MySQL
            self.conn = MySQLdb.connect(user= infoObj.user, passwd= infoObj.passwd, host= infoObj.host, charset="utf8", use_unicode=True, port= infoObj.port)
            self.cursor = self.conn.cursor()

            self.conn.select_db( infoObj.databaseName )
            # create tables
            self.conn.commit()

        except MySQLdb.Error, e:
            # pass
            print "Error %d: %s" % (e.args[0], e.args[1])
            # GlobalInfo.logMonitor.error("MySQL error %d: %s" % (e.args[0], e.args[1]))
    
    def getConn(self):
        return self.conn

    def sqluser(self, userid, password):
        strSQL = 'select password, type from userinfo where userid = "' + str(userid)+'"'
        # print strSQL
        self.cursor.execute( strSQL)
        # fetch results, fetchone or fetchall
        results = list(self.cursor.fetchall())
        # print results
        if results ==[]:
            return -1
        else:
            pwd = results[0][0]
            type = results[0][1]
            if(pwd ==None):
                # print  'no user'
                return -1
            elif(pwd !=password):
                # print  'no user'
                return 0
            else:
                return type
                
    def updateValue(self, tablename, col, val, idcondition):
        #cursor.execute ("UPDATE tblTableName SET Year=%s, Month=%s, Day=%s, Hour=%s, Minute=%s WHERE Server='%s' " % (Year, Month, Day, Hour, Minute, ServerID))
        if len(col) != len(val) :
            print "input error"
        strSQL = 'update %s set ' %(tablename)
        for i in range(0, len(col)):
            if i == len(col)-1:
                if isinstance(val[i],str):
                    strSQL += col[i] + '='+'"'+str(val[i])+ '"' +' '
                else:
                    strSQL += col[i] + '='+str(val[i]) +' '
            else:
                if isinstance(val[i],str):
                    strSQL += col[i] + '='+'"'+str(val[i])+ '"'+','
                else:
                    strSQL += col[i] + '='+str(val[i])+','
        strSQL += 'where ' + idcondition
        #targetid = "hs"
        # print strSQL
        self.cursor.execute( strSQL)
        self.conn.commit()
        
    def selectValue(self, tablename, col, idcondition, pluscondition = ''):
        #cursor.execute ("UPDATE tblTableName SET Year=%s, Month=%s, Day=%s, Hour=%s, Minute=%s WHERE Server='%s' " % (Year, Month, Day, Hour, Minute, ServerID))

        strSQL = 'select '
        if col!=[] :
            for i in range(0, len(col)):
                if i == len(col)-1:
                    strSQL += col[i]+' '
                else:
                    strSQL += col[i] + ','
        else:
            strSQL += '*'
        if idcondition =='':
            strSQL += 'from %s ' %(tablename)
        else:   
            strSQL += 'from %s where ' %(tablename)  + idcondition
        #targetid = "hs"
        strSQL += pluscondition
        # print strSQL
        self.cursor.execute(strSQL)
        # fetch results, fetchone or fetchall
        results = list(self.cursor.fetchall())
        self.conn.commit()
        
        return results
        
    def insertValue(self, tablename, col, val):
        if len(col) != len(val) :
            print "input error"
        strSQL = 'insert into %s (' %(tablename)
        for i in range(0, len(col)):
            if i == len(col)-1:
                strSQL += col[i] + ' '
            else:
                strSQL += col[i] +','
        
        strSQL += ') values ('
        for i in range(0, len(val)):
            if i == len(val)-1:
                if isinstance(val[i],str):
                    strSQL += '"'+str(val[i] )+ '"'+' '
                else:
                    strSQL += str(val[i] )+ ' '
            else:
                if isinstance(val[i],str):
                    strSQL += '"'+str(val[i] )+ '"'+','
                else:
                    strSQL += str(val[i] ) +','
        #targetid = "hs"
        strSQL += ')'
        # print strSQL
        self.cursor.execute( strSQL)
        self.conn.commit()

    def insertMany(self, tablename, col, valtype, vals):
        if len(col) != len(valtype) :
            print "input error"
        strSQL = 'insert into %s (' %(tablename)
        for i in range(0, len(col)):
            if i == len(col)-1:
                strSQL += col[i] + ''
            else:
                strSQL += col[i] +','
        
        strSQL += ') values ('
        for i in range(0, len(valtype)):
            if i == len(valtype)-1:
                strSQL += str(valtype[i] )+ ''
            else:
                strSQL += str(valtype[i] ) +','
        #targetid = "hs"
        strSQL += ')'
        # print vals
        # print strSQL
        self.cursor.executemany(strSQL, vals)
        self.conn.commit()

    def deleteRow(self, tablename, idcondition):
        strSQL = "delete from " + str(tablename) + ' where ' + idcondition
        # print strSQL
        self.cursor.execute( strSQL)
        self.conn.commit()

    def truncateTable(self, tablename):
        strSQL = "truncate table " + str(tablename)
        # print strSQL
        self.cursor.execute( strSQL)
        self.conn.commit()

    def executeSQL(self, strSQL):
        self.cursor.execute( strSQL)
        self.conn.commit()


    # Release
    def __del__(self):
        # disconnect
        self.cursor.close()
        self.conn.close()



if __name__=='__main__':
    print '---start---'
    
    obj = connMySQL()
    print obj.sqluser('11111', '11111')
    obj.updateValue('para', ['sp', 'om'],['1.11', '1.21'],'targetid = "hs"' )
    print obj.selectValue('para', ['sp', 'om'],'targetid = "hs"' )
    print obj.selectValue('parainfo', ['spotprice', 'strike', 'volatility', 'participationrate', 'updatehistory'],'targetid = "'+'HS300'+'";' )

    print '---Done---'
