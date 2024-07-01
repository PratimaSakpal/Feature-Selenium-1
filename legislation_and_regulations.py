"""
Description: Script to crawl data from Legislation and regulations using selenium.
"""
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import re
import pandas as pd


LINK = "https://www.kyberturvallisuuskeskus.fi/fi/saadokset-ohjeistukset-suositukset?group=kyberturvallisuus&limit=100&offset=0&query=&sort=created&toggle=Laki%20vahvasta%20s%C3%A4hk%C3%B6isest%C3%A4%20tunnistamisesta%20ja%20s%C3%A4hk%C3%B6isist%C3%A4%20luottamuspalveluista"

def get_request(link):
    """
    Description: Method to get response from link
    Input: link (string)
    Output: driver (selenium object)
    """
    driver = webdriver.Chrome()
    driver.get(link)
    return driver

def get_soup(driver):
    """
    Description: Method to get soup uning BeautifulSoup
    Input: driver (selenium object)
    Output: driver (Object)
    """
    soup = bs(driver.page_source, features="html.parser")
    return soup

def get_data(soup):
    """
    Description: Method to get extract data
    Input: soup (BeautifulSoup object)
    Output: None
    """
    all_data = soup.findAll('div', {'class': 'ContainerItem__StyledContainerItem-sc-1uad7iv-0 jQyLxJ'})
    final_list = []
    for data in all_data:
        dict_ = {}
        
        title = data.find('div', {'class':'styles__HeaderContent-mvlj9n-2 cISWwJ'})
        if title:
            dict_['Tital'] = title.text

        pdf_link = data.find('li', {'class':'LinkList__ListItem-qw7u8g-2 jDSvNT'})
        if pdf_link:
            dict_['PDF Link'] = 'https://www.kyberturvallisuuskeskus.fi/' + pdf_link.find('a').get('href')

        abstract = data.find('div', {'class': 'Paragraph__StyledSection-sc-1rk24tr-0 jQqNbo'})
        if abstract:
            dict_['Astract'] = abstract.text
            
        teaser_num = data.find('p', {'class':'Teaser__Number-fs59s7-1 ea-dAqi'})
        if teaser_num:
            dict_['Teaser Number'] = teaser_num.text
            
        teaser_valid_date = data.find('p', {'class':'Teaser__ValidFrom-fs59s7-2 gNZDUa'})
        if teaser_valid_date:
            check_date = re.search(r'\d{2}\.\d{2}\.\d{4}', teaser_valid_date.text)
            if check_date:
                dict_['Effective date'] = check_date.group()
        final_list.append(dict_)
    data_frame = pd.DataFrame(final_list)
    compression_config = dict(method='zip', archive_name='Extracted_Data.csv')
    data_frame.to_csv('Extracted_Data.zip',compression=compression_config)

def main():
    driver = get_request(LINK)
    soup = get_soup(driver)
    get_data(soup)
    driver.close()

if __name__ == '__main__':
    main()
