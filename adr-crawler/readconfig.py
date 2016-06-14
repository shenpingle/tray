#-*- coding:utf-8 -*-
import yaml
def readconfiginfo():
    #
    f = open('launcherconfig.yml')
    dataMap = yaml.load(f) 
    mdrconfig = dataMap['mdr']
    adrconfig = dataMap['adr']
    psurconfig = dataMap['psur']
    f.close()
    return (mdrconfig,adrconfig,psurconfig)
if __name__ == "__main__":
    somedata = readconfiginfo()
    p1 = somedata[0]
    p2 = somedata[1]
    p3 = somedata[2]
    print p1,p2,p3