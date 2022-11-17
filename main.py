import random

import wmi
import os
import sys
import csv
import subprocess
import wget
import sqlite3

from PyQt5.QtGui import QColor
from pyqt5_plugins.examplebuttonplugin import QtGui

from db import init_db, get_monitoring_info
from types_of_DDR import types_of_DDR
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QFileDialog, QInputDialog, QDialog, \
    QCheckBox, QButtonGroup
from main_us_ex import Ui_MainWindow
from monitoring import Monitoring
from result_monitoring import Ui_Form

from time_dialog import Ui_Dialog


class Helper(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.computer = wmi.WMI()
        self.show_current_cond()
        self.currentButton.clicked.connect(self.show_current_cond)
        self.confButton.clicked.connect(self.write_configuration)
        self.installButton.clicked.connect(self.download_user_programs)
        self.monitorButton.clicked.connect(self.boost_dialog)

        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.conf.triggered.connect(self.open_conf_dialog)
        self.monitor.triggered.connect(self.open_monitor_dialog)

    def show_current_cond(self):
        self.current_moment.clear()
        self.label.setText('Информация о текущем компьютере')
        self.currentButton.setVisible(False)
        computer_info = self.computer.Win32_ComputerSystem()[0]
        os_info = self.computer.Win32_OperatingSystem()[0]
        proc_info = self.computer.Win32_Processor()[0]  # About processor
        # print(computer_info)
        # print(proc_info)
        # print(os_info)
        proc_name = proc_info.Name
        proc_cores = proc_info.NumberofCores
        proc_threads = proc_info.ThreadCount
        proc_l2 = proc_info.L2CacheSize
        proc_l3 = proc_info.L3CacheSize

        gpu_info = self.computer.Win32_VideoController()[0]  # About GPU
        print(gpu_info)

        gpu_name = gpu_info.Name
        gpu_memory = int(gpu_info.AdapterRAM / 10240000)  # Неясно как работает
        monitor_resolution = 'x'.join(map(str,
                                          [gpu_info.CurrentHorizontalResolution, gpu_info.CurrentVerticalResolution]))

        os_name = os_info.Name.encode('utf-8').split(b'|')[0]  # About Operating System
        os_version = ' '.join([os_info.Version, os_info.BuildNumber])
        os_arch = os_info.OSArchitecture
        model = computer_info.Model

        ram_type = str(subprocess.run('wmic memorychip get ConfiguredVoltage',  # About RAM
                                      capture_output=True).stdout)
        ram_slots = str(subprocess.run('wmic memphysical get MemoryDevices',
                                       capture_output=True).stdout)
        ram_slots = ram_slots.split()[1].lstrip('\\r\\r\\n')
        ram_voltage = ram_type.split()[1].lstrip('\\r\\r\\n')
        ram_ddr = types_of_DDR[ram_voltage]
        ram_count = ram_type.count(ram_voltage)
        system_ram = int(int(os_info.TotalVisibleMemorySize) / 1024000)  # KB to GB

        self.parameters = ['Процессор: ' + proc_name,
                           "Число ядер процессора: " + str(proc_cores),
                           "Потоков: " + str(proc_threads),
                           'Объем кэша второго уровня: ' + str(proc_l2) + ' КБ',
                           'Объем кэша третьего уровня: ' + str(proc_l3) + ' КБ',
                           'Видеокарта: ' + gpu_name,
                           "Разрешение экрана: " + monitor_resolution,
                           'Объём оперативной памяти: ' + str(system_ram) + " ГБ",
                           'Число планок оперативной памяти: ' + str(ram_count),
                           'Число слотов оперативной памяти: ' + ram_slots,
                           'Тип оперативной памяти: ' + ram_ddr,
                           'Название операционной системы: ' + os_name.decode('utf-8'),
                           "Версия операционной системы: " + os_version,
                           'Архитектура операционной системы: ' + os_arch,
                           'Модель устройства: ' + model

                           ]

        for p in self.parameters:
            self.current_moment.appendPlainText(
                p
            )

    def write_configuration(self):

        name, ok = QInputDialog.getText(self, 'Как назвать?', 'Введите название файла:')
        if not name:
            name = 'conf'
        with open(name + '.txt', encoding='utf-8', mode='w+') as con:
            print(*self.parameters, file=con, sep='\n')

    def download_user_programs(self):
        newpath = r'C:\Программы для пользователя'

        if not os.path.exists(newpath):
            os.makedirs(newpath)
        with open('programs.csv', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            programs = []
            for line in reader:
                name = line[0]
                url = line[1]
                programs.append(name)

                ind = url.split('.')[-1]
                wget.download(url, newpath + fr'\{name}.{ind}')
            QMessageBox.about(self, 'Внимание', f'Программой временно пользоваться нельзя. '
                                                f'\nСейчас скачиваются необходимые программы')
            QMessageBox.blockSignals(self, True)
            programs = ', '.join(programs)
            QMessageBox.about(self, 'Ура', f'Программа по скачиванию файлов завершила свою работу.'
                                           f'Были скачаны следующие программы: {programs}\n'  # Ща
                                           f'Теперь откройте папку по адресу "{newpath}"'
                                           f' и установите все программы в ней')

    def open_conf_dialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Выберите файл конфигурации', '',
                                            'Текстовый файл (*.txt);;')[0]
        self.current_moment.clear()
        with open(fname, encoding='utf-8') as conf_file:
            reader = conf_file.readlines()
            for line in reader:
                self.current_moment.appendPlainText(line.rstrip('\n'))
            self.label.setText('Информация о компьютере пользователя')
        self.currentButton.setVisible(True)

    def open_monitor_dialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Выберите файл мониторинга', '',
                                            'База данных (*.db);;')[0]
        print(fname)
        self.show_mon = ShowingMonitoring(fname)
        self.show_mon.show()

    def boost_dialog(self):
        self.dialog = TimeDialog()
        self.dialog.show()


class TimeDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.window_monitoring)

    def window_monitoring(self):

        time = self.min_spinBox.value() * 60 + self.sec_spinBox.value()

        self.mon = Monitoring(time)
        self.mon.show()


class ShowingMonitoring(QWidget, Ui_Form):
    def __init__(self, db_name):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon2.png'))
        self.db_name = db_name
        self.cbx = []
        self.dateButtonGroup = QButtonGroup(self)
        self.dateButtonGroup.setExclusive(False)
        self.CPU_boxes = {}
        self.GPU_boxes = {}
        self.dateButtonGroup.buttonClicked.connect(self.show_data)
        self.CPU_graphicsView.addLegend()
        self.GPU_graphicsView.addLegend()
        self.swap_dates()

    def swap_dates(self):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        self.dates = cur.execute('SELECT * FROM monitoring_ids').fetchall()
        print(self.dates)
        for i, date in self.dates:
            self.cbx.append(QCheckBox(date, self))
            self.dateButtonGroup.addButton(self.cbx[-1])
            self.horizontalLayout.addWidget(self.cbx[-1])
        con.close()

    def show_data(self, boxname: QCheckBox):
        name = boxname.text()
        if boxname.isChecked():
            CPU_temperatures, GPU_temperatures = get_monitoring_info(self.db_name, name)
            CPU_color = random.randint(100, 256), random.randint(100, 256), random.randint(100, 256)
            GPU_color = random.randint(100, 256), random.randint(100, 256), random.randint(100, 256)

            CPU_item = self.CPU_graphicsView.plot([i for i in range(len(CPU_temperatures))],
                                                  CPU_temperatures, pen=QColor(*CPU_color), name=name)
            GPU_item = self.GPU_graphicsView.plot([i for i in range(len(GPU_temperatures))],
                                                  GPU_temperatures, pen=QColor(*GPU_color), name=name)

            self.CPU_boxes[name] = CPU_item
            self.GPU_boxes[name] = GPU_item

        else:
            self.CPU_graphicsView.removeItem(self.CPU_boxes[name])
            self.GPU_graphicsView.removeItem(self.GPU_boxes[name])

            del self.CPU_boxes[name]
            del self.GPU_boxes[name]


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    init_db()
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = Helper()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
