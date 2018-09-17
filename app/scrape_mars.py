
import os
from bs4 import BeautifulSoup as bs
from splinter.exceptions import ElementDoesNotExist
from splinter import Browser
from selenium import webdriver
import re
import pandas as pd


def scrape_all():


#executable_path = {"C:\\Users\\Jeff\\Documents\\BootCamp\\HW\\HW13\\Resources\\chromedriver.exe": 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'}
    executable_path = {'executable_path': "C:\\Users\\Jeff\\Documents\\BootCamp\\HW\\HW13\\Resources\\chromedriver.exe"}
    browser = Browser('chrome', **executable_path,headless=False)
    news_title, news_paragraph = mars_news(browser)
    featured_image_url,featured_image_desc = featured_image(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image,
        "featured_image_desc":featured_image_desc,
        "weather": twitter_weather(browser),
        "hemispheres": hemispheres(browser),
        "facts": mars_facts(browser),
    }
    browser.quit()
    return data

def mars_news(browser):

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    titles_body = soup.find('ul',class_='item_list')
    news_title = titles_body.find('div', class_ = "content_title").get_text()
    news_p = titles_body.find('div', class_='article_teaser_body').get_text()
        
    return news_title, news_p



def featured_image(browser):

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)


    html = browser.html
    soup = bs(html, 'html.parser')
    footer_body = soup.find('footer')
    footer_desc = footer_body.find('a', class_='button fancybox')
    featured_image_desc = footer_desc['data-description']

    featured_button=soup.find("a", {"id": "full_image"})
    #featured_button


    str_fb = str(featured_button)

    img_string = re.findall(r'data-fancybox-href="(.*?)" data-title',str_fb)
    print(img_string)
    string_form_of_link = ''.join(img_string)
    featured_image_url = ('https://www.jpl.nasa.gov' + string_form_of_link)
    #print(featured_image_url)

    return featured_image_url, featured_image_desc


def twitter_weather(browser):
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    recent_tweet_info = soup.find('p', class_='TweetTextSize')
    recent_tweet = recent_tweet_info.text.strip()
    #print(recent_tweet)
    return recent_tweet

def mars_facts(browser):

    url = 'http://space-facts.com/mars/'
    browser.visit(url)


    html = browser.html
    soup=bs(html,'html.parser')


    mf_list = []
    mf_equatorial_diameter = []
    mf_polar_diameter = []
    mf_mass = []
    mf_moons = []
    mf_orbit_distance = []
    mf_orbit_period = []
    mf_surface_temperature = []
    mf_first_record = []
    mf_recorded_by = []


    # mf_pd = pd.DataFrame(columns=['Equatorial Diameter','Polar Diameter', 'Mass', 'Moons', 'Orbit Distance','Orbit Period', 'Surface Temperature', 'First Record', 'Recorded By'])
    mf_pd = pd.DataFrame(columns=['Description','Value'])
    mf_desc_list = ['Equatorial Diameter','Polar Diameter', 'Mass', 'Moons', 'Orbit Distance','Orbit Period', 'Surface Temperature', 'First Record', 'Recorded By']


    table_body = soup.find('table', id='tablepress-mars')
    table_body2 = table_body.find_all('tr')

    for row in table_body.findAll('tr'):
        cells = row.findAll('td')
        info = cells[1].text.strip()
        mf_list.append(info)
        
    # mf_list


    mf_pd['Description']=mf_desc_list
    mf_pd['Value']=mf_list
    # mf_pd

    html_mf_pd = mf_pd.to_html()
    return mf_pd.to_html(classes = "table table-striped")


def hemispheres(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_url = 'https://astrogeology.usgs.gov'
    browser.visit(url)

    html = browser.html
    soup=bs(html,'html.parser')

    hemisphere_image_urls = []

    hemisphere_links = []
    item_body = soup.find('div', class_='collapsible results')
    item_link = item_body.findAll('div', class_='item')

    for links in item_link:
        for link in links.find_all('a', text=True):
            link2 = link.get('href')
            hemisphere_links.append(link2)
        
    # hemisphere_links 


    for link in range(len(hemisphere_links)):
        hemisphere_dict = {}
        new_url = base_url+hemisphere_links[link]
        browser.visit(new_url)
        sample_img= browser.find_link_by_text('Sample').first
        hemisphere_dict['img_url'] = sample_img['href']
        
        html = browser.html
        soup = bs(html,'html.parser')
        title=soup.find('h2', class_='title').text.strip()
        hemisphere_dict['title'] = title
        hemisphere_image_urls.append(hemisphere_dict)
        browser.visit(url)    
        
    # hemisphere_image_urls

    return hemisphere_dict


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
