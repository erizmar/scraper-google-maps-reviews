# -*- coding: utf-8 -*-
from googlemaps import GoogleMapsScraper
from datetime import datetime, timedelta
import argparse
import re
import time

def go(command, url, iteration):
    n = 0
    pagination = 100
    sort_by = command
    
    url = re.sub('2i10', '2i' + str(pagination), url)
    url = re.sub('3e1', '3e' + str(sort_by), url)

    if iteration < args.N:
        iteration = args.N

    while n < iteration:
        url = re.sub('1i' + str(n-100), '1i' + str(n), url)

        print("N = " + str(n))
        error = scraper.open_web(url)
        if error == 0:
            n += pagination

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Google Maps reviews scraper.')
    parser.add_argument('--i', type=str, default='durls.txt', help='target URLs file')
    parser.add_argument('--N', type=int, default=100, help='Number of reviews to scrape')
    parser.add_argument('--S', type=int, default=5, help='Choose sort by, 1-Relevance 2-Newest 3-Highest Rating 4-Lowest Rating 5-Loop All')
    parser.add_argument('--debug', dest='debug', action='store_true', help='Run scraper using browser graphical interface')
    parser.set_defaults(place=False, debug=False, source=False)

    args = parser.parse_args()

    # with GoogleMapsScraper(debug=args.debug) as scraper:
    #     with open(args.i, 'r') as urls_file:

    #         n = 0
    #         pagination = 100
    #         sort_by = args.S

    #         while n < args.N:    
    #             url = "https://www.google.com/maps/preview/review/listentitiesreviews?authuser=0&hl=id&gl=id&pb=!1m2!1y3303385645568173453!2y7918460690842932799!2m2!1i"+str(n)+"!2i"+str(pagination)+"!3e"+str(sort_by)+"!4m5!3b1!4b1!5b1!6b1!7b1!5m2!1sbkv5X6rBD-GbmgfA47DQCQ!7e81"

    #             if args.place:
    #                 print(scraper.get_account(url))
    #             else:
    #                 print("N = " + str(n))
    #                 error = scraper.open_web(url)
    #                 if error == 0:
    #                     n += 100

    with GoogleMapsScraper(debug=args.debug) as scraper:
        t = re.sub(':', '-', str(datetime.now()))
        wait = 10
        with open(args.i, 'r') as urls_file, open("logs/dlogs - " + t + ".txt", 'w') as log_file:
            for line in urls_file:
                line_split = line.split(',')

                url = line_split[0]
                iteration = int(line_split[1])
                name = re.sub('\n', '', line_split[2])

                message = "\nStarted scraping " + name + " at: " + str(datetime.now())
                log_file.write(message)
                print(message)

                if args.S == 5:
                    s = 1
                    wait = 120
                    while s < args.S:
                        message = "\nSort by " + str(s) + " is started at: " + str(datetime.now())
                        log_file.write(message)
                        print(message)

                        go(s, url, iteration)

                        message = "\nSort by " + str(s) + " is ended at: " + str(datetime.now())
                        log_file.write(message)
                        print(message)

                        time.sleep(10)
                        s += 1
                else:
                    go(args.S, url, iteration)
                
                message = "\nFinished scraping " + name + " at: " + str(datetime.now())
                log_file.write(message)
                print(message)

                time.sleep(wait)
