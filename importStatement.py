#coding=gbk
from DBManager2 import connMySQL
import pandas as pd
import re

obj=connMySQL()

#ETF��Ӧ��Ĺ�ϵ
contractdict={'510300.SH':'IF','512660.SH':'399967.SZ',
              '512980.SH':'399971.SZ','159928.SZ':'000932.SH',
              '512800.SH':'399986.SZ'}

def insertMysqlValue(x,dbname):
    contract=x['����']
    #���ݺ�Լ���뻮�ֱ��
    if contract not in contractdict.keys():
        if contract[0].isdigit():
            underlying = contract
        else:
            underlying = re.findall(r'^\D.', contract.split('.')[0])[0].lower()
    else:
        underlying = contractdict[contract]
    #���ݿ��ֵ
    colname=['strategyId','tradeAccount','tradeComment','strikeId','underlyingCode','tradeAmt','tradePrice','tradeTime','tradeId','bidNask','openNclose','totalTradeAmt','avgPrice','tradeDate','underlying']
    vallist=x.values.tolist()
    vallist.append(underlying)
    vallist=map(lambda x:str(x),vallist)
    try:
        obj.insertValue(dbname,colname,vallist)
    except:
        return

#�������ݿ�
createSql='''
    CREATE TABLE IF NOT EXISTS `pnldb`.`statement` (
      `ID` INT NOT NULL AUTO_INCREMENT,
      `strategyId` VARCHAR(10) NOT NULL DEFAULT 'otc',
      `tradeAccount` VARCHAR(30) NOT NULL,
      `tradeComment` VARCHAR(50) NOT NULL,
      `strikeId` VARCHAR(20) NOT NULL,
      `underlyingCode` VARCHAR(15) NOT NULL,
      `underlying` VARCHAR(10) NOT NULL,
      `tradeAmt` INT NOT NULL,
      `tradePrice` DECIMAL(20,10) NOT NULL,
      `tradeTime` VARCHAR(20) NOT NULL,
      `tradeId` VARCHAR(20) NOT NULL,
      `bidNask` ENUM('1','2') NOT NULL,
      `openNclose` ENUM('O', 'C','T','Y') NOT NULL,
      `totalTradeAmt` INT NOT NULL,
      `avgPrice` DECIMAL(20,10) NOT NULL,
      `tradeDate` DATETIME NOT NULL,
      PRIMARY KEY (`ID`)
    )ENGINE = InnoDB;
'''

obj.executeSQL(strSQL=createSql)

#��ˮ�����
dfold=pd.read_excel('�Գ�ͷ������.xlsx',sheet_name='��ˮ���ܾ�')
dfnew=pd.read_excel('�Գ�ͷ������.xlsx',sheet_name='��ˮ����')
dftotal=pd.concat([dfold,dfnew])
dftotal.reset_index(drop=True,inplace=True)

strikeId=obj.selectValue('statement', ['strikeId'],'','ORDER BY ID DESC LIMIT 1' )

#��������
if strikeId==[]:
    print r'Empty database, start initializing.'
    df=dftotal
else:
    strikeId=int(strikeId[0][0])
    print r'The lastest strikeId is ' + str(strikeId)+ r', start updating statement data.'
    df = dftotal[dftotal[dftotal['�ɽ�ID'] == strikeId].index[0]:]

df.apply(insertMysqlValue,args=('statement',),axis=1)

print r'Finish statement data updating.'