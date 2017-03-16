#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'bird'
# 时间：2017年3月11日17:26:00

from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import time,datetime
# html = urlopen('https://q.cnblogs.com/list/unsolved?page=1')
# bsobj = BeautifulSoup(html,'html.parser')
# taglist = bsobj.findAll('div',{'class':'news_footer'})
# print(taglist)

# 创建CSV文件，filename为XX.csv格式，column为列表（题头）
# column = ['标题', '时间', '地点', '评论']
# filename = 'XXX' + '.csv'


def csvcreate(filename,column):
    # 创建CSV文件
    with open(filename, "a+", newline="") as datacsv:
        # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
        csvwriter.writerow(column)


def csvwrite(filename,row):
    with open(filename, 'a+', newline='', encoding='gb18030') as datacsv:
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        csvwriter.writerow(row)


def get_week_day(date):
    week_day_dict = {
      0 : '星期一',
      1 : '星期二',
      2 : '星期三',
      3 : '星期四',
      4 : '星期五',
      5 : '星期六',
      6 : '星期天',
    }
    day = datetime.datetime(date[0],date[1],date[2]).strftime('%w')
    #print(day)
    return week_day_dict[int(day)]

if __name__=='__main__':
    startnum = 80430
    endnum = 91513
    num = startnum
    url = 'https://q.cnblogs.com/q/{}/'
    filename = 'cnblog_博问.csv'
    column = ['问题', '时间', '星期', '标签']
    csvcreate(filename, column)
    while num < endnum:
        try:
            html = urlopen(url.format(num))
            bsobj = BeautifulSoup(html,'html.parser')

            # 获取问题标题
            titles = bsobj.title.string[:-7]
            # print(titles)

            # 获取问题提交的时间
            timelist = str(bsobj.findAll('div',{'class':'question_author'}))
            timelist = timelist.replace(' ','')
            datestr = timelist[-23:-13]
            date = time.strptime(datestr, "%Y-%m-%d")
            #print(date)
            weekday = get_week_day(date)

            # 获取问题的标签，并写入CSV文件，如果没有标签，默认None
            taglist = bsobj.findAll('a',{'class':'detail_tag'})
            # print(taglist)
            for tag in taglist:  # 每一个tag也是一个bs4的队形，可以用bsobj的方法！！！
                row = [titles,datestr,weekday]
                tagtext = tag.string
                # print(tagtext)
                row.append(tagtext)
                csvwrite(filename,row)
        except:
            print('第{}条问题获取失败'.format(num))
        print('第{}条问题获取成功'.format(num))
        num = num + 1




