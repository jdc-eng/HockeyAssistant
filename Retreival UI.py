import tkinter as ttk
from tkinter import *
from tkinter import ttk
import tkinter as tk
from data_retrieval import *

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()

linespage = tk.StringVar()
rospage = tk.StringVar()
statpage = tk.StringVar()
teamname = tk.StringVar()

home = tk.StringVar(value='h')
away = tk.StringVar(value='v')

def retrieve(state):
    lp = linespage.get()
    rp = rospage.get()
    sp = statpage.get()
    driver = driversetup()
    lineup = getlineup(driver=driver, lp=lp, state=state)
    ros = getroster(driver=driver, rp=rp, Lineup=lineup)
    masterdict = getstats(driver=driver, sp=sp, playerdict=ros[0], masterdict=ros[1])
    final = make_final_df(masterdict=masterdict)
    export(teamname=teamname.get(), final=final)
    driversetup().quit()

# L1 = ttk.Label(root, text="Lines Webpage:").grid(column=0, row=2)
# # L1.pack( side = LEFT)
# E1 = ttk.Entry(root, bd =5).grid(column=1, row=2)
# # E1.pack(side = RIGHT)

linelabel = ttk.Label(frm, text="Lines Webpage: ").grid(column=0, row=0)
lineEntry = ttk.Entry(frm, textvariable=linespage, font=('calibre',10,'normal')).grid(column=1, row=0)

Roslabel = ttk.Label(frm, text="Roster Webpage: ").grid(column=0, row=1)
RosEntry = ttk.Entry(frm, textvariable=rospage, font=('calibre',10,'normal')).grid(column=1, row=1)

StatLabel = ttk.Label(frm, text="Stats Webpage: ").grid(column=0, row=2)
StatEntry = ttk.Entry(frm, textvariable=statpage, font=('calibre',10,'normal')).grid(column=1, row=2)

TeamL = ttk.Label(frm, text="Team Name: ").grid(column=0, row=3)
TeamE = ttk.Entry(frm, textvariable= teamname, font=('calibre',10,'normal')).grid(column=1, row=3)


ttk.Label(frm, text="Was this a home or away game for desired team: ").grid(column=0, row=4)
HomeB = ttk.Button(frm, text="Home", textvariable=home, command=retrieve(state=home)).grid(column=2, row=5)
AwayB = ttk.Button(frm, text="Away", textvariable=away, command=retrieve(state=away)).grid(column=3, row=5)
root.mainloop()


