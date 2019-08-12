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
confirm_close = 1
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
  global top_settings
  top_settings = Toplevel(root)
  top_settings.resizable(False, False)
  top_settings.title("Settings")
  
  check_automation_checking(top_settings)
  frequency_checking_new_messages(top_settings)
  set_new_time_or_continue_after_manual_check(top_settings)
  write_logs(top_settings)
  ask_if_close_application(top_settings)

  save_settings_button = Button(top_settings, text = "Save settings", command = save_settings)
  save_settings_button.grid(column = 1, row = 10, sticky = E, padx = 9, pady = 9)

  cancel_settings_button = Button(top_settings, text = "Cancel", command = cancel)
  cancel_settings_button.grid(column = 0, row = 10, sticky = E, padx = 10, pady = 10)

  top_settings.mainloop()

def ask_if_close_application(top_settings):
  global confirm_close_application
  confirm_close_application = IntVar()
  confirm_close_application.set(1)
  label_confirm_close = Label(top_settings, text = "Confirm exit from application:")
  label_confirm_close.grid(column = 0, row = 8, rowspan = 2, sticky = W)
  radiobutton_on = Radiobutton(top_settings, text = "Yes", variable = confirm_close_application, value = 1)
  radiobutton_off = Radiobutton(top_settings, text = "No", variable = confirm_close_application, value = 0)
  radiobutton_on.grid(column = 1, row = 8, sticky = W)
  radiobutton_off.grid(column = 1, row = 9, sticky = W)

def write_logs(top_settings):
  global if_write_logs
  if_write_logs = IntVar()
  if_write_logs.set(False)
  label_write_logs = Label(top_settings, text = "Write logs to file:")
  label_write_logs.grid(column = 0, row = 6, rowspan = 2, sticky = W)
  radiobutton_on = Radiobutton(top_settings, text = "Yes", variable = if_write_logs, value = 1)
  radiobutton_off = Radiobutton(top_settings, text = "No", variable = if_write_logs, value = 0)
  radiobutton_on.grid(column = 1, row = 6, sticky = W)
  radiobutton_off.grid(column = 1, row = 7, sticky = W)

def set_new_time_or_continue_after_manual_check(top_settings):
  global reset_time_after_manually_check
  reset_time_after_manually_check = IntVar()
  reset_time_after_manually_check.set(False)
  label_new_time_after_manual_check = Label(top_settings, text = "After checking manually:")
  label_new_time_after_manual_check.grid(column = 0, row = 4, rowspan = 2, sticky = W)
  radiobutton_on = Radiobutton(top_settings, text = "New time", variable = reset_time_after_manually_check, value = 1)
  radiobutton_off = Radiobutton(top_settings, text = "Continue time", variable = reset_time_after_manually_check, value = 0)
  radiobutton_on.grid(column = 1, row = 4, sticky = W)
  radiobutton_off.grid(column = 1, row = 5, sticky = W)

def frequency_checking_new_messages(top_settings):
  global how_often_to_check_automatically
  how_often_to_check_automatically = IntVar()
  label_frequency = Label(top_settings, text = "Frequency of checking:")
  label_frequency.grid(column = 0, row = 3, sticky = W)
  spinbox_entry = Spinbox(top_settings, textvariable = how_often_to_check_automatically, from_ = 1, to = 120)
  spinbox_entry.grid(column = 1, row = 3)

def check_automation_checking(top_settings):
  global if_check_automatic_new_communicates
  if_check_automatic_new_communicates = IntVar()
  if_check_automatic_new_communicates.set(False)
  label_auto_checking = Label(top_settings, text = "Automatic checking:")
  label_auto_checking.grid(column = 0, row = 0, rowspan = 2, sticky = W)
  radiobutton_on = Radiobutton(top_settings, text = "Turn ON automatic checking", variable = if_check_automatic_new_communicates, value = True)
  radiobutton_off = Radiobutton(top_settings, text = "Turn OFF automatic checking", variable = if_check_automatic_new_communicates, value = False)
  radiobutton_on.grid(column = 1, row = 0)
  radiobutton_off.grid(column = 1, row = 1)

def save_settings():
  global confirm_close
  confirm_close = confirm_close_application.get()
  print('confirm_close {} '.format(confirm_close))

def cancel():
  top_settings.destroy()
  
def about():
  messagebox.showinfo("Information","The program checks messages on the GIF website (Main Pharmaceutical Inspectorate) and informs about new messages.")

def write_information_about_new_messages():
  label_new_communicates.config(text = new_communicates, font=("Helvetica", 18))
  label_new_communicates.pack()

def write_date_time_last_check_new_information():
  last_check = "Last check new information: {}".format(last_check_date_and_time)
  label_last_check.config(text = last_check, font = ("Helvetica", 9))
  label_last_check.pack()

def confirm_quit():
  if confirm_close:
    if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        root.destroy()
  else:
    root.destroy()

def create_menu():
  menubar = Menu(root)
  optionsmenu = Menu(menubar, tearoff=0)
  optionsmenu.add_command(label = "Settings", command = open_settings)
  optionsmenu.add_separator()
  optionsmenu.add_command(label = "Exit", command = confirm_quit)
  menubar.add_cascade(label = "Options", menu = optionsmenu)
  menubar.add_cascade(label = "About", command = about)
  return menubar

if __name__ == "__main__":
  root = Tk()
  root.title("Check_GIF")
  root.minsize(350,150)
  menubar = create_menu()
  root.config(menu = menubar)
  label_new_communicates = Label(root)
  label_last_check = Label(root)
  write_information_about_new_messages()
  write_date_time_last_check_new_information()
  check_icon_svg = PhotoImage(file = "check_icon.svg")
  check_button = Button(root, text = "Check new communicates", image = check_icon_svg, compound = "left", activebackground = "green", bg = "white", command = manually_check_new_messages)
  check_button.place(x = 35, y = 150)
  check_button.pack()
  label = Label(root, fg = "green")
  label.pack(side = BOTTOM)
  counter_label(label)
  check_new_messages()
  root.protocol("WM_DELETE_WINDOW", confirm_quit)
  root.mainloop()
