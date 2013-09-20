#coding=utf-8
import clr

clr.AddReference('System')
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Threading')

from System.Windows.Forms import Application
from System.Threading import Thread, ThreadStart

import Work
import Logger
import Base
import GUI
import Export

from Generator import *

def event_thread():
    """ Logic thread """
    while Base.reset_flag:
        while not Base.out:
            if Base.start:
                try:
                    TimeInfo.init_time()
                    Work.construct()
                    Work.init_devices()
                    while Base.system_is_active is True and Work.items:
                        TimeInfo.init_now()
                        if not Base.end:
                            Base.cur_time = TimeInfo.now() - Base.time_start
                            Work.create_item(Base.counter)
                            Work.item_to_device()
                        if TimeInfo.now() >= Base.total:
                            Logger.stack_items_count()
                            Logger.work_items_count()
                            Logger.add_coef_per_time()
                            Base.total = TimeInfo.now()
                            Base.total += Base.interval
                        if Work.items[Base.number_of_items - 1] != 0:
                            break
                finally:
                    print "====== STATISTICS ======"
                    print "end time: %f" % (TimeInfo.now() - Base.time_start)
                    print "counter: %d" % Base.counter
                    print "ad_counter: %d" % Base.ad_counter
                    Base.end = True
                    Base.system_is_active = False
                    Base.end_time = Base.cur_time
                    Logger.print_avg()
                    Logger.print_disp()
                    Logger.print_interval()
                    Logger.print_items_in_stack()
                    Logger.print_items_in_work()
                    Logger.print_avg_wait_time_stack()
                    Logger.print_avg_wait_time_work()
                    Logger.print_absolute()
                    Logger.print_relative()
                    Logger.print_hi_intervals_adm()
                    Logger.print_hi_intervals_proc()
                    if Base.freeze_outputs is not True:
                        Export.output_html()
                        print "Export was successfully finished"
                    print "Done"


def gui_thread():
    """ GUI thread """
    try:
        Application.EnableVisualStyles()
        form = GUI.MyForm()
        Application.Run(form)
    finally:
        print "Done"

print "Begin"
t_event = Thread(ThreadStart(event_thread))
t_gui = Thread(ThreadStart(gui_thread))
t_event.Start()
#Base.start = True
#Base.system_is_active = True
#Base.out = True
t_gui.Start()

