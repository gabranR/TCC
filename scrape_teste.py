# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 11:54:39 2022

@author: Gabriel
"""

# Scraping file. So, as I didn't have a script for scraping
# I decided to begin from here, i'll just try to output the same file
# format and data sctruture

## /head ---

# main url: https://www.tripadvisor.com.br/Attractions-g303536-Activities-a_allAttractions.true-Gramado_State_of_Rio_Grande_do_Sul.html



## Imports ----

from bs4 import BeautifulSoup as bs4
import requests
import re
import pandas as pd

# Code -----

## Making soup 
trip = 'https://www.tripadvisor.com.br/Attractions-g303536-Activities-a_allAttractions.true-Gramado_State_of_Rio_Grande_do_Sul.html'

trip_dom = 'https://www.tripadvisor.com.br' #to append on stuff

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'
}


html_request = requests.get(trip, headers = headers).text

soup = bs4(html_request, 'lxml')

## Getting only the interesting tags
main = soup.find_all('div', class_ = 'fVbwn cdAAV cagLQ eZTON dofsx')
main = bs4(str(main), 'lxml')
main = main.find_all('a', href = re.compile(".*\.html$"))
main = bs4(str(main), 'lxml') 

# it doesn't make sense to re-assign to the same variable



#concatenating titles and links
places = []
links = []


for place in main.find_all('div', class_ = 'bUshh o csemS'):
    places.append(re.sub('^(.*?) ', '', place.text))
    


for link in main.find_all('a'):
    links.append(trip_dom + link['href'])

# aparentemente existe um method do pandas que estrutura dados html em df - only works with tables :|

atr_info = dict(zip(places, links))

df_atr_info = pd.Series(atr_info)

print(df_atr_info)

