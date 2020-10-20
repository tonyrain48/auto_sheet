#-*- coding: utf-8 -*-

'''
logMonitor, Created on Apl, 2015
#version: 1.0

'''
import logging
#import time  
import datetime

class LogMonitor:
    def __init__(self):
        self.logger=logging.getLogger()
        self.handler=logging.FileHandler("./_log/LogHistory_"+str(datetime.date.today())+".txt")
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.NOTSET)

    def debug(self,message):
        self.logger.debug("[debug "+ self.currentTime()+ "]:    "+message)

    def info(self,message):
        self.logger.info("[info "+ self.currentTime()+ "]:    "+message)

    def warning(self,message):
        self.logger.warning("[warning "+ self.currentTime()+ "]:    "+message)

    def error(self,message):
        self.logger.error("[error "+ self.currentTime()+ "]:    "+message)

    def critical(self,message):
        self.logger.critical("[critical "+ self.currentTime()+ "]:    "+message)

    def currentTime(self):
    	return str(datetime.datetime.now())  #time.strftime('%H:%M:%S')



if __name__=='__main__':
    print '---start---'
    
    lmobj = LogMonitor()
    #lmobj.debug("debug")
    #lmobj.info("info")
    lmobj.warning("warning")
    # lmobj.error("error")
    # lmobj.critical("critical")
    print '---done---'
