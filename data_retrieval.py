from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
import pandas as pd
from bs4 import BeautifulSoup
import re
from time import sleep

if __name__ == '__main__':
    print('Dont use this module by itself cause it dont work properly')

def driversetup():
    '''Set up the driver for the browser for selenium'''
    driver = webdriver.Edge(options=EdgeOptions())
    return driver


def getlineup(driver, lp, state):
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(lp)  # webpage get request
    # driver.get("https://www.uscho.com/gameday/division-i-men/2021-2022/2022-01-31/game-1674/")
    # driver.get('https://www.uscho.com/gameday/division-i-men/2021-2022/2022-01-29/game-1721/')

    driver.implicitly_wait(0.5)

    # this line finds and clicks on the lines part of the table to turn the aria-hidden to false and we can get the data#
    driver.find_element(By.XPATH, '//*[@id="lilines"]').click()
    sleep(1)

    '''Page gives the new lines page to beautiful soup for parsing. table use BS to find the visitors lineup table and returns it as a tabele'''
    page = BeautifulSoup(driver.page_source, 'html.parser')
    table = page.find_all(id=r'linestable' + state)[0]

    '''ptab Turns the table into a panda dataframe for 'easier' manipulation. lines Is the dataframe now as a list of lists'''
    ptab = pd.read_html(str(table))[0]
    lines = ptab.values.tolist()
    # print(lines)
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
            result.append(re.sub(r'[^a-zA-Z0-9\s]', '', re.sub(r'\s+', ' ', string=re.sub(r'[^a-zA-Z0-9]', ' ', re.split(':', e)[-1].strip()))))

        lineup.append(result)

    '''This turns the new lineup list of lists back into a panda df. then it is exported to a csv file'''
    Lineup = pd.DataFrame(lineup)
    print(Lineup)

    return Lineup


def getroster(driver, rp, Lineup):
    driver.get(rp)
    # driver.get('https://cornellbigred.com/sports/mens-ice-hockey/roster')
    # driver.get('https://gobobcats.com/sports/mens-ice-hockey/roster')

    ros = BeautifulSoup(driver.page_source, 'html.parser').find_all('div', class_='sidearm-roster-player-pertinents flex-item-1 column')

    roster = []

    for player in ros:
        # namelist = player.contents[3].contents[4].text.split()
        # roster.append(namelist[0].strip() + " " + namelist[1].strip())
        roster.append(re.sub(r'[^a-zA-Z0-9\s]', '', re.sub(r'\s+', ' ', string=player.contents[3].contents[4].text).strip()))
        # print(re.sub(r'[^a-zA-Z0-9]', ' ', player.contents[3].contents[4].text).strip())

    playerdict = {}
    masterdict = {}
    numbers = []
    print("checking for active players")
    for line in Lineup.itertuples(index=False):
        for skater in line[1:]:

            try:
                spot = roster.index(re.sub(r'\s+', ' ', re.sub(r'[^a-zA-Z0-9]', ' ', skater)))
            except:
                print("Player not found in roster: " + str(skater))

            try:
                hand = ros[spot].contents[1].contents[-2].text.strip()
            except:
                print('No player hand found.')
                continue

            try:
                number = ros[spot].contents[3].contents[1].text.strip()
                numbers.append(number)
                # print('Skater: '+skater+'. Hand: '+hand+'. Number: '+number+'.')
            except:
                print('Wrong index for number. Number not found')
                continue
            playerdict[number] = skater
            masterdict[skater] = [number, hand, '']
    return [playerdict, masterdict]


def getstats(driver, sp, playerdict, masterdict):
    driver.get(sp)
    # driver.get('https://cornellbigred.com/sports/mens-ice-hockey/stats')

    driver.find_element(By.XPATH, '//*[@id="main-content"]/article/div[3]/header/div/ul/li[2]').click()

    stattab = BeautifulSoup(driver.page_source, 'html.parser').find_all(id='DataTables_Table_0')[0]

    ptab2 = pd.read_html(str(stattab), header=None)[0]

    jerseys = ptab2['#'][0:-3].values.tolist()

    plusminus = {}
    for num in jerseys:
        if num[0] in playerdict:
            pmin = ptab2.loc[(ptab2['#'] == num[0]).iloc[:, 0]]['Shots']['+/-'].values[0]
            plusminus[num[0]] = pmin
            masterdict[playerdict[num[0]]][2] = pmin
    return masterdict


'''you left off here. need to finish making the functions for this shit. figure out references and what you should make functions. need a masterdict function?'''


def make_final_df(masterdict, lineup):
    guys = lineup.values.tolist()
    Stuff = []
    for thing in guys:
        result = [thing[0]]
        for name in thing[1:]:
            result.append(['', masterdict[name][0], [name, masterdict[name][2]], masterdict[name][1]])
        Stuff.append(result)
        Stuff.append(['', '', '', ''])

    last = pd.DataFrame(Stuff)
    final = pd.DataFrame()

    for column in last.columns[1:]:
        # print(pd.DataFrame(last[column].tolist()))
        col = pd.DataFrame(last[column].tolist()).explode(2).reset_index(drop=True)
        final = pd.concat([final, col], axis=1)

    return final

def export(teamname, final):
    return final.to_csv(path_or_buf=str(teamname) + '.csv', index=False, header=False)

# need to quit the shit
driversetup().quit()
