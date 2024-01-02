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
#Uncomment the following to avoid having to call with "--" before program args
#os.environ["KIVY_NO_ARGS"] = "1"
#pylint: disable=wrong-import-position
import sys
import getopt
import math
from kivy.utils import platform
from kivy.config import Config
from kivy.app import App
from kivy.clock import Clock
#from kivy.uix.label import Label
#from kivy.uix.widget import Widget
from kivy.uix.pagelayout import PageLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
#from kivy.utils import colormap
from kivy.graphics import Color, Ellipse
#from kivy.properties import DictProperty, BooleanProperty
from kivy.properties import ObjectProperty #pylint: disable=no-name-in-module
from kivy.properties import NumericProperty #pylint: disable=no-name-in-module
from kivy.properties import StringProperty, BooleanProperty #pylint: disable=no-name-in-module
from kivy.core.window import Window
if platform == 'linux':
    #os.environ['input_mouse_%(name)s'] = ''
    Config.set('input', '%(name)s', '')
    Config.set("graphics", "always_on_top", 1)  # The app will start with the window on top
    #print(f"PLATFORM={platform}")

#Uncomment the below to get NO messages at all from Kivy to the console
#os.environ["KIVY_NO_CONSOLELOG"] = "1"


class AnalogClockFace(FloatLayout): #pylint: disable=too-many-instance-attributes
    """Kivy requires defining args passed in before init"""
    # See https://kivy.org/doc/stable/api-kivy.properties.html?highlight=properties
    # Properties: To declare properties, you must declare them at the class level.
    #   The class will then do the work to instantiate the real attributes when
    #   your object is created. These properties are not attributes: they are
    #    mechanisms for creating events based on your attributes:
    #   e.g. clockp_dict = DictProperty({})
    #   e.g. ajoaasdf = StringProperty("hello world")
    str_hours = StringProperty("00")
    str_min = StringProperty("00")
    str_sec = StringProperty("00")
    running = BooleanProperty(True)
    top_opacity = NumericProperty(0)
    f_angle_end = NumericProperty(275)
    ajotest = NumericProperty(Window.width)

    #for using .kv file
    def __init__(self, clock_features=None, **kwargs):
        super().__init__(**kwargs)
        ##the above is the same as super(AnalogClockFace,self)....

        #is it possible to only have these in class PieTimer?
        if clock_features is None:
            clock_features = {'initialized': False, 'debug': False}
        self.running = True
        self.seconds_left = 0.0   #could be a fraction of a second
        self.start_seconds = 0.0   #could be a fraction of a second
        self.countdown = True
        self.clock_interval = .1
        self.repeat = 0
        #clockface clock_widgets (numbers around edge)
        self.clock_widgets = {}
        self.top_opacity = 0
        self.f_angle_end = 275
        self.ajotest = Window.width
        if platform == 'linux':
            Window.always_on_top = True

        if clock_features['debug'] is True:
            #print(f"kivy version = {kivy.__version__}")
            print("DEBUG: AnalogClock clock_features=", clock_features)
            self.ids['"debug_button"'].opacity = 1
            self.ids['"debug_button"'].disabled = False

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
            self.repeat = self.clock_features['total_repeat']
            if self.clock_features['debug'] is True:
                print(f"XWIDTH NOW = {clock_features['initialized']}")
            #add_clock_numbers: puts a series of numbers around the clock/pie
            #  Divisble by 60: 2, *4, 3, 5, 10, *12, 15, *20
            #  these together are interesting
            #  self.add_clock_numbers(4)
            #  self.add_clock_numbers(10)

            self.define_pie_widgets()

            #Note: Changed from calling the widget to a StringProperty
            #self.ids['"hrs"'].text =
            self.str_hours = str(round(self.seconds_left/3600)%24)

            #self.ids['"min"'].text =
            self.str_min = str(round(self.seconds_left/60)%60)

            #self.ids['"sec"'].text =
            self.str_sec = str(round(self.seconds_left)%60)


    #def on_size(self, *args):
    #    """Todo: Unused: change stuff on resizing window"""
    #    print(args)
    #    radius = 0.4*min(Window.width,Window.height)/2
    #    self.pie_timeleft_widget.pos = (self.center_x - radius, self.center_y - radius)

    def define_pie_widgets(self):
        """Setup the dict of elipses (self.clock_widgets) to identify for operations later"""
        #self.root.ids.pie.
        if self.clock_features['debug'] is True:
            #print("IDSPIE = ", self.ids['"pie"'].canvas.children[1].rgba)
            print("IDSPIE = ", self.ids['"pie"'].canvas)
            # Doesn't work
            #print("IDSPIE2 = ", self.ids['pie'])


        # Kivy Canvas elements are identified by "group" not by "id"
        self.clock_widgets["back_pie"] = self.ids['"pie"'].canvas.get_group('back_pie')
        self.clock_widgets["front_pie"] = self.ids['"pie"'].canvas.get_group('fore_pie')


        # Obsoleted by above group. Now debugging if you want to iterate
        #   self.ids['"pie"'].canvas.children[0]
        if self.clock_features['debug'] is True:
            i = 0
            found_background_pie = False

            for child in self.ids['"pie"'].canvas.children:
                if isinstance(child, Color):
                    if self.clock_features['debug'] is True:
                        print("FOUND COLOR", i, ":", child)

                elif isinstance(child, Ellipse):
                    if found_background_pie:
                        #self.clock_widgets["front_pie"].append(child)
                        #Obsoleted by group (see above)
                        #self.clock_widgets["front_pie"] = [child]
                        print("FOUND ELLIPSE BG", i, ":", child)
                    else:
                        #self.clock_widgets["back_pie"].append(child)
                        #Obsoleted by group (see above)
                        #self.clock_widgets["back_pie"] = [child]
                        print("FOUND ELLIPSE BG", i, ":", child)

                    found_background_pie = True
                    if self.clock_features['debug'] is True:
                        print("FOUND ELLIPSE", i, ":", child)

                else:
                    if self.clock_features['debug'] is True:
                        print("Found SOMETHING", i, ":", child)
                i = i + 1



    def update_clock_numbers(self,label,angle):
        """Unused: This is a failed attempt to get the numbers to resize with the window"""
        pie_radius_factor = .74
        label.pos = (Window.width / 2 * (1 + 1.1 * pie_radius_factor * math.sin (angle)),
                Window.height / 2 + 1.1 * pie_radius_factor * (Window.width / 2) * math.cos (angle))


