from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions
from bs4 import BeautifulSoup

from selenium.webdriver.support.ui import WebDriverWait


driver = webdriver.Edge(options=EdgeOptions())

# driver.get('https://www.eliteprospects.com/team/1551/princeton-univ.' + '?sort=jersey')

driver.get('https://www.eliteprospects.com/team/1551/princeton-univ.'+'?tab=stats#players')

stattab = BeautifulSoup(driver.page_source, 'html.parser').find('table', class_='table table-striped table-sortable '
                                                                                'skater-stats '
                                                                                'highlight-stats').find_all('tr', class_= None)
#get table of player stats. The class_=None arg on the last find_all skips the spaces in the table, bc the actual
# player rows dont have any classes associated to them

# print(stattab[3].contents[5].contents[1].text)
for player in stattab[1:]:
    print(player.contents[17].text)   #pm location
    print(player.contents[5].contents[1].text)   #name location

driver.quit()


