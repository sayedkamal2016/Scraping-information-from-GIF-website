from tkinter import messagebox
from tkinter import Button
from tkinter import Tk
from tkinter import Toplevel
from tkinter import Menu
from tkinter import IntVar
from tkinter import Radiobutton
from tkinter import W, X, E, BOTTOM, LEFT
from tkinter import Label, Entry, Spinbox, PhotoImage
import requests
import webbrowser
import time
from lxml import html
from datetime import date

url = 'https://gif.gov.pl/pl/decyzje-i-komunikaty/decyzje/decyzje'

last_check_date_and_time = ''
new_communicates = 'No new messages'
if_found_message_today = False
if_check_manually_new_communicates = False
reset_time_after_manually_check = True
how_often_to_check_automatically = 1800
counter = how_often_to_check_automatically 
def counter_label(label):
  def count():
    global counter
    global if_check_manually_new_communicates
    counter -= 1
    label.after(1000, count)
    if if_check_manually_new_communicates and reset_time_after_manually_check:
      counter = how_often_to_check_automatically
      if_check_manually_new_communicates = False
    elif counter > 0:
      label.config(text = str("Time to automate check: {} seconds ({} minutes)".format(counter, round(counter / 60, 2))))
    elif counter == 0:
      check_new_messages()
    elif counter < 0:
      label.config(text = str("Checking new information on GIF website..."))
      counter = how_often_to_check_automatically
  count()

def check_new_messages():
  try:
    page = requests.get(url)
  except:
    try:
      page = requests.get(url, verify = False)
    except:
      messagebox.showerror('Error', 'Something went wrong')

  page_structure = html.fromstring(page.content) 

  try:  
    date_of_new_messages = page_structure.xpath('//tr[2]/td[3]/text()')
  except:
    messagebox.showerror('Error', 'Problem with downloading information from the site')

  today = ("{:%d.%m.%Y}".format(date.today()))
  global last_check_date_and_time
  global new_communicates
  global if_found_message_today
  last_check_date_and_time = time.asctime(time.localtime(time.time()))

  if today in date_of_new_messages:
    new_communicates = 'New messages on GIF website!'
    if_found_message_today = True
    if (messagebox.askyesno("New messages in GIF", "Check new information in Główny Inspektorat Farmaceutyczny (GIF). Open the GIF page with messages?")) == True:
      webbrowser.open(url)
    else:
      pass
  else:
      pass
  write_information_about_new_messages()  
  write_date_time_last_check_new_information()

def manually_check_new_messages():
  global if_check_manually_new_communicates
  if_check_manually_new_communicates = True
  check_new_messages()

def open_settings():
  messagebox.showwarning("Not implement yet", "It will be implement")

def about():
  messagebox.showinfo("Information","The program checks messages on the GIF website (Main Pharmaceutical Inspectorate) and informs about new messages.")

def write_information_about_new_messages():
  label_new_communicates.config(text = new_communicates, font=("Helvetica", 18))
  label_new_communicates.pack()

def write_date_time_last_check_new_information():
  last_check = "Last check new information: {}".format(last_check_date_and_time)
  label_last_check.config(text = last_check, font = ("Helvetica", 9))
  label_last_check.pack()

root = Tk()
root.title("Check_GIF")
root.minsize(350,150)

label_new_communicates = Label(root)
label_last_check = Label(root)

write_information_about_new_messages()
write_date_time_last_check_new_information()

menubar = Menu(root)
optionsmenu = Menu(menubar, tearoff=0)
optionsmenu.add_command(label = "Settings", command = open_settings)
optionsmenu.add_separator()
optionsmenu.add_command(label = "Exit", command = root.quit)
menubar.add_cascade(label = "Options", menu = optionsmenu)
menubar.add_cascade(label = "About", command = about)
root.config(menu = menubar)
check_icon_svg = PhotoImage(file = "check_icon.svg")
check_button = Button(root, text = "Check new communicates", image = check_icon_svg, compound = "left", activebackground = "green", bg = "white", command = manually_check_new_messages)
check_button.place(x = 35, y = 150)
check_button.pack()
label = Label(root, fg = "green")
label.pack(side = BOTTOM)
counter_label(label)
check_new_messages()
root.mainloop()
