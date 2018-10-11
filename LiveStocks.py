import StockTickerFill
from lxml import html
from bs4 import BeautifulSoup
import re
import requests
#from urllib3 import request
from urllib.request import Request, urlopen

html_doc = ''
bs = BeautifulSoup(html_doc, 'html.parser')
class live_stocks():
    #gets the html data for the given ticker
    def get_html(ticker):
        #print("Getting info") #to confirm the function has started running
        url = 'https://www.nasdaq.com/symbol/'+ ticker
        link = Request(url)
        webpage = urlopen(link).read()
        html_string = webpage.decode('utf-8')
        return html_string
    #gets the price from the given html data
    #Note: only works with html found using the website from get_html
    def get_price(html):
        #print("Parsing") #to confirm the function has started running
        for m in re.finditer("qwidget-dollar", html):
            # print('%02d-%02d: %s' % (m.start(), m.end(), m.group(0))) #for debugging
            # print(m.end(), m.end()+10)    #for debugging
            reqs = re.compile("</div>")
            new_html = html[m.end(): m.end()+25]
            find = reqs.finditer(new_html)
            for match in find:
                #print(match.end())
                dollar = new_html[3: match.end()-6]
                #print(dollar)
                return dollar

#print(live_stocks.get_price(live_stocks.get_html('AMD'))) #line for testing of code
