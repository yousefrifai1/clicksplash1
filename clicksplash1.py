
#======================
# imports
#======================
import tkinter as tk
from tkinter import ttk
import tkinter
from tkinter import messagebox
import sys
import sqlite3 as lite
#sys.path.append("C:\\Users\\user\\Documents\\Yousef\\ClickSplash_1\\procedures_defs")
#import Procedures as pd

# Create instance
win = tk.Tk()

# Add a title
win.title("ClickSplash 1")
# Tab Control introduced here -----------------------------------------
tabControl = ttk.Notebook(win)          # Create Tab Control

tab1 = ttk.Frame(tabControl)            # Create a tab
tabControl.add(tab1, text='Drops')      # Add the tab

tab2 = ttk.Frame(tabControl)            # Add a second tab
tabControl.add(tab2, text='Loops')      # Make second tab visible

tab3 = ttk.Frame(tabControl)            # Add a second tab
tabControl.add(tab3, text='Save & Load')      # Make second tab visible

tabControl.pack(expand=1, fill="both")  # Pack to make visible
# ~ Tab Control introduced here -----------------------------------------

droptab = ttk.LabelFrame(tab1, text=' Drops parameters ')
droptab.grid(column=0, row=0, padx=8, pady=4)

incrtab = ttk.LabelFrame(tab2, text=' Increments parameters ')
incrtab.grid(column=0, row=0, padx=8, pady=4)

# Modify adding a Label
dropsLable = ttk.Label(droptab, text="Number of Drops")
dropsLable.grid(column=0, row=0)

# Drops
for col in range(4):
    dropLable = ttk.Label(droptab, text="Drop " + str(col+1) + " Duration (ms): ")
    dropLable.grid(column=0, row=col+1)
    incrLable = ttk.Label(incrtab, text="Drop " + str(col+1) + " Duration increment (ms): ")
    incrLable.grid(column=0, row=col+1)
    delayLable = ttk.Label(droptab, text="Delay after drop " + str(col+1) + " (ms): ")
    delayLable.grid(column=2, row=col+1, padx=10)
    delayLable = ttk.Label(incrtab, text="Delay after drop " + str(col+1) + " increment(ms): ")
    delayLable.grid(column=2, row=col+1, padx=10)

# Loops lable
incrLable = ttk.Label(incrtab, text="Number of loops: ")
incrLable.grid(column=0, row=6, sticky=tk.W)
incrLable = ttk.Label(incrtab, text="Delay after loop (s): ")
incrLable.grid(column=2, row=6, sticky=tk.W, padx=10 )

# Modified Button Click Functions
# Sql function
def create_tables():
    con = lite.connect('clicksplashdb.db')
    with con:   
        cur = con.cursor()
        create_inputtab = """CREATE TABLE IF NOT EXISTS inputtab(
                                 tag TEXT,
                                 drop1duration REAL,
                                 drop1delay REAL,
                                 drop2duration REAL,
                                 drop2delay REAL,
                                 drop3duration REAL,
                                 drop3delay REAL,
                                 drop4duration REAL,
                                 drop4delay REAL,
                                 drop1inc REAL,
                                 delay1inc REAL,
                                 drop2inc REAL,
                                 delay2inc REAL,
                                 drop3inc REAL,
                                 delay3inc REAL,
                                 drop4inc REAL,
                                 delay4inc REAL,
                                 loops INT,
                                 delay_loops REAL,
                                 comments TEXT
                             ); """        
        cur.execute(create_inputtab)
        create_outputtab = """CREATE TABLE IF NOT EXISTS outputtab(
                                 photo TEXT,
                                 drop1duration REAL,
                                 drop1delay REAL,
                                 drop2duration REAL,
                                 drop2delay REAL,
                                 drop3duration REAL,
                                 drop3delay REAL,
                                 drop4duration REAL,
                                 drop4delay REAL,
                                 comments TEXT
                             ); """
        cur.execute(create_outputtab)
def get_check_float( i):
    try:
        return( float(i))
    except ValueError:
        return( -1)
    
