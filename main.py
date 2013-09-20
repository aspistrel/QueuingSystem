#coding=utf-8
import clr

clr.AddReference('System')
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Threading')

from System.Windows.Forms import Application
from System.Threading import Thread, ThreadStart

import work
import logger
import base
import gui
import export

from generator import *

def event_thread():
    """ Logic thread """
    while base.reset_flag:
        while not base.out:
            if base.start:
                try:
                    TimeInfo.init_time()
                    work.construct()
                    work.init_devices()
                    while base.system_is_active is True and work.items:
                        TimeInfo.init_now()
                        if not base.end:
                            base.cur_time = TimeInfo.now() - base.time_start
                            work.create_item(base.counter)
                            work.item_to_device()
                        if TimeInfo.now() >= base.total:
                            logger.stack_items_count()
                            logger.work_items_count()
                            logger.add_coef_per_time()
                            base.total = TimeInfo.now()
                            base.total += base.interval
                        if work.items[base.number_of_items - 1] != 0:
                            break
                finally:
                    print "====== STATISTICS ======"
                    print "end time: %f" % (TimeInfo.now() - base.time_start)
                    print "counter: %d" % base.counter
                    print "ad_counter: %d" % base.ad_counter
                    base.end = True
                    base.system_is_active = False
                    base.end_time = base.cur_time
                    base.out = True
                    logger.print_avg()
                    logger.print_disp()
                    logger.print_interval()
                    logger.print_items_in_stack()
                    logger.print_items_in_work()
                    logger.print_avg_wait_time_stack()
                    logger.print_avg_wait_time_work()
                    logger.print_absolute()
                    logger.print_relative()
                    logger.print_hi_intervals_adm()
                    logger.print_hi_intervals_proc()
                    if base.freeze_outputs is not True:
                        export.output_html()
                        print "Export was successfully finished"
                    print "Done"


def gui_thread():
    """ GUI thread """
    try:
        Application.EnableVisualStyles()
        form = gui.MyForm()
        Application.Run(form)
    finally:
        print "Done"

def console_mode():
    """ Run program one time with default values without GUI """
    base.start = True
    base.system_is_active = True

print "Begin"
""" uncomment for console_mode """
#console_mode()
#t_event = Thread(ThreadStart(event_thread))
#t_event.Start()

""" uncomment for GUI mode """
t_event = Thread(ThreadStart(event_thread))
t_gui = Thread(ThreadStart(gui_thread))
t_event.Start()
t_gui.Start()

