import sys
import asyncio
import datetime
import pickle
import socket
import pr_pb2 as pr
import datetime
import pickle
import socket
import pr_pb2 as pr
import time
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QThread
from main_gui import Ui_MainWindow
from RequestForFastResponse import Ui_RequestForFastResponse
from RequestForSlowResponse import Ui_RequestForSlowResponse
from option import Ui_Dialog
from PyQt5.QtWidgets import *
import asyncio
from threading import Thread
from threading import Thread
import tkinter as tk
import tkinter as tk
import threading


global client_timeout
client_timeout = 'MissInput'
global message_try
message_try = ''
global schet
schet = 1
global labellist
labellist = []
global in_button
in_button = 0
import inspect
import inspect

glob_glob = pr.WrapperMessage()

class OptionDialog(QtWidgets.QDialogButtonBox):
    def __init__(self):
        super(OptionDialog, self).__init__()
        self.button_option_ok = Ui_Dialog()
        self.button_option_ok.setupUi(self)
        self.init_UI()
             
    def init_UI(self):
        self.setWindowTitle('Option')
        self.button_option_ok.input_currency_3.setPlaceholderText('Reconnection timeout')
        self.button_option_ok.buttonBox.accepted.connect(self.evt_accepted_clicked)
        self.button_option_ok.buttonBox.rejected.connect(self.evt_rejected_clicked)
        self.button_option_ok.checkBox.stateChanged.connect(self.evt_statechanged)
        self.statechanged = 0
    def evt_accepted_clicked(self):
        self.connect_timeout = self.button_option_ok.input_currency_3.text()
        if len(self.connect_timeout) == 0 and self.statechanged == 0:
            self.close()
        elif len(self.connect_timeout) == 0 and self.statechanged != 0:
            self.connect_timeout = '1'
        elif self.connect_timeout.isdigit() == False:
            qmsgBox = QMessageBox()
            qmsgBox.setStyleSheet("background-color: #22222e;\n"
"color: white")
            QMessageBox.critical(qmsgBox,"ValueError","You input in Connect TimeOut not a integer number")
            self.close()
        elif int(self.connect_timeout)<1:
            self.connect_timeout = '1'
        elif int(self.connect_timeout)>10:
            self.connect_timeout = '10'
        global client_timeout
        (client_timeout :=self.connect_timeout) if self.statechanged == 1 and self.connect_timeout.isdigit() == True else (client_timeout :='MissInput')
        self.close()
    
    def evt_rejected_clicked(self):
        self.close()
    
    def evt_statechanged(self, state):
        if state == 0:
            self.statechanged = 0
        else:
            self.statechanged = 1

