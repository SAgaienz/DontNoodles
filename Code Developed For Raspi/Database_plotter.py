import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt 
from sqlite3 import Error
import numpy as np
from collections import Counter
from dateutil.parser import parse 
import sys
from os.path import exists
try:

    
    def check_db(db_file):
        file_not_exists = True
        while file_not_exists:
            if exists(db_file):
                file_not_exists = False
                return db_file
            else:
                file_not_exists = True
                print(">>> Database '"+db_file+ "' does not exist. <<<")
                db_file = str(input('- Try another. (full name of database) '))
                file_not_exists = not exists(db_file)
        return db_file

    which_db = check_db(str(input(" - Which Database do you want to peruse? (full name/path of database) ")))
    def create_conn(db_file):
        db_file = check_db(db_file)
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        return conn
            

    def ava_tab_from_db(db_file):

        conn = create_conn(db_file)

        ava_tabs = []
        res = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for name in res:
            ava_tabs.append(name[0])
        return ava_tabs

    def check_tab(db_file):
        ava_tabs = ava_tab_from_db(db_file)
        if len(ava_tabs) == 0 :
            No_tab = True
        else:
            No_tab = False
        while No_tab:
            print(">>> No avaliable table or database does not exist <<<" )
            new_tab = str(input(" - Open new database? (database name if yes, n if no)  "))
            if new_tab == 'n':
                sys.exit()
            else:
                if len(ava_tab_from_db(new_tab)) != 0:
                    No_tab = False
                    db_file = new_tab
        return [ava_tab_from_db(db_file), db_file]

    ava_tabs, which_db = check_tab(which_db)
    print(">>> Available Tables in " + which_db + " <<<")
    print(np.reshape(ava_tabs, (len(ava_tabs), 1))  )
    which_tab = str(input(" - Which table? (give name) "))

    def ava_probes_from_tab(db_file, tab):
        conn = create_conn(db_file)
        cur = conn.cursor()
        cur.execute("SELECT name FROM "+tab)
        cnted_probes = Counter(cur.fetchall())
        ava_probes = []
        for i in cnted_probes:
            ava_probes.append(i[0])
        return np.reshape(ava_probes, (len(ava_probes), 1) )


    print(">>> Available Probes in " + which_tab + " <<<")
    print(ava_probes_from_tab(which_db, which_tab))

    Probe_input_loop = True
    while Probe_input_loop:
        all_probes_str = str(input("- Select all probes to plot? (y/n) "))
        if all_probes_str =='y':
            all_probes = True
            Probe_input_loop = False
            all_probes_str =='y'
        if all_probes_str == 'n':
            all_probes = False
            Probe_input_loop = False
            all_probes_str == 'n'
        else:
            print(">>> Use 'y' or 'n' <<<")
    

    if all_probes:
        probes_to_plt = ['HLT', 'BK', 'AUX', 'MT']
    else:
        custom_input = str(input("- Which Probes? (Give list ie 'HLT, BK, AUX')"))
        probes_to_plt = custom_input.split(',')

    def data_to_plot(db_file, tab, prb_list):
        conn = create_conn(db_file)
        cur = conn.cursor()
        ydata = {}
        for prb in prb_list: # temperature data
            cur.execute("SELECT tem FROM "+tab+" WHERE name=:Id", {"Id": prb})
            T_prb = cur.fetchall()
            Ts = []
            for row in T_prb:
                Ts.append(row[0])
            Tr_prb = np.array(Ts)
            ydata[prb] = Tr_prb
        xdata = {}
        for prb in prb_list: # time data
            cur.execute("SELECT time FROM "+tab+" WHERE name=:Id", {"Id": prb})
            t_prb = cur.fetchall()
            tspan = [parse(t[0]) for t in t_prb]
            ts = []
            for t in tspan:
                dt = t - tspan[0]
                t_sec = dt.total_seconds()
                ts.append(t_sec) 
            xdata[prb] = ts
        return [xdata, ydata]

    def plotter(xdata, ydata): #  takes 2 dictionaries. 1st is times and 2nd is temps. keys are probes
        name_of_plot = str(input('- Name of Plot File? (no spaces) '))
        plot_title = str(input('- Name of Plot Title? '))
        fig = plt.figure(1, figsize = [14, 14])
        for prb in xdata.keys():
            plt.plot(xdata[prb], ydata[prb], label = prb, ls = '-')
        plt.legend(loc = 'best')
        plt.title(plot_title, fontsize = 14)
        plt.xlabel('Time \n seconds', fontsize = 14)
        plt.ylabel('Temperature \n $^ \circ C$', fontsize = 14) 
        plt.tight_layout()
        plt.tick_params(labelsize = 13)
        plt.grid()
        fig.savefig('Figures/Plots_from_Database_plotter_script/'+ name_of_plot, dpi = 300)
        print('Plotted')

    xdata, ydata = data_to_plot(which_db, which_tab, probes_to_plt)
    plotter(xdata, ydata)

except KeyboardInterrupt:
    print("Keyboard Interrupt")