def get_save_data():
    # declare and initialise variables
    global v_drop1duration
    global v_delay1duration
    global v_drop1inc
    global v_delay1inc
    global v_drop2duration
    global v_delay2duration
    global v_drop2inc
    global v_delay2inc
    global v_drop3duration
    global v_delay3duration
    global v_drop3inc
    global v_delay3inc
    global v_drop4duration
    global v_delay4duration
    global v_drop4inc
    global v_delay4inc

    v_drop1duration = 0
    v_delay1duration = 0
    v_drop1inc = 0
    v_delay1inc = 0
    v_drop2duration = 0
    v_delay2duration = 0
    v_drop2inc = 0
    v_delay2inc = 0
    v_drop3duration = 0
    v_delay3duration = 0
    v_drop3inc = 0
    v_delay3inc = 0
    v_drop4duration = 0
    v_delay4duration = 0
    v_drop4inc = 0
    v_delay4inc = 0    
    
    x = get_check_float( drop1duration.get())
    if( x == -1):
        messagebox.showerror("Error", "Please enter a valid number in Drop 1 Duration")
        drop1entry.focus_set()
        return     
    x = get_check_float( delay1duration.get())
    if( x == -1):
        messagebox.showerror("Error", "Please enter a valid number in delay after drop 1")
        delay1entry.focus_set()
        return
    if(radSel < 2):
        return   
    x = get_check_float( drop2duration.get())
    if( x == -1):
        messagebox.showerror("Error", "Please enter a valid number in Drop 2 Duration")
        drop2entry.focus_set()
        return
    
    x = get_check_float( delay2duration.get())
    if( x == -1):
        messagebox.showerror("Error", "Please enter a valid number in delay after drop 2")
        delay2entry.focus_set()
        return
    if(radSel < 3):
        return   

        #cur.execute("INSERT INTO Cars VALUES(1,'Audi',52642)")
def clickMe():
    create_tables()
    get_save_data()
    
# Adding water drop duration

drop1duration = tk.StringVar()
drop1entry = ttk.Entry(droptab, width=5, textvariable=drop1duration, )
drop1entry.grid(column=1, row=1)

drop1inc = tk.StringVar()
drop1inc_entry = ttk.Entry(incrtab, width=5, textvariable=drop1inc)
drop1inc_entry.grid(column=1, row=1)
#----
drop2duration = tk.StringVar()
drop2entry = ttk.Entry(droptab, width=5, textvariable=drop2duration)
drop2entry.grid(column=1, row=2)

drop2inc = tk.StringVar()
drop2inc_entry = ttk.Entry(incrtab, width=5, textvariable=drop2inc)
drop2inc_entry.grid(column=1, row=2)
#-----
drop3duration = tk.StringVar()
drop3entry = ttk.Entry(droptab, width=5, textvariable=drop3duration)
drop3entry.grid(column=1, row=3)

drop3inc = tk.StringVar()
drop3inc_entry = ttk.Entry(incrtab, width=5, textvariable=drop3inc)
drop3inc_entry.grid(column=1, row=3)
#-----
drop4duration = tk.StringVar()
drop4entry = ttk.Entry(droptab, width=5, textvariable=drop4duration)
drop4entry.grid(column=1, row=4)

drop4inc = tk.StringVar()
drop4inc_entry = ttk.Entry(incrtab, width=5, textvariable=drop4inc)
drop4inc_entry.grid(column=1, row=4)
#-----
# Adding delay duration
delay1duration = tk.StringVar()
delay1entry = ttk.Entry(droptab, width=5, textvariable=delay1duration)
delay1entry.grid(column=3, row=1)

delay1inc_duration = tk.StringVar()
delay1inc_entry = ttk.Entry(incrtab, width=5, textvariable=delay1inc_duration)
delay1inc_entry.grid(column=3, row=1)

delay2duration = tk.StringVar()
delay2entry = ttk.Entry(droptab, width=5, textvariable=delay2duration)
delay2entry.grid(column=3, row=2)

delay2inc_duration = tk.StringVar()
delay2inc_entry = ttk.Entry(incrtab, width=5, textvariable=delay2inc_duration)
delay2inc_entry.grid(column=3, row=2)

delay3duration = tk.StringVar()
delay3entry = ttk.Entry(droptab, width=5, textvariable=delay3duration)
delay3entry.grid(column=3, row=3)

delay3inc_duration = tk.StringVar()
delay3inc_entry = ttk.Entry(incrtab, width=5, textvariable=delay3inc_duration)
delay3inc_entry.grid(column=3, row=3)

delay4duration = tk.StringVar()
delay4entry = ttk.Entry(droptab, width=5, textvariable=delay4duration)
delay4entry.grid(column=3, row=4)

