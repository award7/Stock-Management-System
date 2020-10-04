import sys
import os
import datetime
import manipulation as mp
import sqlite3

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


try:
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE stock (
                name text,
                quantity integer,
                cost integer
                ) """)
    conn.commit()
except Exception:
    print('DB exists')


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
        exitAct = QAction(QIcon('exit_icon.png'), 'Exit', self)
        exitAct.setShortcut('Ctrl+W')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)

        self.statusBar()
        self.setWindowTitle('Schrage Lab Sample Inventory')
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAct)

        self.setCentralWidget(self.st)


class Container0(QWidget):
    def __init__(self):

        super(Container0, self).__init__()
        self.leftlist = QListWidget()
        self.leftlist.setFixedWidth(250)
        self.leftlist.insertItem(0, 'Check-in/Checkout Samples')
        self.leftlist.insertItem(1, 'View Samples')
        self.leftlist.insertItem(2, 'View Sample History')

        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()

        self.stack1UI()
        self.stack2UI()
        self.stack3UI()

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)
        self.Stack.addWidget(self.stack3)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.leftlist)
        hbox.addWidget(self.Stack)

        self.setLayout(hbox)
        self.leftlist.currentRowChanged.connect(self.display)
        self.setGeometry(500, 350, 200, 200)

        # add signals
        self.signals()

        # set initial values
        self.initial_values()


    def stack1UI(self):
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
        layout.addRow("Sample Quantity", self.quantity)

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

        self.stack1.setLayout(layout)


    def on_status_btn_changed(self):
        if self.checkin.isChecked() == True:
            msg = f"{self.checkin.text()} Samples"
            self.add_sample.setText(msg)
        else:
            msg = f"{self.checkout.text()} Samples"
            self.add_sample.setText(msg)


    def signals(self):

        # check-in radio button signal
        self.checkin.toggled.connect(self.on_status_btn_changed)

        # checkout radio button signal
        self.checkout.toggled.connect(self.on_status_btn_changed)

        # study combobox signal
        self.study.currentTextChanged.connect(self.on_study_combobox_change)

        # visit combobox signal

        # freezer combobox signal

        # add sample signal
        # self.add_sample.clicked.connect(self.on_click)


    def initial_values(self):
        # inital values
        self.checkin.setChecked(True)
        self.checkout.setChecked(False)
        self.combobox_data()
        self.study.addItems(list(self.study_visit_data.keys()))
        self.study.setCurrentIndex(0)
        self.on_study_combobox_change(self.study.currentText())
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


    def on_study_combobox_change(self, text):
        # add visits
        try:
            self.visit.clear()
            self.visit.addItems(self.study_visit_data[text])
            self.visit.setCurrentIndex(0)
        except:
            msg = f"Study visits not defined for {text}"
            self.error_dialog(msg)


        # add time points
        try:
            self.time_point.clear()
            self.time_point.addItems(self.visit_time_data[self.study_visit_data[text][0]])
            self.time_point.setCurrentIndex(0)
        except:
            msg = f"Time points not defined for {text} {self.study_visit_data[text]}"
            self.error_dialog(msg)

        # add box colors
        try:
            self.box_color.clear()
            self.box_color.addItems(self.box_color_data[text])
            self.box_color.setCurrentIndex(0)
        except:
            msg = f"Box colors not defined for {text}"
            self.error_dialog(msg)


    def error_dialog(self, msg):
        error_msg = QMessageBox()
        error_msg.setWindowTitle("Error")
        error_msg.setText(msg)
        error_msg.setIcon(QMessageBox.Warning)
        error_msg.exec_()


    def on_click(self):
        now = datetime.datetime.now()
        stock_name_inp = self.stock_name.text().replace(' ','_').lower()
        stock_count_inp = int(self.stock_count.text())
        stock_cost_inp = int(self.stock_cost.text())
        #print(stock_name_inp,stock_count_inp,stock_cost_inp)
        stock_add_date_time = now.strftime("%Y-%m-%d %H:%M")
        # d = mp.insert_prod(stock_name_inp,stock_count_inp,stock_cost_inp,stock_add_date_time)
        # print(d)
        # TODO: add the above details to table


    def call_red(self):
        now = datetime.datetime.now()
        stock_red_date_time = now.strftime("%Y-%m-%d %H:%M")
        stock_name = self.stock_name_red.text().replace(' ','_').lower()
        try:
            stock_val = -(int(self.stock_count_red.text()))
            print(stock_val)
            print(type(stock_val))
            mp.update_quantity(stock_name, stock_val, stock_red_date_time)
        except Exception:
            print('Exception')


    def call_add(self):
        now = datetime.datetime.now()
        stock_call_add_date_time = now.strftime("%Y-%m-%d %H:%M")
        stock_name = self.stock_name_add.text().replace(' ','_').lower()
        stock_val = int(self.stock_count_add.text())
        mp.update_quantity(stock_name, stock_val, stock_call_add_date_time)


    def stack2UI(self):

        table = mp.show_stock()
        print('show')
        print(table)
        layout = QVBoxLayout()
        self.srb = QPushButton()
        self.srb.setText("Get Search Result.")
        self.View = QTableWidget()
        self.lbl3 = QLabel()
        self.lbl_conf_text = QLabel()
        self.lbl_conf_text.setText("Enter the search keyword:")
        self.conf_text = QLineEdit()

        self.View.setColumnCount(3)
        self.View.setColumnWidth(0, 250)
        self.View.setColumnWidth(1, 250)
        self.View.setColumnWidth(2, 200)
        self.View.insertRow(0)
        self.View.setItem(0, 0, QTableWidgetItem('Stock Name'))
        self.View.setItem(0, 1, QTableWidgetItem('Quantity'))
        self.View.setItem(0, 2, QTableWidgetItem('Cost(Per Unit)'))



        layout.addWidget(self.View)
        layout.addWidget(self.lbl_conf_text)
        layout.addWidget(self.conf_text)
        layout.addWidget(self.srb)
        layout.addWidget(self.lbl3)
        self.srb.clicked.connect(self.show_search)
        self.stack2.setLayout(layout)


    def show_search(self):
        if self.View.rowCount()>1:
            for i in range(1,self.View.rowCount()):
                self.View.removeRow(1)


        x_act = mp.show_stock()
        x = []
        if self.conf_text.text() != '':
            for i in range(0,len(x_act)):
                a = list(x_act[i])
                if self.conf_text.text().lower() in a[0].lower():
                    x.append(a)
        else:
            x = mp.show_stock()

        if len(x)!=0:
            for i in range(1,len(x)+1):
                self.View.insertRow(i)
                a = list(x[i-1])
                self.View.setItem(i, 0, QTableWidgetItem(a[0].replace('_',' ').upper()))
                self.View.setItem(i, 1, QTableWidgetItem(str(a[1])))
                self.View.setItem(i, 2, QTableWidgetItem(str(a[2])))
                self.View.setRowHeight(i, 50)
            self.lbl3.setText('Viewing Stock Database.')
        else:
            self.lbl3.setText('No valid information in database.')


    def stack3UI(self):
        layout = QVBoxLayout()
        self.srt = QPushButton()
        self.srt.setText("Get Transaction History.")
        self.Trans = QTableWidget()
        self.lbl4 = QLabel()
        self.lbl_trans_text = QLabel()
        self.lbl_trans_text.setText("Enter the search keyword:")
        self.trans_text = QLineEdit()

        self.Trans.setColumnCount(6)
        self.Trans.setColumnWidth(0, 150)
        self.Trans.setColumnWidth(1, 150)
        self.Trans.setColumnWidth(2, 150)
        self.Trans.setColumnWidth(3, 100)
        self.Trans.setColumnWidth(4, 100)
        self.Trans.setColumnWidth(5, 500)
        self.Trans.insertRow(0)
        self.Trans.setItem(0, 0, QTableWidgetItem('Transaction ID'))
        self.Trans.setItem(0, 1, QTableWidgetItem('Stock Name'))
        self.Trans.setItem(0, 2, QTableWidgetItem('Transaction Type'))
        self.Trans.setItem(0, 3, QTableWidgetItem('Date'))
        self.Trans.setItem(0, 4, QTableWidgetItem('Time'))
        self.Trans.setItem(0, 5, QTableWidgetItem('Transaction Specific'))
        self.Trans.setRowHeight(0, 50)

        layout.addWidget(self.Trans)
        layout.addWidget(self.lbl_trans_text)
        layout.addWidget(self.trans_text)
        layout.addWidget(self.srt)
        layout.addWidget(self.lbl4)
        self.srt.clicked.connect(self.show_trans_history)
        self.stack3.setLayout(layout)


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
        self.Stack.setCurrentIndex(i)




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # login = Login()

    # if login.exec_() == QtWidgets.QDialog.Accepted:
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
