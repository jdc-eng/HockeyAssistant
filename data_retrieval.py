import bs4.dammit
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import element_to_be_clickable as Clickable
from selenium.webdriver.support.expected_conditions import visibility_of_element_located as Visible

from lxml import etree
import pandas as pd
from bs4 import BeautifulSoup
import re
import unidecode
from time import sleep

if __name__ == '__main__':
    print('Dont use this module by itself cause it dont work properly')


def driversetup():
    '''Set up the driver for the browser for selenium'''
    # options = webdriver.ChromeOptions()
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # driver = webdriver.Chrome(options=options)
    #
    driver = webdriver.Edge(options=EdgeOptions())
    return driver


def getlineup(driver, lp, state):
    # driver.get(lp)  # webpage get request
    driver.get('https://www.uscho.com/gameday/division-i-men/2021-2022/2022-02-26/game-1697/')
    driver.implicitly_wait(0.5)

    # this line finds and clicks on the lines part of the table to turn the aria-hidden to false and we can get the data#
    driver.find_element(By.XPATH, '//*[@id="lilines"]').click()

    '''Page gives the new lines page to beautiful soup for parsing. table use BS to find the visitors lineup table and returns it as a tabele'''
    page = BeautifulSoup(driver.page_source, 'html.parser')
    table = page.find_all(id=r'linestable' + state)[0]

    '''ptab Turns the table into a panda dataframe for 'easier' manipulation. lines Is the dataframe now as a list of lists'''
    ptab = pd.read_html(str(table))[0]
    lines = ptab.values.tolist()

    '''This block until the end of the loop does a few things, and it does not do them well.
    The loop iterates over the lines list-of-lists that was the ptab dataframe; each line is a line.
    It then appends each element (player) of the line into the result list, then appends an empty element twice to create a visual seperation.
    After this new line has been created, it is appended to the lineup list, with three more lists consisting of empty shit for more visual seperation.
    I would like to find a way to just add  columns and rows into the panda df, hopefully it has some built in shit. Or at least get a better way of doing it manually.
    or hope nobody gives a fuck that it looks like shit.
    '''
    lineup = []
    for line in lines:
        result = []
        for e in line:
            #this regex stuff basically remones non-alpha numeric, then gets rid of any extra spaces from the players name and then adds it into the lineup
            result.append(re.sub(r'\s+', ' ', string=re.sub(r'[^a-zA-Z0-9\s]', '', string=unidecode.unidecode(re.split(':', e)[-1].strip()))))

        lineup.append(result)

    #This turns the new lineup list of lists back into a panda df. then it is exported to a csv file
    Lineup = pd.DataFrame(lineup)

    return Lineup


