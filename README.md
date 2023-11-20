# pietimer_kivy
A pie timer in python and kivy, based on ajrepo/countdowntimer

# Usage: 

python3 pietimer.py [KIVY OPTION...] [-- PROGRAM OPTIONS]

Arguments:
  [--buttons] [-b] Add buttons to control timer  (not implemented yet in this version)
  [-c <color>] [--color=<color>] Color of time remaining  (not implemented yet in this version)
  [--clock_bg_color=<color>] Color not filled by timer when seconds <= 60  (not implemented yet in this version)
  [--help ]   Print Help (this message) and exit
  [-d ] [--display_numeric]  (not implemented yet in this version)
  [-h <#>] [--hours=<#>]
  [-m <#>] [--minutes=<#>]
  [-n ] [--display_currrent_time]  (not implemented yet in this version)
  [-s <#>] [--secondss=<#>]
  [-q or --quiet]  Do not print time left in terminal  (not implemented yet in this version)
  [--term_ppm] Print to terminal time left each minute  (not implemented yet in this version)
  [-t or --terminal_beep] Execute a beep at t=0  (not implemented yet in this version)
  [-x <#xwidth>] [--x_size=<#xwidth>]
  [-y <#yheight>] [--y_size=<#yheight>]


If the -q or --quiet flag is set then don't print anything on the command line, otherwise print a countdown also.

# Installation

1. Clone the repo

`git clone ... `

2. (optional) If you are installing the .apk file then do a checksum of the .apk file

```
cd pietimer_kivy/bin
sha256sum -c ../SHA256SUMS 
```

# Directions

To change the time, change the timer to not be running (e.g. press the stop button), then
the numbers become active. Click in the number you want to change and then press "Enter"
and that will change the time left. 

Press "Start" to restart the countdown

# Requirements:
Python3, kivy
