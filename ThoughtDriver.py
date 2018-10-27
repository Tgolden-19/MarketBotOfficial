from StockEnviro import play_environment
from LiveStocks import live_stocks
from ArticleGrabber import article_grabber
import time
from multiprocessing import Process
import random
import re

#this file holds the entire thought processes that make this program as intelligent as any normal stock investor

#currently missing most fuctions and needs complete supervision but will be simple to implement full automation
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
        run_time = int(input("how long would you like to run the program for(in minutes) for each company?"))
        then = time.time()
        then = int(then / 60.00)
        print(then)
        tickers = ['AMZN', 'QQQ', 'AAPL', 'FB', 'AMD', 'NFLX', 'MSFT', 'TSLA', 'NVDA', 'GOOGL', 'GOOG', 'MU', 'TLT',
                   'TQQQ', 'AMRN', 'TLRY', 'INTC', 'ROKU', 'CSCO', 'ADBE']
        now = 0
        run = True
        print(len(tickers))
        for j in range(len(tickers)):
            print(j)
            ticker = tickers[j]
            prev_value = 0.00
            high_price = 0.00
            low_price = 0.00
            perc_lower = 0.00
            perc_higher = 0.00
            while run:
                curr_value = float(live_stocks.get_price(live_stocks.get_html(ticker)))
                print(str(curr_value) + ": current value of stock for " + ticker)
                print("=====>" + str(prev_value))
                if(prev_value > curr_value) & (prev_value > high_price):
                    high_price = prev_value
                if(curr_value > prev_value) & (curr_value > high_price):
                    high_price = curr_value
                if(curr_value < prev_value) & (curr_value < low_price):
                    low_price = curr_value
                if(prev_value < curr_value) & (prev_value < low_price):
                    low_price = prev_value
                if(low_price != 0.00):
                    perc_higher = (curr_value / low_price) * 100.00
                    print("-->" + str(perc_higher))
                if(high_price != 0.00):
                    perc_lower = (curr_value / high_price) * 100.00
                    print("==>" + str(perc_lower))

                if perc_lower < 92.00:
                        #amount = int(play_environment.get_curr_hold(ticker) * int(perc_lower / 100.00))
                    play_environment.sell(ticker, play_environment.get_curr_hold(ticker))

                if perc_higher > 105.00:
                    amount = random.randint(50, 100)
                    play_environment.buy(ticker, amount)

                now = time.time()
                now = int(now / 60.00)
                print(now)
                #print(time.time())
                time_passed = now - then
                if time_passed >= run_time:
                    run = False
                #print(curr_value)
                prev_value = curr_value
                #print("()()" + str(prev_value))

    def influenced_logic(ticker):
        print("logic is now influenced by real world events")
        #train_state = input("Would you like to train the bot personally, self train, or just run based on current knowledge?(0=run; 1=self; 2=person)")
        file_name = "ArticleTitles.txt"
        read = open(file_name, "r+")
        file = read.read()
        train_state = 1
        tickers = ['AMZN', 'QQQ', 'AAPL', 'FB', 'AMD', 'NFLX', 'MSFT', 'TSLA', 'NVDA', 'GOOGL', 'GOOG', 'MU', 'TLT',
                   'TQQQ', 'AMRN', 'TLRY', 'INTC', 'ROKU', 'CSCO', 'ADBE']

        #below not functioning yet
        if(train_state == 1):
            print("You chose self training.")
            temp_search = re.search("Good:", file)
            temp_search2 = re.search("Bad:", file)
            good_start = temp_search.end()
            good_end = temp_search2.start()
            bad_start = temp_search2.end()
            temp_run_time = int(input("How long would you like to run for?(in minutes)"))
            temp_run_state = True
            then = time.time()
            then = int(then / 60.00)
            now = 0
            for j in range(len(tickers)):
                ticker_auto = tickers[j]
                print(ticker_auto)
                run2 = True
                while run2:
                    #article_title = input("Enter a real of fake article title...")
                    article_title = article_grabber.find_articles_ticker("", ticker_auto)
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
                        # print(k) #for debugging word splitting
                        # for i in re.finditer(k, good_section):
                        #     print(i)
                        found_good = re.search(k, good_section)
                        found_bad = re.search(k, bad_section)
                        if found_good:
                            good_count = good_count + 1
                            print("found good")
                        # for j in re.finditer(k, bad_section):
                        #     print(j)
                        if found_bad:
                            bad_count = bad_count + 1
                            print("found_bad")

                    if (good_count > 0) | (bad_count > 0):  # causes division by zero (small bug)
                        perc_good = 0.00
                        perc_bad = 0.00
                        if (good_count > bad_count):
                            perc_good = float(good_count / len(article_words))
                            print(perc_good)
                            perc_bad = 0.01
                        else:
                            perc_bad = float(bad_count / len(article_words))
                            print(perc_bad)
                            perc_good = 0.01
                        if (perc_good > perc_bad) & (perc_good > 0.80):
                            new_file = file[:good_start + len(good_section)] + "\n" + article_title + "\n" + file[
                                                                                                             temp_search2.start():]
                            # print(new_file)
                            read.seek(0)
                            read.truncate()
                            read.write(new_file)
                            read.close()
                            read = open(file_name, "r+")
                            file = read.read()
                            amount = random.randint(50, 100)
                            play_environment.buy(ticker, amount)

                        elif (perc_bad > perc_good) & (perc_bad > 0.80):
                            # new_file = file[:bad_start]+ "\n" + article_title
                            # print(new_file)
                            read.write("\n" + article_title)
                            read.close()
                            read = open(file_name, "r+")
                            file = read.read()
                            play_environment.sell(ticker, play_environment.get_curr_hold(ticker))

                        else:
                            ask = "Is this article title [2]: " + article_title + " :Good or Bad?(G/B)"
                            article_state = input(ask)
                            if article_state == "G":
                                new_file = file[:good_start + len(good_section)] + "\n" + article_title + "\n" + file[
                                                                                                                 temp_search2.start():]
                                # print(new_file)  # for debugging file write
                                read.seek(0)
                                read.truncate()
                                read.write(new_file)
                                read.close()
                                read = open(file_name, "r+")
                                file = read.read()
                                amount = random.randint(50, 100)
                                play_environment.buy(ticker, amount)

                            if article_state == "B":
                                # new_file = file[:bad_start] + "\n" + article_title  #for debugging file write
                                # print(new_file)  #for debugging file write
                                read.write("\n" + article_title)
                                read.close()
                                read = open(file_name, "r+")
                                file = read.read()
                                play_environment.sell(ticker, play_environment.get_curr_hold(ticker))
                    else:
                        ask = "Is this article title [3]: " + article_title + " :Good or Bad?(G/B)"
                        article_state = input(ask)
                        if article_state == "G":
                            new_file = file[:good_start + len(good_section)] + "\n" + article_title + "\n" + file[
                                                                                                             temp_search2.start():]
                            # print(new_file)
                            read.seek(0)
                            read.truncate()
                            read.write(new_file)
                            read.close()
                            read = open(file_name, "r+")
                            file = read.read()
                            amount = random.randint(50, 100)
                            play_environment.buy(ticker, amount)

                        if article_state == "B":
                            new_file = file[:bad_start] + "\n" + article_title
                            # print(new_file)
                            read.write("\n" + article_title)
                            read.close()
                            read = open(file_name, "r+")
                            file = read.read()
                            play_environment.sell(ticker, play_environment.get_curr_hold(ticker))
                    # cont = input("would you like to put in another article?Y/N")
                    # if cont == "N":
                    #     temp_run_state = False
                    now = time.time()
                    now = int(now / 60.00)
                    print(now)
                    time_passed = now - then
                    if time_passed >= temp_run_time:
                        run2 = False


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
            temp_run_time = int(input("How long would you like to run for?(in minutes) *if you write zero(0) it will prompt you after every input to ask if you want to continue*"))
            temp_run_state = True
            #temp_run_time = 0
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
                        #print(k) #for debugging word splitting
                        # for i in re.finditer(k, good_section):
                        #     print(i)
                        found_good = re.search(k, good_section)
                        found_bad = re.search(k, bad_section)
                        if found_good:
                            good_count = good_count + 1
                            print("found good")
                        # for j in re.finditer(k, bad_section):
                        #     print(j)
                        if found_bad:
                            bad_count = bad_count + 1
                            print("found_bad")

                    if (good_count > 0) | (bad_count > 0):  # causes division by zero (small bug)
                        perc_good = 0.00
                        perc_bad = 0.00
                        if(good_count > bad_count):
                            perc_good = float(good_count / len(article_words))
                            print(perc_good)
                            perc_bad = 0.01
                        else:
                            perc_bad = float( bad_count / len(article_words) )
                            print(perc_bad)
                            perc_good = 0.01
                        if (perc_good > perc_bad) & (perc_good > 0.80):
                            new_file = file[:good_start + len(good_section)]+ "\n" + article_title + "\n" + file[temp_search2.start():]
                            #print(new_file)
                            read.seek(0)
                            read.truncate()
                            read.write(new_file)
                            read.close()
                            read = open(file_name, "r+")
                            file = read.read()
                            amount = random.randint(50, 100)
                            play_environment.buy(ticker, amount)

                        elif(perc_bad > perc_good) & (perc_bad > 0.80):
                            #new_file = file[:bad_start]+ "\n" + article_title
                            #print(new_file)
                            read.write("\n" + article_title)
                            read.close()
                            read = open(file_name, "r+")
                            file = read.read()
                            play_environment.sell(ticker, play_environment.get_curr_hold(ticker))

                        else:
                            ask = "Is this article title [2]: " + article_title + " :Good or Bad?(G/B)"
                            article_state = input(ask)
                            if article_state == "G":
                                new_file = file[:good_start + len(good_section)] + "\n" + article_title + "\n" + file[temp_search2.start():]
                                #print(new_file)  # for debugging file write
                                read.seek(0)
                                read.truncate()
                                read.write(new_file)
                                read.close()
                                read = open(file_name, "r+")
                                file = read.read()
                                amount = random.randint(50, 100)
                                play_environment.buy(ticker, amount)

                            if article_state == "B":
                                # new_file = file[:bad_start] + "\n" + article_title  #for debugging file write
                                # print(new_file)  #for debugging file write
                                read.write("\n" + article_title)
                                read.close()
                                read = open(file_name, "r+")
                                file = read.read()
                                play_environment.sell(ticker, play_environment.get_curr_hold(ticker))
                    else:
                        ask = "Is this article title [3]: " + article_title + " :Good or Bad?(G/B)"
                        article_state = input(ask)
                        if article_state == "G":
                            new_file = file[:good_start + len(good_section)] + "\n" + article_title + "\n" + file[temp_search2.start():]
                            #print(new_file)
                            read.seek(0)
                            read.truncate()
                            read.write(new_file)
                            read.close()
                            read = open(file_name, "r+")
                            file = read.read()
                            amount = random.randint(50, 100)
                            play_environment.buy(ticker, amount)

                        if article_state == "B":
                            new_file = file[:bad_start] + "\n" + article_title
                            #print(new_file)
                            read.write("\n" + article_title)
                            read.close()
                            read = open(file_name, "r+")
                            file = read.read()
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
                        #print(k) #for debugging word splitting
                        # for i in re.finditer(k, good_section):
                        #     print(i)
                        found_good = re.search(k, good_section)
                        found_bad = re.search(k, bad_section)
                        if found_good:
                            good_count = good_count + 1
                            print("found good")
                        # for j in re.finditer(k, bad_section):
                        #     print(j)
                        if found_bad:
                            bad_count = bad_count + 1
                            print("found_bad")

                    if (good_count > 0) | (bad_count > 0):  # causes division by zero (small bug)
                        perc_good = 0.00
                        perc_bad = 0.00
                        if(good_count > bad_count):
                            perc_good = float(good_count / len(article_words))
                            print(perc_good)
                            perc_bad = 0.01
                        else:
                            perc_bad = float( bad_count / len(article_words))
                            print(perc_bad)
                            perc_good = 0.01
                        if (perc_good > perc_bad) & (perc_good > 0.80):
                            new_file = file[:good_start + len(good_section)]+ "\n" + article_title + "\n" + file[temp_search2.start():]
                            #print(new_file)
                            read.seek(0)
                            read.truncate()
                            read.write(new_file)
                            read.close()
                            read = open(file_name, "r+")
                            file = read.read()
                            amount = random.randint(50, 100)
                            play_environment.buy(ticker, amount)

                        elif(perc_bad > perc_good) & (perc_bad > 0.80):
                            #new_file = file[:bad_start]+ "\n" + article_title
                            #print(new_file)
                            read.write("\n" + article_title)
                            read.close()
                            read = open(file_name, "r+")
                            file = read.read()
                            play_environment.sell(ticker, play_environment.get_curr_hold(ticker))

                        else:
                            ask = "Is this article title [2]: " + article_title + " :Good or Bad?(G/B)"
                            article_state = input(ask)
                            if article_state == "G":
                                new_file = file[:good_start + len(good_section)] + "\n" + article_title + "\n" + file[temp_search2.start():]
                                #print(new_file)  # for debugging file write
                                read.seek(0)
                                read.truncate()
                                read.write(new_file)
                                read.close()
                                read = open(file_name, "r+")
                                file = read.read()
                                amount = random.randint(50, 100)
                                play_environment.buy(ticker, amount)

                            if article_state == "B":
                                # new_file = file[:bad_start] + "\n" + article_title  #for debugging file write
                                # print(new_file)  #for debugging file write
                                read.write("\n" + article_title)
                                read.close()
                                read = open(file_name, "r+")
                                file = read.read()
                                play_environment.sell(ticker, play_environment.get_curr_hold(ticker))
                    else:
                        ask = "Is this article title [3]: " + article_title + " :Good or Bad?(G/B)"
                        article_state = input(ask)
                        if article_state == "G":
                            new_file = file[:good_start + len(good_section)] + "\n" + article_title + "\n" + file[temp_search2.start():]
                            #print(new_file)
                            read.seek(0)
                            read.truncate()
                            read.write(new_file)
                            read.close()
                            read = open(file_name, "r+")
                            file = read.read()
                            amount = random.randint(50, 100)
                            play_environment.buy(ticker, amount)

                        if article_state == "B":
                            new_file = file[:bad_start] + "\n" + article_title
                            #print(new_file)
                            read.write("\n" + article_title)
                            read.close()
                            read = open(file_name, "r+")
                            file = read.read()
                            play_environment.sell(ticker, play_environment.get_curr_hold(ticker))
                    # cont = input("would you like to put in another article?Y/N")
                    # if cont == "N":
                    #     temp_run_state = False
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
            temp_run_time = int(input("How long would you like to run for?(in minutes)"))
            good_start = temp_search.end()
            good_end = temp_search2.start()
            bad_start = temp_search2.end()

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
                    # print(k) #for debugging word splitting
                    # for i in re.finditer(k, good_section):
                    #     print(i)
                    found_good = re.search(k, good_section)
                    found_bad = re.search(k, bad_section)
                    if found_good:
                        good_count = good_count + 1
                        print("found good")
                    # for j in re.finditer(k, bad_section):
                    #     print(j)
                    if found_bad:
                        bad_count = bad_count + 1
                        print("found_bad")

                if (good_count > 0) | (bad_count > 0):  # causes division by zero (small bug)
                    perc_good = 0.00
                    perc_bad = 0.00
                    if (good_count > bad_count):
                        perc_good = float(good_count / len(article_words))
                        print(perc_good)
                        perc_bad = 0.01
                    else:
                        perc_bad = float(bad_count / len(article_words))
                        print(perc_bad)
                        perc_good = 0.01

                    if (perc_good > perc_bad) & (perc_good > 0.80):
                        amount = random.randint(50, 100)
                        play_environment.buy(ticker, amount)

                    elif (perc_bad > perc_good) & (perc_bad > 0.80):
                        play_environment.sell(ticker, play_environment.get_curr_hold(ticker))

                    else:
                        ask = "Is this article title [2]: " + article_title + " :Good or Bad?(G/B)"
                        article_state = input(ask)
                        if article_state == "G":
                            amount = random.randint(50, 100)
                            play_environment.buy(ticker, amount)

                        if article_state == "B":
                            play_environment.sell(ticker, play_environment.get_curr_hold(ticker))
                else:
                    ask = "Is this article title [3]: " + article_title + " :Good or Bad?(G/B)"
                    article_state = input(ask)
                    if article_state == "G":
                        amount = random.randint(50, 100)
                        play_environment.buy(ticker, amount)

                    if article_state == "B":
                        play_environment.sell(ticker, play_environment.get_curr_hold(ticker))
                # cont = input("would you like to put in another article?Y/N")
                # if cont == "N":
                #     temp_run_state = False
                now = time.time()
                now = int(now / 60.00)
                print(now)
                time_passed = now - then
                if time_passed >= temp_run_time:
                    run2 = False
                    file.close()
        return None

print(thought_driver.default_logic(""))
#print(thought_driver.influenced_logic("AAPL"))