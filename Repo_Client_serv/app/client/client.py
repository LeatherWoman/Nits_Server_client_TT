#import libraries
import sys
import asyncio
import datetime
import pickle
import socket
import pr_pb2 as pr # import protocol class
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QThread
from main_gui import Ui_MainWindow # import main window class
from RequestForFastResponse import Ui_RequestForFastResponse # import FastResponse window class
from RequestForSlowResponse import Ui_RequestForSlowResponse # import SlowResponse window class
from option import Ui_Dialog #import option window class
from PyQt5.QtWidgets import *
from threading import Thread
import tkinter as tk
import threading
import inspect
from google.protobuf.internal.encoder import _VarintBytes
from google.protobuf.internal.decoder import _DecodeVarint32

#global values
global client_timeout
client_timeout = 'MissInput' #time of reconnection timeout
global message_try
message_try = '' # additional optional to save message
global schet
schet = 1 
global labellist
labellist = [] # parameter for filling scrollbar
global in_button
in_button = 0 # parameter necssary to not given access to button if there is a reconnection to server

glob_glob = pr.WrapperMessage() # sent to server info

#Dialog option window
class OptionDialog(QtWidgets.QDialogButtonBox):
    
    def __init__(self):
        super(OptionDialog, self).__init__()
        self.button_option_ok = Ui_Dialog()
        self.button_option_ok.setupUi(self)
        self.init_UI()
        
    #filling parametrs of the option window         
    def init_UI(self):
        self.setWindowTitle('Option')
        self.button_option_ok.input_currency_3.setPlaceholderText('Reconnection timeout')
        self.button_option_ok.buttonBox.accepted.connect(self.evt_accepted_clicked)
        self.button_option_ok.buttonBox.rejected.connect(self.evt_rejected_clicked)
        self.button_option_ok.checkBox.stateChanged.connect(self.evt_statechanged)
        self.statechanged = 0
        
    #button click handling    
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

#Dialog RequestForFastResponse window
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
    
    #button click handling
    def evt_accepted_clicked(self):
        self.request_timeout = self.button_fast_ok.input_currency_2.text()
        
        #exc and err handling
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
                glob_glob = pr.WrapperMessage()
                glob_glob.request_for_fast_response.CopyFrom(pr.RequestForFastResponse())
                asyncio.run(main(glob_glob,x[0],int(x[1])))
                asyncio.run(asyncio.sleep(int(self.request_timeout)/1000))
                if message_try!='':
                    #split into main thread and processing thread
                    self.thread = threading.Timer(0, self.rerun)
                    self.thread.start()
                self.close()
        self.close()
      
    #reconnect function
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
            elif message_try == '':
                value = 1001
            else:
                value = 1001
        else:
            in_button = 0
            return
    def evt_rejected_clicked(self):
        self.close()

#timer function for reconnecton
async def timer():
    (local_time := int(client_timeout)) if client_timeout.isdigit()==True else (local_time :=0)
    await asyncio.sleep(local_time)

#Dialog RequestForSlowResponse window
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
    
    #button click handling
    def evt_accepted_clicked(self):
        self.request_timeout = self.button_slow_ok.input_currency_2.text()
        self.server_sleep = self.button_slow_ok.input_currency_3.text()
        
        #exc and err handling
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
                asyncio.run(main(glob_glob,x[0],int(x[1])))
                asyncio.run(asyncio.sleep(int(self.request_timeout)/1000))
                if message_try !='':
                    #split into main thread and processing thread
                    self.thread = threading.Timer(0, self.rerun)
                    self.thread.start()
                self.close()
        self.close()
        
    #reconnect function    
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
            if message_try != '' and local_time!=0:
                asyncio.run(asyncio.sleep(local_time))
            elif message_try == '':
                value = 1001
            else:
                value = 1001
        else:
            in_button = 0
            return
    def evt_rejected_clicked(self):
        self.close()
        

#Dialog main window    
class ClientWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super(ClientWidget, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()
    siganl_protocol_send = pyqtSignal(str) #processing info about conn/no-conn to the server
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
    
    #signal processing function 
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
    
    #function for processing press the "RequestForSlowResponse" button
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
    
    #saving parameter function "press ok button"
    def evt_pushbutton_3_clicked(self):
        global x
        x = self.request_to_server()
    
    
    #function for processing press the "RequestForFastResponse" button
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
    
    #ip and host input processing function 
    def request_to_server(self):
        input_ip = self.ui.input_currency_2.text()
        input_port = self.ui.input_currency_3.text()
        return input_ip,input_port
    
    #function for processing press the "Option" button
    def evt_toolbutton_clicked(self):
        self.button_ok = OptionDialog()
        self.button_ok.show()


global connect
connect = ''


# client protocol class
class EchoClientProtocol(asyncio.Protocol):

    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost

    # send info when connected function
    def connection_made(self, transport):
        size = self.message.ByteSize()
        packed_len = _VarintBytes(size)
        data_string = self.message.SerializeToString()
        transport.write(packed_len + data_string)
        if 'application' in locals() or 'application' in globals():
            application.siganl_protocol_send.emit('Data sent: {!r}'.format(self.message))

    # get info function
    def data_received(self, data):
        global data_decode
        data = bytes(data)
        pos = 0
        while pos < len(data):
            data_decode, pos = self.read_mes(data, pos)
        st = 'Data received: {!r}'.format(data_decode)
        if 'application' in locals() or 'application' in globals():
            application.siganl_protocol_send.emit(st)

    # connection loss function
    def connection_lost(self, exc):
        if data_decode == ValueError:
            st = 'ValueError: the server could not decode the message or received an incorrect one'
            if 'application' in locals() or 'application' in globals():
                application.siganl_protocol_send.emit(st)
        self.on_con_lost.set_result(True)
        if 'application' in locals() or 'application' in globals():
            application.siganl_protocol_send.emit('The server closed the connection')

    def read_mes(self, data, pos):
        msg_len, new_pos = _DecodeVarint32(data, pos)
        pos = new_pos
        msg_buf = data[pos:(pos + msg_len)]
        pos += msg_len
        message = pr.WrapperMessage()
        message.ParseFromString(msg_buf)
        return message, pos


# async server connection function
async def main(message, ip, host):
    global message_try
    global labellist
    global data_decode
    data_decode = ValueError
    try:
        loop = asyncio.get_running_loop()

        on_con_lost = loop.create_future()

        transport, protocol = await loop.create_connection(
            lambda: EchoClientProtocol(message, on_con_lost),
            ip, host)
    except:
        connect = 'ConnectionError: The server with the entered ip and host is not responding\n'
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
        
#class for unittest
class Nado():
    global data_decode
    def __init__(self):
        self.data_decode = data_decode
    

#main app function
def appl():
    global application
    global in_button
    in_button = 0
    app = QtWidgets.QApplication([])
    application = ClientWidget()
    application.show()
    sys.exit(app.exec())
if __name__ == '__main__':
    appl()
