import os
import sys
import time
import webbrowser
from datetime import date
from tkinter import (BOTTOM, LEFT, Button, E, Entry, IntVar, Label, Menu,
                     PhotoImage, Radiobutton, Spinbox, Tk, Toplevel, W, X,
                     messagebox)

import requests
from lxml import html

def GET_URL():
  return 'https://rdg.rejestrymedyczne.csioz.gov.pl/'

FILE_SETTINGS = "settings"
the_message_has_already_been_displayed = False

def read_settings_from_file():
  with open(FILE_SETTINGS, 'r') as settings_file:
    settings_config = [element.strip() for element in settings_file]
    settings_file.close()
  return settings_config

try:
  settings_config = read_settings_from_file()
except:
  try:
    settings_file = open(FILE_SETTINGS, "w+")
    settings_file.write('1\n600\n1\n1')
    settings_file.close()
    settings_config = read_settings_from_file()
  except:
    messagebox.showerror("Error","The settings cannot be loaded")

def MINIMUM_FREQUENCY_CHECKING_NEW_MESSAGES():
  return 300

def MAXIMUM_FREQUENCY_CHECKING_NEW_MESSAGES():
  return 3600

try:
  automatic_checking_is_on_int = int (settings_config[0])
  how_often_to_check_intvar = int (settings_config[1])
  counter = how_often_to_check_intvar 
  how_often_to_check_int = how_often_to_check_intvar
  reset_time_after_manually_check_int = int (settings_config[2])
  confirm_close_application_int = int (settings_config[3])
except:
  try:
    os.remove(FILE_SETTINGS)
    os.execv(sys.executable, ['python'] + sys.argv)
  except:
    os.execv(__file__, sys.argv)
  
found_message_today = False
check_manually_new_communicates = False
last_check_date_and_time = ''
new_communicates = 'No new messages'
def counter_label(label):
  def count():
    global counter
    global check_manually_new_communicates
    counter -= 1
    label.after(1000, count)
    if automatic_checking_is_on_int:
      if check_manually_new_communicates and reset_time_after_manually_check_int:
        counter = how_often_to_check_int
        check_manually_new_communicates = False
      elif counter > 0:
        label.config(text = str("Time to automate check: {} seconds ({} minutes)".format(counter, round(counter / 60, 2))), fg = "green")
      elif counter == 0:
        check_new_messages()
      elif counter < 0:
        label.config(text = str("Checking new information on GIF website..."), fg = "orange")
        counter = how_often_to_check_int
    else:
      label.config(text = str("Automatic checking disabled"), fg = "red")
  count()

def check_new_messages():
  try:
    page = requests.get(GET_URL())
  except:
    try:
      page = requests.get(GET_URL(), verify = False)
    except:
      messagebox.showerror('Error', 'Something went wrong')

  page_structure = html.fromstring(page.content) 

  date_of_new_messages = page_structure.xpath('//table/tbody/tr[1]/td[3]/text()')
  if len(date_of_new_messages) == 0:
    messagebox.showerror('Error', 'Problem with downloading information from the site')
  else:
    pass

  today = ("{:%Y-%m-%d}".format(date.today()))
  global last_check_date_and_time
  global new_communicates
  global found_message_today
  last_check_date_and_time = time.asctime(time.localtime(time.time()))

  global the_message_has_already_been_displayed
  if today in date_of_new_messages and not the_message_has_already_been_displayed:
    new_communicates = 'New messages on GIF website!'
    the_message_has_already_been_displayed = True
    found_message_today = True
    if (messagebox.askyesno("New messages in GIF", "Check new information in Główny Inspektorat Farmaceutyczny (GIF). Open the GIF page with messages?")) == True:
      webbrowser.open(GET_URL())
    else:
      pass
  else:
      pass
  write_information_about_new_messages()  
  write_date_time_last_check_new_information()

def manually_check_new_messages():
  global check_manually_new_communicates
  global the_message_has_already_been_displayed
  the_message_has_already_been_displayed = False
  check_manually_new_communicates = True
  check_new_messages()