class RequestForFastResponseDialog(QtWidgets.QDialogButtonBox):
    def __init__(self):
        super(RequestForFastResponseDialog, self).__init__()
        self.button_fast_ok = Ui_RequestForFastResponse()
        self.button_fast_ok.setupUi(self)
        self.request_timeout = ''
        self.init_UI()
        
    def init_UI(self):
        self.setWindowTitle('Request For Fast Response')
        self.button_fast_ok.input_currency_2.setPlaceholderText('Request TimeOut')
        self.button_fast_ok.buttonBox.accepted.connect(self.evt_accepted_clicked)
        self.button_fast_ok.buttonBox.rejected.connect(self.evt_rejected_clicked)
    
    def evt_accepted_clicked(self):
        self.request_timeout = self.button_fast_ok.input_currency_2.text()
        if self.request_timeout.isdigit() == False:
            qmsgBox = QMessageBox()
            qmsgBox.setStyleSheet("background-color: #22222e;\n"
"color: white")
            QMessageBox.critical(qmsgBox,"ValueError","You input in Request TimeOut not a integer number")
            self.close()
        elif int(self.request_timeout)<10 or int(self.request_timeout)>1000:
            qmsgBox = QMessageBox()
            qmsgBox.setStyleSheet("background-color: #22222e;\n"
"color: white")
            QMessageBox.critical(qmsgBox,"ValueError","You could input from 10 to 1000 msec in Request TimeOut")
            self.close() 
        else:
            self.request_timeout = int(self.request_timeout)
            y = x[0].split('.')
            z = x[1]
            if len(y)!=4:
                qmsgBox = QMessageBox()
                qmsgBox.setStyleSheet("background-color: #22222e;\n"
"color: white")
                QMessageBox.critical(qmsgBox,"IpAddressError_Not_4_argument","Ip-address has the form 'N1.N2.N3.N4', where 0<=Ni<=255")
                self.close()
            elif y[0].isdigit()==False or y[1].isdigit()==False or y[2].isdigit()==False or y[3].isdigit()==False:
                qmsgBox = QMessageBox()
                qmsgBox.setStyleSheet("background-color: #22222e;\n"
"color: white")
                QMessageBox.critical(qmsgBox,"IpAddressError_not_all_int","Ip-address has the form 'N1.N2.N3.N4', where 0<=Ni<=255")
                self.close()
            elif int(y[0])>255 or int(y[1])>255 or int(y[2])>255 or int(y[3])>255:
                qmsgBox = QMessageBox()
                qmsgBox.setStyleSheet("background-color: #22222e;\n"
"color: white")
                QMessageBox.critical(qmsgBox,"IpAddressError","Ip-address has the form 'N1.N2.N3.N4', where 0<=Ni<=255")
                self.close()
            elif z.isdigit() == False or int(z)<0 or int(z)>65535:
                qmsgBox = QMessageBox()
                qmsgBox.setStyleSheet("background-color: #22222e;\n"
"color: white")
                QMessageBox.critical(qmsgBox,"HostError","Host has the form 'N', where 0<=N<=65535")
                self.close()
            else:
                print(message_try)
                glob_glob = pr.WrapperMessage()
                glob_glob.request_for_fast_response.CopyFrom(pr.RequestForFastResponse())
                print(glob_glob)
                asyncio.run(main(glob_glob,x[0],int(x[1])))
                asyncio.run(asyncio.sleep(int(self.request_timeout)/1000))
                if message_try!='':
                    self.thread = threading.Timer(0, self.rerun)
                    self.thread.start()
                self.close()
        self.close()
    def rerun(self):
        value = 0
        while value<100:
            global in_button
            in_button = 1
            if client_timeout =='MissInput':
                value = 1001
                continue
            task1 = asyncio.run(main(glob_glob,x[0],int(x[1])))
            (local_time := int(client_timeout)) if client_timeout.isdigit()==True else (local_time :=0)
            if message_try != '' and local_time!=0:
                asyncio.run(asyncio.sleep(local_time))
                print("Вроде прошло")
            elif message_try == '':
                value = 1001
            else:
                value = 1001
                print("Воу полегче нажми галочку в настройках")
        else:
            in_button = 0
            return
    def evt_rejected_clicked(self):
        self.close()

async def timer():
    (local_time := int(client_timeout)) if client_timeout.isdigit()==True else (local_time :=0)
    await asyncio.sleep(local_time)

    
