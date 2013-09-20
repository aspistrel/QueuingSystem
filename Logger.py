import operator
import Base
import Work
import math

from Generator import TimeInfo

items_in_stack = {}
items_in_work = {}
proc_time_hash = {}
coefs_per_time = {}
sorted_items_in_stack = []
sorted_items_in_work = []
sorted_coefs_per_time = []
wait_time_stack = []
wait_time_work = []
sum_time = 0


def stack_items_count():
    """ Number of items in stack """
    items_in_stack[(TimeInfo.now() - Base.time_start)] = float(len(Base.stack))


def work_items_count():
    """ The number of items in the service process """
    for device in Work.device_list:
        if device.state is True:
            Base.active_devices.append(device)
    items_in_work[(TimeInfo.now() - Base.time_start)] = float(len(Base.stack) + len(Base.active_devices))
    Base.active_devices = []


def print_items_in_stack():
    """ Print number of items in stack """
    sum_values = 0
    for key, value in items_in_stack.iteritems():
        sum_values += value
    print str(sum_values) + " / " + str(len(items_in_stack))
    Base.qN = sum_values / len(items_in_stack)
    print "Nq: %d " % Base.qN


def print_items_in_work():
    """ Print number of items in the service process """
    sum_values = 0
    for key, value in items_in_work.iteritems():
        sum_values += value
    Base.sN = sum_values / len(items_in_work)
    print "Ns: %d" % Base.sN


def print_avg():
    """ Print average values of admission time and processing time """
    print "avg_adm: %f" % float(Base.sum_admission_time / Base.number_of_items)
    Base.avg_adm_time = float(Base.sum_admission_time / Base.number_of_items)
    print "avg_prc: %f" % float(Base.sum_processing_time / Base.number_of_items)
    Base.avg_prc_time = float(Base.sum_processing_time / Base.number_of_items)


def print_disp():
    """ Print dispersion """
    adm_result = 0
    proc_result = 0
    for el in Base.disp_adm:
        adm_result += int((el - Base.avg_adm_time) ** 2)
    for el in Base.disp_proc:
        proc_result += int((el - Base.avg_adm_time) ** 2)
    Base.total_disp_adm = float(float(adm_result)/(Base.number_of_items - 1))
    Base.total_disp_proc = float(float(proc_result)/(Base.number_of_items - 1))
    print "disp_adm: " + str(float(adm_result)/(Base.number_of_items - 1))
    print "disp_proc: " + str(float(proc_result)/(Base.number_of_items - 1))


def print_interval():
    """ Print intervals """
    tmp_adm = (Base.total_disp_adm/Base.number_of_items) ** 0.5
    tmp_proc = (Base.total_disp_proc/Base.number_of_items) ** 0.5
    print "interval_adm: "
    print Base.avg_adm_time - 1.9623*tmp_adm
    print Base.avg_adm_time + 1.9623*tmp_adm
    print "interval_proc: "
    print Base.avg_prc_time - 1.9623*tmp_proc
    print Base.avg_prc_time + 1.9623*tmp_proc



def add_to_time_hash(proc_time, finish_time):
    proc_time_hash[proc_time] = finish_time


def get_coefficient():
    """ Get coefficient of efficiency of the system """
    counter = 0
    tmp_counter = 0
    for key, value in proc_time_hash.iteritems():
        if value > TimeInfo.now():
            tmp_counter = key - (value - TimeInfo.now())
        else:
            tmp_counter = key
        counter += tmp_counter
    if TimeInfo.now() > 0:
        Base.r = float(counter) / float(((TimeInfo.now() - Base.time_start) * Base.number_of_devices))
    else:
        Base.r = 0


def avg_wait_time_stack(item):
    """ Adding to list waiting time of item in stack """
    wait_time_stack.append(TimeInfo.now() - item.enter_stack_time)


def print_avg_wait_time_stack():
    """ Calculate and print the average waiting time of item in stack """
    sum = 0
    for el in wait_time_stack:
        sum += el
    Base.qT = sum / len(wait_time_stack)
    print "Tq = " + str(sum) + " / " + str(len(wait_time_stack))
    print "Tq: %f" % Base.qT


def avg_wait_time_work(item):
    """ Adding to list waiting time of item in service process """
    wait_time_work.append((TimeInfo.now() - item.enter_stack_time) + item.processing_time)


