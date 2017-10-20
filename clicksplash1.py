
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
tabControl.add(tab3, text='Save & Open')      # Make second tab visible

tabControl.pack(expand=1, fill="both")  # Pack to make visible
# ~ Tab Control introduced here -----------------------------------------

droptab = ttk.LabelFrame(tab1, text=' Drops parameters ')
droptab.grid(column=0, row=0, padx=8, pady=4)

incrtab = ttk.LabelFrame(tab2, text=' Increments parameters ')
incrtab.grid(column=0, row=0, padx=8, pady=4)

savetab = ttk.LabelFrame(tab3, text=' Save')
savetab.grid(column=0, row=0, padx=8, pady=4)
opentab = ttk.LabelFrame(tab3, text=' Open ')
opentab.grid(column=0, row=1, padx=8, pady=4, sticky=tk.W)

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
# Save Lables
save_nameLable = ttk.Label(savetab, text="Name of Loop to save:")
save_nameLable.grid(column=0, row=1,sticky=tk.W)
save_nameLable = ttk.Label(savetab, text="Comment to save with the loop:")
save_nameLable.grid(column=0, row=2,sticky=tk.W)

# Open Labels
openDB_Lable = ttk.Label(opentab, text="Name of Database to open:")
openDB_Lable.grid(column=0, row=1,sticky=tk.W)

# Loops lable
incrLable = ttk.Label(incrtab, text="Number of loops: ")
incrLable.grid(column=0, row=6, sticky=tk.W)
incrLable = ttk.Label(incrtab, text="Delay after loop (s): ")
incrLable.grid(column=2, row=6, sticky=tk.W, padx=10 )
incrLable = ttk.Label(incrtab, text="Photo Number: ")
incrLable.grid(column=0, row=7, sticky=tk.W)

