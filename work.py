import base
import logger

from device import *
from item import *
from generator import TimeInfo, RndGen

items = [0] * base.number_of_items
device_list = [0] * base.number_of_devices


def construct():
    """ Set next processing and admission initial values"""
    base.next_processing_init_value = RndGen.get_random(base.processing_init_value)
    base.next_admission_init_value = RndGen.get_random(base.admission_init_value)


def init_devices():
    """ Devices initialization """
    for i in range(0, base.number_of_devices):
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
        if check(device) is True and len(base.stack) > 0:
            busy_item = base.stack[0]
            device.state = True
            device.free_time = busy_item.processing_time
            device.end_time = TimeInfo.now() + device.free_time
            logger.avg_wait_time_stack(busy_item)
            logger.avg_wait_time_work(busy_item)
            logger.add_to_time_hash(busy_item.processing_time, TimeInfo.now() + busy_item.processing_time)
            base.stack.pop()
            base.ad_counter += 1
        clear_device(device)


def clear_device(device):
    """ Clean the device """
    if TimeInfo.now() >= device.end_time:
        device.state = False
        device.end_time = 0


def create_item(i):
    """ Create the item """
    if TimeInfo.now() >= base.next_time:
        base.prc_time_list.append(RndGen.get_avg_random(base.avg_processing_time,
                                                        RndGen.normalize(base.next_processing_init_value)))
        items[i] = Item(RndGen.get_avg_random(base.avg_processing_time,
                                              RndGen.normalize(base.next_processing_init_value)))
        base.next_processing_init_value = RndGen.get_random(base.next_processing_init_value)
        base.counter += 1
        base.sum_processing_time += items[i].processing_time
        base.array_proc.append(items[i].processing_time)
        base.disp_proc.append(items[i].processing_time)
        if len(base.stack) < base.capacity:
            base.stack.append(items[i])
            items[i].enter_stack_time = TimeInfo.now()
        else:
            base.rejected_stack.append(items[i])
        set_timeout()
        print "counter: %s " % base.counter

def set_timeout():
    if TimeInfo.now() >= base.next_time:
        base.adm_time_list.append(RndGen.get_avg_random(base.avg_admission_time,
                                                        RndGen.normalize(base.next_admission_init_value)))
        base.tmp_time = RndGen.get_avg_random(base.avg_admission_time,
                                              RndGen.normalize(base.next_admission_init_value))
        base.next_admission_init_value = RndGen.get_random(base.next_admission_init_value)
        base.next_time = TimeInfo.now() + base.tmp_time
        base.sum_admission_time += base.tmp_time
        base.array_adm.append(base.tmp_time)
        base.disp_adm.append(base.tmp_time)

def reset():
    """ reset to default Base values"""

    #variables
    base.event_model = True
    base.end = False
    base.first_show = True
    base.start = False
    base.out = False
    base.system_is_active = False
    base.reset_flag = True
    base.repeat = False
    base.counter = 0
    base.ad_counter = 0
    base.tmp_time = 0
    base.next_time = 0
    base.time_start = 0
    base.cur_time = 0
    base.end_time = 0
    base.glob_time = 0
    base.sum_admission_time = 0
    base.sum_processing_time = 0
    base.next_admission_init_value = 0
    base.next_processing_init_value = 0
    base.total = 0
    base.disp_adm = []
    base.disp_proc = []
    base.total_disp_adm = 0
    base.total_disp_proc = 0
    base.stack = []
    base.active_devices = []
    base.rejected_stack = []
    base.array_adm = []
    base.array_proc = []

    #outputs
    base.r = 0.0
    base.sT = 0.0
    base.qT = 0.0
    base.sN = 0.0
    base.qN = 0.0
    base.avg_adm_time = 0.0
    base.avg_prc_time = 0.0
    base.aC = 0.0
    base.rC = 0.0

    #for graphs
    base.adm_time_list = []
    base.prc_time_list = []
    base.hist_adm_x = []
    base.hist_adm_y = []
    base.hist_proc_x = []
    base.hist_proc_y = []
