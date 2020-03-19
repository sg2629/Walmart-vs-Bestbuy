# import necessary library
import pandas as pd
import numpy as np
import string
from bs4 import BeautifulSoup
import requests
from lxml import html
import sqlalchemy
import re
from urllib.parse import urljoin
import sqlite3
import requests_cache
from sklearn import feature_extraction, decomposition, cluster

#laptop pages
START_PAGE = 1
MAX_PAGE = 1
#agent header
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
#laptop base url
laptop_base_url = 'https://www.bestbuy.com/site/laptop-computers/all-laptops/pcmcat138500050001.c'


def make_bestbuy_base_request(page,base_url,bestbuy_par):
    """
    Make the request for bestbuy base page
    :param page: the page number
    :param base_url: the base url
    :return: beautiful soup object
    """
    #bestbuy_par = {'cp':str(page),'id':'pcmcat138500050001'}
    bestbuy_req = requests.get(base_url,params = bestbuy_par,headers = headers)
    if bestbuy_req.status_code // 100 != 2:
        return None
    bs = BeautifulSoup(bestbuy_req.text,'lxml')
    return(bs)

def find_all_link(bs):
    """
    On bestbuy base page, find all laptop pages
    :param bs: beautiful soup object of base page
    """
    card_link = bs.findAll('div', class_='information')
    ls = []
    for link in card_link:
        #print('.',end=' ')
        if link.find('div',class_='pl-flex-carousel-slider'):
            link_sub=link.find('div',class_='pl-flex-carousel-slider').find_all('a',href = re.compile('^https'))
            ls_sub = [link2['href'] for link2 in link_sub]
            ls.extend(ls_sub)
        else:
            link2 = link.find('a',href= re.compile("^/site"))
            card_url = urljoin('https://www.bestbuy.com', link2['href'])
            ls.extend([card_url])
    return(ls)

def extract_card_info(link,kind):
    """
    Make the request for bestbuy laptop page
    :param link: for each item
    """
    #link2 = link.find('a',href= re.compile("^/site"))
    #card_url = urljoin('https://www.bestbuy.com', link2['href']) #url to the page of each item
    card_url = link
    card_req = requests.get(card_url,headers = headers)
    card_bs = BeautifulSoup(card_req.text, 'lxml')
    
    #in this new page, scrape useful data
    title = card_bs.find("h1",class_="heading-5 v-fw-regular").text.strip() #title of the product
    try:
        value = card_bs.find('div',class_='pricing-price pricing-lib-price-7-2010-3 priceView-price')\
        .find('div',class_='priceView-hero-price priceView-customer-price')\
        .find('span',attrs = {'aria-hidden':'true'}).text.split('$')[1]
    except AttributeError:
        value = np.nan
    
    color = title.split(' - ')[-1]
    
    try:
        review_rating = card_bs.find('span',class_='overall-rating').text.strip()
    except AttributeError:
        review_rating = np.nan
        
    try:
        review_no = card_bs.find('div',class_='ugc-rating-stars-v2 clearfix')\
        .find('span',attrs={'aria-hidden':"true",'class':"c-total-reviews"}).text.split()[0].split('(')[1]
    except AttributeError:
        review_no = np.nan    
    
    try:
        model = card_bs.find_all('span',class_='product-data-value body-copy')
        if len(model)== 0:
            model = np.nan
        else:
            model = card_bs.find_all('span',class_='product-data-value body-copy')[0].text.strip()
    except AttributeError:
        model = np.nan  
        
    basic = {'title':title,'price':value,'category':kind,'color':color,'review rating':review_rating,'review number':review_no,'model':model}
    
    tabkeys = [row.text.strip() for row in card_bs.find_all(class_='row-title')]
    tabvalues = [row.text.strip() for row in card_bs.find_all(class_='row-value col-xs-6 v-fw-regular')]
    specification = {k: v for k, v in zip(tabkeys,tabvalues)}
    speclist = ['Screen Size','Touch Screen','Storage Type','Total Storage Capacity','Hard Drive Capacity',\
                'System Memory (RAM)','Processor Speed (Base)','Processor Model','Operating System',\
                'Battery Life','Brand','Product Height','Product Width','Product Depth','Product Weight']
    for spec in speclist:
        try:
            basic[spec] = specification[spec]
        except:
            basic[spec] = np.nan
    print('.',end=' ')
    return(basic)


if __name__=="__main__":
    
    Laptop =pd.DataFrame()
    for page in range(START_PAGE,MAX_PAGE+1):
        print(f"PROCESSING PAGE {page}:",end='')
        bestbuy_r1 = make_bestbuy_base_request(page,laptop_base_url,{'cp':str(page),'id':'pcmcat138500050001'})
        if bestbuy_r1:
            laptop = pd.DataFrame(extract_card_info(link,'laptop') for link in find_all_link(bestbuy_r1))
            Laptop=Laptop.append(laptop,ignore_index=True)
        print(f"PAGE {page} DONE!")
    Laptop.to_csv(r'../data/bestbuy_run.csv', index = False, header=True)