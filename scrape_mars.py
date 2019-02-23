import time

import requests
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def get_news():
    url = 'https://mars.nasa.gov/news/'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    articles = soup.body.find('div', class_='content_title')
    news_title = articles.find('a').text.strip()
    news_p = soup.body.find('div', class_='rollover_description_inner') \
        .text.strip()
    return (news_title, news_p)


def get_featured_image():
    browser = init_browser()
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find('figure', class_='lede')
    img_partial = temp.find('a')['href']
    featured_image_url = 'https://www.jpl.nasa.gov' + img_partial
    browser.quit()
    return featured_image_url


def get_tweet():
    url = 'https://twitter.com/marswxreport?lang=en'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    tweets = soup.body.find_all('div', class_='tweet')

    for tweet in tweets:
        if tweet.find('span', class_='js-retweet-text'):
            pass
        else:
            actual_tweet = tweet
            break
            
    mars_weather = actual_tweet.find('p', class_='tweet-text').text \
        .split('pic.')[0]
    return mars_weather


def get_table():
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['', 'value']
    df = df.set_index('')
    html_table = df.to_html(classes="table table-striped table-bordered\
        table-hover table-condensed")
    return html_table


def get_hemispheres():
    browser = init_browser()
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    image_divs = soup.find_all('div', class_='item')
    titles = list()
    for image_div in image_divs:
        title_a = image_div.find('a', class_='itemLink')
        title = title_a.find('h3').text
        titles.append(title)
    hemisphere_image_urls = list()
    for title in titles:
        browser.visit(url)
        browser.click_link_by_partial_text(title)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_link = soup.find('img', class_='wide-image')['src']
        img_url = 'https://astrogeology.usgs.gov' + img_link
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})
    browser.quit()
    return hemisphere_image_urls


def scrape():
    news_title, news_p = get_news()
    featured_image_url = get_featured_image()
    mars_weather = get_tweet()
    html_table = get_table()
    hemisphere_image_urls = get_hemispheres()
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "feature_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "html_table": html_table,
        "hemisphere_image_urls": hemisphere_image_urls,
    }
    return mars_data
