# -*- coding: utf-8 -*-
"""
Created on Tue May 16 18:48:53 2017

@author: Kevin McNamara
@version 2.00.mar.9.2019
"""
import requests
import re
import csv
import sys
import datetime
import optparse

#option parser
parser = optparse.OptionParser()
parser.add_option('-q', '--query', action="store", dest="query", help="query string", default="nothing")
options, args = parser.parse_args()

#Global Constants
linkMarket = 'https://www.marketwatch.com/investing/stock/' + options.query
filename = 'stocks1.csv'

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
        #removeBlankLine(d)       
        return()

#this is a dataparser
def parsedata1(urlin):
    #read from url
    f = requests.get(urlin)
    big = f.text
    #parse specific section
    sstart = big.index('<title>')+7
    eend = big.index('keywords')-12	
    d = f.text[sstart:eend].strip()
    # 1rst filter
    filter1 = d.find('meta property')
    d0 = d[filter1:len(d)]
    # 2nd filter
    filter2 = d0.find('<meta name=')
    d1 = d0[filter2:len(d0)].strip().replace(',','').replace('<meta name','').replace('>',',').replace('content',':').replace('=','').replace('<meta property"og:title','"long name').replace(' ','')
    # 3rd filter
    filter3 = d1.find('"tickerSymbol')
    d2 = d1[filter3:len(d1)]
    # remove blanks and returned lines
    d3 = d2.replace("\n","")
    # format to json
    d4 = '{"datapoint":{"' + d3[1:len(d3)-1] + '}}'
    print d4
    return(d4)

#this function calls a webform
def buildurl(webcall):
        parsedata1(webcall)
	return()

try:
   buildurl(linkMarket)
except:
   print ('An exception occured when connecting to the Market link!')
exit
