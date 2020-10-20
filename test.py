#coding=gbk
from DBManager2 import connMySQL
import pandas as pd
import re

f=pd.ExcelFile(r'�Գ�ͷ������.xlsx')

obj=connMySQL()

# coldict={'����':'Date','��Լ����':'contractMulti','���ս��׳ɱ�':'todayTradeCost',
#          '�Գ��Լ1':'hedgeContract1','���ճֱֲ䶯1':'todayHoldChange1',
#          '�����1':'strikePrice1','���̼�1':'closePrice1','�ۼƳֲ�1':'totalHold1',
#          '�Գ��Լ2': 'hedgeContract2', '���ճֱֲ䶯2': 'todayHoldChange2',
#          '�����2': 'strikePrice2', '���̼�2': 'closePrice2', '�ۼƳֲ�2': 'totalHold2',
#          '�Գ��Լ3':'hedgeContract3','���ճֱֲ䶯3':'todayHoldChange3',
#          '�����3':'strikePrice3','���̼�3':'closePrice3','�ۼƳֲ�3':'totalHold3',
#          '�Գ��Լ4':'hedgeContract4','���ճֱֲ䶯4':'todayHoldChange4',
#          '�����4':'strikePrice4','���̼�4':'closePrice4','�ۼƳֲ�4':'totalHold4',
#          '�Գ��Լ5':'hedgeContract5','���ճֱֲ䶯5':'todayHoldChange5',
#          '�����5':'strikePrice5','���̼�5':'closePrice5','�ۼƳֲ�5':'totalHold5',
#          '����۵���ӯ��':'todayStrikePnL','������ۼ���ӯ��':'totalStrikePnL',
#          '���̼۵���ӯ��':'todayClosePnL','���̼��ۼ���ӯ��':'totalClosePnL',
#          '����Deltaӯ��':'deltaPnL','����Gammaӯ��':'gammaPnL'}

def insertMysqlValue(x,dbname):
    # colname=df.columns
    colname=['strategyId','tradeAccount','tradeComment','strikeId','underlyingCode','tradeAmt','tradePrice','tradeTime','tradeId','bidNask','openNclose','totalTradeAmt','avgPrice','tradeDate']
    vallist=x.values
    vallist=map(lambda x:str(x),vallist)
    # obj.insertValue(dbname, colname, vallist)
    try:
        obj.insertValue(dbname,colname,vallist)
    except:
        return

# for name in f.sheet_names:
#     if name not in [r'��ˮ���ܾ�',r'������',r'��ˮ����',r'ָ����ǿ��ˮ����',r'������Ȩ��ˮ����',r'CorrPro1����',r'CorrPro2����','CorrPro3����']:
#         df = pd.read_excel('�Գ�ͷ������.xlsx', sheet_name=name)
#         df.rename(columns=coldict,inplace=True)
#         df.fillna('0',inplace=True)
#         pattern = re.compile(r'[^\u4e00-\u9fa5]')
#         name=re.sub(pattern, '', name).replace('.','')+'_pnl'
#         sql='''
#             CREATE TABLE IF NOT EXISTS `pnldb`.`'''+name+'''` (
#               `ID` INT NOT NULL AUTO_INCREMENT,
#               `Date` DATETIME NOT NULL,
#               `contractMulti` INT NULL DEFAULT 0,
#               `todayTradeCost` DECIMAL(12,2) NOT NULL DEFAULT 0,
#               `hedgeContract1` VARCHAR(15) NOT NULL,
#               `todayHoldChange1` INT NOT NULL DEFAULT 0,
#               `strikePrice1` DECIMAL(12,2) NOT NULL DEFAULT 0,
#               `closePrice1` DECIMAL(12,2) NOT NULL DEFAULT 0,
#               `totalHold1` INT NOT NULL DEFAULT 0,
#               `hedgeContract2` VARCHAR(15) NOT NULL,
#               `todayHoldChange2` INT NOT NULL DEFAULT 0,
#               `strikePrice2` DECIMAL(12,2) NOT NULL DEFAULT 0,
#               `closePrice2` DECIMAL(12,2) NOT NULL DEFAULT 0,
#               `totalHold2` INT NOT NULL DEFAULT 0,
#               `hedgeContract3` VARCHAR(15) NOT NULL DEFAULT 'NULL',
#               `todayHoldChange3` INT NOT NULL DEFAULT 0,
#               `strikePrice3` DECIMAL(12,2) NOT NULL DEFAULT 0,
#               `closePrice3` DECIMAL(12,2) NOT NULL DEFAULT 0,
#               `totalHold3` INT NOT NULL DEFAULT 0,
#               `hedgeContract4` VARCHAR(15) NOT NULL DEFAULT 'NULL',
#               `todayHoldChange4` INT NOT NULL DEFAULT 0,
#               `strikePrice4` DECIMAL(12,2) NOT NULL DEFAULT 0,
#               `closePrice4` DECIMAL(12,2) NOT NULL DEFAULT 0,
#               `totalHold4` INT NOT NULL DEFAULT 0,
#               `hedgeContract5` VARCHAR(15) NOT NULL DEFAULT 'NULL',
#               `todayHoldChange5` INT NOT NULL DEFAULT 0,
#               `strikePrice5` DECIMAL(12,2) NOT NULL DEFAULT 0,
#               `closePrice5` DECIMAL(12,2) NOT NULL DEFAULT 0,
#               `totalHold5` INT NOT NULL DEFAULT 0,
#               `todayStrikePnL` INT NOT NULL DEFAULT 0,
#               `totalStrikePnL` INT NOT NULL DEFAULT 0,
#               `todayClosePnL` INT NOT NULL DEFAULT 0,
#               `totalClosePnL` INT NOT NULL DEFAULT 0,
#               `deltaPnL` INT NOT NULL DEFAULT 0,
#               `gammaPnL` INT NOT NULL DEFAULT 0,
#                PRIMARY KEY (`ID`))
#             ENGINE = InnoDB;
#         '''
#         obj.executeSQL(strSQL=sql)
#         df.apply(insertMysqlValue,args=(name,),axis=1)




df=pd.read_excel('�Գ�ͷ������.xlsx',sheet_name='��ˮ���ܾ�')
dfnew=pd.read_excel('�Գ�ͷ������.xlsx',sheet_name='��ˮ����')
df=pd.concat([df,dfnew])
df.reset_index(drop=True,inplace=True)
obj=connMySQL()
df.apply(insertMysqlValue,args=('statement',),axis=1)
# df.apply(insertMysqlValue,axis=1)