class RequestForSlowResponseDialog(QtWidgets.QDialogButtonBox):
    def __init__(self):
        super(RequestForSlowResponseDialog, self).__init__()
        self.button_slow_ok = Ui_RequestForSlowResponse()
        self.button_slow_ok.setupUi(self)
        self.request_timeout = ''
        self.server_sleep = ''
        asyncio.run(self.init_UI())
        
    async def init_UI(self):
        self.setWindowTitle('Request For Slow Response')
        self.button_slow_ok.input_currency_2.setPlaceholderText('Request TimeOut')
        self.button_slow_ok.input_currency_3.setPlaceholderText('Server sleep')
        self.button_slow_ok.buttonBox.accepted.connect(self.evt_accepted_clicked)
        self.button_slow_ok.buttonBox.rejected.connect(self.evt_rejected_clicked)
    
    def evt_accepted_clicked(self):
        self.request_timeout = self.button_slow_ok.input_currency_2.text()
        self.server_sleep = self.button_slow_ok.input_currency_3.text()
        if self.request_timeout.isdigit() == False:
            qmsgBox = QMessageBox()
            qmsgBox.setStyleSheet("background-color: #22222e;\n"
"color: white")
            QMessageBox.critical(qmsgBox,"ValueError","You input in Request TimeOut not a integer number")
            self.close()
        elif int(self.request_timeout)<10 or int(self.request_timeout)>1000:
            qmsgBox = QMessageBox()
            qmsgBox.setStyleSheet("background-color: #22222e;\n"
"color: white")
            QMessageBox.critical(qmsgBox,"ValueError","You could input from 10 to 1000 msec in Request TimeOut")
            self.close() 
        elif self.server_sleep.isdigit() == False:
            qmsgBox = QMessageBox()
            qmsgBox.setStyleSheet("background-color: #22222e;\n"
"color: white")
            QMessageBox.critical(qmsgBox,"ValueError","You input in Server sleep not a integer number")
            self.close()
        elif int(self.server_sleep)<1 or int(self.server_sleep)>10:
            qmsgBox = QMessageBox()
            qmsgBox.setStyleSheet("background-color: #22222e;\n"
"color: white")
            QMessageBox.critical(qmsgBox,"ValueError","You could input from 1 to 10 sec in Server sleep")
            self.close()
        else:
            self.request_timeout = int(self.request_timeout)
            self.server_sleep = int(self.server_sleep)
            y = x[0].split('.')
            z = x[1]
            if len(y)!=4:
                qmsgBox = QMessageBox()
                qmsgBox.setStyleSheet("background-color: #22222e;\n"
"color: white")
                QMessageBox.critical(qmsgBox,"IpAddressError_Not_4_argument","Ip-address has the form 'N1.N2.N3.N4', where 0<=Ni<=255")
                self.close()
            elif y[0].isdigit()==False or y[1].isdigit()==False or y[2].isdigit()==False or y[3].isdigit()==False:
                qmsgBox = QMessageBox()
                qmsgBox.setStyleSheet("background-color: #22222e;\n"
"color: white")
                QMessageBox.critical(qmsgBox,"IpAddressError_not_all_int","Ip-address has the form 'N1.N2.N3.N4', where 0<=Ni<=255")
                self.close()
            elif int(y[0])>255 or int(y[1])>255 or int(y[2])>255 or int(y[3])>255:
                qmsgBox = QMessageBox()
                qmsgBox.setStyleSheet("background-color: #22222e;\n"
"color: white")
                QMessageBox.critical(qmsgBox,"IpAddressError","Ip-address has the form 'N1.N2.N3.N4', where 0<=Ni<=255")
                self.close()
            elif z.isdigit() == False or int(z)<0 or int(z)>65535:
                qmsgBox = QMessageBox()
                qmsgBox.setStyleSheet("background-color: #22222e;\n"
"color: white")
                QMessageBox.critical(qmsgBox,"HostError","Host has the form 'N', where 0<=N<=65535")
                self.close()
            else:
                glob_glob = pr.WrapperMessage()
                glob_glob.request_for_slow_response.time_in_seconds_to_sleep = self.server_sleep
                print(glob_glob)
                asyncio.run(main(glob_glob,x[0],int(x[1])))
                asyncio.run(asyncio.sleep(int(self.request_timeout)/1000))
                if message_try !='':
                    self.thread = threading.Timer(0, self.rerun)
                    self.thread.start()
                self.close()
        self.close()
    def rerun(self):
        value = 0
        while value<100:
            global in_button
            in_button = 1
            if client_timeout =='MissInput':
                value = 1001
                continue
            glob_glob = pr.WrapperMessage()
            glob_glob.request_for_slow_response.time_in_seconds_to_sleep = self.server_sleep
            task1 = asyncio.run(main(glob_glob,x[0],int(x[1])))
            (local_time := int(client_timeout)) if client_timeout.isdigit()==True else (local_time :=0)
            print(labellist)
            if message_try != '' and local_time!=0:
                asyncio.run(asyncio.sleep(local_time))
                print("Вроде прошло")
            elif message_try == '':
                value = 1001
            else:
                value = 1001
                print("Воу полегче нажми галочку в настройках")
        else:
            in_button = 0
            return
    def evt_rejected_clicked(self):
        self.close()
        

    
class ClientWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super(ClientWidget, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()
    siganl_protocol_send = pyqtSignal(str)
    def init_UI(self):
        self.setWindowTitle('Client')
        self.ui.input_currency_2.setPlaceholderText('ip-address')
        self.ui.input_currency_3.setPlaceholderText('server port')
        self.ui.pushButton.clicked.connect(self.evt_pushbutton_clicked)
        self.ui.pushButton_2.clicked.connect(self.evt_pushbutton_2_clicked)
        self.ui.toolButton.clicked.connect(self.evt_toolbutton_clicked)
        self.siganl_protocol_send.connect(self.evt_signal_protocol_send)
        self.ui.pushButton_3.clicked.connect(self.evt_pushbutton_3_clicked)
        mygroupbox = QtWidgets.QGroupBox()
        global myform
        myform = QtWidgets.QFormLayout()
        global labellist
        labellist = []
        mygroupbox.setLayout(myform)
        self.ui.scrollArea.setWidget(mygroupbox)
        self.value_fast = 0
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.ui.scrollArea)
        print(1)
    
    @ QtCore.pyqtSlot(str)
    def evt_signal_protocol_send(self,arg):
        connect = arg
        lable = QtWidgets.QLabel()
        lable.setStyleSheet("background-color: #22222e;\n"
"color: white")
        lable.setText(connect)
        labellist.append(lable)
        myform.addRow(labellist[-1])
        lable.close()
        
    def evt_pushbutton_clicked(self):
        if 'x' not in globals():
            qmsgBox = QMessageBox()
            qmsgBox.setStyleSheet("background-color: #22222e;\n"
"color: white")
            QMessageBox.critical(qmsgBox,"ValueError","Please input ip and host")
        elif in_button == 1:
            qmsgBox = QMessageBox()
            qmsgBox.setStyleSheet("background-color: #22222e;\n"
"color: white")
            QMessageBox.critical(qmsgBox,"SendError","Currently waiting for a response from the server on the previous request")
        else:
            self.button_ok = RequestForSlowResponseDialog()
            self.button_ok.show()
    
    def evt_pushbutton_3_clicked(self):
        global x
        x = self.request_to_server()
    
    def evt_pushbutton_2_clicked(self):
        if 'x' not in globals():
            qmsgBox = QMessageBox()
            qmsgBox.setStyleSheet("background-color: #22222e;\n"
"color: white")
            QMessageBox.critical(qmsgBox,"ValueError","Please input ip and host")
        elif in_button == 1:
            qmsgBox = QMessageBox()
            qmsgBox.setStyleSheet("background-color: #22222e;\n"
"color: white")
            QMessageBox.critical(qmsgBox,"SendError","Currently waiting for a response from the server on the previous request")
        else:
            self.button_ok = RequestForFastResponseDialog()
            self.button_ok.show()
    
    def request_to_server(self):
        input_ip = self.ui.input_currency_2.text()
        input_port = self.ui.input_currency_3.text()
        return input_ip,input_port
    
    def evt_toolbutton_clicked(self):
        self.button_ok = OptionDialog()
        self.button_ok.show()
        print(client_timeout)

global connect
connect = ''
class EchoClientProtocol(asyncio.Protocol):
    
    
    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost

    def connection_made(self, transport):
        data_string = pickle.dumps(self.message)
        transport.write(data_string)
        print('Data sent: {!r}'.format(self.message))
        if 'application' in locals() or 'application' in globals():
            application.siganl_protocol_send.emit('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        global data_decode
        data_decode = pickle.loads(data)
        print('Data received: {!r}'.format(data_decode))
        if 'application' in locals() or 'application' in globals():
            application.siganl_protocol_send.emit('Data received: {!r}'.format(data_decode))

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.on_con_lost.set_result(True)
        if 'application' in locals() or 'application' in globals():
            application.siganl_protocol_send.emit('The server closed the connection')
    
    

async def main(message,ip,host):
    global message_try
    global labellist
    global data_decode
    try:
        loop = asyncio.get_running_loop()

        on_con_lost = loop.create_future()

        transport, protocol = await loop.create_connection(
            lambda: EchoClientProtocol(message, on_con_lost),
            ip, host)
        print(transport)
    except:
        connect = 'ConnectionEror: The server with the entered ip and host is not responding\n'
        message_try = message
        if application:
            application.siganl_protocol_send.emit(connect)
        return
    try:
        await on_con_lost
    finally:
        labellist = []
        connect = ''
        message_try = ''
        transport.close()
class Nado():
    global data_decode
    def __init__(self):
        self.data_decode = data_decode
    

def appl():
    print(type(10)==int)
    global application
    global in_button
    in_button = 0
    app = QtWidgets.QApplication([])
    application = ClientWidget()
    application.show()
    print(labellist)
    sys.exit(app.exec())
if __name__ == '__main__':
    appl()
