# pietimer_kivy
A pie timer in python and kivy, based on ajrepo/countdowntimer

Usage: 

python3 pietimer.py [KIVY OPTION...] [-- PROGRAM OPTIONS]

Arguments:
  [--buttons] [-b] Add buttons to control timer
  [--console_only] Only use the console - not graphical timer
  [-c <color>] [--color=<color>] Color of time remaining
  [--clock_bg_color=<color>] Color not filled by timer when seconds <= 60
  [--help ]   Print Help (this message) and exit
  [-d ] [--display_numeric]
  [-h <#>] [--hours=<#>]
  [-m <#>] [--minutes=<#>]
  [-n ] [--display_currrent_time]
  [-s <#>] [--secondss=<#>]
  [-q or --quiet]  Do not print time left in terminal
  [--term_ppm] Print to terminal time left each minute
  [-t or --terminal_beep] Execute a beep at t=0
  [-x <#xwidth>] [--x_size=<#xwidth>]
  [-y <#yheight>] [--y_size=<#yheight>]


If the -q or --quiet flag is set then don't print anything on the command line, otherwise print a countdown also.

Requirements:
Python3, kivy
