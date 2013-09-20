import Base
import Logger

from Device import *
from Item import *
from Generator import TimeInfo, RndGen

items = [0] * Base.number_of_items
device_list = [0] * Base.number_of_devices


def construct():
    """ Set next processing and admission initial values"""
    Base.next_processing_init_value = RndGen.get_random(Base.processing_init_value)
    Base.next_admission_init_value = RndGen.get_random(Base.admission_init_value)


def init_devices():
    """ Devices initialization """
    for i in range(0, Base.number_of_devices):
        device_list[i] = Device()


def check(device):
    """ Check Device state """
    if not device.state:
        return True
    else:
        return False


def item_to_device():
    """ Send item to device """
    for device in device_list:
        if check(device) is True and len(Base.stack) > 0:
            busy_item = Base.stack[0]
            device.state = True
            device.free_time = busy_item.processing_time
            device.end_time = TimeInfo.now() + device.free_time
            Logger.avg_wait_time_stack(busy_item)
            Logger.avg_wait_time_work(busy_item)
            Logger.add_to_time_hash(busy_item.processing_time, TimeInfo.now() + busy_item.processing_time)
            Base.stack.pop()
            Base.ad_counter += 1
        clear_device(device)


def clear_device(device):
    """ Clean the device """
    if TimeInfo.now() >= device.end_time:
        device.state = False
        device.end_time = 0


def create_item(i):
    """ Create the item """
    if TimeInfo.now() >= Base.next_time:
        Base.prc_time_list.append(RndGen.get_avg_random(Base.avg_processing_time,
                                                        RndGen.normalize(Base.next_processing_init_value)))
        items[i] = Item(RndGen.get_avg_random(Base.avg_processing_time,
                                              RndGen.normalize(Base.next_processing_init_value)))
        Base.next_processing_init_value = RndGen.get_random(Base.next_processing_init_value)
        Base.counter += 1
        Base.sum_processing_time += items[i].processing_time
        Base.array_proc.append(items[i].processing_time)
        Base.disp_proc.append(items[i].processing_time)
        if len(Base.stack) < Base.capacity:
            Base.stack.append(items[i])
            items[i].enter_stack_time = TimeInfo.now()
        else:
            Base.rejected_stack.append(items[i])
        set_timeout()
        print "counter: %s " % Base.counter

def set_timeout():
    if TimeInfo.now() >= Base.next_time:
        Base.adm_time_list.append(RndGen.get_avg_random(Base.avg_admission_time,
                                                        RndGen.normalize(Base.next_admission_init_value)))
        Base.tmp_time = RndGen.get_avg_random(Base.avg_admission_time,
                                              RndGen.normalize(Base.next_admission_init_value))
        Base.next_admission_init_value = RndGen.get_random(Base.next_admission_init_value)
        Base.next_time = TimeInfo.now() + Base.tmp_time
        Base.sum_admission_time += Base.tmp_time
        Base.array_adm.append(Base.tmp_time)
        Base.disp_adm.append(Base.tmp_time)

def reset():
    """ reset to default Base values"""

    #variables
    Base.event_model = True
    Base.end = False
    Base.first_show = True
    Base.start = False
    Base.out = False
    Base.system_is_active = False
    Base.reset_flag = True
    Base.repeat = False
    Base.counter = 0
    Base.ad_counter = 0
    Base.tmp_time = 0
    Base.next_time = 0
    Base.time_start = 0
    Base.cur_time = 0
    Base.end_time = 0
    Base.glob_time = 0
    Base.sum_admission_time = 0
    Base.sum_processing_time = 0
    Base.next_admission_init_value = 0
    Base.next_processing_init_value = 0
    Base.total = 0
    Base.disp_adm = []
    Base.disp_proc = []
    Base.total_disp_adm = 0
    Base.total_disp_proc = 0
    Base.stack = []
    Base.active_devices = []
    Base.rejected_stack = []
    Base.array_adm = []
    Base.array_proc = []

    #outputs
    Base.r = 0.0
    Base.sT = 0.0
    Base.qT = 0.0
    Base.sN = 0.0
    Base.qN = 0.0
    Base.avg_adm_time = 0.0
    Base.avg_prc_time = 0.0
    Base.aC = 0.0
    Base.rC = 0.0

    #for graphs
    Base.adm_time_list = []
    Base.prc_time_list = []
    Base.hist_adm_x = []
    Base.hist_adm_y = []
    Base.hist_proc_x = []
    Base.hist_proc_y = []
