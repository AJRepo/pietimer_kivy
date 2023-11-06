#!/usr/bin/python3
"""This implements a graphical countdown timer

Copyright 2023 A. Ottenheimer - use of this code requires this comment to
be kept and aknowledgement sent to the author.
License: GPL 3. See LICENSE file.

#TODO: add plyer for notifications?
#from plyer.notification import notify
# notify('Some title', 'some message')

"""

import os
os.environ["KCFG_KIVY_LOG_LEVEL"] = "warning"
# pylint: disable=wrong-import-position
import sys
import getopt
import math
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
#from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
#from kivy.utils import colormap
from kivy.graphics import Color, Ellipse
#from kivy.properties import DictProperty, BooleanProperty
#from kivy.properties import StringProperty, NumericProperty
from kivy.core.window import Window

#Uncommend the below to get NO messages at all from Kivy to the console
#os.environ["KIVY_NO_CONSOLELOG"] = "1"
#print(kivy.__version__)


class AnalogClockFace(FloatLayout):
    """Kivy requires defining args passed in before init"""
    # See https://kivy.org/doc/stable/api-kivy.properties.html?highlight=properties
    # Properties: To declare properties, you must declare them at the class level.
    #   The class will then do the work to instantiate the real attributes when
    #   your object is created. These properties are not attributes: they are
    #    mechanisms for creating events based on your attributes:
    #   e.g. clockp_dict = DictProperty({})
    #   e.g. ajoaasdf = StringProperty("hello world")


    #for using .kv file
    def __init__(self, clock_features=None, **kwargs):
        super(AnalogClockFace, self).__init__(**kwargs)

        #is it possible to only have these in class PieTimer?
        if clock_features is None:
            clock_features = {'initialized': False, 'debug': False}
        self.running = True
        self.seconds_left = 0.0   #could be a fraction of a second
        self.countdown = True
        self.clock_interval = .1
        #clockface clock_widgets (numbers around edge)
        self.clock_widgets = {}

        if clock_features['debug'] is True:
            print("DEBUG: AnalogClock clock_features=", clock_features)

        #clock_features = PieTimer.setup_args(self)
        #clock_features = AnalogClockFace(clock_features=self.clock_features)
        self.clock_features = clock_features
        if self.clock_features['debug'] is True:
            print("CLOCKFACE IDS = ", self.ids)
            for key, val in self.ids.items():
                print(f"key={key}: val={val}")
                print(f"VALWIDTH = {val.width}")


        if clock_features['initialized'] is True:
            PieTimer.set_start_seconds(self)
            if self.clock_features['debug'] is True:
                print(f"XWIDTH NOW = {clock_features['initialized']}")
            #add_clock_numbers: puts a series of numbers around the clock/pie
            #  Divisble by 60: 2, *4, 3, 5, 10, *12, 15, *20
            #  these together are interesting
            #  self.add_clock_numbers(4)
            #  self.add_clock_numbers(10)
            self.add_clock_numbers(12)
            self.define_pie_widgets()
            self.adjust_pie()
            self.ids['"hrs"'].text = str(round(self.seconds_left/3600)%24)
            self.ids['"min"'].text = str(round(self.seconds_left/60)%60)
            self.ids['"sec"'].text = str(round(self.seconds_left)%60)

            #self.add_pie()

            #run this until it returns False
            Clock.schedule_interval(self.runclock, self.clock_interval)

            #can we change the interval to be 1 sec if sec_left>60?

            if clock_features['debug'] is True:
                print("DEBUG: RIGHT AFTER Clock.schedule------------")
            # Alternatively set event_run = Clock...
            #     and then to stop use event_run.cancel() or Clock.unschedule(event_run)

    def define_pie_widgets(self):
        """Setup the dict of elipses (self.clock_widgets) to identify for operations later"""
        #self.root.ids.pie.
        if self.clock_features['debug'] is True:
            #print("IDSPIE = ", self.ids['"pie"'].canvas.children[1].rgba)
            print("IDSPIE = ", self.ids['"pie"'].canvas)
            # Doesn't work
            #print("IDSPIE2 = ", self.ids['pie'])


        #I guess since the first ellipse is the background and the second is the foreground
        # we don't need to add them to self.clock_widgets and just do
        #   self.ids['"pie"'].canvas.children[0]
        # but this seems easier to read. Change to use the index if too resource intensive.
        i = 0
        found_background_pie = False

        for child in self.ids['"pie"'].canvas.children:
            if isinstance(child, Color):
                if self.clock_features['debug'] is True:
                    print("FOUND COLOR", i, ":", child)

            elif isinstance(child, Ellipse):
                if found_background_pie:
                    #self.clock_widgets["front_pie"].append(child)
                    self.clock_widgets["front_pie"] = [child]
                else:
                    #self.clock_widgets["back_pie"].append(child)
                    self.clock_widgets["back_pie"] = [child]

                found_background_pie = True
                if self.clock_features['debug'] is True:
                    print("FOUND ELLIPSE", i, ":", child)

            else:
                if self.clock_features['debug'] is True:
                    print("Found SOMETHING", i, ":", child)
            i = i + 1



    def add_pie(self):
        """This is just debug code at this point to test adding a pie programatically
            this does not scale as the window is resized
        """
        #idPIE = self.ids["pie"]
        #self.ids["pieleft"].angle_end=90
        #self.ids.pieleft.angle_end=90
        #print(root.width)
        #print("AAAA=", piewidget.ids)

        #doesn't work
        #Ellipse
        #self.ids['"pie"'].canvas.children[2].angle_start=190
        #self.ids['"pie"'].canvas.children[5].angle_end=90
        #Color
        #self.ids['"pie"'].canvas.children[0].rgba=(.8,.8,.8,.5)


        print("ADDPIE IDS = ", self.ids)
        for key, val in self.ids.items():
            print(f"key={key}: val={val}")
            print(f"VALWIDTH = {val.width}")

        Window.clearcolor = (0,0,0,0)
        #with self.canvas:
        with self.ids['"pie"'].canvas:
            Color(1,1,0)
            diameter = 0.4*Window.width
            #diameter = 0.4*self.height
            Ellipse(
                   pos=(Window.center[0] - (0.5*diameter), Window.center[1] - 0.5 * diameter),
                   id="centerpie",
                   #pos_hint=(1.5,.5),
                   #size=(.75*self.width,.75*self.height),
                   #pos_hint=(2,3),
                   size=(diameter, diameter),
                   angle_start=0,
                   angle_end=180
                   )
            print("In Canvas WIDTH_HINT=", self.size_hint_x)
            print("In Canvas SELF_WIDTH=",self.width)
            print("WINDOW_HEIGHT=",Window.height)
            #print("WIDTH=",rooti#.width)
            print("In Canvas CENTER=",self.center_x)
            print(self.pos_hint)
            #self.canvas.clear()

            #Color(colormap['yellow'])

        #print("bbbbbbbbbbbbbbbbbbbbbb")
        #print("Out Canvas WIDTH_HINT=", self.size_hint_x)
        #print("Out Canvas SELF_WIDTH=",self.width)
        #print("WINDOW_HEIGHT=",Window.height)
        #print("Out Canvas CENTER=",self.center_x)
        #print(self.pos_hint)
        #self.canvas.clear()

        #print(self.newpie.canvas.children)

        #c = FloatLayout()
        #c.size_hint = (1,1)


        #TESTING1 deleting one label/widget
        for label in self.clock_widgets["numbers"]:
            if label.text == "30":
                self.remove_widget(label)
        #END TESTING1

        #DEBUG1: Testing adding string
        ajostring = str("X_size = " + str(self.clock_features['x_size']))
        b_var = Label(text=ajostring)
        b_var.pos = ["40dp","40dp"]
        self.add_widget(b_var)
        #END DEBUG1

    def adjust_pie(self):
        """Modify the outer angle"""
        fraction_left = PieTimer.fraction_left(self)
        #print("FRACTION_LEFT=", fraction_left)

        self.clock_widgets["front_pie"][0].angle_end = fraction_left * 360


    def add_clock_numbers(self, total_num=20):
        """Add Lables for Clock Numbers"""
        self.clock_widgets["numbers"] = []
        if total_num < 0:
            print("Can't have count of clock numbers < 0")
            sys.exit()
        slices=60/total_num
        for i in range(0, total_num):
            number = Label(
                text=str(int(i*slices)),
                font_size="20dp",
                bold=False,
                color=(.3, .6, .7, 1),
                pos_hint={
                    # pos_hint is a fraction in range (0, 1)
                    # this is designed to be used with size_hint: 1,1 (see .kv file)
                    "center_x": .5 + .43*math.sin(2 * math.pi * i/total_num),
                    "center_y": .5 + .43*math.cos(2 * math.pi * i/total_num),
                }
            )
            #keep a dict of widgets for use later
            self.clock_widgets["numbers"].append(number)

            self.add_widget(number)
            #self.ids["face"].add_widget(number)


    def toggle_running(self, widget):
        """Toggle self.running variable here in widget and in App"""
        if self.running:
            self.running = False
            widget.text = " Start "
        else:
            self.running = True
            widget.text = " Stop  "


    def print_debug(self, widget):
        """Print debug code"""
        print("DEBUG: Clockface Running State", self.running)
        print("DEBUG: self: ", self.canvas)
        print("WIDGET=", widget)
        print("CLOCK_FEATURES=", self.clock_features)
        if self.clock_features['debug'] is False:
            self.clock_features['debug'] = 'True'
        else:
            self.clock_features['debug'] = False


    def runclock(self,timesince_last_run=0):
        """When called by Clock.asdf it takes two arguments
        """

        round_seconds_left = round(self.seconds_left, 0)


        if self.running is True:
            if self.countdown is True:
                self.seconds_left = self.seconds_left - timesince_last_run
                #print("DEBUG: ----------RUNNING DOWN")
                self.ids['"hrs"'].text = str(int((round_seconds_left/3600)%24)).rjust(2,"0")
                self.ids['"min"'].text = str(int((round_seconds_left/60)%60)).rjust(2,"0")
                self.ids['"sec"'].text = str(int(round_seconds_left%60)).rjust(2,"0")

                self.adjust_pie()
            else:
                self.seconds_left = self.seconds_left + timesince_last_run
                #print("DEBUG: +++++++++++RUNNING UP")

        if self.clock_features['debug'] is True:
            print("DEBUG LAST=", timesince_last_run)
            print("DEBUG LEFT=", self.seconds_left)

        if self.clock_features['term_ppm'] == 1 \
           and abs(round_seconds_left - self.seconds_left) < .1:
            print(f"{round_seconds_left} seconds left")

        if self.seconds_left <=0:
            if self.clock_features['debug'] is True:
                print("ENDING!!!")
            Clock.unschedule(self.runclock)
            sys.exit()
            #  return False will unschedule the clock too
            #  terminate the program

        return True

        #not >= 0 because we don't want @0 to execute

        #when get to 0 unschedule the Clock event by returning False
        #return False



