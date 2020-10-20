#!/usr/bin/python  
# -*- coding:utf-8 -*-  
#desc: use to LoadConfig
#---------------------  
#2016-03-14 created  
  
import ConfigParser  

class LoadConfig:  
    def __init__(self, config_file_path ='./userSettings.ini' ):
        
        self.path = config_file_path  
        self.cf = ConfigParser.ConfigParser()  
        self.cf.read(self.path)  

    def get(self, field, key):  
        result = ""  
        try:  
            result = self.cf.get(field, key)  
        except:  
            result = ""  
        return result  
    def set(self, field, key, value):  
        try:  
            self.cf.set(field, key, value)  
            self.cf.write(open(self.path,'w'))  
        except:  
            return False  
        return True  

if __name__ == "__main__":  
    # if len(sys.argv) < 4:  
    #    sys.exit(1)  
    config_file_path ='./settings.ini'
    lc= LoadConfig(config_file_path)
     
    field = 'baseconf'
    key = 'host'
     
    print lc.get(field,key)