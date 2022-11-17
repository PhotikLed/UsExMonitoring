import datetime
import random
import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget
from pyqt5_plugins.examplebuttonplugin import QtGui
from cpu_and_gpu_monitoring import Ui_Form
from PyQt5 import uic
import sys
import wmi
import subprocess
import pythoncom

from db import add_monitoring


class Monitoring(QWidget, Ui_Form):
    def __init__(self, time: str, parent=None):
        super().__init__(parent)
        self.parameters = None

        self.setupUi(self)
        self.time = time
        self.thread = Finder(self.time)
        self.thread.start()

        self.cpu_graphic = []
        self.gpu_graphic = []
        self.setWindowIcon(QtGui.QIcon('icon2.png'))

        self.thread.sinout.connect(self.get_value)
        self.thread.finished.connect(self.save_data)

    def get_value(self, cpu, gpu):
        self.cpu_graphic.append(cpu)
        self.gpu_graphic.append(gpu)
        self.update_data()

    def update_data(self):
        self.CPU_graphicsView.clear()
        self.GPU_graphicsView.clear()
        self.CPU_graphicsView.plot([i for i in range(len(self.cpu_graphic))], self.cpu_graphic, pen='g')
        self.GPU_graphicsView.plot([i for i in range(len(self.gpu_graphic))], self.gpu_graphic, pen='r')

    def save_data(self):
        t = str(datetime.datetime.now())
        add_monitoring(t, self.cpu_graphic, self.gpu_graphic)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.thread.exit()


class Finder(QThread):
    sinout = pyqtSignal(int, int)

    def __init__(self, time, parent=None):
        super(Finder, self).__init__(parent)
        self.time = time

    def run(self):
        # pythoncom.CoInitialize()
        # command = r'Start-Process -WindowStyle hidden ' \
        #           r'"C:\Users\sotka\PycharmProjects\UeXDiagnoSYS\OpenHardwareMonitor\OpenHardwareMonitor" '
        # subprocess.Popen(command)
        print('start monitoring')
        start_time = time.time()
        # gpu_temperature = 0
        # try:
        #     w = wmi.WMI(namespace="OpenHardwareMonitor")
        #     temperature_infos = w.Sensor()
        #     for sensor in temperature_infos:
        #         print(sensor.Name)
        #         if sensor.SensorType == u'Temperature' and 'GPU' in sensor.Name:
        #             gpu_temperature = sensor.Value
        # except:
        #     gpu_temperature = 0

        while time.time() - start_time < self.time:
            # cpu_temperature = []
            # w = wmi.WMI(namespace="OpenHardwareMonitor")
            # temperature_infos = w.Sensor()
            # for sensor in temperature_infos:
            #     print(sensor.Name)
            #     if sensor.SensorType == u'Temperature' and 'Core' in sensor.Name:
            #         cpu_temperature.append(int(sensor.Value))
            #
            # cpu_temperature = sum(cpu_temperature) // len(cpu_temperature)
            #
            # if gpu_temperature:
            #     for sensor in temperature_infos:
            #         if sensor.SensorType == u'Temperature' and 'GPU' in sensor.Name:
            #             gpu_temperature = int(sensor.Value)

            cpu_temperature = random.randint(40, 100)
            gpu_temperature = random.randint(40, 100)
            self.sinout.emit(cpu_temperature, gpu_temperature)
            print('emit value')
            time.sleep(1)
        print('end monitoring')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
