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
from Model.globalInfo import GlobalInfo

class CreateOutput:
    def __init__(self, _file_path = './SettleReport.xlsx'):
        # print _file_path
        self.workbook = xlsxwriter.Workbook(_file_path)
        self.underlyingType = GlobalInfo.underlyingType

        self.tableItemsFormat_H = self.workbook.add_format({'bold': 0, 'font_size':10,'align':'center','valign':'vcenter','font_name':u'宋体','left':1,'right':1,'top':1,'bottom':1})
        self.tableItemsFormat_H2 = self.workbook.add_format({'bold': 0, 'font_size':10,'bg_color':'#FFFF00','align':'center','valign':'vcenter','font_name':'Cambria','left':1,'right':1,'top':1,'bottom':1})
        self.tableItemsFormat_H3 = self.workbook.add_format({'bold': 0, 'font_size':10,'align':'center','valign':'vcenter','font_name':'Cambria','left':1,'right':1,'top':1,'bottom':1})
        self.tableItemsFormat_H4 = self.workbook.add_format({'bold': 0, 'font_size':10,'align':'center','valign':'vcenter','font_name':u'宋体','left':1,'right':1,'top':1,'bottom':1,'num_format':'yyyy/mm/dd'})
        self.tableItemsFormat_H5 = self.workbook.add_format({'bold': 0, 'font_size':10,'align':'left','valign':'vcenter','font_name':u'宋体','left':1,'right':1,'top':1,'bottom':1})
        self.tableHeadFormat_H = self.workbook.add_format({'bold': 0, 'font_size':11,'bg_color':'#FFFF00', 'align':'center','valign':'vcenter','font_name':u'宋体','left':0,'right':0,'top':0,'bottom':1})
        self.tableHeadFormat_H2 = self.workbook.add_format({'bold': 0, 'font_size':11,'bg_color':'#FFFF00', 'align':'center','valign':'vcenter','font_name':u'宋体','left':0,'right':0,'top':0,'bottom':1,'num_format':'0.00%'})

    def saveSettle(self, lst):
        ws = self.workbook.add_worksheet(u'结算')

        listArr = lst
        start_row = 0

        for row, arr in enumerate(listArr):
            start_row = 10*row
            ws.set_column('A2:A2',15)
            ws.set_column('B2:E2',12)

            ws.write('A%s'%(1+start_row), '', self.tableHeadFormat_H)
            ws.write('B%s'%(1+start_row), '', self.tableHeadFormat_H)
            ws.write('C%s'%(1+start_row), '收益率', self.tableHeadFormat_H)
            ws.write('A%s'%(2+start_row), '甲方', self.tableItemsFormat_H)
            ws.merge_range('B%s:D%s'%(2+start_row,2+start_row), u'申万宏源',self.tableItemsFormat_H)
            ws.merge_range('B%s:D%s'%(3+start_row,3+start_row), arr[1],self.tableItemsFormat_H)
            ws.write('A%s'%(3+start_row), '乙方', self.tableItemsFormat_H)

            ws.write('A%s'%(4+start_row), '交易编号', self.tableItemsFormat_H)
            ws.write('B%s'%(4+start_row), '起始日', self.tableItemsFormat_H)
            ws.write('C%s'%(4+start_row), '结算日', self.tableItemsFormat_H)
            ws.write('D%s'%(4+start_row), '到期日', self.tableItemsFormat_H)
            ws.write('A%s'%(5+start_row), arr[0], self.tableItemsFormat_H)
            ws.write('B%s'%(5+start_row), arr[6], self.tableItemsFormat_H4)
            ws.write('C%s'%(5+start_row), arr[7], self.tableItemsFormat_H4)
            ws.write('D%s'%(5+start_row), arr[8], self.tableItemsFormat_H4)

            sa = '支付浮动收益'
            sb = '支付固定收益'
            temp = "支付轧差金额"

            a= abs(round(arr[11],2))
            if arr[12] =="beg":
                b= 0
                t= "已期初支付期权费"
            else:
                b= abs(round(arr[10],2))
                t= "期末支付期权费"
            dif = a - b
            yld = arr[9]
            
            if str(arr[3]) == 'Bid':
                a, b = b, a
                sa, sb = sb, sa
                if dif <0:
                    info = u"甲方"
                else:
                    info = u"乙方"
            else:
                if dif <0:
                    info = u"乙方"
                else:
                    info = u"甲方"

            if arr[2] =="Swap":
                info += temp
            else:
                if info == u"甲方":
                    t = u"*乙方" +t
                else:
                    t = u"*甲方" +t
                info += "支付"
                ws.merge_range('A%s:D%s'%(8+start_row,8+start_row), t,self.tableItemsFormat_H5)
                

            ws.write('D%s'%(1+start_row), yld, self.tableHeadFormat_H2)

            ws.write('A%s'%(6+start_row), '甲方' + sa , self.tableItemsFormat_H)
            ws.write('A%s'%(7+start_row), '乙方' + sb , self.tableItemsFormat_H)

            ws.write('B%s'%(6+start_row), a, self.tableItemsFormat_H3)
            ws.write('B%s'%(7+start_row), b, self.tableItemsFormat_H3)

            ws.merge_range('C%s:C%s'%(6+start_row,7+start_row), info,self.tableItemsFormat_H)
            ws.merge_range('D%s:D%s'%(6+start_row,7+start_row), abs(dif),self.tableItemsFormat_H2)

        self.close()

    def close(self):
        self.workbook.close()




if __name__ == '__main__':
   test =  CreateDailyReport('./DailyReport.xlsx')
   test.save()