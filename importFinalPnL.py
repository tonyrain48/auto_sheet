from DBManager2 import connMySQL
from WindPy import *
import datetime as dt
import pandas as pd

w.start()

obj=connMySQL()

multidict={'if':300,'au':1000,'ih':300,'ic':200,'cu':5,
           'ap':10,'pp':5,'oi':10,'sc':1000,'cf':5,
           'm':10,'c':10,'sf':5,'jm':60,'zc':100,
           'al':5,'hc':10,'rb':10,'i':100,'fg':20,
           'ta':5,'ag':15,'sr':10,'ru':10,'L':5,'J':100,
           'jd':10,'y':10,'p':10,}

underlying='ic'

#起始日期
totalstart=obj.selectValue('tmppnldb',['Date'], 'underlyingCode="%s"'%underlying,'order by Date limit 1')[0][0]
totaldatelist=w.tdays(totalstart, dt.datetime.today(), "").Data[0]

if obj.selectValue('finalpnldb',['tradeDate'], 'underlyingCode="%s"'%underlying,'order by tradeDate desc limit 1')==[]:
    startdate=obj.selectValue('tmppnldb',['Date'], 'underlyingCode="%s"'%underlying,'order by Date limit 1')[0][0]
else:
    startdate=obj.selectValue('finalpnldb',['tradeDate'], 'underlyingCode="%s"'%underlying,'order by tradeDate desc limit 1')[0][0]
    startdate=startdate+dt.timedelta(days=1)
    print startdate

datelist=w.tdays(startdate, dt.datetime.today(), "").Data[0]

underlyingdict={'SH':'SH','SZ':'SZ','XSGE':'SHF','XINE':'INE',
                'CCFX':'CFE','XZCE':'CZC','XDCE':'DCE','SGE':'SGE'}

minuslist = ['510300.SH']

