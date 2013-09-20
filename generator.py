import clr
import math
import base
import work

from System import DateTime


class TimeInfo():
    """ Class for work with time """
    @staticmethod
    def now():
        """ Get current time """
        if base.event_model:
            return base.glob_time
        else:
            return (DateTime.UtcNow - DateTime(2013, 1, 1)).TotalSeconds / base.multiplier

    @staticmethod
    def init_now():
        """ Initialize current time """
        if base.event_model:
            base.glob_time = TimeInfo.get_closest_time() + base.time_start

    @staticmethod
    def init_time():
        """ Set initialization time """
        base.time_start = TimeInfo.now()

    @staticmethod
    def get_closest_time():
        """ Get time closest to next event """
        closest_generate_time = base.next_time
        closest_log_prev_time = base.total

        tmp = work.device_list
        if tmp[0] is not 0:
            closest_device_time = sorted(tmp, key=lambda device: device.end_time)[0].end_time
        else:
            closest_device_time = 0

        if closest_device_time == 0:
            closest_device_time = closest_generate_time

        return_value = closest_generate_time

        if closest_device_time < return_value:
            return_value = closest_device_time

        if closest_log_prev_time < return_value:
            return_value = closest_log_prev_time
        return return_value


class RndGen():
    """ Random generator """
    @staticmethod
    def get_random(var):
        return (base.a * var) % base.m

    @staticmethod
    def normalize(var):
        return var / base.m

    @staticmethod
    def get_avg_random(k, var):
        return -k * math.log(var)