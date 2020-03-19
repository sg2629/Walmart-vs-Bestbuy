# import necessary library
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
from lxml import html
import sqlalchemy as sqla
import re
from urllib.parse import urljoin
import requests_cache

#print(BeautifulSoup(walmart_req.text,"lxml").prettify())


laptop_url= 'https://www.walmart.com/browse//all-laptop-computers/3944_3951_1089430_132960'
gaming_url='https://www.walmart.com/browse/electronics/gaming-laptops/3944_3951_1089430_1230091_1094888'
touch_url='https://www.walmart.com/browse/electronics/touchscreen-laptops/3944_3951_1089430_1230091_1101633'
twoinone_url='https://www.walmart.com/browse/electronics/2-in-1-laptops/3944_3951_1089430_1230091_1155872'
chromebook_url='https://www.walmart.com/browse/electronics/google-chromebooks/3944_3951_1089430_1230091_1103213'
win10_url='https://www.walmart.com/browse/electronics/windows-10-laptops/3944_3951_1089430_1230457'

def make_walmart_laptop_request(page, base_url):
    """
    Make the request for an etsy page
    :param page: the page number
    :param base_url: the base url - defaults to craft supplies and tools
    :return: beautiful soup object
    """
    par={'page':str(page)}
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    walmart_req = requests.get(base_url,params=par,headers=headers)
    if walmart_req.status_code // 100 != 2:
        return None
    walmart_str=walmart_req.text
    bs_walmart_laptop = BeautifulSoup(walmart_str,'lxml')
    return bs_walmart_laptop

def extract_walmart_laptop_card_info(item):
    link = item.find('a',href= re.compile("^/ip"))['href']
    card_url = urljoin('https://www.walmart.com', link) #url to the page of each item
    card_req = requests.get(card_url)
    card_bs = BeautifulSoup(card_req.text, 'lxml')
    
    #in this new page, scrape useful data
    try:
        title = card_bs.find("h1",class_="prod-ProductTitle font-normal").text.strip() #title of the product
    except AttributeError:
        title = np.nan
    try:
        brand = card_bs.find('span',attrs={'itemprop': 'brand'}).text
    except AttributeError:
        brand = np.nan
    try:
        price=card_bs.find('span',class_="price display-inline-block arrange-fit price")\
        .find('span',class_='visuallyhidden').text.strip('$')
    except AttributeError:
        price = np.nan
    try:
        rating=card_bs.find('span',class_='seo-avg-rating').text
    except AttributeError:
        rating = np.nan
    try:
        review_num=card_bs.find('span',class_='seo-review-count').text
    except AttributeError:
        review_num = np.nan
    try:
        model=card_bs.find('div',attrs={'itemprop': 'model'}).text.strip()
    except AttributeError:
        model = np.nan

    count=0
    i1=999
    i2=999
    i3=999
    i4=999
    i5=999
    i6=999
    i7=999
    i8=999
    for item in card_bs.find('div',attrs={'id':'specifications'}).findAll('td',attrs={'colspan':1}):
        if item.text.strip()=='Operating System':
            i1=count+1

        if item.text.strip()=='Battery Life':
            i2=count+1
        
        if item.text.strip()=='Screen Size':
            i3=count+1
        
        if item.text.strip()=='Assembled Product Dimensions (L x W x H)':
            i4=count+1

        if item.text.strip()=='Processor Type':
            i5=count+1

        if item.text.strip()=='Hard Drive Capacity':
            i6=count+1

        if item.text.strip()=='Processor Speed':
            i7=count+1

        if item.text.strip()=='RAM Memory':
            i8=count+1
    
        count+=1
    try:
        operating_system=card_bs.find('div',attrs={'id':'specifications'}).findAll('td',attrs={'colspan':1})[i1].text.strip()
    except IndexError:
        operating_system = np.nan
    try:
        battery_life=card_bs.find('div',attrs={'id':'specifications'}).findAll('td',attrs={'colspan':1})[i2].text.strip()
    except IndexError:
        battery_life = np.nan
    try:
        screen_size=card_bs.find('div',attrs={'id':'specifications'}).findAll('td',attrs={'colspan':1})[i3].text.strip()
    except IndexError:
        screen_size = np.nan
    try:
        dimensions=card_bs.find('div',attrs={'id':'specifications'}).findAll('td',attrs={'colspan':1})[i4].text.strip()
    except IndexError:
        dimensions = np.nan
        
    try:
        Processor_Type=card_bs.find('div',attrs={'id':'specifications'}).findAll('td',attrs={'colspan':1})[i5].text.strip()
    except IndexError:
        Processor_Type = np.nan

    try:
        Hard_Drive_Capacity=card_bs.find('div',attrs={'id':'specifications'}).findAll('td',attrs={'colspan':1})[i6].text.strip()
    except IndexError:
        Hard_Drive_Capacity= np.nan

    try:
        Processor_Speed=card_bs.find('div',attrs={'id':'specifications'}).findAll('td',attrs={'colspan':1})[i7].text.strip()
    except IndexError:
        Processor_Speed = np.nan

    try:
        RAM_Memory=card_bs.find('div',attrs={'id':'specifications'}).findAll('td',attrs={'colspan':1})[i8].text.strip()
    except IndexError:
        RAM_Memory = np.nan
    return ({"title":title, "brand":brand, "model":model, "price":price, "rating":rating, "review_num":review_num, "operating_system":operating_system, "battery_life":battery_life, "screen_size":screen_size, "dimensions":dimensions,"Hard_Drive_Capacity":Hard_Drive_Capacity, "Processor Type":Processor_Type, "Processor Speed":Processor_Speed, 'RAM Memory':RAM_Memory})

