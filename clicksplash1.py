#======================
# imports
#======================
import tkinter as tk
from tkinter import ttk
import tkinter
from tkinter import messagebox
import sys
import sqlite3 as lite
from time import sleep
import RPi.GPIO as GPIO



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
save_nameLable = ttk.Label(savetab, text="Tick to save:")
save_nameLable.grid(column=0, row=3,sticky=tk.W)

# Open Labels
openDB_Lable = ttk.Label(opentab, text="Name of Database to open:")
openDB_Lable.grid(column=0, row=1,sticky=tk.W)
openDB_Lable = ttk.Label(opentab, text="Load:")
openDB_Lable.grid(column=0, row=2,sticky=tk.W)
openDB_Lable = ttk.Label(opentab, text="Name of Loop to Load:")
openDB_Lable.grid(column=0, row=4,sticky=tk.W)
openDB_Lable = ttk.Label(opentab, text="Photo Number:")
openDB_Lable.grid(column=2, row=4,sticky=tk.W)

# Loops lable
incrLable = ttk.Label(incrtab, text="Number of loops: ")
incrLable.grid(column=0, row=6, sticky=tk.W)
incrLable = ttk.Label(incrtab, text="Delay after loop (s): ")
incrLable.grid(column=2, row=6, sticky=tk.W, padx=10 )
incrLable = ttk.Label(incrtab, text="Photo Number: ")
incrLable.grid(column=0, row=7, sticky=tk.W)

# open database
def open_db(db_name):
    global con
    con = lite.connect(db_name)

