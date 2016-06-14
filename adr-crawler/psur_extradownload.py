#-*- coding:utf-8 -*-
from utils import *
from login2 import login
import psur
def extradown():
    logincounter = 10
    while logincounter:
        print logincounter
        if login():
            print "ok"
            break
        else:
            print "clear"
            cookieManager.clear()
            logincounter = logincounter -1

    psur.myautodown2()