def open_settings():
  global top_settings
  top_settings = Toplevel(root)
  center_window(top_settings, 520, 240)
  top_settings.iconbitmap('settings.ico')
  top_settings.resizable(False, False)
  top_settings.title("Settings")
  
  check_automation_checking(top_settings)
  frequency_checking_new_messages(top_settings)
  set_new_time_or_continue_after_manual_check(top_settings)
  ask_if_close_application(top_settings)

  save_settings_button = Button(top_settings, text = "Save settings", font=('Verdana', 9,'bold'), background = "blue", command = save_settings)
  save_settings_button.grid(column = 1, row = 10, sticky = E, padx = 9, pady = 9)

  cancel_settings_button = Button(top_settings, text = "Close settings", command = exit_from_settings)
  cancel_settings_button.grid(column = 0, row = 10, sticky = E, padx = 10, pady = 10)

  default_settings_button = Button(top_settings, text = "Default settings (no save)", command = set_default_settings)
  default_settings_button.grid(column = 0, row = 10, sticky = W, padx = 11, pady = 11)

  top_settings.mainloop()

def ask_if_close_application(top_settings):
  global confirm_close_application_intvar
  confirm_close_application_intvar = IntVar()
  confirm_close_application_intvar.set(confirm_close_application_int)
  label_confirm_close_application = Label(top_settings, text = "Confirm exit from application:")
  label_confirm_close_application.grid(column = 0, row = 8, rowspan = 2, sticky = W)
  radiobutton_confirm_close_application_on = Radiobutton(top_settings, text = "Yes", variable = confirm_close_application_intvar, value = 1)
  radiobutton_confirm_close_application_off = Radiobutton(top_settings, text = "No", variable = confirm_close_application_intvar, value = 0)
  radiobutton_confirm_close_application_on.grid(column = 1, row = 8, sticky = W)
  radiobutton_confirm_close_application_off.grid(column = 1, row = 9, sticky = W)

def set_new_time_or_continue_after_manual_check(top_settings):
  global reset_time_after_manually_check_intvar
  reset_time_after_manually_check_intvar = IntVar()
  reset_time_after_manually_check_intvar.set(reset_time_after_manually_check_int)
  label_reset_time_after_manually_check_ = Label(top_settings, text = "After checking manually:")
  label_reset_time_after_manually_check_.grid(column = 0, row = 4, rowspan = 2, sticky = W)
  radiobutton_reset_time_after_manually_check_on = Radiobutton(top_settings, text = "New time (reset time)", 
    variable = reset_time_after_manually_check_intvar, value = 1)
  radiobutton_reset_time_after_manually_check_off = Radiobutton(top_settings, text = "Continue time", 
    variable = reset_time_after_manually_check_intvar, value = 0)
  radiobutton_reset_time_after_manually_check_on.grid(column = 1, row = 4, sticky = W)
  radiobutton_reset_time_after_manually_check_off.grid(column = 1, row = 5, sticky = W)

def frequency_checking_new_messages(top_settings):
  global how_often_to_check_intvar
  how_often_to_check_intvar = IntVar()
  how_often_to_check_intvar.set(how_often_to_check_int)
  label_frequency = Label(top_settings, text = "Frequency of checking (in seconds from {} to {}):"
    .format(MINIMUM_FREQUENCY_CHECKING_NEW_MESSAGES(), MAXIMUM_FREQUENCY_CHECKING_NEW_MESSAGES()))
  label_frequency.grid(column = 0, row = 3, sticky = W)
  spinbox_entry = Spinbox(top_settings, textvariable = how_often_to_check_intvar, 
    from_ = MINIMUM_FREQUENCY_CHECKING_NEW_MESSAGES(), to = MAXIMUM_FREQUENCY_CHECKING_NEW_MESSAGES())
  spinbox_entry.grid(column = 1, row = 3)

def check_automation_checking(top_settings):
  global automatic_checking_is_on_intvar
  automatic_checking_is_on_intvar = IntVar()
  automatic_checking_is_on_intvar.set(automatic_checking_is_on_int)
  label_automatic_checking = Label(top_settings, text = "Automatic checking:")
  label_automatic_checking.grid(column = 0, row = 0, rowspan = 2, sticky = W)
  radiobutton_automatic_checking_on = Radiobutton(top_settings, text = "Turn ON automatic checking", variable = automatic_checking_is_on_intvar, value = True)
  radiobutton_automatic_checking_off = Radiobutton(top_settings, text = "Turn OFF automatic checking", variable = automatic_checking_is_on_intvar, value = False)
  radiobutton_automatic_checking_on.grid(column = 1, row = 0)
  radiobutton_automatic_checking_off.grid(column = 1, row = 1)

