import re


class StockSymbols:
   def __init__(self, filename, ticker, company_name):
       self.f = open(filename)
       self.ticker = ticker
       self.arr_temp = False
       self.company_name = company_name
       self.tickers_names()
   #'''Returns array of all tickers'''


   def tickers(self):
      string = self.f.read()
      expression = re.compile("([A-Z]{1,5})\s+")
      self.arr_temp = expression.findall(string)
   # Returns name of company based on recieved ticker
   def tickers_names(self):
      string2 = self.f.read()
      lines = string2.split('\n')
      print(self.company_name)
      print(self.ticker)

      if self.ticker == '':
          for n in range(len(lines)):
             temp_str = lines[n]
             isIn = re.search(self.company_name, temp_str)
             if isIn:
                temp = re.sub(self.company_name, "", temp_str, 1)
          self.company_name = temp
          print(self.company_name)
      elif self.company_name == '':
        #returns the ticker of the company name
          for n in range(len(lines)):
             temp_str = lines[n]
             isIn = re.search(self.ticker, temp_str)
             if isIn:
                temp = re.sub(self.ticker, "", temp_str, 1)
          self.ticker = temp
          print(self.ticker)
      else:
        print("conflict of interest with values or no values given")
   def g(self):
      return (self.company_name + " : " + self.ticker)

#print(StockSymbols('NYSE.txt', '', '').g()) #tests to confirm successful run of company name getter