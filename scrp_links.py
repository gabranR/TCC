# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 11:54:39 2022

@author: Gabriel
"""

# =============================================================================
# This is the scraping implementation using selenium and BeautifulSoup
#
# The steps needed:
# #1 - Acessar a url em trip with pagination
# #2 - MAKE LIST ----
#   1 - Get all links
#   2 - Get all names
#   3 - Get Number of Reviews, Get classification # UPDATE: gave up on this
# 
# #3 - Save all info into a dict or dataframe
# #4 - Filter out shitty attractions or non-attractions
#
#   # PART TWO -------
#
# #5 - Create a function for the review scraper
#   1 - Click:
#       a) Select todos os idiomas
#       b) Paginação
#   2 - Get:
#       a) the link to each profile for the ids
#       b) número de contribuições
#       c) nota (title da tag svg)
#       d) data da avaliação
#       e) data da viagem
#       f) local de origem
#
# #6 - Run the function iterating through the list of selected links
# #7 - Save everything in a dataframe
#
#
# //end code 
#
#
#   # On this version, I am really concerned about memory issues
#
#
# =============================================================================


## /head ---

# main url: https://www.tripadvisor.com.br/Attractions-g303536-Activities-a_allAttractions.true-Gramado_State_of_Rio_Grande_do_Sul.html


## Imports ----


from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd

trip = 'https://www.tripadvisor.com.br/Attractions-g303536-Activities-a_allAttractions.true-Gramado_State_of_Rio_Grande_do_Sul.html'

trip_dom = 'https://www.tripadvisor.com.br' #to append on stuff


## Part 01: Getting the links and selecting the attractions ------------
#

## Part 01: Getting the links and selecting the attractions ------------
#

option = Options()
option.headless = False
with webdriver.Firefox(options=option) as driver:
    driver.get(trip)


    ## Gettiing da cookie --- 

    driver.implicitly_wait(20)

    driver.find_element_by_xpath('//*[@id="onetrust-pc-btn-handler"]').click()
    driver.implicitly_wait(3)
    driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[3]/div[1]/button[1]').click()

    time.sleep(1)

        


    #função para remover os links duplicados
    def remove_dupl(lista):
        return list(dict.fromkeys(lista))





    ##  The scraping function --- 
    # NAVIGATE -> GET HTML -> PARSE -> CLEAN -> SAVE -> REPEAT 


    def get_info():
            element = driver.find_element_by_xpath('/html/body/div[1]/main/span/div/div[3]/div/div[2]/div[2]/span/div/div[2]/div/div[2]/div/div')
            html = element.get_attribute('outerHTML')
            soup = BeautifulSoup(html, 'lxml')
            # ---
            links = soup.find_all('a', href = re.compile("^\/Attraction_Review.*\.html$"))
            nomes = soup.find_all('div', class_ = 'bUshh o csemS')
            main_div = soup.find_all('div', class_ = 'eLWnh P0')

            # getting only the formatted links and attraction's names
            a = []
            b = []
            c = []
            d = []
            e = []
            for i in range(len(links)):
                a.append(trip_dom + links[i]['href'])
            a = remove_dupl(a)
            for j in nomes:
                b.append(re.sub('^(.*?) ', '', j.text))
            for k in main_div:
                temp = k.find('span', class_ = 'WlYyy diXIH bGusc bQCoY')
                if temp is None:
                    c.append(0)
                else:
                    c.append(int(re.sub('\.', '', temp.text)))
            for z in main_div:
                d.append(re.sub('\•', '', z.find('div', class_ = 'WlYyy diXIH fPixj').text))
            for y in main_div:
                temp = y.find('div', class_ =  'WlYyy fSDPY fPixj')
                if temp is None:
                    e.append('Aberto')
                else:
                    e.append(temp.text)
            
            # make the two lists into a dictionary
            temp_dict = {'Atrativos': b, 'Links': a, 'Num_avaliacoes': c, 'Categorias': d, 'Status': e}
            
            return temp_dict


        ## Function to do the pagination and consolidate the data of each page
    def the_whole_thing():
        #temp variables
        a = []
        b = []
        c = []
        d = []
        e = []
        # That's a ugly method, I know, but it gets the lists out of get_info(), extends them, and click next page
        for s in range(10):
            info = get_info()
            a.extend(info['Atrativos'])
            b.extend(info['Links'])
            c.extend(info['Num_avaliacoes'])
            d.extend(info['Categorias'])
            e.extend(info['Status'])
            driver.find_element_by_xpath('/html/body/div[1]/main/span/div/div[3]/div/div[2]/div[2]/span/div/div[2]/div/div[2]/div/div/section[39]/span/div[1]/div/div[1]/div[2]/div/a').click()
            #check out alternatives for this time.sleep, maybe explicity wait idk
            time.sleep(8)
        # save as a DataFrame
        df = pd.DataFrame.from_dict({'Atrativos': a, 'Links': b, 'Num_avaliacoes': c, 'Categorias': d, 'Status': e})
        return df


    df_sujo = the_whole_thing()



## Part 02: Selecting only relevant atractions (FILTERING)--------------------
#
del_list = ['Excursões', 'Passeios', 'Academias', 'estádios', 'Aulas', 'Táxis', 'Passeios turísticos', 'Locação']


for i in del_list:
    df_sujo = df_sujo[~df_sujo['Categorias'].str.contains(i, case = False, regex = True)]

df_limpo = df_sujo
df_limpo = df_limpo[df_limpo['Num_avaliacoes'] > 20]



# Writing it to a file ------



df_limpo.to_csv('data/atrat_links.csv')



# MY WORK HERE IS DONE --- just clean this file a bit and git it









































    # ## Byebye ---






