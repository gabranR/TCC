## Part 03: Scaling the scraper to get the actual reviews  ------------
#
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
# ==============================================

# Imports -----------

from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd

data = pd.read_csv('data/atrat_links.csv')
links = data['Links']
cookie_page = 'https://www.tripadvisor.com.br/'

#just saving this here for better readability since is constant
nxt_css_select = '.cCnaz > div:nth-child(1) > a:nth-child(1) > svg:nth-child(1)'

## Part 01: Getting the links and selecting the attractions ------------
#

option = Options()
option.headless = False
with  webdriver.Firefox(options=option) as driver:


    ## Gettiing da cookie... the smart way --- 
    driver.get(links[41])
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('//*[@id="onetrust-pc-btn-handler"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[3]/div[1]/button[1]').click()

    time.sleep(1)

    # click in 'all languagesss'

    driver.find_element_by_xpath('/html/body/div[1]/main/div[1]/div[2]/div[2]/div/div/span/section[8]/div/div/span/section/section/div[1]/div/div[1]/div/div[2]/div/div/span[2]/span/div/div/button').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="menu-item-all"]').click()
    time.sleep(5)



    ##uhhhh so fancy using classes... OOP uhhh =======
    # The ideia here is to create a commom set of attributes that can be used by the methods, and then I can create objects requesting specific tags

    class Scraper:
        #making the constructor, those are all the parameters I need to navigate and get one info at a time
        def __init__(self, element_css, soup_tag, soup_class, soup_attr):
            self.element_css = element_css
            self.soup_tag = soup_tag
            self.soup_class  = soup_class
            self.soup_attr = soup_attr
        # Just a function to return false when there is no 'next' button anymore
        def stop_pag(self):
            temp = bool(driver.find_elements_by_css_selector(nxt_css_select))
            return temp

        ## Função para encontrar *os elementos*, salvar o html, parsear o html e retornar uma lista com o texto do elemento
        # no momento suporta texto e href, mas caso precise de outra informação é só incluir mais um elif
        def find_each(self):
            lista = []
            element = driver.find_elements_by_css_selector(self.element_css)
            if self.soup_attr == 'href':
                for i in element:
                    html = i.get_attribute('innerHTML')
                    soup = BeautifulSoup(html, 'lxml')
                    lista.append(soup.find(self.soup_tag, self.soup_class)['href'])
            elif self.soup_attr == 'text':
                for i in element:
                    html = i.get_attribute('innerHTML')
                    soup = BeautifulSoup(html, 'lxml')
                    lista.append(soup.find(self.soup_tag, self.soup_class).text)
            else:
                raise ValueError("Você passou o argumento errado, soup_attr recebe 'href' ou 'text'.")
            return lista
        ## A METHOD TO RULE THEM ALL =====
        # This method creates the iteration of the action of clicking on the next button, and also extends the list - consolidates - all info
        def give_me_info(self):
            aa = []    
            while self.stop_pag():
                aa.extend(self.find_each())
                driver.find_element_by_css_selector(nxt_css_select).click()
                time.sleep(2)
            else:
                aa.extend(self.find_each())
            return aa    

    ## Creating the objects with the specific selectors, tags and etc to be called later with the give_me_info function
    user_id = Scraper(
        element_css = '.dHjBB span span[data-ft]',
        soup_tag = 'a',
        soup_class = 'iPqaD _F G- ddFHE eKwUx btBEK fUpii',
        soup_attr = 'href' 
    )

    bb = user_id.give_me_info()
    bb = [re.sub('\/Profile\/', '', i) for i in bb]



print(len(bb))







