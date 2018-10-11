from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from StockTickerFill import StockSymbols
import re
from http.client import IncompleteRead
import threading
from multiprocessing import Process, Manager
#from googlesearch.googlesearch import GoogleSearch
import search_google.api
buildargs = {
  'serviceName': 'customsearch',
  'version': 'v1',
  'developerKey': 'AIzaSyD3kW1v-aLFF8UZt1i-1Y-Vx5fdqD41sCQ'
}

class article_grabber(threading.Thread):
    def __init__(self):
        #self.ticker = ticker
        threading.Thread.__init__(self)
        self.search_keywords = ['release', 'scandal', 'merger', 'crash', 'stock', 'announce', 'buyout',
                                'liquidating', 'liquidation', 'price', 'shares', 'sellout', 'lawsuit', 'suing', 'trending',
                                'assets', 'IPO', 'Initial Public Offer', 'ROI', 'stakes', 'quarterly profit',
                                'marginal profit', 'profit', 'collateral', 'sales', 'revenues', 'losses', 'expenses',
                                'fraud', 'scheme', 'liability', 'tax', 'returns', 'gross', 'valuation',
                                'earnings', 'management', 'divestiture', 'acquisitions', 'acquisition',
                                'acquire', 'acquires'] #array of keywords to search for
        self.filename = 'NYSE.txt'#name of file with tickers and company names
        self.article_req_met = False
        self.title_return = False
        self.url_return = False
        self.url_arr = ['URLs']
        self.title_arr = ['Titles']
        self.title_arr1 = ['Titles']
        self.title_arr2 = ['Titles']
        self.title_arr3 = ['Titles']
        self.title_arr4 = ['Titles']

        # comment out lower section of code if not testing search function
        #num_pages = 1
        #search_results = google.search("Apple", num_pages)
        #print(search_results)
        #until here comment out
    def find_articles_ticker(self, ticker): #returns array of page/article titles without urls
        temp = StockSymbols(self.filename, ticker).g()
        k = 0
        moderator = len(self.search_keywords)//4
        for k in range(moderator):
            search_word = temp
            search_word = "{} {}".format(search_word, self.search_keywords[k])
            cseargs = {
                'q': search_word,
                'cx': '001557614940008904160:nk83rijrjcw',
                'num': 10
            }
            #print(search_word) #prints for debugging
            articles_found = search_google.api.results(buildargs, cseargs).get_values("items", "title")       #GoogleSearch().search(search_word)       #google.search(search_word, 1)
            print(articles_found)
            for i in range(len(self.search_keywords)):
                keyword = self.search_keywords[i]
                for j in articles_found:
                    #article = articles_found[j]
                    #print(search_word, article.description) #prints for debugging
                    #self.title_return = j.title #re.search(keyword, article.description)
                    #self.url_return = j.url
                    #content = j.getText()
                    #print(self.title_return)
                    #print()
                    #print(req_met) #prints for debugging
                    if self.title_return:
                        #print(req_met) #prints for debugging
                        #article_link = str(article.link)
                        #article_description = article.description  #printables for search debugging
                        #article_index = article.index  #printables for search debugging
                        #req = Request(article_link, headers={'User-Agent': 'Mozilla/5.0'})
                        #try:
                        #    try:
                        #        try:
                            #webpage = urlopen(req).read()
                            #soup = BeautifulSoup(webpage, "lxml")
                            #title = soup.find("meta", property="og:title")
                            #url = soup.find("meta", property="og:url")
                            #print(title["content"] if title else "No meta title given")
                            #print(url["content"] if url else "No meta url given")
                            #self.title_return = title["content"] if title else "No title given"
                            #self.url_return = url["content"] if url else "No meta url given"
                        self.title_arr1.append(self.title_return)
                        self.url_arr.append(self.url_return)
                        #except IncompleteRead:
                            #print("a file returned a by site could not be read") #prints for debugging
                        #except TimeoutError:
                            #print("Request timed out") #prints for debugging
                        #except HTTPError:
                            #print("request connection failed/rejected") #prints for debugging

        return self.title_arr1
    '''
    def find_articles_ticker1(self, ticker): #returns array of page/article titles without urls
        temp = StockSymbols(self.filename, ticker).g()
        k = len(self.search_keywords)/4
        moderator = len(self.search_keywords)/4 + len(self.search_keywords)/4
        for k in range(moderator):
            search_word = temp
            search_word = "{} {}".format(search_word, self.search_keywords[k])
            #print(search_word) #prints for debugging
            articles_found = google.search(search_word, 1)
            for i in range(len(self.search_keywords)):
                keyword = self.search_keywords[i]
                for j in range(len(articles_found)):
                    article = articles_found[j]
                    #print(search_word, article.description) #prints for debugging
                    req_met = re.search(keyword, article.description)
                    #print(req_met) #prints for debugging
                    if req_met:
                        #print(req_met) #prints for debugging
                        article_link = str(article.link)
                        #article_description = article.description  #printables for search debugging
                        #article_index = article.index  #printables for search debugging
                        req = Request(article_link, headers={'User-Agent': 'Mozilla/5.0'})
                        try:
                            try:
                                try:
                                    webpage = urlopen(req).read()
                                    soup = BeautifulSoup(webpage, "lxml")
                                    title = soup.find("meta", property="og:title")
                                    url = soup.find("meta", property="og:url")
                                    #print(title["content"] if title else "No meta title given")
                                    #print(url["content"] if url else "No meta url given")
                                    self.title_return = title["content"] if title else "No title given"
                                    self.url_return = url["content"] if url else "No meta url given"
                                    self.title_arr2.append(self.title_return)
                                    self.url_arr.append(self.url_return)
                                except IncompleteRead:
                                    print("a file returned a by site could not be read") #prints for debugging
                            except TimeoutError:
                                print("Request timed out") #prints for debugging
                        except HTTPError:
                            print("request connection failed/rejected") #prints for debugging

        return self.title_arr2
    def find_articles_ticker2(self, ticker): #returns array of page/article titles without urls
        temp = StockSymbols(self.filename, ticker).g()
        k = len(self.search_keywords)/4 + len(self.search_keywords)/4
        moderator = len(self.search_keywords)/4 + len(self.search_keywords)/4 + len(self.search_keywords)/4
        for k in range(moderator):
            search_word = temp
            search_word = "{} {}".format(search_word, self.search_keywords[k])
            #print(search_word) #prints for debugging
            articles_found = google.search(search_word, 1)
            for i in range(len(self.search_keywords)):
                keyword = self.search_keywords[i]
                for j in range(len(articles_found)):
                    article = articles_found[j]
                    #print(search_word, article.description) #prints for debugging
                    req_met = re.search(keyword, article.description)
                    #print(req_met) #prints for debugging
                    if req_met:
                        #print(req_met) #prints for debugging
                        article_link = str(article.link)
                        #article_description = article.description  #printables for search debugging
                        #article_index = article.index  #printables for search debugging
                        req = Request(article_link, headers={'User-Agent': 'Mozilla/5.0'})
                        try:
                            try:
                                try:
                                    webpage = urlopen(req).read()
                                    soup = BeautifulSoup(webpage, "lxml")
                                    title = soup.find("meta", property="og:title")
                                    url = soup.find("meta", property="og:url")
                                    #print(title["content"] if title else "No meta title given")
                                    #print(url["content"] if url else "No meta url given")
                                    self.title_return = title["content"] if title else "No title given"
                                    self.url_return = url["content"] if url else "No meta url given"
                                    self.title_arr3.append(self.title_return)
                                    self.url_arr.append(self.url_return)
                                except IncompleteRead:
                                    print("a file returned a by site could not be read") #prints for debugging
                            except TimeoutError:
                                print("Request timed out") #prints for debugging
                        except HTTPError:
                            print("request connection failed/rejected") #prints for debugging

        return self.title_arr3
    def find_articles_ticker3(self, ticker): #returns array of page/article titles without urls
        temp = StockSymbols(self.filename, ticker).g()
        k = len(self.search_keywords)/4 + len(self.search_keywords)/4 + len(self.search_keywords)/4
        moderator = len(self.search_keywords)/4 + len(self.search_keywords)/4 + len(self.search_keywords)/4+ len(self.search_keywords)/4
        for k in range(moderator):
            search_word = temp
            search_word = "{} {}".format(search_word, self.search_keywords[k])
            #print(search_word) #prints for debugging
            articles_found = google.search(search_word, 1)
            for i in range(len(self.search_keywords)):
                keyword = self.search_keywords[i]
                for j in range(len(articles_found)):
                    article = articles_found[j]
                    #print(search_word, article.description) #prints for debugging
                    req_met = re.search(keyword, article.description)
                    #print(req_met) #prints for debugging
                    if req_met:
                        #print(req_met) #prints for debugging
                        article_link = str(article.link)
                        #article_description = article.description  #printables for search debugging
                        #article_index = article.index  #printables for search debugging
                        req = Request(article_link, headers={'User-Agent': 'Mozilla/5.0'})
                        try:
                            try:
                                try:
                                    webpage = urlopen(req).read()
                                    soup = BeautifulSoup(webpage, "lxml")
                                    title = soup.find("meta", property="og:title")
                                    url = soup.find("meta", property="og:url")
                                    #print(title["content"] if title else "No meta title given")
                                    #print(url["content"] if url else "No meta url given")
                                    self.title_return = title["content"] if title else "No title given"
                                    self.url_return = url["content"] if url else "No meta url given"
                                    self.title_arr4.append(self.title_return)
                                    self.url_arr.append(self.url_return)
                                except IncompleteRead:
                                    print("a file returned a by site could not be read") #prints for debugging
                            except TimeoutError:
                                print("Request timed out") #prints for debugging
                        except HTTPError:
                            print("request connection failed/rejected") #prints for debugging

        return self.title_arr4
        '''
    #def gather_mthread_results(self, ticker):
        #Process(target=find_article_tickers)








print(article_grabber().find_articles_ticker('ABC'))