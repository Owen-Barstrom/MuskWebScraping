from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def getTweets(page):
    ready = ""
    driver = webdriver.Firefox()
    driver.get(page)
    while ready != "complete":
        print("Loading...")
        time.sleep(1)
        ready = driver.execute_script("return document.readyState")
    tweets = driver.find_elements(By.CLASS_NAME, 'tweet-content')
    return tweets

def calcScore(tweets):
    anal = SentimentIntensityAnalyzer()
    for tweet in tweets:
        text = tweet.text
        score = anal.polarity_scores(text)
        neg = score['neg']
        pos = score['pos']
        neu = score['neu']
        
tweets = getTweets("https://xcancel.com/elonmusk")
calcScore(tweets)