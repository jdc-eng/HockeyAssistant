from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions
from bs4 import BeautifulSoup

from selenium.webdriver.support.ui import WebDriverWait


driver = webdriver.Edge(options=EdgeOptions())

# driver.get('https://www.eliteprospects.com/team/1551/princeton-univ.' + '?sort=jersey')
# driver.find_element(By.CSS_SELECTOR, '#players > nav > ul > li:nth-child(2) > a').click()
driver.get('https://www.eliteprospects.com/team/1551/princeton-univ.'+'?tab=stats#players')
# driver.refresh()

# webdriver.ActionChains(driver).pause(5)
# WebDriverWait(driver).until()

stattab = BeautifulSoup(driver.page_source, 'html.parser').find('table', class_='table table-striped table-sortable skater-stats highlight-stats').find_all('tr') #get table of player stats
##stattab only gets the firs table, ie the first ten players, why?
for player in stattab[2:]:
    print(player.contents[17].text)   #pm location
    print(player.contents[5].contents[1].text)   #name location
    # print('')

driver.quit()






