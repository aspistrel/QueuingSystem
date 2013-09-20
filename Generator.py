import clr
import math
import Base
import Work

from System import DateTime


class TimeInfo():
    """ Class for work with time """
    @staticmethod
    def now():
        """ Get current time """
        if Base.event_model:
            return Base.glob_time
        else:
            return (DateTime.UtcNow - DateTime(2013, 1, 1)).TotalSeconds / Base.multiplier

    @staticmethod
    def init_now():
        """ Initialize current time """
        if Base.event_model:
            Base.glob_time = TimeInfo.get_closest_time() + Base.time_start

    @staticmethod
    def init_time():
        """ Set initialization time """
        Base.time_start = TimeInfo.now()

    @staticmethod
    def get_closest_time():
        """ Get time closest to next event """
        closest_generate_time = Base.next_time
        closest_log_prev_time = Base.total

        tmp = Work.device_list
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
        return (Base.a * var) % Base.m

    @staticmethod
    def normalize(var):
        return var / Base.m

    @staticmethod
    def get_avg_random(k, var):
        return -k * math.log(var)