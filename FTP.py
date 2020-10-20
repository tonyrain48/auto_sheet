#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ftplib import FTP

from local_FTP_info import LocalFtpInfo


class FTPSync(object):

    def __init__(self,
                 ftp_server=LocalFtpInfo.ftp_server,
                 username=LocalFtpInfo.username,
                 password=LocalFtpInfo.password):
        self.ftp=FTP()  
        self.ftp.set_debuglevel(2) #打开调试级别2，显示详细信息  
        self.ftp.connect(ftp_server,21) #连接
        self.ftp.login(username,password) #登录，如果匿名登录则用空串代替即可   
    
    def downloadfile(self, remotepath, localpath, bufsize = 1024):

        # print self.ftp.getwelcome() #显示ftp服务器欢迎信息  
        fp = open(localpath,'wb') #以写模式在本地打开文件  
        self.ftp.retrbinary('RETR ' + remotepath,fp.write,bufsize) #接收服务器上文件并写入本地文件  
        self.ftp.set_debuglevel(0) #关闭调试  
        fp.close()  

    def uploadfile(self, localpath, remotepath, bufsize = 1024): 
        file_path = remotepath.split('/')[0]
        # print  file_path,self.ftp.nlst(file_path)
        if self.ftp.nlst(file_path) ==[]:
            try:
                self.ftp.rmd(file_path)
            except:
                pass
            finally:
                self.ftp.mkd(file_path)
        
        fp = open(localpath,'rb') 
        # print 'STOR '+ remotepath
        self.ftp.storbinary('STOR '+ remotepath,fp,bufsize) #上传文件  
        self.ftp.set_debuglevel(0)  
        fp.close() #关闭文件  

    def __del__(self):
        self.ftp.quit()  


if __name__ == '__main__':

    remotepath = "load/t1.txt"
    ftpobj = FTPSync()
    localpath = 'D:/222.txt'
    
    ftpobj.uploadfile(localpath, remotepath)
    # ftpobj.downloadfile(remotepath,localpath)
