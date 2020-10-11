import sys
from string import ascii_uppercase
import os
import re
import datetime
import manipulation as mp
import pandas as pd

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtWidgets import QFormLayout
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import (QWidget, QPushButton,QMainWindow,
                             QHBoxLayout, QApplication,QAction,QFileDialog)


# try:
#     db = 'stock.db'
#     conn = mp.dbActions(db)
#     df = pd.read_csv(os.path.join(os.getcwd(), "sample_db_test_data.csv")).to_sql("BioSamples", conn, if_exists="replace")
#     conn.commit()
# except Exception:
#     print('DB exists')


class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.textName = QtWidgets.QLineEdit(self)
        self.textPass = QtWidgets.QLineEdit(self)
        self.buttonLogin = QtWidgets.QPushButton('Admin Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)


    def handleLogin(self):
        if (self.textName.text() == 'Admin' and
            self.textPass.text() == '1234'):
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Bad user or password')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.st = Container0()
        self.setCentralWidget(self.st)

        self.exitAct = QAction(QIcon('exit_icon.png'), 'Exit', self)
        self.exitAct.setShortcut('Ctrl+W')
        self.exitAct.setStatusTip('Exit application')

        self.statusBar()
        self.setWindowTitle('Schrage Lab Sample Inventory')
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(self.exitAct)

        self.signals()

    def signals(self):
        # exit action
        self.exitAct.triggered.connect(self.close)


class Container0(QWidget):
    def __init__(self):

        super(Container0, self).__init__()

        db = 'biosample_db.db'
        self.db = mp.dbActions(db)

        # make main widget objects
        self.inventory_table = QWidget()
        self.form_fields = QWidget()
        self.box_diagram = QWidget()

        # functions for objects
        self.createInventoryTable()
        self.createFormFields()
        self.createBoxDiagram()

        # bottom layout
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addWidget(self.form_fields)
        self.bottom_layout.addWidget(self.box_diagram)

        # main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.inventory_table, 9)
        self.main_layout.addLayout(self.bottom_layout, 1)

        # TODO: adjust widget sizes

        # set the main layout
        self.setLayout(self.main_layout)

        # add signals
        self.signals() 

        # set initial values
        self.initial_values()


    def createInventoryTable(self):
        self.table = QTableWidget()
        layout = QVBoxLayout()

        col_names = ['Study',
                     'Visit',
                     'Time Point',
                     'Sample ID',
                     'Sample Date',
                     'Quantity',
                     'Box Color',
                     'Box ID',
                     'Grid Location',
                     'Freezer',
                     'Shelf',
                     'Last Checked By',
                     ]
        self.table.setColumnCount(len(col_names))
        self.table.setHorizontalHeaderLabels(col_names)
        for col in range(0, len(col_names)):
            # self.table.setItem(0, col, QTableWidgetItem(col_names[col]))
            # TODO: make column width relative? expand?
            self.table.setColumnWidth(col, 100)
        # TODO: call initial search query to populate table
        self.show_search()

        layout.addWidget(self.table)
        self.inventory_table.setLayout(layout)


    def createFormFields(self):
        layout = QFormLayout()
        hbox = QHBoxLayout()

        # check-in radio button
        self.checkin = QRadioButton()
        self.checkin.setText("Check-In")
        hbox.addWidget(self.checkin)

        # checkout radio button
        self.checkout = QRadioButton()
        self.checkout.setText("Checkout")
        hbox.addWidget(self.checkout)
        layout.addRow("Status", hbox)

        # study combobox
        self.study = QComboBox()
        layout.addRow("Study", self.study)

        # study visit combobox
        self.visit = QComboBox()
        layout.addRow("Study Visit", self.visit)

        # time point
        self.time_point = QComboBox()
        layout.addRow("Time Point", self.time_point)

        # sample ID
        self.sample_id = QLineEdit()
        msg = "Do not include the study number"
        self.sample_id.setStatusTip(msg)
        layout.addRow("Sample ID", self.sample_id)

        # sample quantity
        self.quantity = QSpinBox()
        self.quantity.setMinimum(1)
        layout.addRow("Sample Quantity (in tubes)", self.quantity)

        # grid location
        self.grid_location = QLineEdit()
        msg = "Enter alphanumeric locations separated by a comma"
        self.grid_location.setStatusTip(msg)
        layout.addRow("Grid Location", self.grid_location)

        # box color
        self.box_color = QComboBox()
        layout.addRow("Sample Box Color", self.box_color)

        # box ID
        self.box_id = QSpinBox()
        self.box_id.setMinimum(1)
        layout.addRow("Sample Box ID", self.box_id)

        # freezer
        self.freezer = QComboBox()
        layout.addRow("Freezer", self.freezer)

        # shelf
        self.shelf = QComboBox()
        layout.addRow("Shelf", self.shelf)

        # checked in/out by
        self.personnel = QComboBox()
        layout.addRow("Checked by:", self.personnel)

        # date checked in/out
        self.sample_date = QCalendarWidget()
        layout.addRow("Sample Date", self.sample_date)

        # add sample
        self.add_sample = QPushButton('Add Sample', self)
        layout.addWidget(self.add_sample)

        self.form_fields.setLayout(layout)


    def createBoxDiagram(self):
        self.box = QTableWidget()
        layout = QVBoxLayout()

        row_names = list(ascii_uppercase[0:11])
        self.box.setRowCount(len(row_names))
        self.box.setColumnCount(len(row_names))
        self.box.setRowCount(len(row_names))
        self.box.setAlternatingRowColors(True)
        self.box.setVerticalHeaderLabels(row_names)
        # for row in range(0, len(row_names)):
        #     self.box.setColumnWidth(row, 50)
        layout.addWidget(self.box)
        self.box_diagram.setLayout(layout)


    def signals(self):
        # check-in radio button signal
        self.checkin.toggled.connect(self.on_status_btn_changed)

        # checkout radio button signal
        self.checkout.toggled.connect(self.on_status_btn_changed)

        # study combobox signal
        self.study.currentTextChanged.connect(self.on_study_combobox_changed)

        # visit combobox signal
        self.visit.currentTextChanged.connect(self.on_visit_combobox_changed)

        # freezer combobox signal
        self.freezer.currentTextChanged.connect(self.on_freezer_combobox_changed)

        # add sample signal
        self.add_sample.clicked.connect(self.on_add_sample_click)
        # TODO: add signal for 'enter' being pressed; keyEvent

        # search button for view samples
        # self.srb.clicked.connect(self.show_search)


    def on_status_btn_changed(self):
        if self.checkin.isChecked() == True:
            msg = f"{self.checkin.text()} Samples"
            self.add_sample.setText(msg)
        else:
            msg = f"{self.checkout.text()} Samples"
            self.add_sample.setText(msg)


    def on_study_combobox_changed(self, text):
        # add visits
        try:
            self.visit.clear()
            self.visit.addItems(self.study_visit_data[text])
            self.visit.setCurrentIndex(0)
        except:
            msg = f"Study visits not defined for {text}"
            self.error_dialog(msg)

        # add box colors
        try:
            self.box_color.clear()
            self.box_color.addItems(self.box_color_data[text])
            self.box_color.setCurrentIndex(0)
        except:
            msg = f"Box colors not defined for {text}"
            self.error_dialog(msg)


    def on_visit_combobox_changed(self, text):
        # add time points
        try:
            self.time_point.clear()
            self.time_point.addItems(self.visit_time_data[text])
            self.time_point.setCurrentIndex(0)
        except:
            if text != "":
                msg = f"Time points not defined for {text}"
                self.error_dialog(msg)


    def on_freezer_combobox_changed(self, text):
        try:
            self.shelf.clear()
            self.shelf.addItems(self.freezer_data[text])
            self.shelf.setCurrentIndex(0)
        except:
            if text != "":
                msg = f"Shelves not defined for {text}"
                self.error_dialog(msg)


    def on_add_sample_click(self):
        def validation():
            if self.study.currentText() == "":
                msg = "Please select a study"
                self.error_dialog(msg)
                return 1
            if self.visit.currentText() == "":
                msg = "Please select a visit"
                self.error_dialog(msg)
                return 1
            if self.time_point.currentText() == "":
                msg = "Please select a time point"
                self.error_dialog(msg)
                return 1
            if self.sample_id.text() == "":
                msg = "Please enter the Sample ID"
                self.error_dialog(msg)
                return 1
            if self.quantity.text() == "":
                msg = "Please enter the sample quantity"
                self.error_dialog(msg)
                return 1
            if self.grid_location.text() == "":
                msg = "Please enter grid location(s) for the samples"
                self.error_dialog(msg)
                return 1
            else:
                quantity = int(self.quantity.text())
                grid_locations = self.grid_location.text().replace(" ", "").split(",")
                grid_count = len(grid_locations)

                if quantity != grid_count:
                    msg = f"The sample count and grid locations are not equal\n" \
                          f"{quantity} samples entered\n" \
                          f"{grid_count} locations entered"
                    self.error_dialog(msg)
                    return 1

                # return all valid grid locations
                regex = r"([a-k](?:[1-9]|1[0-1]))\b"
                p = re.compile(regex, re.IGNORECASE)

                for location in grid_locations:
                    result = p.match(location)
                    if result is None:
                        msg = f"Invalid input {location}"
                        self.error_dialog(msg)
                        return 1
            if self.box_color.currentText() == "":
                msg = "Please select a sample box color"
                self.error_dialog(msg)
                return 1
            if self.box_id == "":
                msg = "Please enter a sample box ID"
                self.error_dialog(msg)
                return 1
            if self.freezer.currentText() == "":
                msg = "Please select a freezer"
                self.error_dialog(msg)
                return 1
            if self.shelf.currentText() == "":
                msg = "Please select a freezer shelf"
                self.error_dialog(msg)
                return 1
            if self.personnel.currentText() == "":
                msg = "Please select a lab member"
                self.error_dialog(msg)
                return 1
            if self.sample_date.selectedDate() == "":
                msg = "Please select the sample date"
                self.error_dialog(msg)
                return 1


        result = validation()

        if result is not None:
            pass
        else:
            # pack into dictionary
            kwargs = {
                'study': self.study.currentText(),
                'visit': self.visit.currentText(),
                'time_point': self.time_point.currentText(),
                'sample_id': self.sample_id.text(),
                'quantity': self.quantity.text(),
                'grid_locations': list(self.grid_location.text().replace(" ", "").split(',')),
                'box_color': self.box_color.currentText(),
                'box_id': self.box_id.text(),
                'freezer': self.freezer.currentText(),
                'shelf': self.shelf.currentText(),
                'personnel': self.personnel.currentText(),
                'sample_date': self.sample_date.selectedDate().toPyDate().strftime('%m/%d/%Y')
            }

            if self.checkin.isChecked() == True:
                self.db.insert_sample(**kwargs)
            else:
                self.db.remove_sample(**kwargs)


    def call_red(self):
        now = datetime.datetime.now()
        stock_red_date_time = now.strftime("%Y-%m-%d %H:%M")
        stock_name = self.stock_name_red.text().replace(' ','_').lower()
        try:
            stock_val = -(int(self.stock_count_red.text()))
            print(stock_val)
            print(type(stock_val))
            # mp.update_quantity(stock_name, stock_val, stock_red_date_time)
        except Exception:
            print('Exception')


    def call_add(self):
        now = datetime.datetime.now()
        stock_call_add_date_time = now.strftime("%Y-%m-%d %H:%M")
        stock_name = self.stock_name_add.text().replace(' ','_').lower()
        stock_val = int(self.stock_count_add.text())
        # mp.update_quantity(stock_name, stock_val, stock_call_add_date_time)


    def show_search(self):
        pass
        # delete current table rows
        # if self.table.rowCount() > 1:
        #     for i in range(1, self.table.rowCount()):
        #         self.table.removeRow(1)
        #
        #
        # # x_act = mp.show_stock()
        # x = []
        # # if self.conf_text.text() != '':
        # #     for i in range(0,len(x_act)):
        # #         a = list(x_act[i])
        # #         if self.conf_text.text().lower() in a[0].lower():
        # #             x.append(a)
        # # else:
        # #     x = mp.show_stock()
        # db = "stock.db"
        # # x = mp.dbActions.create_connection(db)
        #
        # if len(x)!=0:
        #     for i in range(1, len(x) + 1):
        #         self.table.insertRow(i)
        #         lst = list(x[i-1])
        #         self.table.setItem(i, 0, QTableWidgetItem(str(lst[0])))
        #         self.table.setItem(i, 1, QTableWidgetItem(str(lst[1])))
        #         self.table.setItem(i, 2, QTableWidgetItem(str(lst[2])))
        #         self.table.setRowHeight(i, 50)
        #
        #
        #     self.lbl3.setText('Viewing Sample Database.')
        # else:
        #     self.lbl3.setText('No valid information in database.')


    def show_trans_history(self):
        if self.Trans.rowCount()>1:
            for i in range(1,self.Trans.rowCount()):
                self.Trans.removeRow(1)

        path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'transaction.txt')
        if os.path.exists(path):
            tsearch = open(path, 'r')
            x_c = tsearch.readlines()
            tsearch.close()
            x = []
            if self.trans_text.text() != '':
                key = self.trans_text.text()
                for i in range(0,len(x_c)):
                    a = x_c[i].split(" ")
                    name = a[0]
                    action = a[-2]
                    if (key.lower() in name.lower()) or (key.lower() in action.lower()) :
                        x.append(a)
            else:
                x = x_c.copy()

            for i in range(0,len(x)):
                x.sort(key=lambda a: a[4])
            #print(x)
            tid = 1900001
            for i in range(1,len(x)+1):
                self.Trans.insertRow(i)

                a = x[i-1].split(" ")
                if a[-2] == 'UPDATE':
                    p = 'Quantity of Stock Changed from '+a[1]+' to '+a[2]
                elif a[-2] == 'INSERT':
                    p = 'Stock added with Quantity : '+a[1]+' and Cost(Per Unit in Rs.) : '+a[2]
                elif a[-2] == 'REMOVE':
                    p = 'Stock information deleted.'
                else:
                    p = 'None'


                self.Trans.setItem(i, 0, QTableWidgetItem(str(tid)))
                self.Trans.setItem(i, 1, QTableWidgetItem(a[0].replace('_',' ')))
                self.Trans.setItem(i, 2, QTableWidgetItem(a[-2]))
                self.Trans.setItem(i, 3, QTableWidgetItem(a[3]))
                self.Trans.setItem(i, 4, QTableWidgetItem(a[4]))
                self.Trans.setItem(i, 5, QTableWidgetItem(p))
                self.Trans.setRowHeight(i, 50)
                tid += 1

            self.lbl4.setText('Transaction History.')
        else:
            self.lbl4.setText('No valid information found.')


    def display(self, i):
        # self.Stack.setCurrentIndex(i)
        pass


    def initial_values(self):
        # inital values
        # self.checkin.setChecked(True)
        # self.checkout.setChecked(False)
        self.combobox_data()
        self.study.addItems(list(self.study_visit_data.keys()))
        self.study.setCurrentIndex(0)
        self.on_study_combobox_changed(self.study.currentText())
        self.freezer.addItems(list(self.freezer_data.keys()))
        self.freezer.setCurrentIndex(0)
        self.shelf.addItems(list(self.freezer_data[list(self.freezer_data)[0]]))
        self.personnel.addItems(self.personnel_data)


    def combobox_data(self):
        self.study_visit_data = {
            '2011-0199': ['ROV', 'EDD'],
            '2015-0197': ['Saline', 'Placebo', 'LNMMA', 'Ambrisentan'],
            '2019-0361': ['Screening', 'OGTT'],
            '2019-0838': ['Screening'],
            '2020-0336': ['Not defined yet']
        }

        self.visit_time_data = {
            'ROV': ['0'],
            'EDD': ['0'],
            'Saline': ['0', '10', '20', '30', '45', '60', '75', '90', '105', '120'],
            'Placebo': ['0', '1', '10', '20', '30', '45', '60', '75', '90', '105', '120'],
            'LNMMA': ['0', '10', '20', '30', '45', '60', '75', '90', '105', '120'],
            'Ambrisentan': ['0', '1', '10', '20', '30', '45', '60', '75', '90', '105', '120'],
            'Screening': ['0'],
            'OGTT': ['0', '5', '10', '20', '30', '45', '60']
        }

        self.box_color_data = {
            '2011-0199': ['Red', 'Green', 'Yellow'],
            '2015-0197': ['Red', 'Green'],
            '2019-0361': ['Red', 'Green', 'Yellow'],
            '2019-0838': ['Red', 'Green', 'Yellow'],
            '2020-0336': ['Not defined yet']
        }

        self.freezer_data = {
            '-80 Freezer': ['1', '2', '3', '4'],
            '-20 Freezer': ['1', '2', '3', '4'],
            '+7 Fridge': ['1', '2', '3', '4']
        }

        self.personnel_data = [
            'Aaron Ward',
            'Katrina Carter',
            'Jessica Muer',
            'Justin Brubaker',
            'Shawn Bolin',
            'William Schrage'
        ]


    def error_dialog(self, msg):
        error_msg = QMessageBox()
        error_msg.setWindowTitle("Error")
        error_msg.setText(msg)
        error_msg.setIcon(QMessageBox.Warning)
        error_msg.exec_()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # login = Login()

    # if login.exec_() == QtWidgets.QDialog.Accepted:
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
