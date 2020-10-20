#coding=gbk
from DBManager2 import connMySQL
import re
import pandas as pd
from WindPy import *

w.start()


obj=connMySQL()

#构造数据库
createSql='''
    CREATE TABLE IF NOT EXISTS `pnldb`.`tmppnldb` (
      `ID` INT NOT NULL AUTO_INCREMENT,
      `underlyingCode` VARCHAR(10) NOT NULL,
      `Multi` INT NOT NULL,
      `hedgeContract` VARCHAR(20) NOT NULL,
      `todayHold` INT NOT NULL,
      `settlePrice` DECIMAL(20,10) NOT NULL,
      `closePrice` DECIMAL(20,10) NOT NULL,
      `totalHold` INT NOT NULL,
      `Date` DATETIME NOT NULL,
      PRIMARY KEY (`ID`))
    ENGINE = InnoDB;
'''

obj.executeSQL(strSQL=createSql)

#流水表汇总
dfold=pd.read_excel('对冲头寸损益.xlsx',sheet_name='流水汇总旧')
dfnew=pd.read_excel('对冲头寸损益.xlsx',sheet_name='流水汇总')
dftotal=pd.concat([dfold,dfnew])
dftotal.reset_index(drop=True,inplace=True)

contractdict={'510300.SH':'IF','512660.SH':'399967.SZ',
              '512980.SH':'399971.SZ','159928.SZ':'000932.SH',
              '512800.SH':'399986.SZ'}

#修改后缀便于wind查询价格
underlyingdict={'SH':'SH','SZ':'SZ','XSGE':'SHF','XINE':'INE',
                'CCFX':'CFE','XZCE':'CZC','XDCE':'DCE','SGE':'SGE'}

#合约乘数
multidict={'if':300,'au':1000,'ih':300,'ic':200,'cu':5,
           'ap':10,'pp':5,'oi':10,'sc':1000,'cf':5,
           'm':10,'c':10,'sf':5,'jm':60,'zc':100,
           'al':5,'hc':10,'rb':10,'i':100,'fg':20,
           'ta':5,'ag':15,'sr':10,'ru':10,'L':5,'J':100,
           'jd':10,'y':10,'p':10,}

datelist=dftotal['委托日期'].unique()[0]

#逐日更新
for date in datelist:
    df = dftotal[dftotal['委托日期'] == date]
    df.loc[df['买卖'] != 1, '成交数量'] = -df['成交数量']
    contractlist=df.groupby('代码').sum()['成交数量'].index
    contractamt=df.groupby('代码').sum()['成交数量'].values
    for index,contract in enumerate(contractlist):
        #根据合约推断标的
        if contract not in contractdict.keys():
            if contract[0].isdigit():
                underlying = contract
            else:
                underlying=re.findall(r'^\D.',contract.split('.')[0])[0].lower()
        else:
            underlying=contractdict[contract]
        #查找合约乘数
        if underlying in multidict.keys():
            multi=multidict[underlying]
        else:
            multi=1
        #计算当日持仓
        todayhold=contractamt[index]
        tmpcontract=contract.split('.')[0]+'.'+underlyingdict[contract.split('.')[-1]]
        #获取当日价格
        price=w.wsd(tmpcontract, "close,settle", "ED0D", str(date), "")
        closeprice=price.Data[0][0]
        settleprice = price.Data[1][0]
        #对于股票没有行权价，默认为收盘价
        if pd.isnull(settleprice):
            settleprice=closeprice
        #查询数据库获得总持仓并更新
        totalhold=obj.selectValue('tmppnldb', ['totalHold'], 'hedgeContract = "%s"'%contract, 'ORDER BY ID DESC LIMIT 1')
        if totalhold==[]:
            totalhold=0
        else:
            totalhold=totalhold[0][0]
        totalhold+=todayhold
        #插入数据库
        collist=['underlyingCode','Multi','hedgeContract','todayHold','settlePrice','closePrice','totalHold','Date']
        vallist=[underlying,multi,contract,todayhold,settleprice,closeprice,totalhold,date]
        vallist = map(lambda x: str(x), vallist)
        obj.insertValue('tmppnldb', collist, vallist)
