
from tkinter import *
from tkinter import ttk
import tkinter as tk
from data_retrieval import *

#create the tk shit
root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
root.title('Hockey Data Assistant')

#store all the necessary the webpage links
linespage = tk.StringVar()
rospage = tk.StringVar()
statpage = tk.StringVar()
teamname = tk.StringVar()

#this is used to pass in home or away game into the function. for selecting proper table from lines page
home = tk.StringVar(value='h').get()
away = tk.StringVar(value='v').get()

def retrieve(state):
    lp = linespage.get()
    rp = rospage.get()
    sp = statpage.get()
    driver = driversetup()
    lineup = getlineup(driver=driver, lp=lp, state=state)
    ros = getroster(driver=driver, rp=rp, Lineup=lineup)
    masterdict = getstats(driver=driver, sp=sp, playerdict=ros[0], masterdict=ros[1])
    final = make_final_df(masterdict=masterdict, lineup=lineup)
    export(teamname=teamname.get(), final=final)
    driversetup().quit()
    root.quit()

#make all the buttons, inputs etc
linelabel = ttk.Label(frm, text="Lines Webpage: ").grid(column=0, row=0)
lineEntry = ttk.Entry(frm, textvariable=linespage, font=('calibre',10,'normal')).grid(column=1, row=0)

Roslabel = ttk.Label(frm, text="Roster Webpage: ").grid(column=0, row=1)
RosEntry = ttk.Entry(frm, textvariable=rospage, font=('calibre',10,'normal')).grid(column=1, row=1)

StatLabel = ttk.Label(frm, text="Stats Webpage: ").grid(column=0, row=2)
StatEntry = ttk.Entry(frm, textvariable=statpage, font=('calibre',10,'normal')).grid(column=1, row=2)

TeamL = ttk.Label(frm, text="Team Name: ").grid(column=0, row=3)
TeamE = ttk.Entry(frm, textvariable= teamname, font=('calibre',10,'normal')).grid(column=1, row=3)

ttk.Label(frm, text="Was this a home or away game for desired team: ").grid(column=0, row=4)
HomeB = ttk.Button(frm, text="Home", command=lambda : retrieve(state=home)).grid(column=2, row=5)
AwayB = ttk.Button(frm, text="Away", command=lambda : retrieve(state=away)).grid(column=3, row=5)

root.mainloop()
