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
 xml data to mysql
'''

import re
import time
import datetime as dt
import numpy as np
#reload(sys)  
#sys.setdefaultencoding('utf-8')
from Control.DBManager import connMySQL
from Model.globalInfo import GlobalInfo

from wind_py import w

class LoadWindData:
    def __init__(self, dbobj=None):
        # w.start()
        self.dbobj =  dbobj
    def __del__(self):
        # w.stop()
        pass

    def start_wind(self):
        w.start()
    def stop_wind(self):
        w.stop()
    #NOTICE: ADD NEW UNDERLYING HERE 
    def get_underlyding_price(self):
        underlyding_list = set(self.get_underlying_codelist())
        today = str(dt.datetime.now().strftime("%Y-%m-%d"))
        # end_date = str(datetime.datetime.now()) #-datetime.timedelta(days=1)
        # print underlyding_list
        underlyingDict = dict(zip(GlobalInfo.underlyingHead, GlobalInfo.underlyingType))
        currentTime = dt.datetime.now()
        # print underlyding_list
        for code in underlyding_list:
            temp_list=[]
            if (currentTime.hour+ currentTime.minute/60.0)> 9.5 and currentTime.hour<15:
                if "Basket" in code:
                    print code
                    data = self.portfolio_index(GlobalInfo.BasketCodeWind[code], GlobalInfo.BasketS0Wind[code] , data_type='wsq')
                else:
                    if code in GlobalInfo.StockList:
                        # data=w.wsd(code,"close", today, today, 'PriceAdj=B').Data[0][0]
                        data = w.wsd(code, "close", today, today,"").Data[0][0]
                        # print data
                    else:
                        data=w.wsq(code,'rt_last').Data[0][0]
            else:
                if "Basket" in code:
                    print code
                    data = self.portfolio_index(GlobalInfo.BasketCodeWind[code], GlobalInfo.BasketS0Wind[code])
                else:
                    if code in GlobalInfo.StockList:
                        # data=w.wsd(code,"close", today, today, 'PriceAdj=B').Data[0][0]
                        data = w.wsd(code, "close", today, today,"").Data[0][0]
                    else:
                        data=w.wsd(code,"close", today).Data[0][0]
            
            w1 = today
            w2 = str(code)
            w_2 = str(code.split('.')[0])
            if "Basket" in code:
                w3 = round(data, 6)
            else:
                w3 = round(data, 4)
            code_len = len(re.findall(r'(\d+)',w_2)[0])
            code_head = str(w_2[:-code_len])

            if "000300" == w_2:
                w4 = "HS300"
            elif  "000905" == w_2:
                w4 = "CSI500"
            elif  "000016" == w_2:
                w4 = "SSE50"
            elif  "510050" == w_2:
                w4 = "50ETF"
            elif "AU9999" == w_2:
                w2 = w_2
                w4 = "XAurum"            
            elif "Basket" in w_2:
                w2 = w_2
                w4 = w2
            else:
                if w2 in GlobalInfo.StockList:
                    w4 = w2
                else:
                    w4 = underlyingDict[code_head]
                    w2 = w_2
        
            temp_list = [w1, w2, w3, w4]

            if temp_list!=[]:
                # pass
                if w2 =="AU9999":
                    idcondition = 'recorddate = "'  + str( GlobalInfo.today) + '" and code = "AU9999"'
                    _holdlst =  self.dbobj.selectValue('greeksunderlying',  ['recorddate', 'closeprice'], idcondition)  #获取最新期货损益 
                    if _holdlst ==[]:
                        self.dbobj.insertValue('greeksunderlying', GlobalInfo.greekssettlecol, temp_list)
                    else:
                        pass
                else:
                    self.dbobj.insertValue('greeksunderlying', GlobalInfo.greekssettlecol, temp_list)

            # print '---',temp_list
    def portfolio_index(self, code_list, S0, data_type='wsd', re_month = None):
        today = str(dt.datetime.now().strftime("%Y-%m-%d"))
        str_code_list = ','.join(code_list)
        # avg = lambda sequence: sum(sequence)*1.0/len(sequence)
        if re_month is None:
            pass
        else:
            # str_code_list = re.sub(r'(\d\d\d\.)', re_month[1:]+'.', str_code_list)
            pass

        data = [0]
        if data_type == 'wsq':
            data=np.array(w.wsq(str_code_list,'rt_last').Data[0])
        else:
            data=np.array(w.wsd(str_code_list,"close", today).Data[0])
        
        close_price = float(np.mean(data/np.array(S0)))
        print "Basket close price", close_price

        return close_price


    def get_settle_price(self):
        settle_codelist = self.get_settle_codelist()
        # code_list =[]
        # for elm in settle_codelist:
        #     code=elm[0]
        #     underlying = elm[1]
        #     code +=  GlobalInfo.underlyingDictCodeWind[underlying]
        #     code_list.append(code)
        
        today = str(dt.datetime.now().strftime("%Y-%m-%d"))
        hedgeCodeHeadDict = dict(zip(GlobalInfo.hedgeCodeHead, GlobalInfo.underlyingType))
        hedgeCodeMultiplierDict = dict(zip(GlobalInfo.hedgeCodeHead, GlobalInfo.hedgeCodeMultiplier))
        hedgeCodeTailWind = dict(zip( GlobalInfo.underlyingType, GlobalInfo.hedgeCodeTailWind))

        valtype=['%s']*len(GlobalInfo.settlecol)
        vals = []

        currentTime = dt.datetime.now()
        for elm in settle_codelist:
            _holdlst =[]
            code=elm[0]
            underlying = elm[1]
            # print underlying

            if 'au' in code:
                idcondition = ' variablename = "%s"'%(code)
                _holdlst =  self.dbobj.selectValue('globals',  ['variablevalue','variablevalue2'], idcondition)  #获取最新期货损益 

            if code in GlobalInfo.StockList:
                wind_code = code
            else:
                wind_code = code.split('.')[0] + hedgeCodeTailWind[underlying]
            
            if _holdlst ==[]:

                if (currentTime.hour+ currentTime.minute/60.0)> 9.5 and currentTime.hour<15:
                    data=w.wsq(wind_code,'rt_last').Data
                    w3 = round(data[0][0], 4)
                    w4 = round(data[0][0], 4)
                else:
                    # print wind_code
                    data=w.wsd(wind_code,"CLOSE,SETTLE", today).Data

                    try:
                        w3 = round(data[0][0], 4)
                    except:
                        print wind_code
                    w4 = data[1][0]
                    if str(w4)=='nan':
                        w4 = w3
                    else:
                        w4 = round(data[1][0], 4)
            else:
                w3 = round(_holdlst[0][1], 4)
                w4 = round(_holdlst[0][0], 4)

            # print w4
            temp_list = []
            w1 = today
            w2 = str(code)
            w_2 = str(code)

            # w3 = round(data[0][0], 2)
            # w4 = round(data[1][0], 2)
            w5 = "HS300"
            w6 = 300
            
            if w_2 in GlobalInfo.StockList:
                w5 = w_2
                w6 = 1
            else:
                w2 = w2[re.match( r'\D+',w2).start():re.match( r'\D+',w2).end()]

                if 'au' in w2:
                    w2 = 'au'
                
                w5 = hedgeCodeHeadDict[w2]
                w6 = hedgeCodeMultiplierDict[w2]
        
            temp_list = [w1, w_2, w3, w4,w5, w6]  

            if temp_list!=[]:
                # pass
                if temp_list not in vals:
                    vals.append(temp_list)
        # print vals
        self.dbobj.insertMany('settle', GlobalInfo.settlecol, valtype, vals)

            # print '---',temp_list     

    def get_settle_codelist(self):
        ''' get current hold contracts, return contract list without suffix'''

        _numList =[]
        for row, underlying in enumerate(GlobalInfo.underlyingType):
            idcondition = 'underlying = "'  + str( underlying) + '"'
            _lstinfo =  self.dbobj.selectValue('transaction',  ['distinct(code)', 'underlying'], idcondition)  

            for elm in _lstinfo:
                idcondition = 'code = "'  + str( elm[0]) + '"'
                _num =  self.dbobj.selectValue('transaction',  ['sum(posnum)'], idcondition) 

                idcondition = 'entrustdate < (select max(entrustdate) from transaction) and code = "'  + str(  elm[0]) + '"'
                # idcondition = 'entrustdate < "' + str(GlobalInfo.curDate)+ '" and code = "'  + str(  elm[0]) + '"'
                pre_num =  self.dbobj.selectValue('transaction',  ['sum(posnum)'], idcondition)
                if pre_num[0][0]==None:
                    pre = 0
                else:
                    pre = int(pre_num[0][0])
                # _num[0][0] == 0 and pre==0:
                if _num[0][0] == 0:
                    continue
                else:
                    _numList.append([elm[0],elm[1]])

        return _numList


    def get_underlying_codelist(self):
        ''' get current hold contracts, return contract list without suffix'''
        idcondition = 'contractstatus != -1 and knockoutstatus !=1 '
        _lstinfo =  self.dbobj.selectValue('tradingbook',  ['distinct(code)', 'underlying'], idcondition)  
        code_list =[]
        underlyingTailWind = dict(zip( GlobalInfo.underlyingType, GlobalInfo.underlyingTailWind))
        for elm in _lstinfo:
            code=elm[0]
            underlying = elm[1]
            if underlying in GlobalInfo.StockList or "Basket" in underlying:
                code = elm[0]
            elif underlying in GlobalInfo.indexcode :
                code =  underlyingTailWind[underlying]
            else:
                code +=  underlyingTailWind[underlying]
            code_list.append(code)
        
        _lstinfo =  self.dbobj.selectValue('exchangetb',  ['distinct(underlyingcode)', 'underlying'], '')  
        for elm in _lstinfo:
            code=elm[0]
            underlying = elm[1]
            if underlying in GlobalInfo.StockList or "Basket" in underlying:
                code = elm[0]
            elif underlying in GlobalInfo.indexcode :
                code =  underlyingTailWind[underlying]
            else:
                code +=  underlyingTailWind[underlying]
            code_list.append(code)

        return code_list

    def get_month_code(self,underlying):
        today = dt.date.today()
        time_code = str(today.year)[2:]

        end = int(dt.datetime(today.year, today.month, today.day).strftime("%W"))
        begin = int(dt.datetime(today.year, today.month, 1).strftime("%W"))
        month = today.month

        if end - begin + 1 <3 or (end - begin + 1 ==3 and dt.datetime.weekday(today)<=4):

            if underlying in ["Palm","Y","JD"]:
                month +=1
            if  month < 10:
                time_code = time_code + "0" + str(month)
            else:
                time_code = time_code +  str(month)

        else:

            if month < 9:
                time_code = time_code + "0" + str(month+1)
            elif month <12:
                time_code = time_code + str(month+1)
            else:
                time_code = str(today.year+1)[2:] +  "01"

        return time_code

    def get_future_list(self):
        hedgeCodeTailWind = dict(zip( GlobalInfo.underlyingType, GlobalInfo.hedgeCodeTailWind))
        hedgeCodeHeadDict = dict(zip(GlobalInfo.underlyingType, GlobalInfo.hedgeCodeHead))
        
        code_dict = {}
        # print time_code[1:],time_code
        for row, underlying in enumerate(GlobalInfo.underlyingType):
            time_code = self.get_month_code(underlying)
            if hedgeCodeTailWind[underlying] == '.CZC':  #郑商所的时间1805改为805
                code_dict[underlying] =  hedgeCodeHeadDict[underlying] + time_code[1:] + hedgeCodeTailWind[underlying]
            else:
                if underlying in ['XAurum']:
                    code_dict[underlying] =  hedgeCodeHeadDict['Aurum'] + time_code + hedgeCodeTailWind['Aurum']
                elif underlying in ['50ETF']:
                    code_dict[underlying] =  hedgeCodeHeadDict['SSE50'] + time_code + hedgeCodeTailWind['SSE50']
                elif 'Basket' in underlying:
                    code_dict[underlying] = underlying + '/' + time_code
                else:
                    code_dict[underlying] =  hedgeCodeHeadDict[underlying] + time_code + hedgeCodeTailWind[underlying]

        return code_dict

    def get_future_price(self):
        underlyding_list = self.get_future_list()
        today = str(dt.datetime.now().strftime("%Y-%m-%d"))
        
        valtype=['%s']*len(GlobalInfo.greekssettlecol)
        vals = []

        currentTime = dt.datetime.now()
        # print underlyding_list
        for underlying, code in underlyding_list.items():
            temp_list=[]
            if (currentTime.hour+ currentTime.minute/60.0)> 9.5 and currentTime.hour<15:
                if "Basket" in underlying:
                    month = code.split('/')[1]
                    data = self.portfolio_index(GlobalInfo.BasketCodeWind[underlying], GlobalInfo.BasketS0Wind[underlying] , data_type='wsq', re_month = month)
                else:
                    data=w.wsq(code,'rt_last').Data[0][0]
            else:
                if "Basket" in underlying:
                    month = code.split('/')[1]
                    data = self.portfolio_index(GlobalInfo.BasketCodeWind[underlying], GlobalInfo.BasketS0Wind[underlying], re_month = month)
                else:
                    data=w.wsd(code,"close", today).Data[0][0]
            w1 = today
            w2 = str(code)
            if "Basket" in code:
                w3 = data
            else:
                w3 = round(data, 4)

            w4 = underlying
        
            temp_list = [w1, w2, w3, w4]

            if temp_list!=[]:
                # pass
                vals.append(temp_list)
        # print vals
        self.dbobj.insertMany('greeksfuture', GlobalInfo.greekssettlecol, valtype, vals)

if __name__ == "__main__":
    obj = LoadWindData()
    obj.get_settle_codelist()
    #excelWriter()
