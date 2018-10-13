from StockEnviro import play_environment
from LiveStocks import live_stocks
import time
from multiprocessing import Process
import random
import re

class thought_driver():

    def timer_func(self):
         mins = 0
         num_checks = input("how long would you like to check for investment oppourtunity using default logic?")
         while mins != num_checks:
            print(">>>>>>>>", mins)
            time.sleep(60)
            mins += 1
         #return mins

    def default_logic(self):
        print("default logic")
        run_time = input("how long would you like to run the program for?(in minutes)")
        then = time.time()
        then = int(then / 60.00)
        print(then)
        tickers = ['AMZN', 'QQQ', 'AAPL', 'FB', 'AMD', 'NFLX', 'MSFT', 'TSLA', 'NVDA', 'GOOGL', 'GOOG', 'MU', 'TLT',
                   'TQQQ', 'AMRN', 'TLRY', 'INTC', 'ROKU', 'CSCO', 'ADBE']
        now = 0
        run = True
        while run :
            for j in range(len(tickers)):
                ticker = tickers[j]
                prev_value = 0.
                high_price = 0.00
                low_price = 0.00
                curr_value = live_stocks.get_price(live_stocks.get_html(ticker))
                if(prev_value > curr_value) & (prev_value > high_price):
                    high_price = prev_value
                if(curr_value > prev_value) & (curr_value > high_price):
                    high_price = curr_value
                if(curr_value < prev_value) & (curr_value < low_price):
                    low_price = curr_value
                if(prev_value < curr_value) & (prev_value < low_price):
                    low_price = prev_value

                perc_higher = (curr_value / low_price) * 100.00
                perc_lower = (curr_value / high_price) * 100.00

                if(perc_lower < 92.00):
                        #amount = int(play_environment.get_curr_hold(ticker) * int(perc_lower / 100.00))
                    play_environment.sell(ticker, play_environment.get_curr_hold(ticker))

                if perc_higher > 105.00 :
                    amount = random.randint(50, 100)
                    play_environment.buy(ticker, amount)
                now = time.time()
                now = int(now / 60.00)
                print(now)
                time_passed = now - then
                if time_passed >= run_time:
                    run = False
                prev_value = curr_value

    def influenced_logic(ticker):
        print("logic is now influenced by real world events")
        #train_state = input("Would you like to train the bot personally, self train, or just run based on current knowledge?(0=run; 1=self; 2=person)")
        read = open("ArticleTitles.txt", "r+")
        file = read.read()
        train_state = 2

        #below not functioning yet
        if(train_state == 1):
            print("You chose self training.")
            temp_search = re.search("Good:", file)
            temp_search2 = re.search("Bad:", file)
            good_start = temp_search.end()
            good_end = temp_search2.start()
            bad_start = temp_search2.end()
            temp_run_time = input("How long would you like to run for?(in minutes)")
            temp_run_state = True


        if(train_state == 2):
            print("You chose to personally supervise the training.")
            # good_keywords = ['release', 'stock', 'announce', 'buyout','trending',
            #                     'IPO', 'Initial Public Offer', 'ROI', 'stakes',
            #                     'profit', 'collateral', 'sales', 'revenues',
            #                     'returns', 'gross',
            #                     'earnings', 'management', 'divestiture', 'acquisitions', 'acquisition',
            #                     'acquire', 'acquires']
            # bad_keywords = ['release', 'scandal', 'merger', 'crash', 'stock', 'announce', 'buyout',
            #                     'liquidating', 'liquidation', 'price', 'shares', 'sellout', 'lawsuit', 'suing', 'trending',
            #                     'assets', 'IPO', 'Initial Public Offer', 'ROI', 'stakes', 'quarterly profit',
            #                     'marginal profit', 'profit', 'collateral', 'sales', 'revenues', 'losses', 'expenses',
            #                     'fraud', 'scheme', 'liability', 'tax', 'returns', 'gross', 'valuation',
            #                     'earnings', 'management', 'divestiture', 'acquisitions', 'acquisition',
            #                     'acquire', 'acquires']
            temp_run_time = input("How long would you like to run for?(in minutes) *if you write zero(0) it will prompt you after every input to ask if you want to continue*")
            temp_run_state = True
            if(temp_run_time == 0):
                while temp_run_state:
                    article_title = input("Enter a real of fake article title...")
                    temp_search = re.search("Good:", file)
                    temp_search2 = re.search("Bad:", file)
                    good_start = temp_search.end()
                    good_end = temp_search2.start()
                    bad_start = temp_search2.end()
                    good_section = file[good_start: good_end]
                    bad_section = file[bad_start:]
                    article_words = article_title.split()
                    good_count = 0
                    bad_count = 0
                    for k in article_words:
                        print(k)
                        # for i in re.finditer(k, good_section):
                        #     print(i)
                        found_good = re.search(k, good_section)
                        found_bad = re.search(k, bad_section)
                        if found_good:
                            good_count = good_count + 1
                        # for j in re.finditer(k, bad_section):
                        #     print(j)
                        if found_bad:
                            bad_count = bad_count + 1

                        if (good_count > 0) | (bad_count > 0):
                            perc_good = float(len(article_words) / good_count)
                            print(perc_good)
                            perc_bad = float(len(article_words) / bad_count)
                            print(perc_bad)
                            if (perc_good > perc_bad) & (perc_good > 80.00):
                                new_file = file[:good_start]+ "\n" + article_title + file[temp_search2.start():]
                                print(new_file)
                                # read.seek(0)
                                # read.truncate()
                                # read.write(new_file)
                                amount = random.randint(50, 100)
                                play_environment.buy(ticker, amount)

                            elif(perc_bad > perc_good) & (perc_bad > 80.00):
                                new_file = file[:bad_start]+ "\n" + article_title
                                print(new_file)
                                #read.write(article_title)
                                play_environment.sell(ticker, play_environment.get_curr_hold(ticker))

                            else:
                                ask = "Is this article title: " + article_title + " :Good or Bad?(G/B)"
                                article_state = input(ask)
                                if article_state == "G":
                                    new_file = file[:good_start] + "\n" + article_title + file[temp_search2.start():]
                                    print(new_file)
                                    # read.seek(0)
                                    # read.truncate()
                                    # read.write(new_file)
                                    amount = random.randint(50, 100)
                                    play_environment.buy(ticker, amount)

                                if article_state == "B":
                                    new_file = file[:bad_start] + "\n" + article_title
                                    print(new_file)
                                    # read.write(article_title)
                                    play_environment.sell(ticker, play_environment.get_curr_hold(ticker))
                        else:
                            ask = "Is this article title: " + article_title + " :Good or Bad?(G/B)"
                            article_state = input(ask)
                            if article_state == "G":
                                new_file = file[:good_start] + "\n" + article_title + file[temp_search2.start():]
                                print(new_file)
                                # read.seek(0)
                                # read.truncate()
                                # read.write(new_file)
                                amount = random.randint(50, 100)
                                play_environment.buy(ticker, amount)

                            if article_state == "B":
                                new_file = file[:bad_start] + "\n" + article_title
                                print(new_file)
                                # read.write(article_title)
                                play_environment.sell(ticker, play_environment.get_curr_hold(ticker))
                    cont = input("would you like to put in another article?Y/N")
                    if cont == "N":
                        temp_run_state = False
            else:
                then = time.time()
                then = int(then / 60.00)
                now = 0
                run2 = True
                while run2:
                    article_title = input("Enter a real of fake article title...")
                    temp_search = re.search("Good:", file)
                    temp_search2 = re.search("Bad:", file)
                    good_start = temp_search.end()
                    good_end = temp_search2.start()
                    bad_start = temp_search2.end()
                    good_section = file[good_start: good_end]
                    bad_section = file[bad_start:]
                    article_words = article_title.split()
                    good_count = 0
                    bad_count = 0
                    for k in article_words:
                        print(k)
                        # for i in re.finditer(k, good_section):
                        #     print(i)
                        found_good = re.search(k, good_section)
                        found_bad = re.search(k, bad_section)
                        if found_good:
                            good_count = good_count + 1
                        # for j in re.finditer(k, bad_section):
                        #     print(j)
                        if found_bad:
                            bad_count = bad_count + 1
                        if(good_count > 0) | (bad_count > 0):
                            perc_good = float(len(article_words) / good_count)
                            print(perc_good)
                            perc_bad = float(len(article_words) / bad_count)
                            print(perc_bad)
                            if (perc_good > perc_bad) & (perc_good > 80.00):
                                new_file = file[:good_start] + "\n" + article_title + file[temp_search2.start():]
                                print(new_file)
                                # read.seek(0)
                                # read.truncate()
                                # read.write(new_file)
                            elif (perc_bad > perc_good) & (perc_bad > 80.00):
                                new_file = file[:bad_start] + "\n" + article_title
                                print(new_file)
                                # read.write(article_title)

                            else:
                                ask = "Is this article title: " + article_title + " :Good or Bad?(G/B)"
                                article_state = input(ask)
                                if article_state == "G":
                                    new_file = file[:good_start] + "\n" + article_title + file[temp_search2.start():]
                                    print(new_file)
                                    # read.seek(0)
                                    # read.truncate()
                                    # read.write(new_file)
                                if article_state == "B":
                                    new_file = file[:bad_start] + "\n" + article_title
                                    print(new_file)
                                    # read.write(article_title)
                now = time.time()
                now = int(now / 60.00)
                print(now)
                time_passed = now - then
                if time_passed >= temp_run_time:
                    run2 = False



        #not functioning yet
        if(train_state == 0):
            print("Running the current state of bot knowledge")
            temp_search = re.search("Good:", file)
            temp_search2 = re.search("Bad:", file)
            good_start = temp_search.end()
            good_end = temp_search2.start()
            bad_start = temp_search2.end()
        return None

#print(thought_driver.default_logic(""))
print(thought_driver.influenced_logic("AMD"))