# Modified Button Click Functions
# Sql function
def create_tables():
    con = lite.connect(v_db_name)
    with con:   
        cur = con.cursor()
        create_inputtab = """CREATE TABLE IF NOT EXISTS inputtab(
                                 name TEXT PRIMERY KEY UNIQUE,
                                 photo INT,
                                 drop1duration REAL,
                                 drop1delay REAL,
                                 drop1inc REAL,                               
                                 delay1inc REAL,                                 
                                 drop2duration REAL,
                                 drop2delay REAL,
                                 drop2inc REAL,
                                 delay2inc REAL,                                 
                                 drop3duration REAL,
                                 drop3delay REAL,
                                 drop3inc REAL,
                                 delay3inc REAL,                                 
                                 drop4duration REAL,                                
                                 drop4delay REAL,
                                 drop4inc REAL,
                                 delay4inc REAL,
                                 loops INT,
                                 loop_delay INT,                                 
                                 comments TEXT
                             ); """        
        cur.execute(create_inputtab)
        create_outputtab = """CREATE TABLE IF NOT EXISTS outputtab(
                                 photo INT,
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
    
def get_check_int( i):
    try:
        return( int(i))
    except ValueError:
        return( -1)
    
def get_save_data():
    # declare and initialise variables

    global v_save_name
    global v_photo_number
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
    global v_loops
    global v_loop_delay
    global v_save_comment
    global v_db_name


    # Get save name and comment
    v_save_name = save_name.get()
    if( v_save_name == ''):
        messagebox.showerror("Error", "The save name cannot be empty")
        loops_entry.focus_set()
        return
    v_db_name = db_name.get()
    if( v_db_name == ''):
        messagebox.showerror("Error", "The database name cannot be empty")
        db_name_entry.focus_set()
        return
    v_db_name = v_db_name + ".db"
    
    v_save_comment = save_comment.get()
    
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
# Get Loops data
    x = get_check_int(loops_value.get())
    if( x < 1):
        messagebox.showerror("Error", "Please enter a valid number larger than 0 for loops")
        loops_entry.focus_set()
        return
    v_loops = x
    x = get_check_int(delay_loop.get())
    if( x < 0 ):
        messagebox.showerror("Error", "Please enter a valid number larger than 0 for loop delay")
        delay_loop_entry.focus_set()
        return
    v_loop_delay = x
    
# Get photo_number data
    x = get_check_int(photo_number_value.get())
    if( x < 1):
        messagebox.showerror("Error", "Please enter a valid positive number for photo_number")
        photo_number_entry.focus_set()
        return
    v_photo_number = x    
# First drop data    
    x = get_check_float( drop1duration.get())
    if( x == -1):
        messagebox.showerror("Error", "Please enter a valid number in Drop 1 Duration")
        drop1entry.focus_set()
        return
    v_drop1duration = x
    
    x = get_check_float( delay1duration.get())
    if( x == -1):
        messagebox.showerror("Error", "Please enter a valid number in delay after drop 1")
        delay1entry.focus_set()
        return
    v_delay1duration = x

    if( v_loops > 1):  
        x = get_check_float( drop1inc.get())
        if( x == -1):
            messagebox.showerror("Error", "Please enter a valid number in Drop 1 increment")
            drop1inc_entry.focus_set()
            return
        v_drop1inc = x
        
        x = get_check_float( delay1inc_duration.get())
        if( x == -1):
            messagebox.showerror("Error", "Please enter a valid number in delay after drop 1 increment")
            delay1inc_entry.focus_set()
            return
        v_delay1inc = x   
    if(radSel < 2):
        return   
# Second drop data    
    x = get_check_float( drop2duration.get())
    if( x == -1):
        messagebox.showerror("Error", "Please enter a valid number in Drop 2 Duration")
        drop2entry.focus_set()
        return
    v_drop2duration = x
    
    x = get_check_float( delay2duration.get())
    if( x == -1):
        messagebox.showerror("Error", "Please enter a valid number in delay after drop 2")
        delay2entry.focus_set()
        return
    v_delay2duration = x

    if( v_loops > 1):  
        x = get_check_float( drop2inc.get())
        if( x == -1):
            messagebox.showerror("Error", "Please enter a valid number in Drop 2 increment")
            drop2inc_entry.focus_set()
            return
        v_drop2inc = x
        
        x = get_check_float( delay2inc_duration.get())
        if( x == -1):
            messagebox.showerror("Error", "Please enter a valid number in delay after drop 2 increment")
            delay2inc_entry.focus_set()
            return
        v_delay2inc = x   
    if(radSel < 3):
        return
# Third drop data    
    x = get_check_float( drop3duration.get())
    if( x == -1):
        messagebox.showerror("Error", "Please enter a valid number in Drop 3 Duration")
        drop3entry.focus_set()
        return
    v_drop3duration = x
    
    x = get_check_float( delay3duration.get())
    if( x == -1):
        messagebox.showerror("Error", "Please enter a valid number in delay after drop 3")
        delay3entry.focus_set()
        return
    v_delay3duration = x

    if( v_loops > 1):  
        x = get_check_float( drop3inc.get())
        if( x == -1):
            messagebox.showerror("Error", "Please enter a valid number in Drop 3 increment")
            drop3inc_entry.focus_set()
            return
        v_drop3inc = x
        
        x = get_check_float( delay3inc_duration.get())
        if( x == -1):
            messagebox.showerror("Error", "Please enter a valid number in delay after drop 3 increment")
            delay3inc_entry.focus_set()
            return
        v_delay3inc = x   
    if(radSel < 4):
        return
# Forth drop data    
    x = get_check_float( drop4duration.get())
    if( x == -1):
        messagebox.showerror("Error", "Please enter a valid number in Drop 4 Duration")
        drop4entry.focus_set()
        return
    v_drop4duration = x
    
    x = get_check_float( delay4duration.get())
    if( x == -1):
        messagebox.showerror("Error", "Please enter a valid number in delay after drop 4")
        delay4entry.focus_set()
        return
    v_delay4duration = x

    if( v_loops > 1):  
        x = get_check_float( drop4inc.get())
        if( x == -1):
            messagebox.showerror("Error", "Please enter a valid number in Drop 4 increment")
            drop4inc_entry.focus_set()
            return
        v_drop4inc = x
        
        x = get_check_float( delay4inc_duration.get())
        if( x == -1):
            messagebox.showerror("Error", "Please enter a valid number in delay after drop 4 increment")
            delay4inc_entry.focus_set()
            return
        v_delay4inc = x

# Insert loop information in the database.
def save_loop():
    global v_inputtab_data    
    inputtab_data = (
        v_save_name,
        v_photo_number,
        v_drop1duration,
        v_delay1duration,
        v_drop1inc,
        v_delay1inc,
        v_drop2duration,
        v_delay2duration,
        v_drop2inc,
        v_delay2inc,
        v_drop3duration,
        v_delay3duration,
        v_drop3inc,
        v_delay3inc,
        v_drop4duration,
        v_delay4duration,
        v_drop4inc,
        v_delay4inc,
        v_loops,
        v_loop_delay,
        v_save_comment
    )
    statement = """ INSERT INTO inputtab VALUES( ?,?,?,?,?, ?,?,?,?,?, ?,?,?,?,?, ?,?,?,?,?, ?)"""
    con = lite.connect('clicksplashdb.db')
    with con:   
        cur = con.cursor()
        cur.execute(statement, inputtab_data)
    
def process_input():
    global v_next_photo
    global v_next_drop1duration
    global v_next_drop1delay
    global v_next_drop2duration
    global v_next_drop2delay
    global v_next_drop3duration
    global v_next_drop3delay
    global v_next_drop4duration
    global v_next_drop4delay
    global v_next_comments

    v_next_photo = v_photo_number
    v_next_drop1duration = v_drop1duration
    v_next_drop1delay = v_delay1duration
    v_next_drop2duration = v_drop2duration
    v_next_drop2delay = v_delay2duration
    v_next_drop3duration = v_drop3duration
    v_next_drop3delay = v_delay3duration
    v_next_drop4duration = v_drop4duration
    v_next_drop4delay = v_delay4duration
    v_next_comments = ""
    insert_output()
    for seq in range(2, v_loops ):
        v_next_photo = v_next_photo +1
        v_next_drop1duration = v_next_drop1duration + v_drop1inc
        v_next_drop1delay = v_next_drop1delay + v_delay1inc
        if (radSel > 1):
            v_next_drop2duration = v_next_drop2duration + v_drop2inc
            v_next_drop2delay = v_next_drop2delay + v_delay2inc
        if (radSel > 2):
            v_next_drop3duration = v_next_drop3duration + v_drop3inc
            v_next_drop3delay = v_next_drop3delay + v_delay3inc            
        if (radSel > 3):
            v_next_drop4duration = v_next_drop4duration + v_drop4inc
            v_next_drop4delay = v_next_drop4delay + v_delay4inc
        insert_output()    
        
def insert_output():
    outputtab_data = (
        v_next_photo ,
        v_next_drop1duration ,
        v_next_drop1delay  ,
        v_next_drop2duration ,
        v_next_drop2delay  ,
        v_next_drop3duration ,
        v_next_drop3delay ,
        v_next_drop4duration ,
        v_next_drop4delay ,
        v_next_comments 
        )
    statement = """ INSERT INTO outputtab VALUES( ?,?,?,?,?, ?,?,?,?,?)"""
    con = lite.connect('clicksplashdb.db')
    with con:   
        cur = con.cursor()
        cur.execute(statement, outputtab_data)
    
def clickMe():
    get_save_data()    
    create_tables()
    save_loop()
    process_input()

    
# Adding water drop duration

drop1duration = tk.StringVar()
drop1entry = ttk.Entry(droptab, width=5, textvariable=drop1duration)
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

# Save entries
save_name = tk.StringVar()
save_name_entry = ttk.Entry(savetab, width=25, textvariable=save_name)
save_name_entry.grid(column=1, row=1, sticky=tk.W)

save_comment = tk.StringVar()
save_comment_entry = ttk.Entry(savetab, width=35, textvariable=save_comment)
save_comment_entry.grid(column=1, row=2, sticky=tk.W)

# Open entries
db_name = tk.StringVar()
db_name_entry = ttk.Entry(opentab, width=25, textvariable=db_name)
db_name_entry.grid(column=1, row=1, sticky=tk.W)
db_name.set("clicksplashdb")

# The processing buttons
action = ttk.Button(droptab, text="Start Process", command=clickMe)
action.grid(column=0, row=6, sticky=tk.W)
action.configure(state='disabled')    # Disable the Button Widget
action1 = ttk.Button(incrtab, text="Start Process", command=clickMe)
action1.grid(column=0, row=8, sticky=tk.W)
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

# Add photo number
photo_number_value = tk.StringVar()
photo_number_entry = ttk.Entry(incrtab, width=5, textvariable=photo_number_value)
photo_number_entry.grid(column=1, row=7)
photo_number_value.set("1")

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