START_PAGE = 1
MAX_PAGE = 1
if __name__=="__main__":
    for page in range(START_PAGE,MAX_PAGE+1):
        print(f"PROCESSING PAGE {page}...")
        walmart_r1 = make_walmart_laptop_request(page,laptop_url)
        walmart_r2 = make_walmart_laptop_request(page,gaming_url)
        walmart_r3 = make_walmart_laptop_request(page,touch_url)
        walmart_r4 = make_walmart_laptop_request(page,twoinone_url)
        walmart_r5 = make_walmart_laptop_request(page,chromebook_url)
        walmart_r6 = make_walmart_laptop_request(page,win10_url)
        cards=pd.DataFrame()

        
        if walmart_r1:
            wt_grid = walmart_r1.findAll('div', class_='search-result-product-title gridview')
            cards1= pd.DataFrame(extract_walmart_laptop_card_info(item) for item in wt_grid )
            cards=cards.append(cards1,ignore_index=True)
        
        if walmart_r2:
            wt_grid = walmart_r2.findAll('div', class_='search-result-product-title gridview')
            cards2= pd.DataFrame(extract_walmart_laptop_card_info(item) for item in wt_grid )
            cards=cards.append(cards2,ignore_index = True)
        if walmart_r3:
            wt_grid = walmart_r3.findAll('div', class_='search-result-product-title gridview')
            cards=cards.append( pd.DataFrame(extract_walmart_laptop_card_info(item) for item in wt_grid ),ignore_index = True)
            
        if walmart_r4:
            wt_grid = walmart_r4.findAll('div', class_='search-result-product-title gridview')
            cards=cards.append( pd.DataFrame(extract_walmart_laptop_card_info(item) for item in wt_grid ),ignore_index = True)
            
        if walmart_r5:
            wt_grid = walmart_r5.findAll('div', class_='search-result-product-title gridview')
            cards=cards.append( pd.DataFrame(extract_walmart_laptop_card_info(item) for item in wt_grid ),ignore_index = True)
            
        if walmart_r6:
            wt_grid = walmart_r6.findAll('div', class_='search-result-product-title gridview')
            cards=cards.append( pd.DataFrame(extract_walmart_laptop_card_info(item) for item in wt_grid ),ignore_index = True)
     
    cards.to_csv(r'../data/walmart_run.csv', index = False, header=True)
    