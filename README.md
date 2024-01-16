# pietimer_kivy
A pie timer in python and kivy, based on ajrepo/countdowntimer

# Usage: 

```
python3 src/main.py [KIVY OPTION...] [-- PROGRAM OPTIONS]

Arguments:
  [--buttons] [-b] Add buttons to control timer  (not implemented yet in this version)
  [-c <color>] [--color=<color>] Color of time remaining  (not implemented yet in this version)
  [--clock_bg_color=<color>] Color not filled by timer when seconds <= 60  (not implemented yet in this version)
  [--help ]   Print Help (this message) and exit
  [-d ] [--display_numeric]  (not implemented yet in this version)
  [-h <#>] [--hours=<#>]
  [-m <#>] [--minutes=<#>]
  [-n ] [--display_currrent_time]  (always true in this version)
  [-s <#>] [--secondss=<#>]
  [-p or --page_layout]  New feature: add PageLayout of numbers over pie timer
  [-q or --quiet]  Do not print time left in terminal  (not implemented yet in this version)
  [--term_ppm] Print to terminal time left each minute  (not implemented yet in this version)
  [-t or --terminal_beep] Execute a beep at t=0  (not implemented yet in this version)
  [-x <#xwidth>] [--x_size=<#xwidth>]
  [-y <#yheight>] [--y_size=<#yheight>]
```

If the -q or --quiet flag is set then don't print anything on the command line, otherwise print a countdown also.

# Installation on Desktop

0. Install prerequisites: python3, kivy and xclip (a kivy requirement)

If you are on a Debian environment you can run

`apt install python3 python3-kivy xclip`

1. Clone the repo

`git clone ... `

2. Make executable (optional)

`chmod u+x main.py`

That's it. You've installed it. If you made it executable you can call it directly
as src/main.py, otherwise call it as "python3 /path/to/main.py"

# Installation on Mobile Device (Android)

0. Get the .apk file from https://github.com/AJRepo/pietimer_kivy/releases/

If you are on your mobile device, then that's it. But if you want to run 
a security checksum on it first and use adb, then follow steps 1-4 below.

1. Do a checksum of the .apk file

```
cd pietimer_kivy/bin
sha256sum -c ../SHA256SUMS 
```

2. Connect your device and run

`adb devices`

3. With the reported name (e.g. XXXX) run

`adb -s XXXX install YYYY.apk `

where XXXX is your android device and YYYY is the apk binary. 

4. (debugging) If you want to see the logs run 

`adb -s XXXX logcat *:S python:D`


# Directions

To change the time, change the timer to not be running (e.g. press the stop button), then
the numbers become active. Click in the number you want to change and then press "Enter"
and that will change the time left. 

Press "Start" to restart the countdown

# Requirements:
Python3, kivy
