from LiveStocks import live_stocks
import re

class play_environment():
     # def __init__(self):
     #   self.file_name = "Portfolio.txt"
     #    self.spendable_money = 100000

    #gets holdings for a certain stock
    def get_curr_hold(ticker):
        print("Getting current holdings for: " + ticker)
        file_name = "Portfolio.txt"
        file = open(file_name, "r+")
        holdings = file.read()
        for i in re.finditer(ticker, holdings):
            pattern = re.compile("\n")
            pattern2 = pattern.search(holdings, i.end())
            stock = int(holdings[i.end() + 2: pattern2.start()])
            return stock

    #function to buy stock in the play environment
    def buy(ticker, amount):
        file_name = "Portfolio.txt"
        file = open(file_name, "r+")
        holdings = file.read()
        new_amount = play_environment.get_curr_hold(ticker) + amount
        print("Buying!")
        stocks = str(new_amount)
        for i in re.finditer(ticker, holdings):
            new_file = holdings[:i.end()+2] + stocks + "\n" + holdings[i.end() + len(stocks) + 2: ]
            file.truncate(0)
            #print(file.read()) #for debugging
            file.write(new_file)
            #print(file.read()) #for debugging
            play_environment.remove_money(ticker,amount)


        # with open(file_name, 'r') as file:
        #     # read a list of lines into data
        #     data = file.readlines()
        #     print("File found! Portfolio loaded!")
        # # __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) #separate way of getting file
        # # read = open(os.path.join(__location__, 'Portfolio.txt')); #separate way of getting file
        # #print(read.read()) #read debugging
        #     for i in range(20):
        #         portfo_str = str(data[i])
        #         print(portfo_str)
        #         print(re.finditer(portfo_str, 'AMD'))
        #         print(amount)
        #file.close()
        return file.read()


    #function to sell stock in play environment
    def sell(ticker, amount):
        file_name = "Portfolio.txt"
        file = open(file_name, "r+")
        holdings = file.read()
        new_amount = play_environment.get_curr_hold(ticker) - amount
        print("Selling!")
        stocks = str(new_amount)
        for i in re.finditer(ticker, holdings):
            new_file = holdings[:i.end() + 1] + stocks + "\n" + holdings[i.end() + len(stocks) + 1:]
            file.seek(0)
            file.truncate()
            #print(file.read()) #for debugging
            file.write(new_file)
            #print(file.read()) #for debugging
            play_environment.add_money(ticker, amount)
        #file.close()
        return file.read()


    #currently non functional part of play environment
    def short(ticker, amount):
        print("Shorting!")
        file_name = "Portfolio.txt"
        read = open(file_name, "r+")
        print("File found! Portfolio loaded!")
        portfo_str = read.read()
        print(re.search(ticker))
        print(amount)
        return None

    #just prints the file
    def curr_holdings(self):
        print("Your/bots current holdings are...")
        file_name = "Portfolio.txt"
        read_portfo = open(file_name, "r")
        return read_portfo.read()


    # returns the value of portfolio aside from money left
    def value_portfo(self):
        print("Getting value of your/bot's portolio!")
        file_name = "Portfolio.txt"
        file = open(file_name, "r")
        file_str = file.read()
        tickers = ['AMZN', 'QQQ', 'AAPL', 'FB', 'AMD', 'NFLX', 'MSFT', 'TSLA', 'NVDA', 'GOOGL', 'GOOG', 'MU', 'TLT', 'TQQQ', 'AMRN', 'TLRY', 'INTC', 'ROKU', 'CSCO', 'ADBE']
        sum = 0.00
        for k in range(len(tickers)):
            curr_ticker = tickers[k]
            value = float(live_stocks.get_price(live_stocks.get_html(curr_ticker)))
            for found in re.finditer(curr_ticker, file_str):
                pattern = re.compile("\n")
                pattern2 = pattern.search(file_str, found.end())
                #print(file_str[found.end() + 2: pattern2.start()])
                stocks = float(file_str[found.end() + 2: pattern2.start()])
                value_curr = stocks * value
                print(value_curr)
                sum = sum + value_curr
                #stocks = file[found.end() + 1:] + stocks + "\n" + file[found.end() + len(stocks) + 1:]
            # file.close()
        return sum


    #just returns the money available to spend
    def get_money_left(self):
        money_sign = "Money left:"
        print("Getting Money left!")
        file_name = "Portfolio.txt"
        file = open(file_name, "r+")
        holdings = file.read()
        for i in re.finditer(money_sign, holdings):
            pattern = re.compile("\n")
            pattern2 = pattern.search(holdings, i.end())
            money_left = float(holdings[i.end(): pattern2.start()])
            file.close()
            return money_left

    #removes money from the money left
    def remove_money(ticker, amount):
        file_name = "Portfolio.txt"
        money_sign = "Money left:"
        file = open(file_name, "r+")
        holdings = file.read()
        spendable_money = play_environment.get_money_left("")
        for i in re.finditer(money_sign, holdings):
            pattern = re.compile("\n")
            pattern2 = pattern.search(holdings, i.end())
            money_left = float(holdings[i.end(): pattern2.start()])
            stock_price = live_stocks.get_price(live_stocks.get_html(ticker))
            taken = float(stock_price) * amount
            spendable_money = spendable_money - taken
            new_file = holdings[:i.end() + 1] + str(spendable_money) + "\n" + holdings[i.end() + len(str(spendable_money)) + 1:]
            file.seek(0)
            file.truncate()
        # print(file.read()) #for debugging
            file.write(new_file)
        #file.close()
        return spendable_money

    #adds money to money left to spend in play environment
    def add_money(ticker, amount):
        file_name = "Portfolio.txt"
        money_sign = "Money left:"
        file = open(file_name, "r+")
        holdings = file.read()
        spendable_money = play_environment.get_money_left("")
        for i in re.finditer(money_sign, holdings):
            pattern = re.compile("\n")
            pattern2 = pattern.search(holdings, i.end())
            money_left = float(holdings[i.end(): pattern2.start()])
            stock_price = live_stocks.get_price(live_stocks.get_html(ticker))
            taken = float(stock_price) * amount
            spendable_money = spendable_money + taken
            new_file = holdings[:i.end() + 1] + str(spendable_money) + "\n" + holdings[i.end() + len(str(spendable_money)) + 1:]
            file.seek(0)
            file.truncate()
            # print(file.read()) #for debugging
            file.write(new_file)
        #file.close()
        return spendable_money



#print(play_environment.sell("AMD", 20)) #test line for code sell
#print(play_environment.buy("AMD", 20)) #test line for code buy
#print(play_environment.get_curr_hold("AMD")) #test line for code get_curr_hold
#print(play_environment.curr_holdings("")) #test code for curr_holdings
#print(play_environment.get_money_left("")) #test code for get_money_left
#print(play_environment.remove_money("AMD", 20)) #test code for remove_money()
#print(play_environment.add_money("AMD", 20)) #test code for add_money()
#print(play_environment.value_portfo(""))