class PieTimer(App): #pylint: disable=too-many-instance-attributes
    """PieTimer Child Class of App Parent class
    """
    acf_object = ObjectProperty(None)
    def __init__(self, sys_args, **kwargs):
        super().__init__(**kwargs)
        self.args = sys_args

        self.clock_features = self.setup_args()
        self.running = True
        self.seconds_left = 0.0   #could be a fraction of a second
        self.start_seconds = 0.0   #could be a fraction of a second
        self.countdown = True
        self.clock_interval = .1
        self.repeat = 0

        #this sets the variable self.seconds_left based on what is returned by setup_args
        self.set_start_seconds()


        #don't set size of window on mobile devices
        #if kivy.utils.platform == 'linux' or kivy.utils.platform == 'win':
        #    if self.clock_features['debug'] is True:
        #        print(f"sys.platform={sys.platform}")
        #else:
        #    if Window.width > Window.height:
        #        self.clock_features['x_size'] = Window.height
        #        self.clock_features['y_size'] = Window.height
        #    else:
        #        self.clock_features['x_size'] = Window.width
        #        self.clock_features['y_size'] = Window.width

        if self.clock_features['debug'] is True:
            print(f"sys.platform={sys.platform}")
            print(f"platform={sys.platform}")
        if platform == "android":
            if Window.width > Window.height:
                self.clock_features['x_size'] = Window.height
                self.clock_features['y_size'] = Window.height
            else:
                self.clock_features['x_size'] = Window.width
                self.clock_features['y_size'] = Window.width
            Window.maximize()
        else:
            Window.size = (self.clock_features['x_size'], self.clock_features['y_size'])

         #run this until it returns False
        if self.clock_features['debug'] is True:
            self.clock_interval = 1
        self.myclock = Clock.schedule_interval(self.runclock, self.clock_interval)

        #can we change the interval to be 1 sec if sec_left>60?

        if self.clock_features['debug'] is True:
            print("DEBUG: RIGHT AFTER Clock.schedule------------")
        # Alternatively set event_run = Clock...
        #     and then to stop use event_run.cancel() or Clock.unschedule(event_run)



    #def __init__(self, sys_args):
    #    self.args = sys_args
    #    App.__init__(self)
    #    self.clock_features = self.setup_args()
    #    #self.build()


    def build(self):
        """Pietimer. This is the last setup of the app. All stuff modifying wigets overridden"""
        page_layout = PageLayout()
        box_layout_txt = BoxLayout()
        #create a pie timer widget and addit to the first page
        self.acf_object = AnalogClockFace(clock_features=self.clock_features)
        page_layout.add_widget(self.acf_object)
        # Create stuff and add it to a second PageLayout Page
        textin_h = TextInput(text=self.acf_object.str_hours,  #HOW TO BIND text to str_hours????
                            font_size=Window.width/6,
                            multiline=False,
                            halign="center",
                            write_tab=False
                    )
        #both self. and app. give accurate time, but does not change. Binding? 
        textin_m = TextInput(text=app.acf_object.str_min,
                            font_size=Window.width/6,
                            multiline=False,
                            halign="center",
                            write_tab=False
                    )
        textin_s = TextInput(text=app.acf_object.str_sec,
                            font_size=Window.width/6,
                            multiline=False,
                            halign="center",
                            write_tab=False
                    )
        box_layout_txt.add_widget(textin_h)
        box_layout_txt.add_widget(textin_m)
        box_layout_txt.add_widget(textin_s)
        page_layout.add_widget(box_layout_txt)

        #return this entire thing
        return page_layout
        #return self.acf_object
        #b = Label(text="2")
        #self.add_widget(b)
        #return Label(text="Code Button!!!")
        #return Label(text="Code Button 2!!!")
        #return Label(text=str(self.clock_features['x_size']))

    # pylint: disable=too-many-locals
    def setup_args(self):
        """Pietimer. Setup parameters from command line"""
        # There are that many command line options (branches, statements)
        #pylint: disable=too-many-branches
        #pylint: disable=too-many-statements
        #setup the defaults
        quiet = 0
        total_repeat = 0
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
                                    "bdntqh:m:s:x:y:c:r:",
                                    ["terminal_beep", "quiet", "hours=", "minutes=", "seconds=",
                                     "buttons", "x_size=", "y_size=", "color=", "clock_bg_color=",
                                     "display_current_time", "console_only", "term_ppm",
                                     "display_numeric","debug","repeat="]
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
            print("  [-r <#> or --repeat <#> ]  Repeat the countdown # times")
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
            elif opt in ("-r", "--repeat"):
                total_repeat = int(arg)
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
                'total_repeat': total_repeat,\
                'dict_time': dict_time,\
                'exiting': False, \
                'console_only': console_only, \
                'display_numeric': display_numeric, \
                'display_current_time': display_current_time, \
                'debug': debug, \
                'initialized': True
               }

    def default_size_check(self, int_size, other_axis):
        """Pietimer. setup Default window size if size not set"""
        #
        if int_size <= 0 < other_axis:
            int_size = other_axis
        elif self.args == "" or int_size <= 0:
            int_size = 300
        return int_size

    def setup_size(self, size_arg):
        """Pietimer. Setup size of window for program"""
        if size_arg == '%':
            width_px = .5 * self.root_window.winfo_screenwidth()
            int_size = int(width_px)
        else:
            int_size = int(size_arg)
        return int_size

    def adjust_pie(self):
        """Pietimer. Modify the outer angle"""
        #fraction_left = self.fraction_left()
        #print("FRACTION_LEFT=", fraction_left)

        #Note: front_pie is .py, fore_pie is .kv
        #self.acf_object.clock_widgets["front_pie"][0].angle_end = self.fraction_left() * 360
        self.acf_object.f_angle_end = self.fraction_left() * 360
        #print("front_pie=", self.acf_object.clock_widgets["front_pie"][0].angle_end )

    def fraction_left(self):
        """Pietimer. Calculate fraction of clock to display as time left"""
        if self.seconds_left <= 60:
            fraction_left = self.seconds_left/60
        else:
            fraction_left = (self.seconds_left%3600)/3600

        #always make sure fraction_left has a value > 0
        fraction_left = max(fraction_left, 0)

        return fraction_left

    def set_start_seconds(self):
        """Pietimer. Convert start time parameters to seconds"""

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

        self.start_seconds = self.seconds_left
        return self.seconds_left

    def runclock(self,delta_t=0):
        """Pietimer. When called by Clock.asdf it takes two arguments
        """

        round_seconds_left = round(self.seconds_left, 0)


        if self.running is True:
            if self.countdown is True:
                self.seconds_left = self.seconds_left - delta_t
                #print("DEBUG: ----------RUNNING DOWN")
                #Note: Changed from calling the widget to a StringProperty
                #self.ids['"hrs"'].text =
                self.acf_object.str_hours = str(int((round_seconds_left/3600)%24)).rjust(2,"0")
                #self.ids['"min"'].text =
                self.acf_object.str_min = str(int((round_seconds_left/60)%60)).rjust(2,"0")
                #self.ids['"sec"'].text =
                self.acf_object.str_sec = str(int(round_seconds_left%60)).rjust(2,"0")

                if self.clock_features['term_ppm'] == 1 \
                   and abs(round_seconds_left - self.seconds_left) < .1:
                    print(f"{round_seconds_left} seconds left")

                self.adjust_pie()
            else:
                #To Do: count up feature
                self.seconds_left = self.seconds_left + delta_t
                #print("DEBUG: +++++++++++RUNNING UP")

        if self.clock_features['debug'] is True:
            print("DEBUG LAST=", delta_t)
            print("DEBUG LEFT=", self.seconds_left)
            print("DEBUG REPEAT=", self.repeat)
            print("DEBUG self.RUNNING=", self.running)

        if self.seconds_left <=0:
            if self.clock_features['debug'] is True:
                print("ENDING or REPEATING!!!")
            #Handle Repeat flag if set
            self.repeat = self.repeat - 1
            if self.repeat >= 1:
                if self.clock_features['debug'] is True:
                    print("DEBUG REPEAT=", self.repeat)
                self.seconds_left = self.start_seconds
                return True

            Clock.unschedule(self.runclock)
            sys.exit()
            #  return False will unschedule the clock too
            #  terminate the program

        return True

        #not >= 0 because we don't want @0 to execute

        #when get to 0 unschedule the Clock event by returning False
        #return False

    def toggle_running(self, widget):
        """Pietimer. Toggle self.running variable here in widget and in App"""
        #acf_object is the class, top_opacity is the numeric property
        if self.running:
            self.running = False
            self.acf_object.running = False
            self.myclock.cancel()
            self.acf_object.top_opacity = 1
            widget.text = " Start "
        else:
            self.running = True
            self.acf_object.running = True
            self.acf_object.top_opacity = 0
            widget.text = " Stop  "
            self.myclock = Clock.schedule_interval(self.runclock, self.clock_interval)

    def set_new_time(self, widget):  #pylint: disable=unused-argument
        """Pietimer. If user updates any hr,min,sec update seconds left"""
        try:
            self.seconds_left = int(self.acf_object.ids['"sec_top"'].text) + \
                60*int(self.acf_object.ids['"min_top"'].text) + \
                3600*int(self.acf_object.ids['"hrs_top"'].text)
            #self.seconds_left = int(widget.text) + \
            #    60*int(widget.text) + \
            #    3600*int(widget.text)
        except (TypeError, ValueError):
            #do nothing
            #print("not an int")
            self.acf_object.ids['"hrs_top"'].text = "00"

        self.start_seconds = self.seconds_left
        self.adjust_pie()

        if self.clock_features['debug'] is True:
            print("IDS=",self.acf_object.ids)
            print("HRS=",self.acf_object.ids['"hrs_top"'].text)
            print(self.acf_object.ids['"min_top"'].text)
            print(self.acf_object.ids['"sec_top"'].text)
            print(self.seconds_left)
            print("===========================")
            print("START=",self.start_seconds)

        #print(widget.parent.parent.parent.ids.obj.ids['"hrs_top"'].text)
        #for id, value in self.ids.items():
        #    if value.__self__ == widget:
        #        print(f"ID={id}")
        #    else:
        #        print(f"NOT={id}")
        #PieTimer.set_start_seconds(self)

    def print_debug(self, widget):
        """Pietimer. Print debug code"""
        print("DEBUG: App State", self.running)
        print("DEBUG: acf_object: ", self.acf_object.running)
        print("DEBUG: self: ", self.acf_object.canvas)
        print("WIDGET=", widget)
        print("CLOCK_FEATURES=", self.clock_features)
        #perhaps change this to a toggle button
        #if self.clock_features['debug'] is False:
        #    self.clock_features['debug'] = 'True'
        #else:
        #    self.clock_features['debug'] = False



#initiate class and run
if __name__ == "__main__":
    __version__ = "1.1.7"
    #Use variable app so we can call it from .kv file
    app = PieTimer(sys.argv[1:])
    app.run()
    sys.exit(0)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
