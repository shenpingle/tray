#-*- coding:utf-8 -*-
import yaml
def readlogininfo():
    #
    #return ()
    f = open('logininfo.yml')  
    dataMap = yaml.load(f) 
    name = dataMap['name'] 
    ps = dataMap['password']
    #print name,ps
    f.close()
    return (name,ps)
if __name__ == "__main__":
    somedata = readlogininfo()
    name = somedata[0]
    ps = somedata[1]
    print name,ps