#逐日更新
for index,calcdate in enumerate(datelist):
    #如果是第一天，则把今日昨日作为一天代入计算；否则按照昨交易日日期作为昨日日期
    if totaldatelist.index(calcdate)==0:
        print('True')
        yesterday=calcdate
        today=calcdate
    else:
        yesterday=totaldatelist[totaldatelist.index(calcdate)-1]
        today=calcdate
    yesterday=yesterday.strftime('%Y-%m-%d')
    today=today.strftime('%Y-%m-%d')

    tradecostlist=obj.selectValue('statement',['underlyingCode','tradeAmt','tradePrice','bidNask'], 'underlying="%s" and tradeDate="%s"'%(underlying,today),'')

    #计算当日交易成本
    todaycost=0
    for cost in tradecostlist:
        if cost[0] not in minuslist:
            if int(cost[-1])==1:
                todaycost += -multidict[underlying] * (cost[1] * cost[2])
            else:
                todaycost -= -multidict[underlying] * (cost[1] * cost[2])
        else:
            if int(cost[-1]) == 1:
                todaycost -= cost[1] * cost[2]
            else:
                todaycost += cost[1] * cost[2]

    #查数据库查看标的对应合约
    contractsql='''
        SELECT distinct hedgeContract FROM tmppnldb 
        where underlyingCode="%s" and date<="%s"
    '''%(underlying,today)

    contractlist=obj.selectExecuteSQL(contractsql)
    contractlist=[i for k in contractlist for i in k]

    settlepnl = todaycost
    closepnl = todaycost
    deltapnl = 0
    calcdict = {}

    for contract in contractlist:
        #获取当天和昨天的合约数据
        todaysql='''
            select Multi,hedgeContract,totalHold from tmppnldb 
            where `Date`=(select date from tmppnldb where `Date`<="%s" 
            and hedgeContract="%s" order by date desc limit 1) 
            and hedgeContract="%s";
        '''%(today,contract,contract)

        yesterdaysql='''
            select Multi,hedgeContract,totalHold from tmppnldb 
            where `Date`=(select date from tmppnldb where `Date`<="%s" 
            and hedgeContract="%s" order by date desc limit 1) 
            and hedgeContract="%s";
        '''%(yesterday,contract,contract)

        todaydata=obj.selectExecuteSQL(todaysql)
        yesterdaydata=obj.selectExecuteSQL(yesterdaysql)

        #获取今天和昨天的收盘价行权价
        for data in todaydata:
            multi=data[0]
            underlyingcontract=data[1]
            totalhold=data[2]
            calcdict[underlyingcontract]={}
            tmpcontract = underlyingcontract.split('.')[0] + '.' + underlyingdict[underlyingcontract.split('.')[-1]]
            price = w.wsd(tmpcontract, "close,settle", "ED0D", today, "")
            if pd.isnull(price.Data[1][0]):
                price.Data[1][0]=price.Data[0][0]
            closeprice = price.Data[0][0] if price.Data[0][0]!=None else 0
            settleprice = price.Data[1][0] if price.Data[1][0]!=None else 0
            calcdict[underlyingcontract]['nowcloseprice']=closeprice
            calcdict[underlyingcontract]['nowsettleprice']=settleprice
            calcdict[underlyingcontract]['nowamt']=totalhold
            calcdict[underlyingcontract]['multi']=multi

        for data in yesterdaydata:
            if totaldatelist.index(calcdate)==0:
                calcdict[underlyingcontract]['precloseprice'] = 0
                calcdict[underlyingcontract]['presettleprice'] = 0
                calcdict[underlyingcontract]['preamt'] = 0
            else:
                multi = data[0]
                underlyingcontract = data[1]
                totalhold = data[2]
                tmpcontract = underlyingcontract.split('.')[0] + '.' + underlyingdict[underlyingcontract.split('.')[-1]]
                price = w.wsd(tmpcontract, "close,settle", "ED0D", yesterday, "")
                if pd.isnull(price.Data[1][0]):
                    price.Data[1][0] = price.Data[0][0]
                closeprice = price.Data[0][0] if price.Data[0][0]!=None else 0
                settleprice = price.Data[1][0] if price.Data[1][0]!=None else 0
                if underlyingcontract not in calcdict.keys():
                    calcdict[underlyingcontract]={}
                calcdict[underlyingcontract]['precloseprice'] = closeprice
                calcdict[underlyingcontract]['presettleprice'] = settleprice
                calcdict[underlyingcontract]['preamt'] = totalhold
                calcdict[underlyingcontract]['multi'] = multi

    #计算pnl
    for key,val in calcdict.items():
        if 'presettleprice' not in val.keys():
            tmpcontract = key.split('.')[0] + '.' + underlyingdict[key.split('.')[-1]]
            price = w.wsd(tmpcontract, "close,settle", "ED0D", yesterday, "")
            if pd.isnull(price.Data[1][0]):
                price.Data[1][0]=price.Data[0][0]
            closeprice = price.Data[0][0] if price.Data[0][0]!=None else 0
            settleprice = price.Data[1][0] if price.Data[1][0]!=None else 0
            calcdict[key]['precloseprice'] = closeprice
            calcdict[key]['presettleprice'] = settleprice
            calcdict[key]['preamt']=0
        if 'nowsettleprice' not in val.keys():
            tmpcontract = key.split('.')[0] + '.' + underlyingdict[key.split('.')[-1]]
            price = w.wsd(tmpcontract, "close,settle", "ED0D", today, "")
            if pd.isnull(price.Data[1][0]):
                price.Data[1][0]=price.Data[0][0]
            closeprice = price.Data[0][0] if price.Data[0][0]!=None else 0
            settleprice = price.Data[1][0] if price.Data[1][0]!=None else 0
            calcdict[key]['nowcloseprice'] = closeprice
            calcdict[key]['nowsettleprice'] = settleprice
            calcdict[key]['nowamt'] = calcdict[key]['preamt']
        if key not in minuslist:
            settlepnl = float(settlepnl)+val['multi']*val['nowsettleprice']*val['nowamt']-val['multi']*val['presettleprice']*val['preamt']
            closepnl = float(closepnl)+val['multi']*val['nowcloseprice']*val['nowamt']-val['multi']*val['precloseprice']*val['preamt']
            deltapnl = float(deltapnl)+(float(val['nowcloseprice']) - float(val['precloseprice'])) * float(val['multi']) * float(val['preamt'])
        else:
            print val
            settlepnl = float(settlepnl)+val['nowsettleprice']*val['nowamt']-val['presettleprice']*val['preamt']
            closepnl = float(closepnl)+val['nowcloseprice']*val['nowamt']-val['precloseprice']*val['preamt']
            deltapnl = float(deltapnl)+(float(val['nowcloseprice']) - float(val['precloseprice'])) * float(val['preamt'])

    gammapnl=float(closepnl)-deltapnl

    #计算pnl总和
    sumlist=obj.selectValue('finalpnldb',['closeSumPnL','settleSumPnL'], 'underlyingCode="%s" and tradeDate<="%s"'%(underlying,yesterday),' order by tradeDate desc limit 1')

    if sumlist==[]:
        closesumpnl=closepnl
        settlesumpnl=settlepnl
    else:
        closesumpnl=float(sumlist[0][0])+closepnl
        settlesumpnl=float(sumlist[0][1])+settlepnl

    #插入数据库
    collist=['underlyingCode','todayTradeCost','closePnL','closeSumPnL','settlePnL','settleSumPnL','deltaPnL','gammaPnL','tradeDate']
    vallist=[underlying,todaycost,closepnl,closesumpnl,settlepnl,settlesumpnl,deltapnl,gammapnl,today]
    vallist = map(lambda x: str(x), vallist)
    obj.insertValue('finalpnldb', collist, vallist)