import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

def getTweets(page):
    ready = ""
    settings = Options()
    settings.headless = True
    driver = webdriver.Firefox(options=settings)
    driver.get(page)
    while ready != "complete":
        time.sleep(1)
        ready = driver.execute_script("return document.readyState")
    tweets = driver.find_elements(By.CLASS_NAME, 'tweet-content')
    return tweets

#runs sentiment analysis on the tweets. Takes the json data, then updates it with
#the average daily and overall sentiments, and the most negative and positive tweets of the day
def sendTweetData(tweets):
    low = 1
    high = -1
    total = 0
    anal = SentimentIntensityAnalyzer()
    tweetData = {}
    count = 0
    for tweet in tweets:
        score = anal.polarity_scores(tweet.text)
        comp = score['compound']
        total += comp
        #checks if the tweet's score is highest or lowest of day
        if comp < low:
            tweetData['low'] = {
                'post': tweet.text,
                'neg': score['neg'],
                'pos': score['pos'],
                'neu': score['neu'],
                'comp': comp
            }
            low = comp
        
        if comp > high:
            tweetData['high'] = {
                'post': tweet.text,
                'neg': score['neg'],
                'pos': score['pos'],
                'neu': score['neu'],
                'comp': comp
            }
            high = comp
        count += 1
    
    trend = open('dataTrends.json')    
    data = json.load(trend)
    temp = round(float(total)/count,2)
    data['todayAvgSentiment'] = temp
    data['days'] = data['days'] + 1
    temp = round((data['totalAvgSentiment'] + temp)/data['days'], 2)
    data['totalAvgSentiment'] = temp
    data['high'] = tweetData['high']
    data['low'] = tweetData['low']
    with open('dataTrends.json', "w") as f:     
        json.dump(data, f, indent = 6)

def getPrice(page):
    ready = ""
    settings = Options()
    settings.headless = True
    driver = webdriver.Firefox(options=settings)
    driver.get(page)
    while ready != "complete":
        time.sleep(1)
        ready = driver.execute_script("return document.readyState")
    price = driver.find_element(By.XPATH, "/html/body/div[2]/main/section/section/section/article/section[1]/div[2]/div[1]/section/div/section/div[1]/div[3]/span")
    price = float(price.text.strip("+, (, ), %"))
    return price

def sendPriceData(price):
    trend = open('dataTrends.json')
    data = json.load(trend)
    data['totalPriceChange'] = data['totalPriceChange'] + price
    data['todayPriceChange'] = price
    with open('dataTrends.json', "w") as f:
        json.dump(data, f, indent = 6)

tweets = getTweets("https://xcancel.com/elonmusk")
sendTweetData(tweets)
price = getPrice("https://finance.yahoo.com/quote/TSLA/")
sendPriceData(price)