def print_avg_wait_time_work():
    """ Calculate and print the average waiting time of item in service process """
    sum = 0
    for el in wait_time_work:
        sum += el
    Base.sT = sum / len(wait_time_work)
    print "Ts: %f" % Base.sT


def print_absolute():
    """ Calculate and print absolute bandwidth """
    print str(Base.ad_counter) + " / (" + str(Base.counter) + " + " + str(len(Base.rejected_stack)) + ")"
    print float(Base.ad_counter / (Base.counter + len(Base.rejected_stack)))
    Base.aC = float(float(Base.ad_counter) / (float(Base.counter) + float(len(Base.rejected_stack))))
    print "Ca: %f" % Base.aC


def print_relative():
    """ Calculate and print relative bandwidth """
    Base.rC = Base.ad_counter / Base.end_time
    print "Cr: %f" % Base.rC


def get_count_sum_stack(time):
    """ Calculates for graph of the average number of claims in the queue at the time """
    return_double = 0
    for item in sorted_items_in_stack:
        return_double += item[1]
        if item[0] == time:
            return return_double
    return return_double


def get_count_sum_work(time):
    """ Calculates for graph of the average number of claims in the system at the time """
    return_double = 0
    for item in sorted_items_in_work:
        return_double += item[1]
        if item[0] == time:
            return return_double
    return return_double


def sorted_dict_keys(dictionary):
    return sorted(dictionary.iteritems(), key=operator.itemgetter(0))


def add_coef_per_time():
    """ Coefficient value per time (for graphs) """
    get_coefficient()
    coefs_per_time[(TimeInfo.now() - Base.time_start)] = Base.r


def get_correlation_adm(array, j):
    """ Get correlation of admission time """
    k = 0.
    n = len(array)
    mu = Base.avg_admission_time

    i = 0
    while i < (n - j):
        k += (array[i] - mu) * (array[i + j] - mu)
        i += 1

    k = k / (n - j)

    return k / Base.total_disp_adm


def get_correlation_proc(array, j):
    """ Get correlation of processing time """
    k = 0.
    n = len(array)
    mu = Base.avg_processing_time

    i = 0
    while i < (n - j):
        k += (array[i] - mu) * (array[i + j] - mu)
        i += 1

    k = k / (n - j)

    return k / Base.total_disp_proc


def hi_square_adm():
    """ Formula for admission time Hi^2 """
    return (max(Base.array_adm) - min(Base.array_adm)) / 17


def hi_square_proc():
    """ Formula for processing time Hi^2 """
    return (max(Base.array_proc) - min(Base.array_proc)) / 17


def get_hi(min, max,array):
    """ Get Hi """
    return_count = 0
    for el in array:
        if min <= el < max:
            return_count += 1
    return return_count


def print_hi_intervals_adm():
    """ Print Hi intervals for admission time """
    start_int_adm = 0
    end_int_adm = hi_square_adm()
    i = 1
    out = 0
    while i < 18:
        intervalProbability = (-math.exp(-end_int_adm / Base.avg_admission_time)) - (-math.exp(-start_int_adm / Base.avg_admission_time))
        hi = get_hi(start_int_adm, end_int_adm, Base.array_adm)
        out += ((hi - Base.number_of_items * intervalProbability) ** 2) / (Base.number_of_items * intervalProbability)
        Base.hist_adm_y.append(hi)
        Base.hist_adm_x.append((end_int_adm - start_int_adm)/2 + start_int_adm)
        i += 1
        start_int_adm += hi_square_adm()
        end_int_adm += hi_square_adm()


def print_hi_intervals_proc():
    """ Print Hi interval for processing time """
    start_int_proc = 0
    end_int_proc = hi_square_proc()
    i = 1
    out = 0
    while i < 18:
        intervalProbability = (-math.exp(-end_int_proc / Base.avg_processing_time)) - (-math.exp(-start_int_proc / Base.avg_processing_time))
        hi = get_hi(start_int_proc, end_int_proc, Base.array_proc)
        out += ((hi - Base.number_of_items * intervalProbability) ** 2) / (Base.number_of_items * intervalProbability)
        Base.hist_proc_y.append(hi)
        Base.hist_proc_x.append((end_int_proc - start_int_proc)/2 + start_int_proc)
        i += 1
        start_int_proc += hi_square_proc()
        end_int_proc += hi_square_proc()


