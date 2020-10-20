#coding=gbk
from DBManager2 import connMySQL
import re
import pandas as pd
from WindPy import *

w.start()


obj=connMySQL()

#�������ݿ�
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

#��ˮ�����
dfold=pd.read_excel('�Գ�ͷ������.xlsx',sheet_name='��ˮ���ܾ�')
dfnew=pd.read_excel('�Գ�ͷ������.xlsx',sheet_name='��ˮ����')
dftotal=pd.concat([dfold,dfnew])
dftotal.reset_index(drop=True,inplace=True)

contractdict={'510300.SH':'IF','512660.SH':'399967.SZ',
              '512980.SH':'399971.SZ','159928.SZ':'000932.SH',
              '512800.SH':'399986.SZ'}

#�޸ĺ�׺����wind��ѯ�۸�
underlyingdict={'SH':'SH','SZ':'SZ','XSGE':'SHF','XINE':'INE',
                'CCFX':'CFE','XZCE':'CZC','XDCE':'DCE','SGE':'SGE'}

#��Լ����
multidict={'if':300,'au':1000,'ih':300,'ic':200,'cu':5,
           'ap':10,'pp':5,'oi':10,'sc':1000,'cf':5,
           'm':10,'c':10,'sf':5,'jm':60,'zc':100,
           'al':5,'hc':10,'rb':10,'i':100,'fg':20,
           'ta':5,'ag':15,'sr':10,'ru':10,'L':5,'J':100,
           'jd':10,'y':10,'p':10,}

datelist=dftotal['ί������'].unique()[0]

#���ո���
for date in datelist:
    df = dftotal[dftotal['ί������'] == date]
    df.loc[df['����'] != 1, '�ɽ�����'] = -df['�ɽ�����']
    contractlist=df.groupby('����').sum()['�ɽ�����'].index
    contractamt=df.groupby('����').sum()['�ɽ�����'].values
    for index,contract in enumerate(contractlist):
        #���ݺ�Լ�ƶϱ��
        if contract not in contractdict.keys():
            if contract[0].isdigit():
                underlying = contract
            else:
                underlying=re.findall(r'^\D.',contract.split('.')[0])[0].lower()
        else:
            underlying=contractdict[contract]
        #���Һ�Լ����
        if underlying in multidict.keys():
            multi=multidict[underlying]
        else:
            multi=1
        #���㵱�ճֲ�
        todayhold=contractamt[index]
        tmpcontract=contract.split('.')[0]+'.'+underlyingdict[contract.split('.')[-1]]
        #��ȡ���ռ۸�
        price=w.wsd(tmpcontract, "close,settle", "ED0D", str(date), "")
        closeprice=price.Data[0][0]
        settleprice = price.Data[1][0]
        #���ڹ�Ʊû����Ȩ�ۣ�Ĭ��Ϊ���̼�
        if pd.isnull(settleprice):
            settleprice=closeprice
        #��ѯ���ݿ����ֲֲܳ�����
        totalhold=obj.selectValue('tmppnldb', ['totalHold'], 'hedgeContract = "%s"'%contract, 'ORDER BY ID DESC LIMIT 1')
        if totalhold==[]:
            totalhold=0
        else:
            totalhold=totalhold[0][0]
        totalhold+=todayhold
        #�������ݿ�
        collist=['underlyingCode','Multi','hedgeContract','todayHold','settlePrice','closePrice','totalHold','Date']
        vallist=[underlying,multi,contract,todayhold,settleprice,closeprice,totalhold,date]
        vallist = map(lambda x: str(x), vallist)
        obj.insertValue('tmppnldb', collist, vallist)
