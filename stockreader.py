# -*- coding: utf-8 -*-
"""
Created on Tue May 16 18:48:53 2017

@author: Kevin McNamara
"""
import requests
import re
import csv
import sys
import datetime

#Global Constants
linkNASADAQ = 'http://eoddata.com/stocklist/NASDAQ/'
linkNYSE = 'http://eoddata.com/stocklist/NYSE/'
alphalist = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
filename = 'stocks.csv'

#Fomat Data before writing to file
def removeBlankLine(data1):
    reader = csv.reader(data1.split('\n'), delimiter='|')
    utc_datetime = datetime.datetime.utcnow()
    d1=utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
    for row in reader:
        if len(row)!=0:
            #DayOfWeek,GMTLong,DateEST,Symbol,Description,High,Low,Close,Volume,Change
            rowout=d1+',\t'.join(row)+','+'\n'
            print(rowout) 
    return()

#this function writes rows to a file
def writeToFile(data):
    f = open(filename,"a+")
    try:
        f.write(data)
    except csv.Error as e:
        sys.exit()
    f.close()    
    return()

#this function formats a raw string to a line return row string      
def fomatdata(txt):
        d = ('\n'.join([x for x in txt.split("\n") if x.strip()!=''])+'\n')
        removeBlankLine(d)       
        return()

#this function reads a web form and strips out the raw data
def parsedata(urlin):
    f = requests.get(urlin)    
    data0 = re.sub('<[^>]*>', '|', f.text)
    data1 = data0.replace(',','')
    data = data1.replace('|',',')
    do1= data.replace(',,,,', ',').replace(',,,', ',').replace(',,', ',').replace(',&nbsp;,', '').strip().strip(',') 
    begin_index = do1.index("W,X,Y,Z,")
    end_index = do1.index(".ld")
    dataout =  do1[begin_index+50:end_index-37].strip().strip(',').replace('Change','')
    fomatdata(dataout)
    return(dataout)

#this function calls a webform and iterates through an array of pages
def buildurl(webcall):
    for letter in alphalist:
        webcallA=webcall+letter+'.htm'
        parsedata(webcallA)
    return()

buildurl(linkNASADAQ)
buildurl(linkNYSE)

exit