delay4inc_duration = tk.StringVar()
delay4inc_entry = ttk.Entry(incrtab, width=5, textvariable=delay4inc_duration)
delay4inc_entry.grid(column=3, row=4)


# The processing buttons
action = ttk.Button(droptab, text="Start Process", command=clickMe)
action.grid(column=0, row=6, sticky=tk.W)
action.configure(state='disabled')    # Disable the Button Widget
action1 = ttk.Button(incrtab, text="Start Process", command=clickMe)
action1.grid(column=0, row=7, sticky=tk.W)
action1.configure(state='disabled')    # Disable the Button Widget

# Add loops entry
loops_value = tk.StringVar()
loops_entry = ttk.Entry(incrtab, width=5, textvariable=loops_value)
loops_entry.grid(column=1, row=6)
loops_value.set("1")
delay_loop = tk.StringVar()
delay_loop_entry = ttk.Entry(incrtab, width=5, textvariable=delay_loop)
delay_loop_entry.grid(column=3, row=6)
delay_loop.set("0")

radVar = tk.IntVar()

def radCall():
    action.configure(state='normal')
    action1.configure(state='normal')            
    global radSel
    radSel=radVar.get()	
    if  radSel == 1:
	# Drops
        drop2entry.configure(state='disabled')
        drop3entry.configure(state='disabled')
        drop4entry.configure(state='disabled')
        
        drop2inc_entry.configure(state='disabled')
        drop3inc_entry.configure(state='disabled')
        drop4inc_entry.configure(state='disabled')        
	# Delays
        delay2entry.configure(state='disabled')
        delay3entry.configure(state='disabled')
        delay4entry.configure(state='disabled')

        delay2inc_entry.configure(state='disabled')
        delay3inc_entry.configure(state='disabled')
        delay4inc_entry.configure(state='disabled')
    elif radSel == 2:
	# Drops
        drop2entry.configure(state='normal')
        drop3entry.configure(state='disabled')
        drop4entry.configure(state='disabled')
        
        drop2inc_entry.configure(state='normal')
        drop3inc_entry.configure(state='disabled')
        drop4inc_entry.configure(state='disabled')       
	# Delay
        delay2entry.configure(state='normal')
        delay3entry.configure(state='disabled')
        delay4entry.configure(state='disabled')
        
        delay2inc_entry.configure(state='normal')
        delay3inc_entry.configure(state='disabled')
        delay4inc_entry.configure(state='disabled')        
    elif radSel == 3:
        drop2entry.configure(state='normal')
        drop3entry.configure(state='normal')
        drop4entry.configure(state='disabled')
        
        drop2inc_entry.configure(state='normal')
        drop3inc_entry.configure(state='normal')
        drop4inc_entry.configure(state='disabled')        
	# Delay
        delay2entry.configure(state='normal')
        delay3entry.configure(state='normal')
        delay4entry.configure(state='disabled')

        delay2inc_entry.configure(state='normal')
        delay3inc_entry.configure(state='normal')
        delay4inc_entry.configure(state='disabled')	        
    elif radSel == 4:
        drop2entry.configure(state='normal')
        drop3entry.configure(state='normal')
        drop4entry.configure(state='normal')

        drop2inc_entry.configure(state='normal')
        drop3inc_entry.configure(state='normal')
        drop4inc_entry.configure(state='normal')        
	# Delay
        delay2entry.configure(state='normal')
        delay3entry.configure(state='normal')
        delay4entry.configure(state='normal')
        
        delay2inc_entry.configure(state='normal')
        delay3inc_entry.configure(state='normal')
        delay4inc_entry.configure(state='normal')        

tk.Label(droptab, text="Number of Drops:").grid(column=0, row=0)
# create 4 Radiobuttons using one variable

rad1 = tk.Radiobutton(droptab, text="1", variable=radVar, value=1, command=radCall)
rad1.grid(column=1, row=0)   
rad2 = tk.Radiobutton(droptab, text="2", variable=radVar, value=2, command=radCall)
rad2.grid(column=2, row=0)   
rad3 = tk.Radiobutton(droptab, text="3", variable=radVar, value=3, command=radCall)
rad3.grid(column=3, row=0)
rad4 = tk.Radiobutton(droptab, text="4", variable=radVar, value=4, command=radCall)
rad4.grid(column=4, row=0)

   
#======================
# Start GUI
#======================
win.mainloop()
