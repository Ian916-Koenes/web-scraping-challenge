from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests 
import time

def init_browswer():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape():
    browser = init_browswer
    mars_data = {}

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    time.sleep(1)

    soup = bs(browser.html, 'html.parser')

    Title = soup.find_all('div', class_= 'content_title')[1].text

    mars_data['news_title'] = Title

    Teaser = soup.find_all('div', class_= 'article_teaser_body')[1].text

    mars_data['news_paragraph'] = Teaser

    url = 'https://www.jpl.nasa.gov/images/?search=&category=Mars'
    browser.visit(url)

    time.sleep(1)

    cards = browser.find_by_css('.BaseImage')
    cards

    [x.text for x in cards]

    cards[0].click()

    soup=bs(browser.html, 'html.parser')

    images=soup.find_all('img', class_='BaseImage')[0]

    featured_images = ['data-src']

    mars_data['featured_image_url'] = featured_images

    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    time.sleep(1)
    
    tables = pd.read_html(url)
    tables
    html_table = tables.to_html()
    html_table
    mars_data['table_url'] = html_table

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    time.sleep(1)

    html = browser.html 
    soup=bs(html,'html.parser')
    main_url = 'https://astrogeology.usgs.gov'
    image_urls = []

    items = soup.find_all('div', class_='item')

    print(items)

    # Loop through the items previously stored
    for item in items:
    # Store title
        title = item.find('h3').text

    # Store link that leads to full image website
        img_url = item.find('a', class_='itemLink product-item')['href']

    # Visit the link that contains the full image website
        browser.visit(main_url + img_url)

        time.sleep(1)

    # HTML Object of individual hemisphere information website
        img_html = browser.html

    # Parse HTML with Beautiful Soup for every individual hemisphere information website
        soup = bs(img_html, 'html.parser')

    # Retrieve full image source
        img_url = main_url + soup.find('img', class_='wide-image')['src']

    # Append the retrieved information into a list of dictionaries
        image_urls.append({"title" : title, "image_url" : img_url})

    mars_data['hemi_image_urls'] = image_urls

    browser.quit()

    return mars_data