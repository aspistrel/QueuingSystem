#coding=utf-8
import clr

clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System.Drawing import *
from System.Windows.Forms import Form, Button, Label, TextBox, Timer

import base
import work

class MyForm(Form):
    def create_button(self, name, text, x_pos, y_pos, on_click_action):
        """ Create windows forms element Button """
        self.name = Button()
        self.name.Parent = self
        self.name.Text = text
        self.name.Location = Point(x_pos, y_pos)
        self.name.Click += on_click_action
        return self.name

    def create_label(self, name, text, x_pos, y_pos, width, height):
        """ Create windows forms element Label """
        self.name = Label()
        self.name.Parent = self
        self.name.Text = text
        self.name.Location = Point(x_pos, y_pos)
        self.name.Width = width
        self.name.Height = height
        return self.name

    def create_textbox(self, name, text, x_pos, y_pos):
        """ Create windows forms element TextBox """
        self.name = TextBox()
        self.name.Parent = self
        self.name.Text = str(text)
        self.name.Location = Point(x_pos, y_pos)
        return self.name

    def __init__(self):
        """ Create child controls and initialize form """
        self.Text = 'Simulation v1.2'
        self.Width = 500
        self.Height = 500
        self.CenterToScreen()

        #timer
        self.timer = Timer()
        self.timer.Interval = 10
        self.timer.Tick += self.OnTick
        self.timer.Start()

        #buttons
        self.start_btn = self.create_button("start_btn", "СТАРТ", 10, 400, self.OnStart)
        self.stop_btn = self.create_button("stop_btn", "СТОП", 100, 400, self.OnStop)
        #self.reset_btn = self.create_button("reset_btn", "РЕЗЕТ", 370, 400, self.OnShow)
        self.vis_btn = self.create_button("vis_btn", "ВИЗУАЛ", 190, 400, self.OnSimulation)
        self.exit_btn = self.create_button("exit_btn", "ВЫХОД", 280, 400, self.OnExit)

        #lables
        #---- output info
        self.r_l = self.create_label("r_l", "r: ", 50, 45, 40, 12)
        self.Ts_l = self.create_label("Ts_l", "Ts: ", 50, 85, 40, 12)
        self.Tq_l = self.create_label("Tq_l", "Tq: ", 50, 125, 40, 12)
        self.Ns_l = self.create_label("Ns_l", "Ns: ", 50, 165, 40, 12)
        self.Nq_l = self.create_label("Nq_l", "Nq: ", 50, 205, 40, 12)
        self.Ca_l = self.create_label("Ca_l", "Cr: ", 50, 245, 40, 12)
        self.Cr_l = self.create_label("Cr_l", "Ca: ", 50, 285, 40, 12)
        #---- modify info
        self.dc_l = self.create_label("dc_l", u"Устройства: ", 200, 45, 140, 12)
        self.ic_l = self.create_label("ic_l", u"Заявки: ", 200, 85, 140, 12)
        self.aa_l = self.create_label("aa_l", u"Сред t поступления: ", 200, 125, 140, 12)
        self.ap_l = self.create_label("ap_l", u"Сред t обработки: ", 200, 165, 140, 12)
        self.cap_l = self.create_label("cap_l", u"Емкость: ", 200, 205, 140, 12)
        self.init_a_l = self.create_label("init_a_l", u"Случ знач  A: ", 200, 245, 140, 12)
        self.init_p_l = self.create_label("init_p_l", u"Случ знач  Б: ", 200, 285, 140, 12)
        #---- dynamic info
        self.cur_time_l = self.create_label("cur_time_l", u"Время: ", 350, 200, 60, 12)
        self.cur_time = self.create_label("cur_time", str(base.cur_time), 420, 200, 60, 12)
        self.cur_count_l = self.create_label("cur_count_l", u"Заявки: ", 350, 220, 60, 12)
        self.cur_count = self.create_label("cur_count", str(base.counter), 420, 220, 60, 12)
        self.devices_l = self.create_label("devices_l", u"Устройства: \n система не активна", 350, 40, 180, 180)
        self.stack_l = self.create_label("stack_l", u"Стек: ", 20, 350, 400, 50)

        #textboxes
        #---- output info
        self.r = self.create_textbox("r", base.r, 50, 60)
        self.Ts = self.create_textbox("Ts", base.sT, 50, 100)
        self.Tq = self.create_textbox("Tq", base.qT, 50, 140)
        self.Ns = self.create_textbox("Ns", base.sN, 50, 180)
        self.Nq = self.create_textbox("Nq", base.qN, 50, 220)
        self.Ca = self.create_textbox("Cr", base.aC, 50, 260)
        self.Cr = self.create_textbox("Ca", base.rC, 50, 300)
        #---- modify info
        self.dc = self.create_textbox("dc", base.number_of_devices, 200, 60)
        self.ic = self.create_textbox("ic", base.number_of_items, 200, 100)
        self.aa = self.create_textbox("aa", base.avg_admission_time, 200, 140)
        self.ap = self.create_textbox("ap", base.avg_processing_time, 200, 180)
        self.cap = self.create_textbox("cap", base.capacity, 200, 220)
        self.init_a = self.create_textbox("init_a", base.admission_init_value, 200, 260)
        self.init_p = self.create_textbox("init_p", base.processing_init_value, 200, 300)

    def OnTick(self, sender, event):
        """ Take actions per tick """
        self.update()
        #if Base.freeze_outputs is not True:
        self.result()
        self.devices_l.Text = u"Устройства: \n система не активна"
        if base.system_is_active:
            self.stack_l.Text = u"Стек: "
            self.devices_l.Text = u"Устройство: \n"
            self.cur_time.Text = "%s" % str(base.cur_time)
            self.cur_count.Text = "%s" % str(base.counter)
            if base.cur_time >= 0.5:
                for i in range(0, len(work.device_list)):
                    if work.device_list[i].state:
                        self.devices_l.Text += u"устройство " + str(i + 1) + u" ...... занято \n"
                    else:
                        self.devices_l.Text += u"устройство " + str(i + 1) + u" ...... свободно \n"
                self.stack_l.Text += "X " * len(base.stack) + "0 " * (base.capacity - len(base.stack))
        else:
            self.set_constants()


    def OnStart(self, sender, args):
        """ Start the program """
        work.reset()
        base.start = True
        base.system_is_active = True
        base.out = True

    def OnStop(self, sender, args):
        """ Stop simulation """
        base.system_is_active = False
        self.cur_time.Text = "%s" % str(base.cur_time)
        self.cur_count.Text = "%s" % str(base.counter)

    def OnShow(self, sender, args):
        """ Show values """
        base.repeat = False

    def OnSimulation(self, sender, args):
        """ Run real-time simulation  """
        work.reset()
        self.set_constants()
        base.start = True
        base.system_is_active = True
        base.out = True
        base.event_model = False
        base.freeze_outputs = True

    def OnExit(self, sender, event):
        """ Exit the program """
        base.system_is_active = False
        self.Close()

    def set_constants(self):
        """ Set constants values from Base """
        base.admission_init_value = int(self.init_a.Text)
        base.processing_init_value = int(self.init_p.Text)
        base.capacity = int(self.cap.Text)
        base.avg_admission_time = int(self.aa.Text)
        base.avg_processing_time = int(self.ap.Text)
        base.number_of_devices = int(self.dc.Text)
        base.number_of_items = int(self.ic.Text)
        work.items = [0] * base.number_of_items
        work.device_list = [0] * base.number_of_devices

    def result(self):
        """ Show the resulting values """
        self.r.Text = str(base.r)
        self.Ts.Text = str(base.sT)
        self.Tq.Text = str(base.qT)
        self.Ns.Text = str(base.sN)
        self.Nq.Text = str(base.qN)
        self.Ca.Text = str(base.aC)
        self.Cr.Text = str(base.rC)

    def update(self):
        """ Update current time and number of requests """
        self.cur_count.Text = str(base.counter)
        self.cur_time.Text = str(base.cur_time)
