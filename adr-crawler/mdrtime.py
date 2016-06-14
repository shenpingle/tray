# -*- coding: utf-8 -*-
###########################################################################################
#  author:touchluu2010@gmail.com
#  说明:封装和计算上年度、上半年度、下半年度、本月、本周、上周、上月、当天的时间函数
#  Revision: 1.0
###########################################################################################
import time
import datetime
'''抓取上一年度的'''
def last_year_cal():
    year = datetime.datetime.today().year - 1
    last_year_start = datetime.date(year, 1, 1)
    last_year_end = datetime.date(year, 12, 31)
    start_time = last_year_start.strftime('%Y-%m-%d')
    end_time = last_year_end.strftime('%Y-%m-%d')
    filters = {
        "beginTime":    start_time,
        "endTime":      end_time
    }
    return filters
'''抓取上半年度的'''
def halfyear_before_cal():
    year = datetime.datetime.today().year
    last_year_start = datetime.date(year, 1, 1)
    last_year_end = datetime.date(year, 6, 30)
    start_time = last_year_start.strftime('%Y-%m-%d')
    end_time = last_year_end.strftime('%Y-%m-%d')
    filters = {
        "beginTime":    start_time,
        "endTime":      end_time
    }
    return filters

'''抓取下半年度的'''
def halfyear_after_cal():
    year = datetime.datetime.today().year
    start_time = datetime.date(year, 7, 1)
    end_time = datetime.date(year, 12, 31)
    start_time = start_time.strftime('%Y-%m-%d')
    end_time = end_time.strftime('%Y-%m-%d')
    filters = {
        "beginTime":    start_time,
        "endTime":      end_time
    }
    return filters

'''抓取本周的'''
def current_week_cal():
    end_time = datetime.datetime.today()
    delta = datetime.timedelta(days=end_time.weekday())
    start_time = end_time - delta
    start_time = start_time.strftime('%Y-%m-%d')
    end_time = end_time.strftime('%Y-%m-%d')
    filters = {
        "beginTime":    start_time,
        "endTime":      end_time
    }
    return filters
'''抓取上周的'''
def last_week_cal():
    end_time = datetime.datetime.today()
    delta_day = end_time.weekday() + 7
    delta = datetime.timedelta(days=delta_day)
    start_time = end_time - delta
    end_time = start_time + datetime.timedelta(days=6)
    start_time = start_time.strftime('%Y-%m-%d')
    end_time = end_time.strftime('%Y-%m-%d')
    filters = {
        "beginTime":    start_time,
        "endTime":      end_time
    }
    return filters
'''抓取上月的'''
def last_month_cal():
    cur_time = datetime.datetime.today()
    year = cur_time.year
    month = cur_time.month - 1
    if month == 0 :
        month = 12
        year -= 1
    start_time = datetime.datetime(year, month, 1)
    end_time = datetime.datetime(cur_time.year, cur_time.month, 1) - datetime.timedelta(days=1)
    start_time = start_time.strftime('%Y-%m-%d')
    end_time = end_time.strftime('%Y-%m-%d')
    filters = {
        "beginTime":    start_time,
        "endTime":      end_time
    }
    return filters
'''抓取今天的的'''
def toady_cal():
    start_time = datetime.datetime.today()
    end_time = start_time + datetime.timedelta(days=1)
    start_time = start_time.strftime('%Y-%m-%d')
    end_time = end_time.strftime('%Y-%m-%d')
    filters = {
        "beginTime":    start_time,
        "endTime":      start_time
    }
    return filters

def init_cal():
    start_time = '2001-01-01'
    end_time = datetime.datetime.today()
    end_time = end_time.strftime('%Y-%m-%d')
    filters = {
        "beginTime":    start_time,
        "endTime":      end_time
    }
    return filters

def anytime():
    start_time = raw_input("input start_time,eg:'2014-01-01': ")
    end_time = raw_input("input start_end,eg:'2014-01-01': ")
    filters = {
        "beginTime":    start_time,
        "endTime":      end_time
    }
    return filters

def anytime2(start_time, end_time):
    filters = {
        "beginTime":    start_time,
        "endTime":      end_time
    }
    return filters

def validate_date(d):
    try:
        #datetime.datetime.strptime
        datetime.datetime.strptime(d, '%Y-%m-%d')
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    t = current_week_cal()
    print t['beginTime']
    print t['endTime']


