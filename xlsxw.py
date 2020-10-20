#-*- coding: utf-8 -*-
'''
write dailyreport to excel
'''

import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')

import time
import datetime
import xlsxwriter
from Control.DBManager import connMySQL
from Control.StatTableData import StatTableData
from Model.globalInfo import GlobalInfo

class CreateDailyReport:
    def __init__(self, _file_path = './DailyReport.xlsx'):
        # print _file_path
        self.dbobj =  connMySQL()
        self.std = StatTableData()
        self.workbook = xlsxwriter.Workbook(_file_path)
        self.underlyingType = GlobalInfo.p_underlyingType

        # self.subtitleformat = self.workbook.add_format({'bold': 1, 'font_size':11,'align':'center','valign':'vcenter'})
        self.tableformat = self.workbook.add_format({'bold': 1, 'font_size':10,'align':'center','valign':'vcenter','font_name':u'楷体'})
        # self.contentformat = self.workbook.add_format({'bold': 0, 'font_size':10,'align':'center','valign':'vcenter'})
        # self.date_format = self.workbook.add_format({'num_format':'yyyy/mm/dd'})
        # self.ifformat = self.workbook.add_format({'bold': 0, 'font_size':10,'align':'justify','valign':'top'})

        self.titleFormat = self.workbook.add_format({'bold': 1, 'font_size':18,'align':'center','valign':'vcenter','bg_color':'#D99795','font_name':u'黑体'}) 
        self.date_format = self.workbook.add_format({'bold':1,'num_format':'yyyy/mm/dd'})
        self.subtitleFormat_Onright = self.workbook.add_format({'bold': 1, 'font_size':11,'align':'right','valign':'vcenter','font_name':u'楷体'})
        self.subtitleFormat_Onleft = self.workbook.add_format({'bold': 1, 'font_size':11,'align':'left','valign':'vcenter','font_name':u'楷体'})
        self.tableTitleFormat = self.workbook.add_format({'bold': 1, 'font_size':16,'align':'left','valign':'vcenter','font_name':u'楷体'})
        self.tableItemsFormat_H = self.workbook.add_format({'bold': 1, 'font_size':12,'align':'center','valign':'vcenter','bg_color':'#D99795','font_name':u'楷体','left':0,'right':0,'top':2,'bottom':1})
        self.tableItemsFormat_H1 = self.workbook.add_format({'bold': 1, 'font_size':10,'align':'center','valign':'vcenter','font_name':u'楷体','left':0,'right':0,'top':2,'bottom':1})
        self.tableItemsFormat_V = self.workbook.add_format({'bold': 0, 'font_size':12,'align':'center','valign':'vcenter','font_name':u'楷体'})
        self.tableItemsFormat_V1 = self.workbook.add_format({'bold': 0, 'font_size':10,'align':'center','valign':'vcenter','font_name':u'楷体'})
        self.tableItemsFormat_date_format = self.workbook.add_format({'bold': 0, 'font_size':10,'align':'center','valign':'vcenter','font_name':u'楷体','num_format':'yyyy/mm/dd'})
        self.tableTotalItemFormat = self.workbook.add_format({'bold': 1, 'font_size':10,'align':'center','valign':'vcenter','font_name':u'楷体','top':2,'bottom':0})
        self.ifformat = self.workbook.add_format({'bold': 0, 'font_size':10,'align':'justify','valign':'top'})
        
        self.cellFormat_Onleft = self.workbook.add_format({'bold': 1, 'font_size':11,'align':'left','valign':'vcenter','bg_color':'#F2DDDC','font_name':u'楷体', 'top':1,'bottom':1})
        self.cellFormat_OnHcenter = self.workbook.add_format({'bold': 1, 'font_size':11,'align':'center','valign':'vcenter','bg_color':'#F2DDDC','font_name':u'楷体', 'top':1,'bottom':1})
        self.cellFormat_Oncenter = self.workbook.add_format({'bold': 1, 'font_size':10,'align':'center','valign':'vcenter','font_name':u'楷体'})
        self.cellFormat_Onright = self.workbook.add_format({'bold': 0, 'font_size':10,'align':'right','valign':'vcenter','font_name':u'楷体'})
       
     
    def Summary(self):
        ws = self.workbook.add_worksheet( u'总表')
        titleformat = self.workbook.add_format({'bold': 1, 'font_size':18,'align':'center','valign':'vcenter','bg_color':'#FA8072'})      
        ws.merge_range('C1:G3', u'策略交易与衍生品总部场外期权日报',self.titleFormat)
        infoformat = self.workbook.add_format({'bold': 1, 'font_size':11,'align':'justify','valign':'top','font_name':u'楷体'})

        ws.write('F5', u'日期:', self.subtitleFormat_Onright )
        ws.set_column('G5:G5',12)
        ws.write('G5',datetime.datetime.today() , self.date_format)
        ws.write('B7', u'场外期权信息概况', self.subtitleFormat_Onleft)

        # ws.merge_range('B9:L10', '', self.tableformat)
        # # ws.merge_range('B7:C7', u'场外期权信息概况', ws.format)
        # ws.write_formula('B9', '="  策略交易与衍生品总部共开展了"&沪深300!B3+黄金!B3&"单场外期权业务，总名义本金额"&ROUND((沪深300!H3+黄金!H3)/10^8,2)&"亿元，存量投资规模"&ROUND(G20/10^8,2)&"亿元。"',infoformat)
        ws.merge_range('B9:G10', '', self.tableformat)
        udl_len = len(self.underlyingType)
        _lst =  self.dbobj.selectValue('tradingbook',  ['count(*)'], '')
        ws.write_formula('B9', '="  策略交易与衍生品总部共开展了%s单场外期权业务，总名义本金额"&ROUND((业务概况!H%s)/10^8,2)&"亿元，存量投资规模"&ROUND(业务概况!J%s/10^8,2)&"亿元。"'%(_lst[0][0], udl_len+3,udl_len+3),infoformat)
        # ws.merge_range('B13:L14', '', self.tableformat)
        # ws.write_formula('B13', '="  其中，以黄金为标的共"&黄金!B3&"单。黄金场外期权业务总名义本金额达"&ROUND(黄金!H3/10^8,2)&"亿元,实际存量名义本金额"&ROUND(黄金!G3/10^8,2)&"亿元。"',infoformat)
        
        ws.set_column('B13:I16',20)
        ws.write('B12',u'盈亏统计',self.tableTitleFormat)
        text_PL = [u'业务类型',u'总盈亏（会计）',u'当日盈亏（会计）',u'总盈亏（交易）',u'当日盈亏（交易）',u'Delta风险敞口',u'总投资规模',u'存量投资规模']
        for item in zip(text_PL,['B','C','D','E','F','G','H','I']):
            ws.write(item[1]+'13',item[0],self.tableItemsFormat_H1)

        listArr = self.std.GetSS()

        for row, arr in enumerate(listArr):
            for col, elm in enumerate(arr):
                if isinstance(elm, float):
                    elm = round(elm, 2)
                if row ==len(listArr)-1:
                    ws.write(row+13, col+1, elm, self.tableTotalItemFormat)
                else:
                    ws.write(row+13, col+1, elm, self.tableItemsFormat_V1)

        formatTable2 = self.workbook.add_format({'bold': 1, 'font_color':'#FFFFFF','font_size':11,'align':'center','valign':'vcenter','bg_color':'#C0504D','font_name':u'楷体','left':0,'right':0,'top':2,'bottom':0})
        ws.merge_range('B%s:B%s'%(row+17,row+18),'行标签', formatTable2)
        ws.merge_range('C%s:C%s'%(row+17,row+18),'求和项:最大支付', formatTable2)
        ws.merge_range('D%s:D%s'%(row+17,row+18),'求和项:名义金额', formatTable2)
        ws.merge_range('E%s:E%s'%(row+17,row+18),'求和项:内在价值', formatTable2)
        ws.merge_range('F%s:F%s'%(row+17,row+18),'求和项:Delta金额', formatTable2)
        
        _lst =  self.dbobj.selectValue('tradingbook',  ['distinct(counterparty)'], '', 'order by counterparty asc')
        counterparty = map(list, zip(*_lst))[0]
        # print 'counterparty',counterparty
        counterparty_dict = {}

        underlying_dict ={}
        sumcol = ['sum(maxpayment)', 'sum(notamt)', 'sum(intrinsicvalue)', 'sum(deltaamt)']
        row_record = row+18
        for item in counterparty:
            idcondition = 'counterparty = "'  + str( item) + '"'
            rowlist = [str( item)]
            self.writeSS(ws, row_record, rowlist, self.cellFormat_Onleft, 1)
            _lst =  self.dbobj.selectValue('tradingbook',  sumcol, idcondition)
            rowlist = _lst[0]
            self.writeSS(ws, row_record, rowlist, self.cellFormat_OnHcenter)
            row_record = row_record+1
            
            _lst =  self.dbobj.selectValue('tradingbook', ['distinct(code)'] , idcondition, 'order by code asc')
            code_list =  map(list, zip(*_lst))[0]

            for code_item in code_list:
                idcondition = 'counterparty = "'  + str( item) + '" and code = "'  + str( code_item) + '"'
                rowlist = [code_item]
                self.writeSS(ws, row_record, rowlist, self.cellFormat_Oncenter, 1)
                _lst =  self.dbobj.selectValue('tradingbook',  sumcol, idcondition)
                rowlist = _lst[0]
                self.writeSS(ws, row_record, rowlist, self.cellFormat_Oncenter)
                row_record = row_record+1                
                _lst =  self.dbobj.selectValue('tradingbook',  ['distinct(optiontype)'], idcondition, 'order by optiontype asc')
                optiontype = map(list, zip(*_lst))[0]

                for optiontype_item in optiontype:
                    idcondition = 'counterparty = "'  + str( item) + '" and code = "'  + str( code_item) + '" and optiontype = "'  + str( optiontype_item) + '"'
                    rowlist = [GlobalInfo.optionNameDict[optiontype_item]]
                    self.writeSS(ws, row_record, rowlist, self.cellFormat_Onright, 1)
                    _lst =  self.dbobj.selectValue('tradingbook',  sumcol, idcondition)
                    rowlist = _lst[0]
                    self.writeSS(ws, row_record, rowlist, self.tableItemsFormat_V1)
                    row_record = row_record+1   

        idcondition = ''
        rowlist = ["总计"]
        self.writeSS(ws, row_record, rowlist, self.cellFormat_Onleft, 1)
        _lst =  self.dbobj.selectValue('tradingbook',  sumcol, idcondition)
        rowlist = _lst[0]
        self.writeSS(ws, row_record, rowlist, self.cellFormat_OnHcenter) 

        ws.insert_image('A1', './images/logo_sw.png')

    def writeSS(self, ws, startrow, elm_list, celltype, step=2):

        for col, elm in enumerate(elm_list):
            # print col, elm
            if isinstance(elm, float):
                elm = round(elm, 2)

            ws.write(startrow, col + step, elm, celltype)

    def Overview(self):
        ws = self.workbook.add_worksheet(u'业务概况')

        ws.set_column('A2:L2',15)
        ws.write('A1', '业务概况', self.tableTitleFormat)
        ws.write('A2', '标的', self.tableItemsFormat_H)
        ws.write('B2', '合约数量', self.tableItemsFormat_H)
        ws.write('C2', '已到期', self.tableItemsFormat_H)
        ws.write('D2', '未到期', self.tableItemsFormat_H)
        ws.write('E2', '实际名义本金额', self.tableItemsFormat_H)
        ws.write('F2', '实际期权费', self.tableItemsFormat_H)
        ws.write('G2', '实际存量名义本金额', self.tableItemsFormat_H)
        ws.write('H2', '总名义本金额', self.tableItemsFormat_H)
        ws.write('I2', '总投资规模', self.tableItemsFormat_H)
        ws.write('J2', '存量投资规模', self.tableItemsFormat_H)
        # ws.write('A3', 'HS300', self.tableItemsFormat_V)

        listArr = self.std.GetOverviewData()

        for row, arr in enumerate(listArr):
            for col, elm in enumerate(arr):
                if isinstance(elm, float):
                    elm = round(elm, 2)
                if row ==len(listArr)-1:
                    ws.write(row+2, col, elm, self.cellFormat_OnHcenter)
                else:
                    ws.write(row+2, col, elm, self.tableItemsFormat_V)

    def ResultsTable(self):
        ws = self.workbook.add_worksheet(u'盈亏统计')

        ws.set_column('A2:L2',15)
        ws.write('A1', '盈亏表', self.tableTitleFormat)
        ws.write('A2', '标的', self.tableItemsFormat_H)
        ws.write('B2', '总盈亏', self.tableItemsFormat_H)
        ws.write('C2', '期货盈亏', self.tableItemsFormat_H)
        ws.write('D2', '期权负债盈亏', self.tableItemsFormat_H)
        ws.write('E2', '期权费', self.tableItemsFormat_H)
        ws.write('F2', '行权费', self.tableItemsFormat_H)
        ws.write('G2', '市值', self.tableItemsFormat_H)
        ws.write('H2', '当日总盈亏', self.tableItemsFormat_H)
        ws.write('I2', '当日期货盈亏', self.tableItemsFormat_H)
        ws.write('J2', '当日期权负债盈亏', self.tableItemsFormat_H)
        ws.write('K2', '当日期权费', self.tableItemsFormat_H)
        ws.write('L2', '当日行权费', self.tableItemsFormat_H)
        ws.write('M2', '当日市值', self.tableItemsFormat_H)
        ws.write('N2', '收盘价总盈亏', self.tableItemsFormat_H)
        ws.write('O2', '收盘价当日总盈亏', self.tableItemsFormat_H)
        ws.write('P2', '收盘价期货盈亏', self.tableItemsFormat_H)

        for row, underlying in enumerate(self.underlyingType):
            idcondition = 'recorddate in (select max(recorddate) from newprofitandloss) and '+ 'underlying = "'  + str( underlying) + '"' 
            _lst =  self.dbobj.selectValue('newprofitandloss',  ['underlyingpnl','underlyingtde','underlyingdnl' ,'underlyingpremium','underlyingpayout','underlyingprice',\
                                                                'dayunderlyingpnl','dayunderlyingtde','dayunderlyingdnl' ,'dayunderlyingpremium','dayunderlyingpayout','dayunderlyingprice', 'closepriceunderlyingpnl','closepricedayunderlyingpnl', 'closepriceunderlyingtde'], idcondition)  #['sum(posnum)', 'sum(notamt)', 'sum(actualnotamt)', 'sum(premium)', 'sum(actualpremium)', 'sum(gincome)', 'sum(precharge)']
            ws.write(row+2, 0, underlying, self.tableItemsFormat_V)
            if _lst==[]:
                pass
            else:
                for i in range (len(_lst[0])):
                    if isinstance(_lst[0][i], float):
                        ws.write(row+2, i+1, round(_lst[0][i], 2), self.tableItemsFormat_V)
                    else:
                        ws.write(row+2, i+1, _lst[0][i], self.tableItemsFormat_V)

        col =['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P']
        ws.write(row+3, 0, "合计", self.cellFormat_OnHcenter)
        for i in range (1,16):
            ws.write(row+3, i, '=SUM(%s%s:%s%s)'%(col[i],3,col[i],row+3), self.cellFormat_OnHcenter)

    def Position(self):
        ws = self.workbook.add_worksheet(u'持仓统计')

        ws.set_column('A2:L2',15)
        ws.write('A1', '持仓统计', self.tableTitleFormat)
        ws.write('A2', '标的', self.tableItemsFormat_H)
        ws.write('B2', '当日交易成本', self.tableItemsFormat_H)
        ws.write('C2', '对冲合约1', self.tableItemsFormat_H)
        ws.write('D2', '当日持仓变动1', self.tableItemsFormat_H)
        ws.write('E2', '结算价1', self.tableItemsFormat_H)
        ws.write('F2', '收盘价1', self.tableItemsFormat_H)
        ws.write('G2', '累计持仓1', self.tableItemsFormat_H)
        ws.write('H2', '对冲合约2', self.tableItemsFormat_H)
        ws.write('I2', '当日持仓变动2', self.tableItemsFormat_H)
        ws.write('J2', '结算价2', self.tableItemsFormat_H)
        ws.write('K2', '收盘价2', self.tableItemsFormat_H)
        ws.write('L2', '累计持仓2', self.tableItemsFormat_H)
        ws.write('M2', '当日盈亏变动', self.tableItemsFormat_H)
        ws.write('N2', '累计总盈亏', self.tableItemsFormat_H)
        ws.write('O2', '累计总持仓', self.tableItemsFormat_H)
        ws.write('P2', '当前持仓市值', self.tableItemsFormat_H)
        ws.write('Q2', '收盘持仓市值', self.tableItemsFormat_H)
        ws.write('R2', '收盘价当日总盈亏', self.tableItemsFormat_H)
        ws.write('S2', '收盘价累计总盈亏', self.tableItemsFormat_H)
        write_row=0
        for row, underlying in enumerate(self.underlyingType): 
            _lst = self.holdnum(underlying)
            if _lst ==[]:
                continue

            ws.write(write_row+2, 0, underlying, self.tableItemsFormat_V)
            ws.write(write_row+2, 1, self.daily_cost(underlying), self.tableItemsFormat_V)

            lstlen = len(_lst)
            sum_hedgeamt = 0
            sum_closeprice_hedgeamt = 0
            sum_holdnum  = 0
            for i in range(0, lstlen):
                # print _lst
                ws.write(write_row+2 , 2 + i*5, _lst[i][0], self.tableItemsFormat_V)
                ws.write(write_row+2 , 3 + i*5, _lst[i][3]-_lst[i][4], self.tableItemsFormat_V)
                ws.write(write_row+2, 4+ i*5, _lst[i][5], self.tableItemsFormat_V)
                ws.write(write_row+2, 5+ i*5, _lst[i][7], self.tableItemsFormat_V)
                ws.write(write_row+2, 6+ i*5, _lst[i][3], self.tableItemsFormat_V)
                hedgeamt = int(_lst[i][3])*_lst[i][5]*_lst[i][6]
                closeprice_hedgeamt = int(_lst[i][3])*_lst[i][7]*_lst[i][6]
                sum_hedgeamt = sum_hedgeamt +hedgeamt
                sum_closeprice_hedgeamt = sum_closeprice_hedgeamt + closeprice_hedgeamt
                sum_holdnum  = sum_holdnum + _lst[i][3]
            idcondition = 'recorddate in (select max(recorddate) from newprofitandloss where underlying = "'  + str( underlying) + '"' +') and underlying = "'  + str( underlying) + '"' 
            _lstinfo =  self.dbobj.selectValue('newprofitandloss', ['dayunderlyingtde', 'underlyingtde', 'closepricedayunderlyingtde','closepriceunderlyingtde'], idcondition)
            ws.write(write_row+2, 12, _lstinfo[0][0], self.tableItemsFormat_V)
            ws.write(write_row+2, 13, _lstinfo[0][1], self.tableItemsFormat_V)
            ws.write(write_row+2, 14, sum_holdnum, self.tableItemsFormat_V)
            ws.write(write_row+2, 15, sum_hedgeamt, self.tableItemsFormat_V)
            ws.write(write_row+2, 16, sum_closeprice_hedgeamt, self.tableItemsFormat_V)
            ws.write(write_row+2, 17, _lstinfo[0][2], self.tableItemsFormat_V)
            ws.write(write_row+2, 18, _lstinfo[0][3], self.tableItemsFormat_V)
            write_row +=1

    def RiskMonitor(self):
        ws = self.workbook.add_worksheet(u'风险监控')

        ws.set_column('A2:L2',15)
        ws.write('A1', '风险指标及风险限额使用情况', self.tableTitleFormat)
        ws.write('A2', '标的', self.tableItemsFormat_H)
        ws.write('B2', '标的代码', self.tableItemsFormat_H)
        ws.write('C2', '收盘价', self.tableItemsFormat_H)
        ws.write('D2', '理论Delta金额', self.tableItemsFormat_H)
        ws.write('E2', '理论Gamma金额', self.tableItemsFormat_H)
        ws.write('F2', '理论Vanna金额', self.tableItemsFormat_H)
        ws.write('G2', '实际对冲金额', self.tableItemsFormat_H)
        ws.write('H2', 'Delta风险敞口', self.tableItemsFormat_H)
        ws.write('I2', '对冲比例', self.tableItemsFormat_H)
        ws.write('J2', 'Delta风险限额', self.tableItemsFormat_H)
        ws.write('K2', '使用额度', self.tableItemsFormat_H)
        ws.write('L2', '总Delta', self.tableItemsFormat_H)
        ws.write('M2', '总Gamma', self.tableItemsFormat_H)
        ws.write('N2', '总Theta', self.tableItemsFormat_H)
        ws.write('O2', '总Vega', self.tableItemsFormat_H)
        ws.write('P2', '总Rho', self.tableItemsFormat_H)
        ws.write('Q2', '总Vanna', self.tableItemsFormat_H)

        for row, underlying in enumerate(self.underlyingType):
            ws.write(row+2, 0, underlying, self.tableItemsFormat_V)
            idcondition = 'recorddate in (select max(recorddate) from greeksunderlying) and underlying = "'  + str( underlying) + '"'
            _lst =  self.dbobj.selectValue('greeksunderlying',  ['closeprice'], idcondition)  #获取最新期货损益  
            if _lst==[]:
                udlprice =0
            else:
                udlprice = _lst[0][0]
            ws.write(row+2, 2, udlprice, self.tableItemsFormat_V)
            idcondition = 'punderlying = "'  + str( underlying) + '" and contractstatus = 1 '
            _lst = self.dbobj.selectValue('tradingbook',  ['sum(delta)', 'sum(gamma)', 'sum(theta)', 'sum(vega)', 'sum(rho)', 'sum(vanna)'], idcondition)

            ws.write_formula(row+2, 3, '=C%s*L%s'%(row+3,row+3), self.tableItemsFormat_V)
            ws.write_formula(row+2, 4, '=(C%s)^2*M%s'%(row+3,row+3), self.tableItemsFormat_V)
            ws.write_formula(row+2, 5, '=C%s*Q%s'%(row+3,row+3), self.tableItemsFormat_V)
           
            _hn = self.holdnum(underlying)
            # _lst = [[1,1,1,1,1,1],[2,2,2,2,2,2]]
            # print _lst
            lstlen = len(_hn)
            sum_hedgeamt = 0

            for i in range(0, lstlen):
                hedgeamt = int(_hn[i][3])*_hn[i][7]*_hn[i][6]
                sum_hedgeamt =sum_hedgeamt +hedgeamt
                
            # ws.write(13 + i, 3, hedgeamt, self.tableItemsFormat_V)
            # print _lst,'---------------------------',_hn, '---',sum_hedgeamt
            ws.write(row+2, 6, sum_hedgeamt, self.tableItemsFormat_V)

            ws.write_formula(row+2, 7, '=G%s-D%s'%(row+3,row+3), self.tableItemsFormat_V)
            ws.write_formula(row+2, 8, '=IFERROR(G%s/D%s,0)'%(row+3,row+3), self.tableItemsFormat_V)

            ws.write_formula(row+2, 9, '=MAX(5000000,ABS(0.1*D%s),ABS(E%s*0.02)+ABS(F%s*0.02))'%(row+3,row+3,row+3),self.tableItemsFormat_V)
            ws.write_formula(row+2, 10, '=ABS(H%s/J%s)'%(row+3,row+3), self.tableItemsFormat_V)
            if _lst[0][0] ==None:
                _lst=[[0]*6]
            ws.write(row+2, 11, _lst[0][0], self.tableItemsFormat_V)
            ws.write(row+2, 12, _lst[0][1], self.tableItemsFormat_V)
            ws.write(row+2, 13, _lst[0][2], self.tableItemsFormat_V)
            ws.write(row+2, 14, _lst[0][3], self.tableItemsFormat_V)
            ws.write(row+2, 15, _lst[0][4], self.tableItemsFormat_V)
            ws.write(row+2, 16, _lst[0][5], self.tableItemsFormat_V)


    def TransactionFlow(self):
        ws = self.workbook.add_worksheet(u'交易流水')

        ws.set_column('A2:L2',15)
        ws.write('A1', '当日成交记录', self.tableTitleFormat)
        ws.write('A2', '策略ID', self.tableItemsFormat_H)
        ws.write('B2', '交易帐号', self.tableItemsFormat_H)
        ws.write('C2', '下单备注', self.tableItemsFormat_H)
        ws.write('D2', '成交ID', self.tableItemsFormat_H)
        ws.write('E2', '代码', self.tableItemsFormat_H)
        ws.write('F2', '成交数量', self.tableItemsFormat_H)
        ws.write('G2', '成交价格', self.tableItemsFormat_H)
        ws.write('H2', '成交时间', self.tableItemsFormat_H)
        ws.write('I2', '委托ID', self.tableItemsFormat_H)
        ws.write('J2', '买卖', self.tableItemsFormat_H)
        ws.write('K2', '开平', self.tableItemsFormat_H)
        ws.write('L2', '总成交数量', self.tableItemsFormat_H)
        ws.write('M2', '总成交均价', self.tableItemsFormat_H)
        ws.write('N2', '委托时间', self.tableItemsFormat_H)

        idcondition = 'entrustdate in (select max(entrustdate) from transaction) '
        _lstinfo =  self.dbobj.selectValue('transaction',  ['strategyid', 'tradeaccount','info', 'dealid','code', 'dealnum', 'dealprice', 'dealtime', 'entrustid','askbid', 'openclose', 'totalnum', 'avgdealprice', 'entrustdate'], idcondition) 

        for row,item in enumerate(_lstinfo):
            for col,elm in enumerate(item):

                if col in [13]:
                    ws.write(row+2, col, elm, self.tableItemsFormat_date_format)
                else:
                    ws.write(row+2, col, elm, self.tableItemsFormat_V1)

    def Contract(self):
        ws = self.workbook.add_worksheet(u'场外期权合约信息')
        ws.write(0, 0, "合约明细",self.tableTitleFormat)

        titlecol = ['序号','协议编号','交易对手','合约类型', "合约方向", "期权类型","标的",'代码',"名义金额","交易期限(天)","交易起始日","交易结算日","交易到期日","起始价格","高行权价","低行权价","高触碰价","低触碰价","浮动收益","浮动收益(2)","浮动收益(3)","敲出收益率","合约期权费"
        ,"保底收益","前段收益","实际名义金额","实际期权费","行权费","最大支付","内在价值","市值",'Delta','Gamma','Theta','Vega','Rho', 'Vanna','Delta金额','Gamma金额','Vanna金额','合约状态','付费时点']
        for item in zip(range(0,41), titlecol):
            ws.write(1,item[0],item[1],self.tableItemsFormat_H )
        
        ws.autofilter('A2:AK2')
        ws.set_column('A2:X2',10)
        ws.set_column('B2:B2',15)
        ws.set_column('E2:E2',15)

        contactcol = ['contractid', 'counterparty', 'contracttype','bidorask', 'optiontype','underlying', 'code', 'notamt', 'tradematurity', 'begmat','dealmat', 'endmat',
                        's0', 'hstrike','lstrike', 'htouch', 'ltouch', 'ggainratio', 'ggainratio2', 'ggainratio3', 'tgainratio','premium', 'gincome','precharge','actualnotamt', 
                        'actualpremium','payout','maxpayment', 'intrinsicvalue','price', 'delta', 'gamma', 'theta', 'vega', 'rho', 'vanna','deltaamt','gammaamt', 'vannaamt','contractstatus']
        # idcondition  = 'contractstatus > 0 '
        plusidcondition = 'order by begmat asc'
        _lstinfo =  self.dbobj.selectValue('tradingbook', contactcol, '',plusidcondition)

        for row,item in enumerate(_lstinfo):
            ws.write(row+2, 0, row+1, self.tableItemsFormat_V)
            for col,elm in enumerate(item):
                if col in [16,17] and elm ==1:
                    elm = 0
                if col in [4]:
                    elm = GlobalInfo.optionNameDict[elm]

                if col in [9, 10, 11]:
                    ws.write(row+2, col+1, elm, self.tableItemsFormat_date_format)
                else:
                    ws.write(row+2, col+1, elm, self.tableItemsFormat_V1)

    def EXGContract(self):
        ws = self.workbook.add_worksheet(u'场内信息')

        ws.set_column('A2:L2',15)
        ws.write('A1', '场内信息', self.tableTitleFormat)
        ws.write('A2', '名称', self.tableItemsFormat_H)
        ws.write('B2', '方向', self.tableItemsFormat_H)
        ws.write('C2', '备兑', self.tableItemsFormat_H)
        ws.write('D2', '实时持仓', self.tableItemsFormat_H)
        ws.write('E2', '成本价', self.tableItemsFormat_H)
        ws.write('F2', '最新价', self.tableItemsFormat_H)
        ws.write('G2', '浮动盈亏', self.tableItemsFormat_H)
        ws.write('H2', '资金占用', self.tableItemsFormat_H)
        ws.write('I2', '代码', self.tableItemsFormat_H)
        ws.write('J2', '持仓市值', self.tableItemsFormat_H)
        ws.write('K2', '场外方向', self.tableItemsFormat_H)
        ws.write('L2', '交易类型', self.tableItemsFormat_H)
        ws.write('M2', '总Price', self.tableItemsFormat_H)
        ws.write('N2', '总Delta', self.tableItemsFormat_H)
        ws.write('O2', '总Gamma', self.tableItemsFormat_H)
        ws.write('P2', '总Theta', self.tableItemsFormat_H)
        ws.write('Q2', '总Vega', self.tableItemsFormat_H)
        ws.write('R2', '总Rho', self.tableItemsFormat_H)
        ws.write('S2', '总Delta金额', self.tableItemsFormat_H)
        ws.write('T2', '总Gamma金额', self.tableItemsFormat_H)

        contactcol = ['contractdetail', 'chbidorask', 'covered', 'realtimepos', 'costprice', 'latestprice', 'floatingpnl', 'recua', 'contractidcode', 
                        'holdvalue', 'bidorask', 'optiontype','price', 'delta', 'gamma', 'theta', 'vega', 'rho', 'deltaamt','gammaamt']
        # idcondition  = 'contractstatus > 0 '
        idcondition = 'realtimepos >0 '
        plusidcondition = 'order by contractidcode asc'
        _lstinfo =  self.dbobj.selectValue('exchangetb', contactcol, idcondition,plusidcondition)

        for row,item in enumerate(_lstinfo):
            for col,elm in enumerate(item):
                ws.write(row+2, col, elm, self.tableItemsFormat_V1)

    def save(self):
        self.Summary()
        self.Overview()
        self.ResultsTable()
        self.Position()
        self.RiskMonitor()
        self.TransactionFlow()
        self.Contract()
        self.EXGContract()
        self.workbook.close()


    def holdnum(self, underlying):
        # print 'cal hold amount'
        _numArr = []
        idcondition = 'underlying = "'  + str( underlying) + '"'
        _lstinfo =  self.dbobj.selectValue('transaction',  ['distinct(code)'], idcondition)  

        for elm in _lstinfo:
            _numList = []
            idcondition = 'code = "'  + str( elm[0]) + '"'
            _numList.append(elm[0])

            _num =  self.dbobj.selectValue('transaction',  ['sum(dealnum)'], 'code = "'  + str( elm[0]) + '" and askbid = 1')
            if _num[0][0]==None:
                _numList.append(0)
            else:
                _numList.append(_num[0][0])

            _num =  self.dbobj.selectValue('transaction',  ['-sum(dealnum)'], 'code = "'  + str( elm[0]) + '" and askbid = 2')
            if _num[0][0]==None:
                _numList.append(0)
            else:
                _numList.append(_num[0][0])

            _num =  self.dbobj.selectValue('transaction',  ['sum(posnum)'], idcondition)  
            
            if _num[0][0]==None:
                _numList.append(0)
            else:
                _numList.append(_num[0][0])

            idcondition = 'entrustdate < (select max(entrustdate) from transaction) and code = "'  + str(  elm[0]) + '"'
            # idcondition = 'entrustdate < "' + str(GlobalInfo.curDate)+ '" and code = "'  + str(  elm[0]) + '"'
            pre_num =  self.dbobj.selectValue('transaction',  ['sum(posnum)'], idcondition) 
            if pre_num[0][0]==None:
                _numList.append(0)
            else:
                _numList.append(pre_num[0][0])

            # _numList.append(pre_num[0][0]) 

            # print _num[0][0],elm[0]
            if _num[0][0] == 0:
                continue  #pass
            else:
                # print _num[0][0],elm[0]
                idcondition = 'recorddate in (select max(recorddate) from settle) and code = "'  + str(  elm[0]) + '"'
                _price =  self.dbobj.selectValue('settle',  ['settleprice', 'coefficient', 'closeprice'], idcondition)  #获取最新期货损益 
                _numList.append( _price[0][0])
                _numList.append( _price[0][1])
                _numList.append( _price[0][2])

                _numArr.append(_numList)
        
        return _numArr

    def daily_cost(self, underlying):
        dailycost = 0
        idcondition = 'underlying = "'  + str( underlying) + '" and entrustdate = (select max(entrustdate) from transaction)'
        _lstinfo =  self.dbobj.selectValue('transaction',  ['distinct(code)'], idcondition)

        for elm in _lstinfo:
            idcondition = 'code = "'  + str( elm[0]) + '" and entrustdate = (select max(entrustdate) from transaction)'
            _num =  self.dbobj.selectValue('transaction',  ['sum(dealamt)'], idcondition)
            if _num[0][0]==None:
                dailycost += 0
            else:
                dailycost += _num[0][0]

        return -dailycost


    def GetColSum(self,arr, col):
        _sum = 0
        for elm in arr:
            _sum = _sum + elm[col]

        return _sum

if __name__ == '__main__':
   test =  CreateDailyReport('./DailyReport.xlsx')
   test.save()