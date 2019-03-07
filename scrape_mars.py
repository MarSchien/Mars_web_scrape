# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pymongo
import pandas as pd
import time


    # # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    # return Browser("chrome", **executable_path, headless=False)


def scrape():
    

    url_1 = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'


    response = requests.get(url_1)
    soup = BeautifulSoup(response.text, 'html.parser')

    latest_news_title = soup.find('div', class_="content_title").a.text.strip()
    latest_news_paragraph = soup.find('div', class_="rollover_description_inner").text.strip()       




    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    
    url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_2)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    first_image = soup.find('img', class_="main_image")['src']
    
    root_url = 'https://www.jpl.nasa.gov'
    featured_image_url = root_url + str(first_image)




    url_3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text




    url_4 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url_4)
    df = tables[0]

    df.columns=['Measurement', 'Value']
    df.set_index('Measurement', inplace=True)
    table_html = df.to_html().replace('\n','')

    data = {} 

    data['latest_news_title'] = latest_news_title
    data['latest_news_paragraph'] = latest_news_paragraph
    data['latest_image'] = featured_image_url
    data['mars_weather'] = mars_weather
    data['table'] = table_html

    return data
