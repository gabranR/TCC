from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd

data = pd.read_csv('data/atrat_links.csv')
links = data['Links']
nomes_atr = data['Atrativos']
#just saving this here for better readability
nxt_css_select = '.cCnaz > div:nth-child(1) > a:nth-child(1) > svg:nth-child(1)'

## Part 01: Getting the links and selecting the attractions ------------
#
option = Options()
option.headless = True
driver = webdriver.Firefox(options=option)


## Gettiing da cookie... the smart way --- 
driver.get(links[57])
time.sleep(3)
driver.implicitly_wait(10)
driver.find_element_by_xpath('//*[@id="onetrust-pc-btn-handler"]').click()
time.sleep(1)
driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[3]/div[1]/button[1]').click()

time.sleep(1)

# click in 'all languagesss'

driver.find_element_by_xpath('/html/body/div[1]/main/div[1]/div[3]/div[2]/div/div/span/section[8]/div/div/span/section/section/div[1]/div/div[1]/span/div/div[2]/div/div/span[2]/span/div/div/button').click()
time.sleep(2)                
driver.find_element_by_xpath('//*[@id="menu-item-all"]').click()
time.sleep(1)

##uhhhh so fancy using classes... OOP uhhh =======
# The ideia here is to create a commom set of attributes that can be used by the methods, and then I can create objects requesting specific tags

class main:
    def __init__(self, dict_):
        self.dict = dict_
    # Just a function to return false when there is no 'next' button anymore
    def stop_pag(self):
        temp = bool(driver.find_elements_by_css_selector(nxt_css_select))
        return temp
    

    ## Função para encontrar *os elementos*, salvar o html, parsear o html e retornar uma lista com o texto do elemento
    # no momento suporta texto e href, mas caso precise de outra informação é só incluir mais um elif

    # for every element in elements I should locate, parse and copy ALL the info i'll need
    def find_them(self):
        elements = driver.find_elements_by_css_selector('div.ffbzW')
        a = []
        b = []
        #df = pd.DataFrame({'User_ID': [], 'Data': []})
        for element in elements:
            html = element.get_attribute('innerHTML')
            soup = BeautifulSoup(html, 'lxml')
            a.append(soup.find(self.dict['user_id']['tag'], self.dict['user_id']['class'])['href'])
            temp = soup.find(self.dict['date']['tag'], self.dict['date']['class'])
            b.append(temp.text if temp else 'NA')

        #df = pd.concat( objs = [df, pd.DataFrame([a, b])])
        #print(len(a))
        print('Completed Successifuri')
        return [a, b]


    ## A METHOD TO RULE THEM ALL =====
    # This method creates the iteration of the action of clicking on the next button, and also extends the list - consolidates - all info
    def give_me_info(self):
        temp = [[], []]
        while self.stop_pag():
            temp2 = self.find_them()
            temp[0].extend(temp2[0])
            temp[1].extend(temp2[1])
            #print(len(temp))
            driver.find_element_by_css_selector(nxt_css_select).click()
            time.sleep(2)
        else:
            temp3 = self.find_them()
            temp[0].extend(temp3[0])
            temp[1].extend(temp3[1])
        
        df = pd.DataFrame(data = {'User_ID': temp[0], 'Data': temp[1]})
        df.to_csv('data/info_test.csv', mode = 'a', index = False)
        print('We\'ve reached the last page')

    def quit_():
        driver.quit()
