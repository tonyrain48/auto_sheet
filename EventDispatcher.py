# -*- coding: utf-8 -*-
# Copyright (C) 2016 SWFE Limited.
#
# Created: Fri Otc 05  2016
#      by: chenqiuxing, 18317010980
#          1078494347@qq.com, chenqiuxing@sjtu.edu.cn
#          
#
# WARNING! All changes made in this file will be lost!

from Queue import Queue, Empty
from threading import Thread
from time import sleep

import eventType as ET

class Event(object):
    """
    Generic base event object to use with EventDispatcher.
    """

    def __init__(self, event_type=None, data=None):
        """
        The constructor accepts an event type as string and a custom data
        define event type and data
        """
        self._type = event_type
        self._data = data

    @property
    def type(self):
        """
        Returns the event type
        return event type
        """
        return self._type

    @property
    def data(self):
        """
        Returns the data associated to the event
        return event data
        """
        return self._data

# EventDispatcher
class EventDispatcher(object):
    """
    EventDispatcher

    Generic event dispatcher which listen and dispatch events
    event class  listening and dispatching event

    class list
    
    variables desc:
        __queue：private, evnet queue
        __active：private, turn on and off dispatcher 
        __thread：private, event process thread
        __timer：private, time
        __handlers：private, function dict of event process
        
    method desc:
        __run: private, run event process thread
        __process: private, process event, call listeners
        __runTimer：private, triggered in T, check and put timer event
        start: turn on dispatcher
        stop：turn off dispatcher
        register：add listening event
        unregister：add  listening function
        put：put new event into process evnet queue
    
    """
    # define time dispatcher event
    # EVENT_TIMER = 'eTimer'

    #----------------------------------------------------------------------
    def __init__(self, T=1, Tevent_type=None):
        """init"""
        # evnet queue
        self.__queue = Queue()
        
        # on/off this EventDispatcher
        self.__active = False
        
        # event ispatching thread
        self.__thread = Thread(target = self.__run)
        
        # timer, used to trigger the timer event
        self.__timer = Thread(target = self.__runTimer)
        self.__timerActive = False                      # 计时器工作状态
        self.__timerSleep = T                           # 计时器触发间隔（默认1秒）     
        self.__Tevent_type = Tevent_type 
        
        # 这里的__handlers是一个字典，用来保存对应的事件调用关系
        # 其中每个键对应的值是一个列表，列表中保存了对该事件进行监听的函数功能
        self.__handlers = {}
        
    #----------------------------------------------------------------------
    def __run(self):
        """引擎运行"""
        while self.__active == True:
            try:
                event = self.__queue.get(block = True, timeout = 1)  # 获取事件的阻塞时间设为1秒
                self.__process(event)
            except Empty:
                pass
            
    #----------------------------------------------------------------------
    def __process(self, event):
        """处理事件"""
        # 检查是否存在对该事件进行监听的处理函数
        if event.type in self.__handlers:
            # 若存在，则按顺序将事件传递给处理函数执行
            [handler(event) for handler in self.__handlers[event.type]]
            
            # 以上语句为Python列表解析方式的写法，对应的常规循环写法为：
            #for handler in self.__handlers[event.event_type]:
                #handler(event)    
               
    #----------------------------------------------------------------------
    def __runTimer(self):
        """运行在计时器线程中的循环函数"""
        while self.__timerActive:
            # 创建计时器事件
            event = Event(event_type=self.__Tevent_type)
        
            # 向队列中存入计时器事件
            self.put(event)    
            
            # sleep
            sleep(self.__timerSleep)

    #----------------------------------------------------------------------
    def start(self):
        """引擎启动"""
        # 将引擎设为启动
        self.__active = True
        
        # 启动事件处理线程
        self.__thread.start()
        
        # 启动计时器，计时器事件间隔默认设定为1秒
        self.__timerActive = True
        self.__timer.start()
    
    #----------------------------------------------------------------------
    def stop(self):
        """停止引擎"""
        # 将引擎设为停止
        self.__active = False
        
        # 停止计时器
        self.__timerActive = False
        # self.__timer.join()
        
        # # 等待事件处理线程退出
        # self.__thread.join()

        # force eixt
        import os
        os._exit(0)
        # self.__timer=None
        # self.__thread=None
            
    #----------------------------------------------------------------------
    def register(self, event_type, handler):
        """注册事件处理函数监听"""
        # get the process function list of the event_type, if null, create.
        handlerList = self.__handlers.get(event_type, [])

        self.__handlers[event_type] = handlerList
        
        # 若要注册的处理器不在该事件的处理器列表中，则注册该事件
        if handler not in handlerList:
            handlerList.append(handler)
            
    #----------------------------------------------------------------------
    def unregister(self, event_type, handler):
        """注销事件处理函数监听"""
        # 尝试获取该事件类型对应的处理函数列表，若无则忽略该次注销请求

        handlerList = self.__handlers.get(event_type, [])
            
        # remove the listener function if exit in handlerList
        if handler in handlerList:
            handlerList.remove(handler)

        # if function handlerList is null, remove the event type
        if not handlerList:
            del self.__handlers[event_type]

    #----------------------------------------------------------------------
    def put(self, event):
        """put event into event queue"""
        self.__queue.put(event)

# define event type like this
# class MyEvent:
#     """
#     When subclassing Event class the only thing you must do is to define
#     a list of class level constants which defines the event types and the
#     string associated to them
#     """

#     EVENT_TIMER     = 'eTimer'
    # RESPOND = "respondMyEvent"

def test():
    """测试函数"""
    import sys
    from datetime import datetime
    
    def simpletest(event):
        print '处理每秒触发的计时器事件：%s' % str(datetime.now())
 
    ee = EventDispatcher(T=30*60, Tevent_type= ET.EVENT_THIRTY_MIN_TIMER)
    ee.register(ET.EVENT_THIRTY_MIN_TIMER, simpletest)
    ee.start()

    
# 直接运行脚本可以进行测试
if __name__ == '__main__':
    test()