import math

#constants
a = 630360016
m = math.pow(2, 31.0) - 1
capacity = 30
interval = 50
multiplier = 0.1
number_of_items = 1000
number_of_devices = 10
avg_admission_time = 20
avg_processing_time = 60
admission_init_value = 216
processing_init_value = 1455


#variables
event_model = True
end = False
first_show = True
start = False
out = False
system_is_active = False
reset_flag = True
freeze_outputs = False
repeat = False
counter = 0
ad_counter = 0
tmp_time = 0	
next_time = 0
time_start = 0
cur_time = 0
end_time = 0
glob_time = 0
sum_admission_time = 0
sum_processing_time = 0
next_admission_init_value = 0
next_processing_init_value = 0
total = 0
disp_adm = []
disp_proc = []
total_disp_adm = 0
total_disp_proc = 0
stack = []
active_devices = []
rejected_stack = []
array_adm = []
array_proc = []

#outputs
r = 0.0
sT = 0.0
qT = 0.0
sN = 0.0
qN = 0.0
avg_adm_time = 0.0
avg_prc_time = 0.0
aC = 0.0
rC = 0.0

#for graphs
adm_time_list = []
prc_time_list = []
hist_adm_x = []
hist_adm_y = []
hist_proc_x = []
hist_proc_y = []

