#coding=gbk
from DBManager2 import connMySQL
import pandas as pd
import re

f=pd.ExcelFile(r'对冲头寸损益.xlsx')

obj=connMySQL()

# coldict={'日期':'Date','合约乘数':'contractMulti','当日交易成本':'todayTradeCost',
#          '对冲合约1':'hedgeContract1','当日持仓变动1':'todayHoldChange1',
#          '结算价1':'strikePrice1','收盘价1':'closePrice1','累计持仓1':'totalHold1',
#          '对冲合约2': 'hedgeContract2', '当日持仓变动2': 'todayHoldChange2',
#          '结算价2': 'strikePrice2', '收盘价2': 'closePrice2', '累计持仓2': 'totalHold2',
#          '对冲合约3':'hedgeContract3','当日持仓变动3':'todayHoldChange3',
#          '结算价3':'strikePrice3','收盘价3':'closePrice3','累计持仓3':'totalHold3',
#          '对冲合约4':'hedgeContract4','当日持仓变动4':'todayHoldChange4',
#          '结算价4':'strikePrice4','收盘价4':'closePrice4','累计持仓4':'totalHold4',
#          '对冲合约5':'hedgeContract5','当日持仓变动5':'todayHoldChange5',
#          '结算价5':'strikePrice5','收盘价5':'closePrice5','累计持仓5':'totalHold5',
#          '结算价当日盈亏':'todayStrikePnL','结算价累计总盈亏':'totalStrikePnL',
#          '收盘价当日盈亏':'todayClosePnL','收盘价累计总盈亏':'totalClosePnL',
#          '昨日Delta盈亏':'deltaPnL','今日Gamma盈亏':'gammaPnL'}

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
#     if name not in [r'流水汇总旧',r'交易日',r'流水汇总',r'指数增强流水汇总',r'买入期权流水汇总',r'CorrPro1损益',r'CorrPro2损益','CorrPro3损益']:
#         df = pd.read_excel('对冲头寸损益.xlsx', sheet_name=name)
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




df=pd.read_excel('对冲头寸损益.xlsx',sheet_name='流水汇总旧')
dfnew=pd.read_excel('对冲头寸损益.xlsx',sheet_name='流水汇总')
df=pd.concat([df,dfnew])
df.reset_index(drop=True,inplace=True)
obj=connMySQL()
df.apply(insertMysqlValue,args=('statement',),axis=1)
# df.apply(insertMysqlValue,axis=1)