def set_default_settings():
  automatic_checking_is_on_intvar.set(1)
  how_often_to_check_intvar.set(MINIMUM_FREQUENCY_CHECKING_NEW_MESSAGES())
  reset_time_after_manually_check_intvar.set(1)
  confirm_close_application_intvar.set(1)

def save_settings():
  global automatic_checking_is_on_int 
  automatic_checking_is_on_int = automatic_checking_is_on_intvar.get()

  global how_often_to_check_int
  try:
    how_often_to_check_int = how_often_to_check_intvar.get()
    how_often_to_check_int = vaidate_time_for_automatic_checking(how_often_to_check_int)
  except:
    messagebox.showwarning("Warning!", "The value is not a number. The check frequency is set to {} seconds."
      .format(MINIMUM_FREQUENCY_CHECKING_NEW_MESSAGES()))
    how_often_to_check_intvar.set(MINIMUM_FREQUENCY_CHECKING_NEW_MESSAGES())
    how_often_to_check_int = MINIMUM_FREQUENCY_CHECKING_NEW_MESSAGES()

  global reset_time_after_manually_check_int
  reset_time_after_manually_check_int = reset_time_after_manually_check_intvar.get()

  global confirm_close_application_int
  confirm_close_application_int = confirm_close_application_intvar.get()

  save_settings_to_file()
  confirm_save()
  exit_from_settings()

def save_settings_to_file():
  settings_config = [str (automatic_checking_is_on_int), str (how_often_to_check_int), 
                    str (reset_time_after_manually_check_int), str (confirm_close_application_int)]
  with open(FILE_SETTINGS, "w") as settings_file:
    settings_file.write('\n'.join(settings_config))
    settings_file.close()

def vaidate_time_for_automatic_checking(how_often_to_check_int):
  if how_often_to_check_int < MINIMUM_FREQUENCY_CHECKING_NEW_MESSAGES():
    how_often_to_check_intvar.set(MINIMUM_FREQUENCY_CHECKING_NEW_MESSAGES())
    how_often_to_check_int = MINIMUM_FREQUENCY_CHECKING_NEW_MESSAGES()
  elif how_often_to_check_int > MAXIMUM_FREQUENCY_CHECKING_NEW_MESSAGES():
    how_often_to_check_intvar.set(MAXIMUM_FREQUENCY_CHECKING_NEW_MESSAGES())
    how_often_to_check_int = MAXIMUM_FREQUENCY_CHECKING_NEW_MESSAGES()
  else:
    pass
  return how_often_to_check_int

def confirm_save():
  messagebox.showinfo("Success","Settings saved.")

def exit_from_settings():
  top_settings.destroy()
  
def about():
  messagebox.showinfo("Information","The program checks messages on the GIF website (Main Pharmaceutical Inspectorate) and informs about new messages.\nYou can check the source of the code and make improvements https://github.com/olekstomek")

def write_information_about_new_messages():
  label_new_communicates.config(text = new_communicates, font=("Helvetica", 18))
  label_new_communicates.pack()

def write_date_time_last_check_new_information():
  last_check = "Last check new information: {}".format(last_check_date_and_time)
  label_last_check.config(text = last_check, font = ("Helvetica", 9))
  label_last_check.pack()

def confirm_quit():
  if confirm_close_application_int:
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

def center_window(root, width, height):
  screen_width = root.winfo_screenwidth()
  screen_height = root.winfo_screenheight()
  x = (screen_width/2) - (width/2)
  y = (screen_height/2) - (height/2)
  root.geometry('%dx%d+%d+%d' % (width, height, x, y))

if __name__ == "__main__":
  width_application = 350
  height_application = 150
  root = Tk()
  center_window(root, width_application, height_application)
  root.iconbitmap('main.ico')
  root.title("Check_GIF")
  root.minsize(width_application,height_application)
  menubar = create_menu()
  root.config(menu = menubar)
  label_new_communicates = Label(root)
  label_last_check = Label(root)
  write_information_about_new_messages()
  write_date_time_last_check_new_information()
  check_icon_svg = PhotoImage(file = "check_icon.svg")
  check_button = Button(root, text = "Check new communicates", image = check_icon_svg, compound = "left", 
    activebackground = "green", bg = "white", command = manually_check_new_messages)
  check_button.place(x = 35, y = 150)
  check_button.pack()
  label = Label(root)
  label.pack(side = BOTTOM)
  counter_label(label)
  check_new_messages()
  root.protocol("WM_DELETE_WINDOW", confirm_quit)
  root.mainloop()