def getroster(driver, rp, Lineup):
    # driver.get(rp) #get request for the roster webpage
    driver.get('https://www.eliteprospects.com/team/1551/princeton-univ.'+'?sort=jersey')
    # Select(driver.find_element(By.XPATH, '//*[@id="sidearm-roster-select-template-dropdown"]')).select_by_visible_text('Roster View - List')
    # driver.find_element(By.XPATH, '//*[@id="roster"]/div/div[3]/table/thead/tr/th[2]/a').click() #clicks the number thing to sort by jersey num, really to get everyone in one table

    ros = BeautifulSoup(driver.page_source, 'html.parser').find('table', class_='table table-striped table-sortable roster').find('tbody').find_all('tr') #this gets the actual players in a list
    # print(ros)
    roster = []
    playerdict = []
    for player in ros:
        # this loop/line appends the names of the players that are in the ros player list from the webpage lineup IF AND ONLY IF they are in the lineup DataFrame.
        # This is done because i havent yet looked into a way of searching for a specific string in the ros type list, and if that is good for actually getting the hand data
        # The regex line is funky, basically it removes/sub first all of the non alphanumeric characters from the name, and that is passed into another sub to replace any extra spaces with a single space
        shortened = re.sub(r'\s+', ' ', string=re.sub(r'[^a-zA-Z0-9\s]', '', string=unidecode.unidecode(player.contents[7].contents[1].text.strip())))
        playerdict.append(shortened)
        name = ''
        for thing in shortened.split()[0:-1]:
            name = name+' '+thing
        roster.append(name.strip().lower())
    # playerdict and masterdict are used for the plus/minus. because the plus minus is gotten by iterating over a table with the numbers and the final thig is made with the number as the dict key, there needs to be a dictionary of number to name to add the plus minus. see line 11 2
    #     print(player.contents[3].contents[0])

    masterdict = {}
    numbers = []
    # print("checking for active players")
    for line in Lineup.itertuples(index=False):
        for skater in line[1:]:

            try:
                spot = roster.index(re.sub(r'\s+', ' ', re.sub(r'[^a-zA-Z0-9\s]', '', unidecode.unidecode(skater).lower())))
            except:
                print("Player not found in roster: " + str(skater))

            try:
                hand = ros[spot].contents[19].contents[-1].text.strip()
            except:
                print('No player hand found.')
                continue

            try:
                number = re.sub(r'[^a-zA-Z0-9\s]', '', string=ros[spot].contents[3].contents[0].text.strip())
                print(number)
                numbers.append(number)
            except:
                print('Wrong index for number. Number not found')
                continue
            # playerdict[number] = skater
            masterdict[skater] = [number, hand, '']
    # print(playerdict)

    # WebDriverWait(driver, 20).until(Clickable((By.XPATH, '//*[@id="players"]/nav/ul/li[2]/a')))
    driver.get('https://www.eliteprospects.com/team/1551/princeton-univ.' + '?sort=jersey')
    driver.find_element(By.XPATH, '//*[@id="players"]/nav/ul/li[2]/a').click()
    driver.implicitly_wait(5)
    # webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    driver.find_element(By.XPATH, '//*[@id="dismiss-button"]/div/svg/path[1]').click()
    driver.find_element(By.XPATH, '//*[@id="dismiss-button"]/div/svg')
    stattab = BeautifulSoup(driver.page_source, 'html.parser').find_all('div', id='players')  # extract the table

    print(stattab)
    sleep(20)
    return [playerdict, masterdict]


def getstats(driver, sp, playerdict, masterdict):
    # driver.get(sp) #driver init
    # driver.get()
    # driver.find_element(By.XPATH, '//*[@id="players"]/nav/ul/li[2]/a').click() #click on the individua button for player stats

    stattab = BeautifulSoup(driver.page_source, 'html.parser').find('table', _class='table table-striped table-sortable skater-stats highlight-stats') #extract the table

    # ptab2 = pd.read_html(str(stattab), header=None)[0]  #this line gets all the plus minuses
    # print(ptab2)
    # jerseys = ptab2['#'][0:-3].to_numpy().astype(dtype=int).astype(dtype=str).tolist() #make a list of all the jersey numbers on the website
    # print(jerseys)
    print(stattab)

    # for player in playerdict:
    #     if player in playerdict:
    #         # loop through all the jersey nums in the stats table, and only get the plus minus if it is inn the player dictionary
    #         pmin = ptab2.loc[(ptab2['#'] == num[0]).iloc[:, 0]]['Shots']['+/-'].to_numpy()
    #         masterdict[playerdict[num[0]]][2] = pmin # change the plus minus in the master dict to the players plus minus using the number as a key in playerdict to get their name, and pass that into masterdict to add the plus minus of the player
    #         # print(pmin)
    return masterdict

def make_final_df(masterdict, lineup):
    guys = lineup.values.tolist()
    Stuff = []
    for thing in guys:
        result = [thing[0]]
        for name in thing[1:]:
            result.append(['', masterdict[name][0], [name, masterdict[name][2]], masterdict[name][1]]) #creates a single players entry into the final df
        Stuff.append(result)
        Stuff.append(['', '', '', '']) #creates empty columns between the names; for pretty

    last = pd.DataFrame(Stuff) #this is used to store the card with almost final formating except for the plus minus explode; used df to make use of pandas good stuff
    final = pd.DataFrame() #empty dataframe for adding the finished column dfs to. will be what is returned to the user

    for column in last.columns[1:]:
        col = pd.DataFrame(last[column].tolist()).explode(2).reset_index(drop=True) # iterates over the three player columns and explodes the name column with the plus minus into new df. this is an entire player column, eg column 2
        final = pd.concat([final, col], axis=1) #concat each of above line to final

    return final

def export(teamname, final):
    return final.to_csv(path_or_buf=str(teamname) + '.csv', index=False, header=False, ) #export

# need to quit the shit
driversetup().quit()