class PieTimer(App):
    """PieTimer Child Class of App Parent class
    """
    def __init__(self, sys_args, **kwargs):
        super(PieTimer,self).__init__(**kwargs)
        self.args = sys_args
        self.running = True
        self.seconds_left = 0  #Not int. Could be fractions of a second

        self.clock_features = self.setup_args()

        #this sets the variable self.seconds_left based on what is returned by setup_args
        self.set_start_seconds()


        Window.size = (self.clock_features['x_size'], self.clock_features['y_size'])



    #def __init__(self, sys_args):
    #    self.args = sys_args
    #    App.__init__(self)
    #    self.clock_features = self.setup_args()
    #    #self.build()


    def build(self):
        """This is the last setup of the app. All stuff modifying wigets overridden"""
        return AnalogClockFace(clock_features=self.clock_features)
        #b = Label(text="2")
        #self.add_widget(b)
        #return Label(text="Code Button!!!")
        #return Label(text="Code Button 2!!!")
        #return Label(text=str(self.clock_features['x_size']))

    # pylint: disable=too-many-locals
    def setup_args(self):
        """Setup parameters from command line"""
        # There are that many command line options (branches, statements)
        #pylint: disable=too-many-branches
        #pylint: disable=too-many-statements
        #setup the defaults
        quiet = 0
        term_ppm = 0
        terminal_beep = 0
        debug=False
        buttons = False
        console_only = False
        display_numeric = False
        display_current_time = False
        dict_time = {'seconds': 0, 'minutes': 0, 'hours': 0}
        int_x_size = int_y_size = 0
        time_left_color = "red"
        clock_bg_color = "white"
        #If need args uncomment below and replace _ with args
        #args = []
        opts = []
        try:
            opts, _ = getopt.getopt(self.args,
                                    "bdntqh:m:s:x:y:c:",
                                    ["terminal_beep", "quiet", "hours=", "minutes=", "seconds=",
                                     "buttons", "x_size=", "y_size=", "color=", "clock_bg_color=",
                                     "display_current_time", "console_only", "term_ppm",
                                     "display_numeric","debug"]
                                   )
        except getopt.GetoptError:
            print("Usage:\n pietimer.py [Arguments]\n")
            print("Arguments:")
            print("  [--buttons] [-b] Add buttons to control timer")
            print("  [--console_only] Only use the console - not graphical timer")
            print("  [-c <color>] [--color=<color>] Color of time remaining")
            print("  [--clock_bg_color=<color>] Color not filled by timer when seconds <= 60")
            print("  [--debug ] Enable debugging mode and print debugging code to terminal")
            print("  [--help ]   Print Help (this message) and exit")
            print("  [-d ] [--display_numeric]")
            print("  [-h <#>] [--hours=<#>]")
            print("  [-m <#>] [--minutes=<#>]")
            print("  [-n ] [--display_currrent_time]")
            print("  [-s <#>] [--secondss=<#>]")
            print("  [-q or --quiet]  Do not print time left in terminal")
            print("  [--term_ppm] Print to terminal time left each minute")
            print("  [-t or --terminal_beep] Execute a beep at t=0")
            print("  [-x <#xwidth>] [--x_size=<#xwidth>]")
            print("  [-y <#yheight>] [--y_size=<#yheight>]")
            sys.exit(2)

        for opt, arg in opts:
            if opt in ("-h", "--hours"):
                dict_time['hours'] = float(arg)
            elif opt in ("-m", "--minutes"):
                dict_time['minutes'] = float(arg)
            elif opt in ("-s", "--seconds"):
                dict_time['seconds'] = float(arg)
            elif opt in ("-n", "--display_current_time"):
                display_current_time = True
            elif opt in ("-d", "--display_numeric"):
                display_numeric = True
            elif opt in ("--debug"):
                debug = True
            elif opt in ("-x", "--x_size"):
                int_x_size = self.setup_size(arg)
            elif opt in ("-y", "--y_size"):
                int_y_size = self.setup_size(arg)
            elif opt == "--console_only":
                console_only = True
            elif opt in ("-c", "--color"):
                time_left_color = arg
            elif opt == "--clock_bg_color":
                clock_bg_color = arg
            elif opt in ("-t", "--terminal_beep"):
                terminal_beep = 1
            elif opt in ("--term_ppm"):
                term_ppm = 1
            elif opt in ("-q", "--quiet"):
                quiet = 1
            elif opt in ("-b", "--buttons"):
                buttons = True

        int_y_size = self.default_size_check(int_y_size, int_x_size)
        int_x_size = self.default_size_check(int_x_size, int_y_size)

        #Debugging
        if debug is True:
            for opt, arg in opts:
                print("DEBUG: In setup_args: opt,arg =", opt, arg)

        return {'x_size': int_x_size, 'y_size': int_y_size,\
                'quiet': quiet,\
                'term_ppm': term_ppm,\
                'terminal_beep': terminal_beep,\
                'time_left_color': time_left_color,\
                'clock_bg_color': clock_bg_color,\
                'buttons': buttons,\
                'dict_time': dict_time,\
                'exiting': False, \
                'console_only': console_only, \
                'display_numeric': display_numeric, \
                'display_current_time': display_current_time, \
                'debug': debug, \
                'initialized': True
               }

    def default_size_check(self, int_size, other_axis):
        """setup Default window size if size not set"""
        #
        if int_size <= 0 < other_axis:
            int_size = other_axis
        elif self.args == "" or int_size <= 0:
            int_size = 300
        return int_size

    def setup_size(self, size_arg):
        """Setup size of window for program"""
        if size_arg == '%':
            width_px = .5 * self.root_window.winfo_screenwidth()
            int_size = int(width_px)
        else:
            int_size = int(size_arg)
        return int_size

    def fraction_left(self):
        """Calculate fraction of clock to display as time left"""
        if self.seconds_left <= 60:
            fraction_left = self.seconds_left/60
        else:
            fraction_left = (self.seconds_left%3600)/3600

        #always make sure fraction_left has a value > 0
        fraction_left = max(fraction_left, 0)

        return fraction_left

    def set_start_seconds(self):
        """Convert start time parameters to seconds"""

        if self.clock_features['debug'] is True:
            print("IN: set_start_seconds: ", self.clock_features)
        #if everything is 0 then set it to 15 minutes
        if self.clock_features['dict_time']['hours'] == 0 and \
           self.clock_features['dict_time']['minutes'] == 0 and \
           self.clock_features['dict_time']['seconds'] == 0:
            self.clock_features['dict_time']['minutes'] = 15

        #total seconds calculation
        self.seconds_left = self.clock_features['dict_time']['hours']*3600 + \
                        self.clock_features['dict_time']['minutes']*60 + \
                        self.clock_features['dict_time']['seconds']

        return self.seconds_left


#initiate class and run
if __name__ == "__main__":
    PieTimer(sys.argv[1:]).run()
    #PieTimer().run()
    sys.exit(0)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
