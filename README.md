# Scraping-information-from-GIF-website
The program checks messages on the GIF website (Main Pharmaceutical Inspectorate) and informs about new messages.


Program written in Python using tkinter. You may need to install requests, webbrowser, lxml.

The program's task is to automatically check whether new decisions on pharmaceutical products appeared on the website of the Main Pharmaceutical Inspectorate (https://gif.gov.pl/pl/decyzje-i-komunikaty/decyzje/decyzje).

![GIF](https://user-images.githubusercontent.com/26818304/63369461-4b6a5200-c380-11e9-8b4b-33b9a295f91e.png)

In the main window:
- if you see the message "No new messages" it means that currently no new information was found on the site,
- if you see "New messages on GIF website!" this means that new information has been found on the page, the program will also suggest opening a web page containing detailed information in the default operating system browser. The program will not show this message during automatic checking (except for the first time unless manual checking has been done before) because displaying the message after each automatic check would be cumbersome. The message will always appear when checking manually.

In the program window you can also see when the last message check took place (applies to manual as well as automatic). You can perform a manual check by clicking the "Check new communicates" button. At the bottom of the window you can see the countdown to be automatically checked in seconds and also in minutes. If you turn off automatic checking, a message will appear in the program window: "Automatic checking disabled" (the time will count down in the background but no automatic checking will be performed). Saving the settings does not reset the countdown of the current time (even if a new time value has been set) - the new time will be counted down after checking the information automatically or after checking the information manually.

In the settings you can:
- you can enable or disable automatic checking of information on the website,
- you can set how often automatic checking of new messages should take place - minimum every 300 seconds (5 minutes) and maximum every 3600 seconds (one hour),
- you can set whether after the manual check (by clicking the "Check new communicates" button) the countdown to the next automatic check is to reset or whether the countdown should continue,
- you can set whether the program should ask you before closing the program (option to avoid accidental closing of the program)

The program saves the settings in a text file. If the file does not exist, the program will automatically create a file with default settings (Automatic checking: Yes, Frequency of checking: 600 seconds, After checking manually: New time, Confirm exit from application: Yes). You can always choose the button in the settings that will restore the default settings - set the parameters as above and check frequency to 300 seconds (minimum value). If you enter a value other than the number in the check frequency field (e.g. text string), the program will automatically take the value of 300 seconds. If you set the check time above 3600 seconds, the value 3600 will be set, the same if the time is set below 300 seconds - then the value will be set to a minimum value of 300 seconds. If it turns out that the text file in which the settings are corrupted (e.g. all parameters that the program needs to load all settings are missing), the program will automatically delete the damaged file, create a new file with settings and the program will restart automatically.
