from MarketWatch.MarketWatch import MarketWatch
#import MarketWatch.driver
# from MarketWatch import Order



mwatch_email = 'stockmarketbot1@gmail.com'
mwatch_pass = 'marketbotpass'
mwatch_gameID = 'API python function test'
#ID possibilities : api-python-function-test, API python function test
mwatch_testTicker = 'AAPL'
#api = MarketWatch(mwatch_email, mwatch_pass, mwatch_gameID, True)



def APITest():
    print("API test has started...")
    print("Starting sign in...")
    MarketWatch(mwatch_email, mwatch_pass, mwatch_gameID, debug = True)
    print("Signed in and in game!")
    print("Testing functions...")
    print("AAPL: ", MarketWatch.getPrice(mwatch_testTicker), " AMZN: ", MarketWatch.getPrice('AMZN'))
    print("Price getter functioning correctly!")
    print("Buying Apple(APPL) shares for testing...")
    print(MarketWatch.buy(mwatch_testTicker, 10), MarketWatch.buy('AMZN', 5), "\n Success!")
    print("Checking orders with order function...", "\n", MarketWatch.getOrders(), "\n", "DONE!")
    print("Getting remaining cash...", "\n", MarketWatch.getCashRemaining(), "\n", "DONE!")
    print("Testing ticker to name transfer: ", MarketWatch.ticker(mwatch_testTicker), "\n Success!")
    print("Checking orders with order function...", "\n", MarketWatch.getOrders(), "\n", "DONE!")
    print("Getting remaining cash...", "\n", MarketWatch.getCashRemaining(), "\n", "DONE!")
    print("Testing shorting Amazon shares...", "\n", MarketWatch.short('AMZN', 5), "\n Success!")
    print("Checking orders with order function...", "\n", MarketWatch.getOrders(), "\n", "DONE!")
    print("Getting remaining cash...", "\n", MarketWatch.getCashRemaining(), "\n", "DONE!")
    print("Selling Apple shares for testing...", "\n", MarketWatch.sell(mwatch_testTicker, 5), "\n Success!")
    print("Checking orders with order function...", "\n", MarketWatch.getOrders(), "\n", "DONE!")
    print("Getting remaining cash...", "\n", MarketWatch.getCashRemaining(), "\n", "DONE!")




APITest()