# Modified Button Click Functions
# Sql function
def create_tables():
#    con = lite.connect(v_db_name)
    with con:
        cur = con.cursor()
        create_inputtab = """CREATE TABLE IF NOT EXISTS inputtab(
                                 loopname TEXT PRIMERY KEY UNIQUE,
                                 photo INT,
                                 drops INT,
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
                                 photo INT PRIMERY KEY UNIQUE,
                                 loopname TEXT,
                                 drops INT,
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
        return( -9999)

def get_db_name():
    global v_db_name
    v_db_name = db_name.get()
    if( v_db_name == ''):
        messagebox.showerror("Error", "The database name cannot be empty")
        db_name_entry.focus_set()
        return "ERROR"
    v_db_name = v_db_name + ".db"
    return "GOOD"

# process save_tick
def do_save_tick():
    global v_save_tick
    v_save_tick = save_tick.get()
    if( v_save_tick == 1):
       save_name_entry.configure(state='normal')
    else:
       save_name_entry.configure(state='disabled')

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

    # Get save name and comment
    v_save_name = save_name.get()
    if( v_save_name == '' and v_save_tick == 1):
        messagebox.showerror("Error", "The save name cannot be empty")
        loops_entry.focus_set()
        return "ERROR"

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
        return "ERROR"
    v_loops = x
    x = get_check_int(delay_loop.get())
    if( x < 0 ):
        messagebox.showerror("Error", "Please enter a valid number larger than 0 for loop delay")
        delay_loop_entry.focus_set()
        return "ERROR"
    v_loop_delay = x

# Get photo_number data
    x = get_check_int(photo_number_value.get())
    if( x < 1):
        messagebox.showerror("Error", "Please enter a valid positive number for photo_number")
        photo_number_entry.focus_set()
        return "ERROR"
    v_photo_number = x
# First drop data
    x = get_check_float( drop1duration.get())
    if( x < 0):
        messagebox.showerror("Error", "Please enter a valid number in Drop 1 Duration")
        drop1entry.focus_set()
        return "ERROR"
    v_drop1duration = x

    x = get_check_float( delay1duration.get())
    if( x < 0):
        messagebox.showerror("Error", "Please enter a valid number in delay after drop 1")
        delay1entry.focus_set()
        return "ERROR"
    v_delay1duration = x

    if( v_loops > 1):
        x = get_check_float( drop1inc.get())
        if( x == -9999):
            messagebox.showerror("Error", "Please enter a valid number in Drop 1 increment")
            drop1inc_entry.focus_set()
            return "ERROR"
        v_drop1inc = x

        x = get_check_float( delay1inc_duration.get())
        if( x == -9999):
            messagebox.showerror("Error", "Please enter a valid number in delay after drop 1 increment")
            delay1inc_entry.focus_set()
            return "ERROR"
        v_delay1inc = x
    if(radSel < 2):
        return "GOOD"
# Second drop data
    x = get_check_float( drop2duration.get())
    if( x < 0):
        messagebox.showerror("Error", "Please enter a valid number in Drop 2 Duration")
        drop2entry.focus_set()
        return "ERROR"
    v_drop2duration = x

    x = get_check_float( delay2duration.get())
    if( x == -1):
        messagebox.showerror("Error", "Please enter a valid number in delay after drop 2")
        delay2entry.focus_set()
        return "ERROR"
    v_delay2duration = x

    if( v_loops > 1):
        x = get_check_float( drop2inc.get())
        if( x == -9999):
            messagebox.showerror("Error", "Please enter a valid number in Drop 2 increment")
            drop2inc_entry.focus_set()
            return "ERROR"
        v_drop2inc = x

        x = get_check_float( delay2inc_duration.get())
        if( x == -9999):
            messagebox.showerror("Error", "Please enter a valid number in delay after drop 2 increment")
            delay2inc_entry.focus_set()
            return "ERROR"
        v_delay2inc = x
    if(radSel < 3):
        return "GOOD"
# Third drop data
    x = get_check_float( drop3duration.get())
    if( x < 0):
        messagebox.showerror("Error", "Please enter a valid number in Drop 3 Duration")
        drop3entry.focus_set()
        return "ERROR"
    v_drop3duration = x

    x = get_check_float( delay3duration.get())
    if( x < 0):
        messagebox.showerror("Error", "Please enter a valid number in delay after drop 3")
        delay3entry.focus_set()
        return "ERROR"
    v_delay3duration = x

    if( v_loops > 1):
        x = get_check_float( drop3inc.get())
        if( x == -9999):
            messagebox.showerror("Error", "Please enter a valid number in Drop 3 increment")
            drop3inc_entry.focus_set()
            return "ERROR"
        v_drop3inc = x

        x = get_check_float( delay3inc_duration.get())
        if( x == -9999):
            messagebox.showerror("Error", "Please enter a valid number in delay after drop 3 increment")
            delay3inc_entry.focus_set()
            return "ERROR"
        v_delay3inc = x
    if(radSel < 4):
        return "GOOD"
# Forth drop data
    x = get_check_float( drop4duration.get())
    if( x < 0):
        messagebox.showerror("Error", "Please enter a valid number in Drop 4 Duration")
        drop4entry.focus_set()
        return "ERROR"
    v_drop4duration = x

    x = get_check_float( delay4duration.get())
    if( x < 0):
        messagebox.showerror("Error", "Please enter a valid number in delay after drop 4")
        delay4entry.focus_set()
        return "ERROR"
    v_delay4duration = x

    if( v_loops > 1):
        x = get_check_float( drop4inc.get())
        if( x == -9999):
            messagebox.showerror("Error", "Please enter a valid number in Drop 4 increment")
            drop4inc_entry.focus_set()
            return "ERROR"
        v_drop4inc = x

        x = get_check_float( delay4inc_duration.get())
        if( x == -9999):
            messagebox.showerror("Error", "Please enter a valid number in delay after drop 4 increment")
            delay4inc_entry.focus_set()
            return "ERROR"
        v_delay4inc = x
        return "GOOD"

# Insert loop information in the database.
def save_loop():
    global v_inputtab_data
    inputtab_data = (
        v_save_name,
        v_photo_number,
        radSel,
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
    statement = """ INSERT INTO inputtab VALUES( ?,?,?,?,?, ?,?,?,?,?, ?,?,?,?,?, ?,?,?,?,?, ?,?)"""
#    con = lite.connect(v_db_name)
    with con:
        cur = con.cursor()
        cur.execute(statement, inputtab_data)

def trigger_drops():

    GPIO.output(shutterpin,GPIO.HIGH)
    sleep(0.1)
    GPIO.output(shutterpin,GPIO.LOW)
    sleep(0.1)
    GPIO.output(solenoidpin,GPIO.HIGH)
    sleep(v_next_drop1duration/1000)
    GPIO.output(solenoidpin,GPIO.LOW)
    sleep(v_next_drop1delay/1000)
    if( radSel == 1):
        return
    GPIO.output(solenoidpin,GPIO.HIGH)
    sleep(v_next_drop2duration/1000)
    GPIO.output(solenoidpin,GPIO.LOW)
    sleep(v_delay2duration/1000)
    if( radSel == 2):
        return
    GPIO.output(solenoidpin,GPIO.HIGH)
    sleep(v_next_drop3duration/1000)
    GPIO.output(solenoidpin,GPIO.LOW)
    sleep(v_delay3duration/1000)
    if( radSel == 3):
        return
    GPIO.output(solenoidpin,GPIO.HIGH)
    sleep(v_next_drop4duration/1000)
    GPIO.output(solenoidpin,GPIO.LOW)
    sleep(v_delay4duration/1000)


def trigger_flash():
    flashpin = 25
    GPIO.output(flashpin,GPIO.HIGH)
    sleep(0.008)
    GPIO.output(flashpin,GPIO.LOW)

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
    global shutterpin
    global solenoidpin
    global flashpin

    shutterpin = 17
    solenoidpin = 18
    flashpin = 25
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(shutterpin,GPIO.OUT)
    GPIO.setup(solenoidpin,GPIO.OUT)
    GPIO.setup(flashpin,GPIO.OUT)


    v_next_photo = v_photo_number
    v_next_drop1duration = v_drop1duration
    v_next_drop1delay = v_delay1duration
    v_next_drop2duration = v_drop2duration
    v_next_drop2delay = v_delay2duration
    v_next_drop3duration = v_drop3duration
    v_next_drop3delay = v_delay3duration
    v_next_drop4duration = v_drop4duration
    v_next_drop4delay = v_delay4duration
    v_next_comments = "1"
    trigger_drops()
    trigger_flash()
    sleep(v_loop_delay)

    if (save_tick.get() == 1):
        insert_output()
    for seq in range(2, v_loops +1 ):
        v_next_comments = str(seq)
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
        trigger_drops()
        trigger_flash()
        sleep(v_loop_delay)

        if (save_tick.get() == 1):
            insert_output()
    GPIO.cleanup()

def insert_output():
    outputtab_data = (
        v_next_photo ,
        v_save_name,
        radSel ,
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
    statement = """ INSERT INTO outputtab VALUES( ?,?,?,?,?, ?,?,?,?,?, ?,?)"""
    with con:
        cur = con.cursor()
        cur.execute(statement, outputtab_data)

def open_loop():
    v_open_name = open_name.get()
    if( v_open_name == ''):
        messagebox.showerror("Error", "The loading loop name cannot be empty")
        open_name_entry.focus_set()
        return "ERROR"
    statement = """SELECT * FROM inputtab WHERE loopname = ?"""
    with con:
        cur = con.cursor()
        cur.execute(statement,[open_name.get()] )
        row = cur.fetchone()
        save_name.set(row[0] ) # loopname TEXT
        photo_number_value.set(row[1] ) # photo INT
        radVar.set(row[2] ) # drops INT
        drop1duration.set(row[3] ) # drop1duration REAL
        delay1duration.set(row[4] ) # drop1delay REAL
        drop1inc.set(row[5] ) # drop1inc REAL
        delay1inc_duration.set(row[6] ) # delay1inc REAL
        drop2duration.set(row[7] ) # drop2duration REAL
        delay2duration.set(row[8] ) # drop2delay REAL
        drop2inc.set(row[9] ) # drop2inc REAL
        delay2inc_duration.set(row[10]) # delay2inc REAL
        drop3duration.set(row[11]) # drop3duration REAL
        delay3duration.set(row[12]) # drop3delay REAL
        drop3inc.set(row[13]) # drop3inc REAL
        delay3inc_duration.set(row[14]) # delay3inc REAL
        drop4duration.set(row[15]) # drop4duration REAL
        delay4duration.set(row[16]) # drop4delay REAL
        drop4inc.set(row[17]) # drop4inc REAL
        delay4inc_duration.set(row[18]) # delay4inc REAL
        loops_value.set(row[19]) # loops INT
        delay_loop.set(row[20]) # loop_delay INT
        save_comment.set(row[21]) # comments TEXT
    save_tick.set(0)
    action.configure(state='normal')
    radCall()
    return "GOOD"

def open_photo():
    v_open_photo_value = get_check_int(open_photo_value.get())
    if( v_open_photo_value == -1):
        messagebox.showerror("Error", "The photo number must be a valid positive number")
        return "ERROR"
    statement = """SELECT * FROM outputtab WHERE photo = ?"""
    with con:
        cur = con.cursor()
        cur.execute(statement, [open_photo_value.get()])
        row = cur.fetchone()
        photo_number_value.set( row[0]) # photo
        save_name.set( row[1]) # loopname
        radVar.set( row[2]) # drops
        drop1duration.set( row[3]) # "drop1duration"
        delay1duration.set( row[4]) # drop1delay
        drop2duration.set( row[5]) # drop2duration
        delay2duration.set( row[6]) # drop2delay
        drop3duration.set( row[7]) # drop3duration
        delay3duration.set( row[8]) # drop3delay
        drop4duration.set( row[9]) # drop4duration
        delay4duration.set(row[10]) # drop4delay
        save_comment.set( row[11]) # comments
    save_tick.set(0)
    action.configure(state='normal')
    radCall()
    return "GOOD"

def open_action():
    if (get_db_name() == "EROOR"):
        return
    open_db(v_db_name)
    if( OpenRadSel == 1):
        open_loop()
    elif (OpenRadSel == 2):
        open_photo()

def clickMe():
    if (get_save_data()== "ERROR"):
        return
    if (get_db_name() == "EROOR"):
        return
    open_db(v_db_name)
    create_tables()
    if (save_tick.get() == 1):
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

save_tick = tk.IntVar()
save_tick_entry = ttk.Checkbutton(savetab, variable=save_tick, command=do_save_tick)
save_tick_entry.grid(column=1, row=3, sticky=tk.W)
save_tick.set(1)

# Open entries
db_name = tk.StringVar()
db_name_entry = ttk.Entry(opentab, width=25, textvariable=db_name)
db_name_entry.grid(column=1, row=1, sticky=tk.W)
db_name.set("clicksplashdb")
open_name = tk.StringVar()
open_name_entry = ttk.Entry(opentab, width=25, textvariable=open_name)
open_name_entry.grid(column=1, row=4, sticky=tk.W)
open_photo_value = tk.StringVar()
open_photo_entry = ttk.Entry(opentab, width=5, textvariable=open_photo_value)
open_photo_entry.grid(column=3, row=4, sticky=tk.W)

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
delay_loop.set("1")

# Add photo number
photo_number_value = tk.StringVar()
photo_number_entry = ttk.Entry(incrtab, width=5, textvariable=photo_number_value)
photo_number_entry.grid(column=1, row=7)
photo_number_value.set("1")

radVar = tk.IntVar()

def OpenRadCall():
    global OpenRadSel
    OpenRadSel=OpenRadVar.get()
    if (OpenRadSel == 1):
        open_photo_entry.configure(state='disabled')
        open_name_entry.configure(state='normal')
        open_button.configure(state='normal')
        open_button.configure(text='Load Loop ')
    elif (OpenRadSel == 2):
        open_photo_entry.configure(state='normal')
        open_name_entry.configure(state='disabled')
        open_button.configure(state='normal')
        open_button.configure(text='Load Photo Number ')
    elif (OpenRadSel == 3):
        open_photo_entry.configure(state='disabled')
        open_name_entry.configure(state='disabled')
        open_button.configure(text='Click on Loop or Photo to load ')
        open_button.configure(state='disabled')

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

# Create 3 Radio Buttons
OpenRadVar = tk.IntVar()
OpenRad1 = tk.Radiobutton(opentab, text="Loop", variable=OpenRadVar, value=1, command=OpenRadCall)
OpenRad1.grid(column=0, row=3, sticky=tk.W)
OpenRad2 = tk.Radiobutton(opentab, text="Photo", variable=OpenRadVar, value=2, command=OpenRadCall)
OpenRad2.grid(column=1, row=3, sticky=tk.W)
OpenRad3 = tk.Radiobutton(opentab, text="None", variable=OpenRadVar, value=3, command=OpenRadCall)
OpenRad3.grid(column=2, row=3, sticky=tk.W)
OpenRadVar.set(3)
open_photo_entry.configure(state='disabled')
open_name_entry.configure(state='disabled')
# Open button
open_button = ttk.Button(opentab, text="Click on Loop or Photo to load ", command=open_action)
open_button.grid(column=0, row=5, sticky=tk.W)
open_button.configure(state='disabled')    # Disable the Button Widget

#======================
# Start GUI
#======================
win.mainloop()
