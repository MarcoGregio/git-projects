#!/usr/bin/env python

'''
## Project: QT Control Panel 

## Author: Francesco Benente / Lorenzo Fazio
## Company: IDT Solution S.r.l. S.B.

## Creation date: 2021/11/15
## Latest edit: 2021/11/15

## Description: Standard Python Modbus HMI for Raspberry Pi based Control Panels
## Version: v. 5.1.0

PLEASE KEEP UPDATED CHANGELOG.md !
'''

'''
## COMMESSA: 21064
## CLIENTE: SIGIT
## Release: 1.0

## Changelog:
##  
'''
# import pandas as sql

# Drive types
# from ctypes.wintypes import PLONG
# from QLed import QLed
# from selectors import DefaultSelector, EVENT_READ
from asyncio import subprocess
import sys, os, csv, json, socket
from ftplib import FTP
import subprocess
from subprocess import call, check_output
import hashlib
from threading import Thread, Event
from time import sleep
from PyQt5 import QtCore
from PyQt5.QtWidgets import QSizePolicy, QApplication, QMainWindow, QWidget, QStackedWidget, QLabel, QPushButton, QLineEdit, QMessageBox, QCheckBox, QComboBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QAbstractItemView, QFrame, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon, QPalette, QBrush, QImage, QPixmap, QFontMetrics, QMovie, QPainter, QPen, QColor, QFont
from PyQt5.QtCore import QSize, Qt, QThread, pyqtSignal, QObject, QCoreApplication, QDateTime, QDate, QTime, QTimer, QRect
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ModbusException
from DBMethods import *
from CustomWidgets import *
import Style
from IO_Constants import *
from VirtualKeyboard import VirtualKeyboard
from VirtualKeyboard import ClickableLineEdit
import datetime
import calendar
import serial
import os
import logging
from pynput import keyboard
import ctypes
import shutil
DRIVE_UNKNOWN     = 0  # The drive type cannot be determined.
# The root path is invalid; for example, there is no volume mounted at the specified path.
DRIVE_NO_ROOT_DIR = 1
# The drive has removable media; for example, a floppy drive, thumb drive, or flash card reader.
DRIVE_REMOVABLE = 2
# The drive has fixed media; for example, a hard disk drive or flash drive.
DRIVE_FIXED = 3
DRIVE_REMOTE = 4  # The drive is a remote (network) drive.
DRIVE_CDROM = 5  # The drive is a CD-ROM drive.
DRIVE_RAMDISK = 6  # The drive is a RAM disk.

# Map drive types to strings
DRIVE_TYPE_MAP = {DRIVE_UNKNOWN: 'DRIVE_UNKNOWN',
                  DRIVE_NO_ROOT_DIR: 'DRIVE_NO_ROOT_DIR',
                  DRIVE_REMOVABLE: 'DRIVE_REMOVABLE',
                  DRIVE_FIXED: 'DRIVE_FIXED',
                  DRIVE_REMOTE: 'DRIVE_REMOTE',
                  DRIVE_CDROM: 'DRIVE_CDROM',
                  DRIVE_RAMDISK: 'DRIVE_RAMDISK'}

# if LINUX:
#    import evdev
#    from evdev import InputDevice, categorize, ecodes, list_devices

'''
    Logger dell'HMI. Stampa sul log alcune informazioni o errori che possono occorrere durante l'esecuzione.

    N.B: filemode="w" sta ad indicare che la modalità di apertura del file indicato in filename è in scrittura e
          quando viene specificato ad ogni avvio il file viene sovrascritto, mentre se non fosse stato specificato nulla
          i log sarebbero appesi in fondo al file.
'''
logging.basicConfig(level=logging.ERROR, format='%(asctime)s: %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', filename='log_file.log', filemode="w")
# logging.basicConfig(level=logging.ERROR, filename='log_file.log', filemode="w")
logger = logging.getLogger('HMI_logger')


def draw_cover(label, bitmap):
    colour = {0: "white", 1: "red", 2: "yellow", 3: "lime"}

    try:
        # Mantenere l'ordine della bitmap presente su DB
        rects = [
            QRect(50, 275, 30, 30),  # PP1
            QRect(545, 275, 30, 30),  # PP2
            QRect(155, 260, 30, 30),  # B1SX
            QRect(425, 262, 30, 30),  # B1DX
            QRect(290, 262, 30, 30),  # B00
            QRect(25, 215, 30, 30),  # B2
            QRect(95, 170, 30, 30),  # B3
            QRect(225, 170, 30, 30),  # B4
            QRect(550, 215, 30, 30),  # B22
            QRect(485, 170, 30, 30),  # B33
            QRect(355, 170, 30, 30)  # B44
        ]

        painter = QPainter(label.pixmap())
        painter.setOpacity(1)
        '''pen = QPen()
        pen.setWidth(0)
        pen.setColor(QColor("black"))
        painter.setPen(pen)

        font = QFont()
        font.setFamily('Arial')
        font.setBold(True)
        font.setPointSize(10)
        painter.setFont(font)'''

        i = 0
        for bit in bitmap:
            brush = QBrush()
            brush.setColor(QColor(colour[bit]))
            brush.setStyle(Qt.SolidPattern)
            painter.setBrush(brush)
            painter.drawRoundedRect(rects[i], 30, 30)
            i = i + 1

    except AttributeError:
        pass
    except IndexError:
        pass


'''
    Funzione che si occupa di convertire il valore del registro intero in lista ordinata.
    I bit vuoti vengono inizilizzati a zero.
'''


def getBitmap(n):
    n = bin(n)[2::]
    n = list(map(int, n[::-1]))
    if len(n) < 16:
        i = 16 - len(n)
        for e in range(i):
            n.append(0)
    return n


'''
    Confronta posizione per posizione l'array di valori dei singoli registri utilizzati per
    gli elementi grafici ed ottiene il colore dell'elemento in questione, in particolare:
    il valore di default è grigio, segue giallo poi rosso ed infine verde.
    
    N.B: se tutti i bit dei tre registri valgono 1, vince il verde. Segue un esempio
    0 0     1      1     1     0 0 0 0 0 0 0 0 0 0 0
    0 1     0      1     1     0 0 0 0 0 0 0 0 0 0 0
    0 1     0      1     0     0 0 0 0 0 0 0 0 0 0 0
    / VERDE GIALLO VERDE ROSSO / / / / / / / / / / /
'''


def getSemaphoreArray(yellow, red, green):
    array = []
    for i in range(16):
        val = GRAY
        if yellow[i] == 1:
            val = YELLOW
        if red[i] == 1:
            val = RED
        if green[i] == 1:
            val = GREEN
        array.append(val)
    return array


'''
    Cripta la stringa passata come parametro utilizzando la funzione di hash sha-256
    (utilizzata per criptare principalmente le password degli utenti)
'''


def encryptString(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


'''
    Ottiene data e ora correnti, in formato: 2021-11-16
'''


def getCurrentTimestamp():
    d = QDate.currentDate().toString(Qt.ISODate)
    t = QTime.currentTime().toString()
    timestamp = d + " " + t
    return timestamp


'''
    Richiede come parametri il buffer dell'etichetta, la data, l'utente, il codice ed il seriale e
    si occupa di sostituire questi valori nel buffer e stampare poi l'etichetta
'''


def printZebraLabel(buffer, datetime, user_id, customer_code, n, counter_id):
    error = True
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((PRINTER_IP, PRINTER_PORT))
        buffer = buffer.replace("{counter_id}", counter_id)
        buffer = buffer.replace("{datetime}", datetime)
        buffer = buffer.replace("{user_id}", user_id)
        buffer = buffer.replace("{customer_code}", customer_code)
        buffer = buffer.replace("{n}", n)

        s.send(buffer.encode())
        s.close()
        error = False
    except socket.error as se:
        logger.error(format(se))
    finally:
        return error


'''
    Timer che cambia lo stato di un segnale passato come parametro ogni @time tempo trascorso
'''


class ClientTimer(QThread):
    signal = pyqtSignal()

    def __init__(self, event, time):
        QThread.__init__(self)
        self.stop = event
        self.time = time

    def run(self):
        self.signal.emit()
        while not self.stop.wait(self.time):
            self.signal.emit()


'''
    Thread che tiene conto del tempo che passa
'''


class TimeThread(QThread):
    trigger = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        while True:
            self.sleep(1)
            timestamp = getCurrentTimestamp()
            self.trigger.emit(timestamp)


'''
    Thread di scan della porta seriale.
    Emette nel segnale prodSignal il valore letto dalla porta seriale aperta.
'''


class SerialScan(QThread):
    prodSignal = pyqtSignal(str)

    def run(self):
        while (self.isAlive):
            try:
                if self.serial_port.isOpen():
                    try:
                        self.scan_data = self.serial_port.read_until(
                            '\r'.encode())
                    except serial.serialutil.SerialException as serialEx:
                        logger.error(format(serialEx))
                        pass

                    try:
                        # print("SCAN DATA: ", self.scan_data[0:len(self.scan_data)-1].decode())
                        self.scan_data_decoded = self.scan_data[0:len(
                            self.scan_data)-1].decode()
                        self.prodSignal.emit(self.scan_data_decoded)
                    except AttributeError as ae:
                        logger.error(format(ae))
                        pass
                    except IndexError as ie:
                        logger.error(format(ie))
                        pass
                    except TypeError as te:
                        logger.error(format(te))
                        pass
                else:
                    try:
                        if LINUX:
                            self.serial_port = serial.Serial(
                                '/dev/ttyACM0', timeout=60)
                        else:
                            self.serial_port = serial.Serial(
                                'COM5', timeout=30)
                    except serial.SerialException as se:
                        logger.error(format(se))
                        pass
                    except AttributeError as ae:
                        logger.error(format(ae))
                        pass
            except AttributeError as ae:
                logger.error(format(ae))
                pass
            except TypeError as te:
                logger.error(format(te))
                pass

            try:
                if self.serial_port.isOpen():
                    self.serial_port.reset_input_buffer()
            except AttributeError as ae:
                logger.error(format(ae))
                pass
            except TypeError as te:
                logger.error(format(te))
                pass

    def killMe(self):
        try:
            if self.serial_port.isOpen():
                self.serial_port.close()
        except AttributeError as ae:
            logger.error(format(ae))
            pass
        self.isAlive = False

    def restartMe(self):
        self.isAlive = True

    def __init__(self):
        QThread.__init__(self)
        self.isAlive = True
        try:
            if LINUX:
                self.serial_port = serial.Serial('/dev/ttyACM0', timeout=60)
            else:
                self.serial_port = serial.Serial('COM5', timeout=30)
        except serial.SerialException as se:
            logger.error(format(se))
            pass
        except AttributeError as ae:
            logger.error(format(ae))
            pass


'''
    Oggetto che si occupa della scrittura dei registri MODBUS.
    Il parametro register deve essere indicato in questo modo: (register, value)
'''
'''class ModbusWriter(QThread):
    def setRegisters(self, intervals):
        self.intervals = intervals
        
    def run(self):
        try:
            self.client.connect()
        except ModbusException as mbuse:
            logger.error("ModbusWriter exception: "+format(mbuse))
            pass
        while not self.stop.wait(self.time):
            ###
            # WRITE OPERATION
            try:
                for self.register in self.intervals:
                    rq = self.client.write_registers(self.register[0], self.register[1], unit=1)
            except ModbusException as mbuse:
                logger.error("ModbusWriter Exception: "+format(mbuse))
                pass
        # When alive is False
        self.client.close()

    def __init__(self, event, time):
        QThread.__init__(self)
        self.stop = event
        self.time = time
        self.modbusDict = {}
        self.intervals = []
        self.client = ModbusClient(CONTROL_PANEL_IP, SERVER_MODBUS_PORT)'''


class ModbusWriter():
    def setRegister(self, register):
        self.register = register

        try:
            self.client.connect()
            rq = self.client.write_registers(
                self.register[0], self.register[1], unit=1)
            # rr = self.client.read_holding_registers(self.register[0], 1, unit=1)
        except ModbusException as mbuse:
            logger.error("ModbusWriter Exception: "+format(mbuse))
            pass
        finally:
            self.client.close()

    def __init__(self):
        self.client = ModbusClient(CONTROL_PANEL_IP, SERVER_MODBUS_PORT)


'''
    Oggetto che legge un singolo registro MODBUS
    NON UTILIZZATO
'''


class ModbusReaderSingleReg():
    def readHoldingRegisters(self, first_register, n):
        self.client.connect()
        rr = self.client.read_holding_registers(first_register, n, unit=1)
        self.client.close()
        return rr.registers

    def __init__(self):
        self.client = ModbusClient(CONTROL_PANEL_IP, SERVER_MODBUS_PORT)


'''
    Oggetto che si occupa della lettura dei registri MODBUS.
'''


class ModbusReader(QThread):
    modbusSignal = pyqtSignal(dict)
    heartbitSignal = pyqtSignal(bool)

    def setRegisters(self, intervals):
        self.intervals = intervals
        self.modbusDict = {}
        self.heartbitCounter = 0
        self.heartbit = -1

    def run(self):
        self.modbusDict = {}
        try:
            self.client.connect()
        except ModbusException as mbuse:
            logger.error("ModbusReader exception: "+format(mbuse))
            pass
        while not self.stop.wait(self.time):
            ##
            # HEARTBIT
            try:
                rr = self.client.read_holding_registers(
                    INPUT_HEARTBIT[0], INPUT_HEARTBIT[1], unit=1)
                if rr.registers[0] == self.heartbit:
                    self.heartbitCounter = self.heartbitCounter + 1
                else:
                    self.heartbitCounter = 0
                    self.heartbit = rr.registers[0]
                # Indica il timeout dell'errore di lettura del PLC, attualmente scatta a 10s, dato che la funzione gira ogni 100ms
                if self.heartbitCounter == HEARTBIT_COUNTER_ERROR:
                    self.heartbitSignal.emit(True)
                    self.heartbitCounter = 0
            except ModbusException as mbuse:
                logger.error("ModbusReader exception: "+format(mbuse))
                pass
            except AttributeError as ae:
                logger.error("AttributeError exception: "+format(ae))
                pass

            ##
            # READING OPERATION
            modbusDict = {}
            # - Per ogni tupla nell'intervallo di registri cerca i registri e mettili nel dizionario
            # - Setta indice partenza del dizionario
            # - Per ogni registro aggiorna chiave/valore in modbusDict
            # print("INTERVALS:", self.intervals)
            try:
                for e in self.intervals:
                    rr = self.client.read_holding_registers(e[0], e[1], unit=1)
                    i = e[0]
                    for j in rr.registers:
                        modbusDict.update({str(i): j})
                        i = i + 1
                # self.modbusSignal.emit(modbusDict)
                # self.modbusDict = modbusDict

                # PER ORA NON NECESSARIO, SOLO SE PROCESSO SUBISCE STUCK
                if self.modbusDict != modbusDict:
                    self.modbusSignal.emit(modbusDict)
                    self.modbusDict = modbusDict
            except ModbusException as mbuse:
                logger.error("ModbusReader exception: "+format(mbuse))
                pass
        # When alive is False
        self.client.close()

    def __init__(self, event, time):
        QThread.__init__(self)
        self.stop = event
        self.time = time
        self.modbusDict = {}
        self.intervals = []
        self.client = ModbusClient(CONTROL_PANEL_IP, SERVER_MODBUS_PORT)
        self.heartbitCounter = 0
        self.heartbit = -1

# REV. 5.0


class InitFrame(QFrame):
    check_sig = pyqtSignal(int)
    hid_sig = pyqtSignal(str)       # OBSOLETO

    '''
        Ottiene l'intero dizionario di traduzioni presenti sul DB
    '''

    def getLangDict(self):
        return self.lang_dictionary

    '''
        Ottiene l'intero dizionario delle frasi del sinottico, presenti sul DB.
        (con frasi del sinottico si intende frasi che vengono mostrate al di sotto dell'immagine presente in produzione)
    '''

    def getSynopticString(self):
        return self.synoptic

    '''
        Imposta la gif di caricamento per i vari moduli, PLC, Modbus server e DB
    '''

    def initMe(self):
        if LINUX:
            movie = QMovie(IMG_LINUX_PATH+"loading.gif")
        else:
            movie = QMovie(os.path.join(IMG_WIN_PATH, "loading.gif"))
        movie.setScaledSize(
            QSize(self.dbTestIconLabel.width(), self.dbTestIconLabel.height()))
        self.dbTestIconLabel.setMovie(movie)
        self.modbusTestIconLabel.setMovie(movie)
        movie.start()
        self.setVisible(True)

        self.err = False

        thread_test = Thread(target=self.pingTest)
        thread_test.start()

    '''
        Nasconde il frame con le immagini di caricamento per i moduli
    '''

    def finishMe(self):
        self.setVisible(False)

    '''
        Esegue un ping di test per verificare il corretto collegamento dei servizi utilizzati e dispositivi,
        PLC, server modbus e DB.
        Inoltre salva nelle variabili self.lang_dictionary e self.synoptic i risultati delle query effettuate,
        la classica definizione di unire utile a dilettevole.
    '''

    def pingTest(self):
        defLang = "description_EN"
        sql = "SELECT value FROM configuration WHERE configuration_id='default_lang'"
        value = {}
        records, n_row, err = selectMethod(sql, value, logger)
        if not err and n_row > 0:
            if records[0][0] == 1:
                defLang = "description_IT"
            elif records[0][0] == 2:
                defLang = "description_EN"
            elif records[0][0] == 3:
                defLang = "description_LANG1"
            elif records[0][0] == 4:
                defLang = "description_LANG2"
            else:
                defLang = "description_EN"
        # Test DB connection
        sql = "SELECT international_id, phase, " + \
            defLang.replace("description_", "") + " FROM international"
        value = {}
        records, n_row, err = selectMethod(sql, value, logger)
        if err:
            self.err = True
            if LINUX:
                self.dbTestIconLabel.setPixmap(QPixmap(IMG_LINUX_PATH+"cancel.png").scaled(
                    self.dbTestIconLabel.width()-10, self.dbTestIconLabel.height()-10))
            else:
                self.dbTestIconLabel.setPixmap(QPixmap(os.path.join(IMG_WIN_PATH, "cancel.png")).scaled(
                    self.dbTestIconLabel.width()-10, self.dbTestIconLabel.height()-10))
        else:
            self.lang_dictionary = records
            sql = "SELECT synoptic_id, " + \
                defLang.replace("description_", "") + " FROM synoptic"
            value = {}
            records, n_row, err = selectMethod(sql, value, logger)
            if not err:
                self.synoptic = records
                if LINUX:
                    self.dbTestIconLabel.setPixmap(QPixmap(IMG_LINUX_PATH+"checked.png").scaled(
                        self.dbTestIconLabel.width(), self.dbTestIconLabel.height()))
                else:
                    self.dbTestIconLabel.setPixmap(QPixmap(os.path.join(IMG_WIN_PATH, "checked.png")).scaled(
                        self.dbTestIconLabel.width(), self.dbTestIconLabel.height()))
            else:
                if LINUX:
                    self.dbTestIconLabel.setPixmap(QPixmap(IMG_LINUX_PATH+"cancel.png").scaled(
                        self.dbTestIconLabel.width()-10, self.dbTestIconLabel.height()-10))
                else:
                    self.dbTestIconLabel.setPixmap(QPixmap(os.path.join(IMG_WIN_PATH, "cancel.png")).scaled(
                        self.dbTestIconLabel.width()-10, self.dbTestIconLabel.height()-10))

        # Test modbus server connection
        client = ModbusClient(CONTROL_PANEL_IP, SERVER_MODBUS_PORT)
        c = 5
        while (c > 0):
            try:
                c = client.connect()
                rr = client.read_holding_registers(161, 1, unit=1)
                client.close()
                if LINUX:
                    self.modbusTestIconLabel.setPixmap(QPixmap(IMG_LINUX_PATH+"checked.png").scaled(
                        self.modbusTestIconLabel.width(), self.modbusTestIconLabel.height()))
                else:
                    self.modbusTestIconLabel.setPixmap(QPixmap(os.path.join(IMG_WIN_PATH, "checked.png")).scaled(
                        self.modbusTestIconLabel.width(), self.modbusTestIconLabel.height()))
                c = 0
            except ModbusException as mbuse:
                self.err = True
                if LINUX:
                    self.modbusTestIconLabel.setPixmap(QPixmap(IMG_LINUX_PATH+"cancel.png").scaled(
                        self.modbusTestIconLabel.width()-10, self.modbusTestIconLabel.height()-10))
                else:
                    self.modbusTestIconLabel.setPixmap(QPixmap(os.path.join(IMG_WIN_PATH, "cancel.png")).scaled(
                        self.modbusTestIconLabel.width()-10, self.modbusTestIconLabel.height()-10))
                c = c-1
        '''
        if LINUX:
            res = os.system("ping -c 2 " + PRINTER_IP)
            #res = 0
        else:
            #res = os.system("ping " + PRINTER_IP)
            res = 0
        if res == 0:
            self.printerTestIconLabel.setPixmap(QPixmap("img/checked.png").scaled(self.printerTestIconLabel.width(),self.printerTestIconLabel.height()))
        else:
            self.err = True 
            self.printerTestIconLabel.setPixmap(QPixmap("img/cancel.png").scaled(self.printerTestIconLabel.width()-10,self.printerTestIconLabel.height()-10))
        '''
        if LINUX:
            res = os.system("ping -c 2 " + PLC_IP)
            # res = 0
        else:
            # res = os.system("ping " + PLC_IP)
            res = 0
        if res == 0:
            if LINUX:
                self.plcTestIconLabel.setPixmap(QPixmap(IMG_LINUX_PATH+"checked.png").scaled(
                    self.plcTestIconLabel.width(), self.plcTestIconLabel.height()))
            else:
                self.plcTestIconLabel.setPixmap(QPixmap(os.path.join(IMG_WIN_PATH, "checked.png")).scaled(
                    self.plcTestIconLabel.width(), self.plcTestIconLabel.height()))
        else:
            self.err = True
            if LINUX:
                self.plcTestIconLabel.setPixmap(QPixmap(IMG_LINUX_PATH+"cancel.png").scaled(
                    self.plcTestIconLabel.width()-10, self.plcTestIconLabel.height()-10))
            else:
                self.plcTestIconLabel.setPixmap(QPixmap(os.path.join(IMG_WIN_PATH, "cancel.png")).scaled(
                    self.plcTestIconLabel.width()-10, self.plcTestIconLabel.height()-10))

        # Se è presente un errore
        if self.err:
            self.check_sig.emit(False)
        else:
            self.check_sig.emit(True)

    def __init__(self, parent):
        super(InitFrame, self).__init__(parent)

        self.err = False
        self.lang_dictionary = []
        self.synoptic = []

        self.setGeometry(0, 0, Style.WIDTH, Style.HEIGHT)

        self.frame = QFrame(self)
        self.frame.setGeometry(50, 100, Style.WIDTH-100, Style.HEIGHT-125)
        self.frame.setStyleSheet(Style.INIT_STYLE)

        self.titleLabel = QLabel("Control Panel Initialization", self.frame)
        self.titleLabel.setStyleSheet(Style.TITLE_STYLE)
        self.titleLabel.setGeometry(0, 50, Style.WIDTH, 50)

        self.dbTestIconLabel = QLabel("", self.frame)
        self.dbTestIconLabel.setStyleSheet(
            "QLabel {background-color: rgba(255,255,255,0)}")
        self.dbTestIconLabel.setGeometry(200, 125, 50, 50)
        self.dbTestLabel = QLabel("Database syncing", self.frame)
        self.dbTestLabel.setGeometry(285, 125, 515, 50)
        self.dbTestLabel.setStyleSheet(Style.SUBTITLE_STYLE)

        self.modbusTestIconLabel = QLabel("", self.frame)
        self.modbusTestIconLabel.setStyleSheet(
            "QLabel {background-color: rgba(255,255,255,0)}")
        self.modbusTestIconLabel.setGeometry(200, 225, 50, 50)
        self.modbusTestLabel = QLabel("Modbus Server connection", self.frame)
        self.modbusTestLabel.setGeometry(285, 225, 515, 50)
        self.modbusTestLabel.setStyleSheet(Style.SUBTITLE_STYLE)

        self.printerTestIconLabel = QLabel("", self.frame)
        self.printerTestIconLabel.setStyleSheet(
            "QLabel {background-color: rgba(255,255,255,0)}")
        self.printerTestIconLabel.setGeometry(200, 325, 50, 50)
        self.printerTestLabel = QLabel("Printer Server connection", self.frame)
        self.printerTestLabel.setGeometry(285, 325, 515, 50)
        self.printerTestLabel.setStyleSheet(Style.SUBTITLE_STYLE)
        self.printerTestIconLabel.setVisible(False)
        self.printerTestLabel.setVisible(False)

        self.plcTestIconLabel = QLabel("", self.frame)
        self.plcTestIconLabel.setStyleSheet(
            "QLabel {background-color: rgba(255,255,255,0)}")
        self.plcTestIconLabel.setGeometry(200, 325, 50, 50)
        self.plcTestLabel = QLabel("PLC connection", self.frame)
        self.plcTestLabel.setGeometry(285, 325, 515, 50)
        self.plcTestLabel.setStyleSheet(Style.SUBTITLE_STYLE)
        self.setVisible(False)

# REV. 5.0


class Login(QWidget):
    phase = pyqtSignal(int)

    '''
        Metodo getter per le credenziali
    '''

    def getCredentials(self):
        return self.user_id, self.permission

    '''
        Esegue l'updateData della pagina di login:
        - Crea il dizionario con le stringhe del pannello
    '''

    def updateData(self, lang_dictionary, phase):
        self.updateEdit()
        self.user_id = ""
        self.name = ""
        self.surname = ""
        self.permission = {}
        self.lang_dictionary = {}

        for e in lang_dictionary:
            if e[1] == phase:
                self.lang_dictionary.update({e[0]: e[2]})

        self.descriptionBadgeLabel.setText(
            self.lang_dictionary['descriptionBadgeLabel'])
        self.descriptionSuperLabel.setText(
            self.lang_dictionary['descriptionSuperLabel'])

        self.badgeLoginFrame.setVisible(True)
        self.superLoginFrame.setVisible(False)

    '''
        Riporta le label allo stato iniziale
    '''

    def updateEdit(self):
        self.idSuperLineEdit.setText("")
        self.passwordSuperLineEdit.setText("")
        self.idBadgeLineEdit.setText("")

    '''
        Funzione che porta il pannello nella pagina di settings
    '''

    def goToSettings(self):
        self.phase.emit(PHASE_SHUTDOWN)

    '''
        Funzione che porta il pannello in pagina di home, occupandosi di tutta la parte di autenticazione,
        divisa nei due tipi di login, in base al parametro @logintype
    '''

    def goToMain(self, logintype):
        if logintype == "super":
            voidcounter = 0
            if len(str(self.idSuperLineEdit.text()).strip()) == 0:
                QMessageBox.critical(
                    self, self.lang_dictionary['qmessagebox_error_title'], self.lang_dictionary['qmessagebox_error_userid'])
                voidcounter = voidcounter + 1
            if len(str(self.passwordSuperLineEdit.text()).strip()) == 0:
                QMessageBox.critical(
                    self, self.lang_dictionary['qmessagebox_error_title'], self.lang_dictionary['qmessagebox_error_password'])
                voidcounter = voidcounter + 1
            if voidcounter == 0:
                password = encryptString(
                    str(self.passwordSuperLineEdit.text()).strip())
                sql = "SELECT user_id, name, surname, password, usergroup_id FROM users WHERE user_id = %(user_id)s"
                value = {'user_id': self.idSuperLineEdit.text().strip()}
                records, n_row, err = selectMethod(sql, value, logger)
                if not err:
                    if n_row == 0:
                        QMessageBox.critical(
                            self, self.lang_dictionary['qmessagebox_error_title'], self.lang_dictionary['qmessagebox_error_credentials'])
                        self.updateEdit()
                    else:
                        if records[0][3] == password:
                            self.user_id = records[0][0]
                            self.permission = {}
                            sql = "SELECT productionMode, manualMode, configuration, counters, manualCommands, log, users, superLogin FROM usersgroup WHERE usergroup_id = %(usergroup)s"
                            value = {"usergroup": records[0][4]}
                            records, n_row, err = selectMethod(
                                sql, value, logger)
                            self.permission.update(
                                {"productionMode": records[0][0]})
                            self.permission.update(
                                {"manualMode": records[0][1]})
                            self.permission.update(
                                {"configuration": records[0][2]})
                            self.permission.update({"counters": records[0][3]})
                            self.permission.update(
                                {"manualCommands": records[0][4]})
                            self.permission.update({"log": records[0][5]})
                            self.permission.update({"users": records[0][6]})
                            self.permission.update(
                                {"superLogin": records[0][7]})
                            counter_id, counter_num = self.parent.configuration.getCurrentProduct()
                            insert_userslog_query_method(
                                "LOGIN", self.user_id, counter_id, logger)
                            self.phase.emit(PHASE_HOME)
                        else:
                            QMessageBox.critical(
                                self, self.lang_dictionary['qmessagebox_error_title'], self.lang_dictionary['qmessagebox_error_credentials'])
                            self.updateEdit()
                else:
                    QMessageBox.critical(
                        self, self.lang_dictionary['qmessagebox_error_title'], self.lang_dictionary['qmessagebox_error_credentials'])
                    self.updateEdit()
        elif logintype == "badge":
            if len(str(self.idBadgeLineEdit.text()).strip()) == 0:
                QMessageBox.critical(
                    self, self.lang_dictionary['qmessagebox_error_title'], self.lang_dictionary['qmessagebox_error_idnumber'])
            else:
                sql = "SELECT * FROM (SELECT users.user_id, users.name, users.surname, users.scancode, usersgroup.productionMode, usersgroup.manualMode, usersgroup.configuration, usersgroup.counters, usersgroup.manualCommands, usersgroup.log, usersgroup.users, usersgroup.superLogin FROM users INNER JOIN usersgroup WHERE users.usergroup_id = usersgroup.usergroup_id) \
                    AS user WHERE user.scancode = %(scancode)s"
                value = {'scancode': str(self.idBadgeLineEdit.text()).strip()}
                records, n_row, err = selectMethod(sql, value, logger)
                if not err:
                    if n_row == 0:
                        QMessageBox.critical(
                            self, self.lang_dictionary['qmessagebox_error_title'], self.lang_dictionary['qmessagebox_error_credentials'])
                        self.idBadgeLineEdit.setText("")
                    else:
                        self.user_id = records[0][0]
                        self.permission = {}
                        self.permission.update(
                            {"productionMode": records[0][4]})
                        self.permission.update({"manualMode": records[0][5]})
                        self.permission.update(
                            {"configuration": records[0][6]})
                        self.permission.update({"counters": records[0][7]})
                        self.permission.update(
                            {"manualCommands": records[0][8]})
                        self.permission.update({"log": records[0][9]})
                        self.permission.update({"users": records[0][10]})
                        self.permission.update({"superLogin": records[0][11]})
                        counter_id, counter_num = self.parent.configuration.getCurrentProduct()
                        insert_userslog_query_method(
                            "LOGIN", self.user_id, counter_id, logger)
                        self.phase.emit(PHASE_HOME)
                else:
                    QMessageBox.critical(
                        self, self.lang_dictionary['qmessagebox_error_title'], self.lang_dictionary['qmessagebox_error_credentials'])
                    self.idBadgeLineEdit.setText("")

    '''
        Apre la virtual keuboard nel momento in cui una label viene premuta
    '''

    def callKey(self, edit):
        temp = edit.text()
        self.parent.virtualKeyboard.edit.setText("")
        self.parent.virtualKeyboard.exec_()
        self.parent.virtualKeyboard.edit.setFocus()
        if len(self.parent.virtualKeyboard.sendDateEnter()) == 0:
            edit.setText(temp)
        else:
            edit.setText(self.parent.virtualKeyboard.sendDateEnter())
        edit.repaint()

    '''
        Modifica la modalità di visualizzazione delle label di login tra login manuale e con badge
    '''

    def changeLogin(self, logintype):
        if logintype == "super":
            self.idSuperLineEdit.setText("")
            self.passwordSuperLineEdit.setText("")
            self.badgeLoginFrame.setVisible(False)
            self.superLoginFrame.setVisible(True)
        elif logintype == "badge":
            self.idBadgeLineEdit.setText("")
            self.badgeLoginFrame.setVisible(True)
            self.superLoginFrame.setVisible(False)

    '''
        Funzione che inserisce nella label dedicata il codice del badge ottenuto dalla lettura del reader
    '''

    def setScancode(self, scancode):
        self.idBadgeLineEdit.setEnabled(True)
        self.idBadgeLineEdit.setText(scancode)
        self.idBadgeLineEdit.setEnabled(False)

    def __init__(self, parent):
        super(Login, self).__init__(parent)

        self.parent = parent
        self.lang_dictionary = {}
        self.user_id = ""
        self.permission = {}

        ##
        # LOGIN CON BADGE

        self.badgeLoginFrame = QFrame(self)
        self.badgeLoginFrame.setGeometry(0, 60, Style.WIDTH, Style.HEIGHT-140)

        self.titleBadgeLabel = QLabel("BADGE LOGIN", self.badgeLoginFrame)
        self.titleBadgeLabel.setGeometry(
            0, 100, self.badgeLoginFrame.width(), 50)
        self.titleBadgeLabel.setStyleSheet(Style.TITLE_STYLE)

        self.descriptionBadgeLabel = QLabel("", self.badgeLoginFrame)
        self.descriptionBadgeLabel.setGeometry(
            0, 210, self.badgeLoginFrame.width(), 50)
        self.descriptionBadgeLabel.setStyleSheet(Style.SUBTITLE_CENTERED_STYLE)

        self.idBadgeLineEdit = QLineEdit(self.badgeLoginFrame)
        self.idBadgeLineEdit.setGeometry(
            300, 275, self.badgeLoginFrame.width()-600, 50)
        self.idBadgeLineEdit.setStyleSheet(Style.TITLE3_LINEEDIT)
        self.idBadgeLineEdit.setEchoMode(QLineEdit.Password)

        if LINUX:
            self.idBadgeLineEdit.setEnabled(False)

        self.okButtonBadge = QPushButton("OK", self.badgeLoginFrame)
        self.okButtonBadge.setGeometry(
            int((self.badgeLoginFrame.width()/2)-125), 350, 100, 75)
        self.okButtonBadge.setStyleSheet(Style.BUTTONMENU_STYLE)
        self.okButtonBadge.clicked.connect(lambda: self.goToMain("badge"))

        self.changeFrameFromBadgeButton = QPushButton("", self.badgeLoginFrame)
        self.changeFrameFromBadgeButton.setGeometry(
            int((self.badgeLoginFrame.width()/2) + 25), 350, 100, 75)
        self.changeFrameFromBadgeButton.setStyleSheet(Style.BUTTONMENU_STYLE)
        if LINUX:
            changeFrameFromBadgeIcon = QIcon(IMG_LINUX_PATH+"key.png")
        else:
            changeFrameFromBadgeIcon = QIcon(
                os.path.join(IMG_WIN_PATH, "key.png"))
        self.changeFrameFromBadgeButton.setIcon(changeFrameFromBadgeIcon)
        self.changeFrameFromBadgeButton.setIconSize(QSize(
            self.changeFrameFromBadgeButton.width()-25, self.changeFrameFromBadgeButton.height()-25))
        self.changeFrameFromBadgeButton.clicked.connect(
            lambda: self.changeLogin("super"))

        ##
        # LOGIN MANUALE
        self.superLoginFrame = QFrame(self)
        self.superLoginFrame.setGeometry(0, 60, Style.WIDTH, Style.HEIGHT-140)

        self.titleSuperLabel = QLabel("USER LOGIN", self.superLoginFrame)
        self.titleSuperLabel.setGeometry(
            0, 75, self.superLoginFrame.width(), 50)
        self.titleSuperLabel.setStyleSheet(Style.TITLE_STYLE)

        self.descriptionSuperLabel = QLabel("", self.superLoginFrame)
        self.descriptionSuperLabel.setGeometry(
            0, 150, self.superLoginFrame.width(), 50)
        self.descriptionSuperLabel.setStyleSheet(Style.SUBTITLE_CENTERED_STYLE)

        self.idSuperLabel = QLabel("User ID", self.superLoginFrame)
        self.idSuperLabel.setGeometry(
            0, 225, int(self.superLoginFrame.width()/3), 50)
        self.idSuperLabel.setStyleSheet(Style.TITLE2_CENTERED_STYLE)

        self.idSuperLineEdit = ClickableLineEdit(self.superLoginFrame)
        self.idSuperLineEdit.setGeometry(int(self.superLoginFrame.width(
        )/3), 225, int(self.superLoginFrame.width()/3*1.7-50), 50)
        self.idSuperLineEdit.setStyleSheet(Style.TITLE3_LINEEDIT)
        self.idSuperLineEdit.clicked.connect(
            lambda: self.callKey(self.idSuperLineEdit))

        self.passwordSuperLabel = QLabel("Password", self.superLoginFrame)
        self.passwordSuperLabel.setGeometry(
            0, 300, int(self.superLoginFrame.width()/3), 50)
        self.passwordSuperLabel.setStyleSheet(Style.TITLE2_CENTERED_STYLE)

        self.passwordSuperLineEdit = ClickableLineEdit(self.superLoginFrame)
        self.passwordSuperLineEdit.setGeometry(int(self.superLoginFrame.width(
        )/3), 300, int(self.superLoginFrame.width()/3*1.7-50), 50)
        self.passwordSuperLineEdit.setStyleSheet(Style.TITLE3_LINEEDIT)
        self.passwordSuperLineEdit.clicked.connect(
            lambda: self.callKey(self.passwordSuperLineEdit))
        self.passwordSuperLineEdit.setEchoMode(QLineEdit.Password)

        self.changeFrameFromSuperButton = QPushButton("", self.superLoginFrame)
        self.changeFrameFromSuperButton.setGeometry(
            int(self.superLoginFrame.width()/3), 375, 100, 75)
        self.changeFrameFromSuperButton.setStyleSheet(Style.BUTTONMENU_STYLE)
        if LINUX:
            changeFrameFromSuperIcon = QIcon(IMG_LINUX_PATH+"hid.png")
        else:
            changeFrameFromSuperIcon = QIcon(
                os.path.join(IMG_WIN_PATH, "hid.png"))
        self.changeFrameFromSuperButton.setIcon(changeFrameFromSuperIcon)
        self.changeFrameFromSuperButton.setIconSize(QSize(int(
            self.changeFrameFromSuperButton.width()-25), self.changeFrameFromSuperButton.height()-25))
        self.changeFrameFromSuperButton.clicked.connect(
            lambda: self.changeLogin("badge"))
        # self.changeFrameFromSuperButton.setVisible(False)

        self.okButtonSuper = QPushButton("OK", self.superLoginFrame)
        self.okButtonSuper.setGeometry(
            int(self.superLoginFrame.width()/3 + 120), 375, 100, 75)
        # self.okButtonSuper.setGeometry(self.superLoginFrame.width()/3,450,100,75)
        self.okButtonSuper.setStyleSheet(Style.BUTTONMENU_STYLE)
        self.okButtonSuper.clicked.connect(lambda: self.goToMain("super"))

        ##
        # ALTRI OGGETTI

        self.settingsButton = QPushButton(self)
        self.settingsButton.setGeometry(int(Style.BUTTONBAR_WIDTH*8+Style.BUTTONBAR_X*8),
                                        Style.BUTTONBAR_Y, Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT)
        if LINUX:
            settingsImage = QIcon(IMG_LINUX_PATH+"settings.png")
        else:
            settingsImage = QIcon(os.path.join(IMG_WIN_PATH, "settings.png"))
        self.settingsButton.setIcon(settingsImage)
        self.settingsButton.setIconSize(
            QSize(self.settingsButton.width(), self.settingsButton.height()))
        self.settingsButton.clicked.connect(self.goToSettings)
        self.settingsButton.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.settingsButton.setVisible(False)

# REV. 5.0


class Home(QWidget):
    phase = pyqtSignal(int)

    '''
        Metodo getter per il dizionario
    '''

    def getLangDict(self):
        return self.lang_dictionary

    '''
        Ottiene il valore di registri contenti informazioni sulla produzione selezionata, quando queste sono fornite da un multicavo ad esempio,
        o da una codifica particolare di posaggi
    '''

    def getPlc(self, modbusDict):
        '''
        if self.enable_manconf == 0:
            if modbusDict[INPUT_CONF_PLC_COUNTERNUM] > 9:
                temp_counter_num=0
            else:
                temp_counter_num=modbusDict[INPUT_CONF_PLC_COUNTERNUM]
            if temp_counter_num < 1:
                self.enable_production = False
            else:
                self.enable_production = True

            if self.counter_num != temp_counter_num:
                self.counter_num = temp_counter_num
                sql = "SELECT counter_id FROM counters WHERE counter_num = %s"
                err, res = new_select_query_method(sql, (self.counter_num,))
                self.ttModbus.setRegister((OUTPUT_CONF_COUNTERNUM, self.counter_num))
                self.counter_id = res[0][0]
                reset_counter_selected_query_method()
                update_counter_selected_query_method(self.counter_id)
                self.prod_label.setText(res[0][0])
        '''

    '''
        Esegue l'updateData della classe Home:
        - Compone il dizionario
        - Aggiorna il prodotto corrente selzionato
    '''

    def updateData(self, lang_dictionary, phase, user_id, counter_id, counter_num):
        self.lang_dictionary = {}
        self.counter_id = counter_id
        self.counter_num = counter_num

        for e in lang_dictionary:
            if e[1] == phase:
                self.lang_dictionary.update({e[0]: e[2]})

        self.autoModeButton.setText(self.lang_dictionary["button_auto"])
        self.manualModeButton.setText(self.lang_dictionary["button_manual"])
        self.configurationButton.setText(
            self.lang_dictionary["button_configuration"])
        self.countersButton.setText(self.lang_dictionary["button_counters"])
        self.manualCommandsButton.setText(
            self.lang_dictionary["button_manualcommands"])
        self.logButton.setText(self.lang_dictionary["button_log"])
        self.prod_n_label.setText(self.lang_dictionary["label_currentprod"])
        self.userIdLabel.setText(user_id)
        self.ttModbus.setRegister((OUTPUT_COUNTER_NUM, self.counter_num))

        if self.parent.permission['superLogin'] == 'yes':
            self.idt.setEnabled(True)
        elif self.parent.permission['superLogin'] == 'no':
            self.idt.setEnabled(False)

        self.enable_printer = 0
        self.enable_manconf = 0
        sql = "SELECT configuration_id, value FROM configuration"
        value = {}
        records, n_row, err = selectMethod(sql, value, logger)
        if not err:
            for e in records:
                if e[0] == "enable_printer":
                    self.enable_printer = int(e[1])
                    # self.ttModbus.setRegister((OUTPUT_CONF_ENAPRINTER, self.enable_printer))
                if e[0] == "enable_manconf":
                    self.enable_manconf = int(e[1])

        '''
        if self.enable_manconf == 1:
            #QMessageBox.warning(self, self.lang_dictionary["label_warning"], self.lang_dictionary["label_warnconf"])
            self.ttModbus.setRegister((OUTPUT_CONF_MANUALCONFIG, 1))
        else:
            self.ttModbus.setRegister((OUTPUT_CONF_MANUALCONFIG, 0))
        '''

        '''
        #self.enable_production = False
        if self.counter_num == 0:
            QMessageBox.critical(self, self.lang_dictionary["label_warning"], self.lang_dictionary["label_warninvalidconfnone"])
            self.enable_production = False
        elif self.counter_num > 0 and self.counter_num < 1:
            QMessageBox.critical(self, self.lang_dictionary["label_warning"], self.lang_dictionary["label_warninvalidconf"])
            self.enable_production = False
        else:
            self.enable_production = True
        '''
        # self.ttModbus.setRegister((OUTPUT_CONF_COUNTERNUM, self.counter_num))
        self.prod_label.setText(self.counter_id)

        self.stopModbusTimer.clear()
        self.tModbus.start()

    '''
        Metodo getter per verificare l'abilitazione della configurazione manuale
    '''

    def getEnabledManConf(self):
        return self.enable_manconf

    '''
        Metodo getter per verificare l'abilitazione della stampante
    '''

    def getEnabledPrinter(self):
        return self.enable_printer

    '''
        Verifica che il pulsante della modalità manuale sia stato selezionato
    '''

    def getManualEnabling(self):
        if self.manualModeButton.palette().button().color().red() == 0 and self.manualModeButton.palette().button().color().green() == 255 and self.manualModeButton.palette().button().color().blue() == 0:
            return True
        else:
            return False

    '''
        Funzione che effettua il logout
    '''

    def goToLogin(self):
        reply = QMessageBox.question(
            self, "Logout", self.lang_dictionary["qmessagebox_information_logout"], QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            insert_userslog_query_method(
                "LOGOUT", self.userIdLabel.text(), self.counter_id, logger)
            self.changePhase(PHASE_LOGIN)

    '''
        Si sposta nella pagina della produzione automatica
    '''

    def goToAuto(self):
        self.autoModeButton.setStyleSheet(
            "QPushButton{font: bold;font-size: 20px; font-family:'Arial';color : black; background: rgba(0,255,0,0.8); border: 2px solid #262626; border-radius: 16px; color: #262626;}")
        self.manualModeButton.setStyleSheet(
            "QPushButton{font: bold;font-size: 20px; font-family: 'Arial';color : black; background: rgba(255,0,0,0.8); border: 2px solid #262626; border-radius: 16px; color: #262626;}")
        self.ttModbus.setRegister((OUTPUT_ALARM_ACCEPTED[0], 0))
        # self.ttModbus.setRegister((OUTPUT_START_PRODUCTION, 0))

        self.changePhase(PHASE_PRODUCTION)

    '''
        Funzione che si sposta nella pagina dei comandi manuali, se il pulsante è stato selezionato
    '''

    def goToManual(self):
        if self.getManualEnabling() == True:
            self.changePhase(PHASE_MANUAL)
        else:
            QMessageBox.critical(
                self, self.lang_dictionary["qmessagebox_error_title"], self.lang_dictionary["qmessagebox_error_manualmodedisabled"])

    '''
        Set della label con l'ora e la data corrente
    '''

    def timeSignal(self, val):
        self.labelh5.setText(val)
        self.labelh5.repaint()

    '''
        Istanza e start del thread che imposta la label con il tempo che scorre
    '''

    def startTime(self):
        self.thread = TimeThread()
        self.thread.trigger.connect(self.timeSignal)
        self.thread.start()

    '''
        Colora ed imposta il registro che indica la modalità attualmente selezionata, se auto o manuale
    '''

    def setCurrentMode(self):
        self.manualModeButton.setStyleSheet(
            "QPushButton{font: bold;font-size: 20px; font-family: 'Arial';color : black; background: rgba(0,255,0,0.8); border: 2px solid #262626; border-radius: 16px; color: #262626;}")
        self.autoModeButton.setStyleSheet(
            "QPushButton{font: bold;font-size: 20px; font-family: 'Arial';color : black; background: rgba(255,0,0,0.8); border: 2px solid #262626; border-radius: 16px; color: #262626;}")

    '''
        Cambio di fase
    '''

    def changePhase(self, n):
        self.stopModbusTimer.set()
        self.phase.emit(n)

    def __init__(self, parent):
        super(Home, self).__init__(parent)
        self.parent = parent
        self.lang_dictionary = {}
        self.counter_id = ""

        ##
        # MAIN MENU
        self.autoModeButton = QPushButton("", self)
        self.autoModeButton.setGeometry(225, 100, 300, 90)
        self.autoModeButton.setStyleSheet(Style.BUTTONMENU_STYLE)
        self.autoModeButton.clicked.connect(self.goToAuto)

        self.manualModeButton = QPushButton("", self)
        self.manualModeButton.setGeometry(555, 100, 300, 90)
        self.manualModeButton.setStyleSheet(Style.BUTTONMENU_STYLE)
        self.manualModeButton.clicked.connect(self.setCurrentMode)

        self.configurationButton = QPushButton("", self)
        self.configurationButton.setGeometry(225, 220, 300, 90)
        self.configurationButton.setStyleSheet(Style.BUTTONMENU_STYLE)
        self.configurationButton.clicked.connect(
            lambda: self.changePhase(PHASE_CONFIGURATION))
        # self.configurationButton.setEnabled(False)

        self.countersButton = QPushButton("", self)
        self.countersButton.setGeometry(555, 220, 300, 90)
        self.countersButton.setStyleSheet(Style.BUTTONMENU_STYLE)
        self.countersButton.clicked.connect(lambda: self.changePhase(4))

        self.manualCommandsButton = QPushButton("", self)
        self.manualCommandsButton.setGeometry(225, 340, 300, 90)
        self.manualCommandsButton.setStyleSheet(Style.BUTTONMENU_STYLE)
        self.manualCommandsButton.clicked.connect(self.goToManual)

        self.logButton = QPushButton("", self)
        self.logButton.setGeometry(555, 340, 300, 90)
        self.logButton.setStyleSheet(Style.BUTTONMENU_STYLE)
        self.logButton.clicked.connect(lambda: self.changePhase(PHASE_LOG))

        ##
        # BUTTONBAR
        self.user = QPushButton("", self)
        self.user.setGeometry(int(Style.BUTTONBAR_WIDTH*5+Style.BUTTONBAR_X*5),
                              Style.BUTTONBAR_Y, Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT)
        self.user.setStyleSheet(Style.BUTTONBAR_STYLE)
        if LINUX:
            userImage = QIcon(IMG_LINUX_PATH+"user.png")
        else:
            userImage = QIcon(os.path.join(IMG_WIN_PATH, "user.png"))
        self.user.setIcon(userImage)
        self.user.setIconSize(QSize(self.user.width(), self.user.height()))
        self.user.clicked.connect(lambda: self.changePhase(PHASE_USERS))
        self.user.setStyleSheet(Style.BUTTONBAR_STYLE)

        self.datetime = QPushButton("", self)
        self.datetime.setGeometry(int(Style.BUTTONBAR_WIDTH*7+Style.BUTTONBAR_X*7),
                                  Style.BUTTONBAR_Y, Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT)
        self.datetime.setStyleSheet(Style.BUTTONBAR_STYLE)
        if LINUX:
            datetimeImage = QIcon(IMG_LINUX_PATH+"datetime.png")
        else:
            datetimeImage = QIcon(os.path.join(IMG_WIN_PATH, "datetime.png"))
        self.datetime.setIcon(datetimeImage)
        self.datetime.setIconSize(
            QSize(self.datetime.width(), self.datetime.height()))
        self.datetime.clicked.connect(lambda: self.changePhase(PHASE_DATETIME))
        self.datetime.setStyleSheet(Style.BUTTONBAR_STYLE)

        self.lang = QPushButton("", self)
        self.lang.setGeometry(Style.BUTTONBAR_WIDTH*6+Style.BUTTONBAR_X*6,
                              Style.BUTTONBAR_Y, Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT)
        self.lang.setStyleSheet(Style.BUTTONBAR_STYLE)
        if LINUX:
            langImage = QIcon(IMG_LINUX_PATH+"lang.png")
        else:
            langImage = QIcon(os.path.join(IMG_WIN_PATH, "lang.png"))
        self.lang.setIcon(langImage)
        self.lang.setIconSize(QSize(self.lang.width(), self.lang.height()))
        self.lang.clicked.connect(lambda: self.changePhase(PHASE_LANG))
        self.lang.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.lang.setEnabled(True)

        self.idt = QPushButton("", self)
        self.idt.setGeometry(int(Style.BUTTONBAR_WIDTH*4+Style.BUTTONBAR_X*4),
                             Style.BUTTONBAR_Y, Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT)
        self.idt.setStyleSheet(Style.BUTTONBAR_STYLE)
        if LINUX:
            idtImage = QIcon(IMG_LINUX_PATH+"idt_black.png")
        else:
            idtImage = QIcon(os.path.join(IMG_WIN_PATH, "idt_black.png"))
        self.idt.setIcon(idtImage)
        self.idt.setIconSize(
            QSize(self.idt.width() - 20, self.idt.height() - 20))
        self.idt.clicked.connect(lambda: self.changePhase(16))
        self.idt.setStyleSheet(Style.BUTTONBAR_STYLE)

        self.logout = QPushButton("", self)
        self.logout.setGeometry(int(Style.BUTTONBAR_WIDTH*8+Style.BUTTONBAR_X*8),
                                Style.BUTTONBAR_Y, Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT)
        if LINUX:
            logoutImage = QIcon(IMG_LINUX_PATH+"logout.png")
        else:
            logoutImage = QIcon(os.path.join(IMG_WIN_PATH, "logout.png"))
        self.logout.setIcon(logoutImage)
        self.logout.setIconSize(
            QSize(self.logout.width(), self.logout.height()))
        self.logout.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.logout.clicked.connect(self.goToLogin)

        ##
        # LABELS
        self.prod_n_label = QLabel("", self)
        self.prod_n_label.setGeometry(225, 425, 200, 100)
        self.prod_n_label.setWordWrap(True)
        self.prod_n_label.setStyleSheet(Style.TITLE5_CENTERED_STYLE)

        self.prod_label = QLabel("", self)
        self.prod_label.setGeometry(425, 450, 440, 45)
        self.prod_label.setWordWrap(True)
        self.prod_label.setStyleSheet(Style.BODY4_BG_CENTERED_STYLE)

        self.userIdNLabel = QLabel("User ID:", self)
        self.userIdNLabel.setGeometry(250, 25, 125, 50)
        self.userIdNLabel.setStyleSheet(Style.TITLE5_STYLE)

        self.userIdLabel = QLabel(self)
        self.userIdLabel.setGeometry(350, 25, 150, 50)
        self.userIdLabel.setStyleSheet(Style.BODY4_BG_CENTERED_STYLE)

        self.startTime()
        self.labelh5 = QLabel(self)
        self.labelh5.setGeometry(550, 25, 300, 50)
        self.labelh5.setStyleSheet(Style.BODY4_BG_CENTERED_STYLE)

        self.ttModbus = ModbusWriter()

        self.stopModbusTimer = Event()
        self.tModbus = ModbusReader(self.stopModbusTimer, MODBUS_TIMER)
        self.tModbus.setRegisters(INPUT_CONFIGURATION)
        self.tModbus.modbusSignal.connect(self.getPlc)

# REV. 5.0


class Lang(QWidget):
    phase = pyqtSignal(int)

    def updateData(self, lang_dictionary, phase):
        self.lang_dictionary = {}
        for e in lang_dictionary:
            if e[1] == phase:
                self.lang_dictionary.update({e[0]: e[2]})

        self.title.setText(self.lang_dictionary["title_label"])

    def __init__(self, parent):
        super(Lang, self).__init__(parent)
        self.parent = parent
        self.lang_dictionary = {}

        self.title = QLabel("", self)
        self.title.setGeometry(0, 75, Style.WIDTH, 50)
        self.title.setStyleSheet(Style.TITLE2_CENTERED_STYLE)

        self.it = QPushButton("", self)
        self.it.setGeometry(415, 150, 200, 200)
        self.it.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.it.clicked.connect(lambda: self.phase.emit(PHASE_IT))
        if LINUX:
            self.it.setIcon(QIcon(IMG_LINUX_PATH+"it.png"))
        else:
            self.it.setIcon(QIcon(os.path.join(IMG_WIN_PATH, "it.png")))
        self.it.setIconSize(QSize(self.it.width()-20, self.it.height()))

        self.en = QPushButton("", self)
        self.en.setGeometry(665, 150, 200, 200)
        self.en.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.en.clicked.connect(lambda: self.phase.emit(PHASE_EN))
        if LINUX:
            self.en.setIcon(QIcon(IMG_LINUX_PATH+"en.png"))
        else:
            self.en.setIcon(QIcon(os.path.join(IMG_WIN_PATH, "en.png")))
        self.en.setIconSize(QSize(self.en.width()-20, self.en.height()))

        self.lang1 = QPushButton("", self)
        self.lang1.setGeometry(150, 150, 200, 200)
        self.lang1.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.lang1.clicked.connect(lambda: self.phase.emit(PHASE_LANG1))
        if LINUX:
            self.lang1.setIcon(QIcon(IMG_LINUX_PATH+"pl.png"))
        else:
            self.lang1.setIcon(QIcon(os.path.join(IMG_WIN_PATH, "pl.png")))
        self.lang1.setIconSize(QSize(self.it.width()-20, self.it.height()))
        self.lang1.setVisible(True)

        self.lang2 = QPushButton("", self)
        self.lang2.setGeometry(665, 400, 200, 200)
        self.lang2.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.lang2.clicked.connect(lambda: self.phase.emit(PHASE_LANG2))
        if LINUX:
            self.lang2.setIcon(QIcon(IMG_LINUX_PATH+"en.png"))
        else:
            self.lang2.setIcon(QIcon(os.path.join(IMG_WIN_PATH, "en.png")))
        self.lang2.setIconSize(QSize(self.en.width()-20, self.en.height()))
        self.lang2.setVisible(False)

        self.buttonHome = QPushButton("", self)
        self.buttonHome.setGeometry(int(Style.BUTTONBAR_X), int(
            Style.BUTTONBAR_Y), int(Style.BUTTONBAR_WIDTH), int(Style.BUTTONBAR_HEIGHT))
        self.buttonHome.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.buttonHome.clicked.connect(lambda: self.phase.emit(PHASE_HOME))
        if LINUX:
            homeImage = QIcon(IMG_LINUX_PATH+"home.png")
        else:
            homeImage = QIcon(os.path.join(IMG_WIN_PATH, "home.png"))
        self.buttonHome.setIcon(homeImage)
        self.buttonHome.setIconSize(
            QSize(int(Style.BUTTONBAR_WIDTH - 20), int(Style.BUTTONBAR_HEIGHT - 20)))

# REV. 5.0


class DatabaseOptions:
    '''
        Resetta i contatori dei singoli prodotti, DX e SX
    '''

    def resetCounters(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(
            "COUNTERS HARD RESET Requested. Do you really want to proceed?")
        msg.setWindowTitle("Database Advanced Options")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        reply = msg.exec_()
        if reply == QMessageBox.Yes:
            update_counters_psx_query_method(
                0, 0, 0, 0, self.parent.parent.counter_id, logger)
            update_counters_pdx_query_method(
                0, 0, 0, 0, self.parent.parent.counter_id, logger)
            # update_configuration_query_method("totalGood", 0)
            # update_configuration_query_method("totalRefuse", 0)

    '''
        Svuota la tabella contenente i log di produzione
    '''

    def resetProdlog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(
            "COUNTERS HARD RESET Requested. Do you really want to proceed?")
        msg.setWindowTitle("Database Advanced Options")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        reply = msg.exec_()
        if reply == QMessageBox.Yes:
            truncate_query_method("prod_log", logger)

    '''
        Svuota la tabella contenente i log degli allarmi
    '''

    def resetAlarmlog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(
            "COUNTERS HARD RESET Requested. Do you really want to proceed?")
        msg.setWindowTitle("Database Advanced Options")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        reply = msg.exec_()
        if reply == QMessageBox.Yes:
            truncate_query_method("alarm_log", logger)

    '''
        Svuota la tabella contenente i log degli utenti
    '''

    def resetUserlog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(
            "COUNTERS HARD RESET Requested. Do you really want to proceed?")
        msg.setWindowTitle("Database Advanced Options")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        reply = msg.exec_()
        if reply == QMessageBox.Yes:
            truncate_query_method("users_log", logger)

    def __init__(self, parent):
        self.parent = parent

        self.frame = QFrame(self.parent)
        # self.frame.setStyleSheet(Style.INIT_STYLE)
        self.frame.setGeometry(0, 80, Style.WIDTH, Style.HEIGHT-200)

        self.title = QLabel("Database Advanced Options", self.frame)
        self.title.setGeometry(0, 0, self.frame.width(), 50)
        self.title.setStyleSheet(Style.TITLE2_CENTERED_STYLE)

        self.counters_button = QPushButton("HARD RESET COUNTERS", self.frame)
        self.counters_button.setGeometry(330, 75, 355, 55)
        self.counters_button.setStyleSheet(Style.BUTTONMENU_STYLE)
        self.counters_button.clicked.connect(self.resetCounters)
        self.prodlog_button = QPushButton(
            "HARD RESET PRODUCTION LOG", self.frame)
        self.prodlog_button.setGeometry(330, 155, 355, 55)
        self.prodlog_button.setStyleSheet(Style.BUTTONMENU_STYLE)
        self.prodlog_button.clicked.connect(self.resetProdlog)
        self.alarmlog_button = QPushButton("HARD RESET ALARM LOG", self.frame)
        self.alarmlog_button.setGeometry(330, 235, 355, 55)
        self.alarmlog_button.setStyleSheet(Style.BUTTONMENU_STYLE)
        self.alarmlog_button.clicked.connect(self.resetAlarmlog)
        self.alarmlog_button = QPushButton("HARD RESET USERS LOG", self.frame)
        self.alarmlog_button.setGeometry(330, 315, 355, 55)
        self.alarmlog_button.setStyleSheet(Style.BUTTONMENU_STYLE)
        self.alarmlog_button.clicked.connect(self.resetUserlog)
        self.frame.setVisible(False)


# REV. 5.0 -> OBSOLETA
'''class HID:
    def get_selected_device(self):
        return self.combo.currentText()

    def updateData(self):
        self.combo.clear()
        if LINUX:
            devices = [InputDevice(path) for path in list_devices()]
            dev = ""
            for device in devices:
                self.combo.addItem(device.name)

    def save_device(self):
        update_hid_query_method(self.get_selected_device())

    def __init__(self, parent):
        self.parent = parent

        self.frame = QFrame(self.parent)
        #self.frame.setStyleSheet(Style.INIT_STYLE)
        self.frame.setGeometry(0,80,Style.WIDTH,Style.HEIGHT-200)
        
        self.title = QLabel("HID Options", self.frame)
        self.title.setGeometry(0,0,self.frame.width(),50)
        self.title.setStyleSheet(Style.TITLE2_CENTERED_STYLE)

        self.label = QLabel("Select HID device:", self.frame)
        self.label.setGeometry(160,120,280,50)
        self.label.setStyleSheet(Style.SUBTITLE2_CENTERED_STYLE)
        
        self.combo = QComboBox(self.frame)
        self.combo.setStyleSheet(Style.QCOMBOBOX_TITLE5)
        self.combo.setGeometry(440,120,350,50)

        self.button = QPushButton("Save", self.frame)
        self.button.setGeometry(440,180,220,50)
        self.button.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.button.clicked.connect(self.save_device)


        self.frame.setVisible(False)'''


class NetworkOptions:
    def __init__(self, parent):
        self.parent = parent

        self.frame = QFrame(self.parent)
        self.frame.setStyleSheet(Style.INIT_STYLE)
        self.frame.setGeometry(0, 50, Style.WIDTH, Style.HEIGHT-50)

        self.title = QLabel("Network Options", self.frame)
        self.title.setGeometry(0, 0, self.frame.width(), 50)
        self.title.setStyleSheet(Style.TITLE2_STYLE)

        self.interface_name_label = QLabel("Interface", self.frame)
        self.interface_name_label.setGeometry(215, 75, 200, 75)
        self.interface_name_label.setStyleSheet(Style.TITLE3_STYLE)

        self.address_name_label = QLabel(
            "IP Address Configuration", self.frame)
        self.address_name_label.setGeometry(415, 75, 600, 75)
        self.address_name_label.setStyleSheet(Style.TITLE3_STYLE)

        self.frame.setVisible(False)

# REV. 5.0


class IDT(QWidget):
    phase = pyqtSignal(int)

    '''
        Esegue l'updateData della classe IDT
        - Compone il dizionario
    '''

    def updateData(self, lang_dictionary, phase):
        self.lang_dictionary = {}

        for e in lang_dictionary:
            if e[1] == phase:
                self.lang_dictionary.update({e[0]: e[2]})
        for e in self.frame:
            e.frame.setVisible(False)
        self.frame[0].frame.setVisible(True)

    '''
        Torna in home page
    '''

    def goHome(self):
        self.phase.emit(PHASE_HOME)

    '''
        In base al parametro option si muove all'interno delle configurazioni
    '''

    def goToOption(self, option):
        for e in self.frame:
            e.frame.setVisible(False)
        if option == "db_settings":
            self.frame[0].frame.setVisible(True)
        if option == "hid":
            self.frame[1].frame.setVisible(True)
            self.frame[1].updateData()
        if option == "lan":
            self.frame[2].frame.setVisible(True)

    '''
        Chiude l'applicazione HMI
    '''

    def goToExit(self):
        sys.exit()

    def __init__(self, parent):
        super(IDT, self).__init__(parent)

        self.parent = parent
        self.counter_id = self.parent.counter_id
        # self.frame = [DatabaseOptions(self), HID(self), NetworkOptions(self)]
        self.frame = [DatabaseOptions(self), NetworkOptions(self)]

        self.go_db = QPushButton("", self)
        self.go_db.setGeometry(int(Style.BUTTONBAR_X*2 + Style.BUTTONBAR_WIDTH),
                               Style.BUTTONBAR_Y, Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT)
        if LINUX:
            self.go_db.setIcon(QIcon(IMG_LINUX_PATH+"database.png"))
        else:
            self.go_db.setIcon(
                QIcon(os.path.join(IMG_WIN_PATH, "database.png")))
        self.go_db.setIconSize(
            QSize(Style.BUTTONBAR_WIDTH - 20, Style.BUTTONBAR_HEIGHT - 20))
        self.go_db.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.go_db.clicked.connect(lambda: self.goToOption("db_settings"))

        self.go_hid = QPushButton("", self)
        self.go_hid.setGeometry(int(Style.BUTTONBAR_X*3 + Style.BUTTONBAR_WIDTH*2),
                                Style.BUTTONBAR_Y, Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT)
        if LINUX:
            self.go_hid.setIcon(QIcon(IMG_LINUX_PATH+"hid.png"))
        else:
            self.go_hid.setIcon(QIcon(os.path.join(IMG_WIN_PATH, "hid.png")))
        self.go_hid.setIconSize(
            QSize(int(Style.BUTTONBAR_WIDTH - 20), int(Style.BUTTONBAR_HEIGHT - 20)))
        self.go_hid.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.go_hid.clicked.connect(lambda: self.goToOption("hid"))
        self.go_hid.setVisible(False)

        self.go_lan = QPushButton("", self)
        self.go_lan.setGeometry(int(Style.BUTTONBAR_X*4 + Style.BUTTONBAR_WIDTH*3),
                                Style.BUTTONBAR_Y, Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT)
        if LINUX:
            self.go_lan.setIcon(QIcon(IMG_LINUX_PATH+"cpu.png"))
        else:
            self.go_lan.setIcon(QIcon(os.path.join(IMG_WIN_PATH, "cpu.png")))
        self.go_lan.setIconSize(
            QSize(int(Style.BUTTONBAR_WIDTH - 20), int(Style.BUTTONBAR_HEIGHT - 20)))
        self.go_lan.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.go_lan.clicked.connect(lambda: self.goToOption("lan"))
        self.go_lan.setVisible(False)

        self.go_exit = QPushButton("", self)
        self.go_exit.setGeometry(int(Style.WIDTH - Style.BUTTONBAR_X - Style.BUTTONBAR_WIDTH),
                                 Style.BUTTONBAR_Y, Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT)
        if LINUX:
            self.go_exit.setIcon(QIcon(IMG_LINUX_PATH+"exit.png"))
        else:
            self.go_exit.setIcon(QIcon(os.path.join(IMG_WIN_PATH, "exit.png")))
        self.go_exit.setIconSize(
            QSize(int(Style.BUTTONBAR_WIDTH - 20), int(Style.BUTTONBAR_HEIGHT - 20)))
        self.go_exit.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.go_exit.clicked.connect(self.goToExit)

        self.go_back = QPushButton("", self)
        self.go_back.setGeometry(
            Style.BUTTONBAR_X, Style.BUTTONBAR_Y, Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT)
        if LINUX:
            self.go_back.setIcon(QIcon(IMG_LINUX_PATH+"home.png"))
        else:
            self.go_back.setIcon(QIcon(os.path.join(IMG_WIN_PATH, "home.png")))
        self.go_back.setIconSize(
            QSize(int(Style.BUTTONBAR_WIDTH - 20), int(Style.BUTTONBAR_HEIGHT - 20)))
        self.go_back.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.go_back.clicked.connect(self.goHome)

# REV. 5.0


class Users(QWidget):
    phase = pyqtSignal(int)

    '''
        Esegue l'updateData della classe Users
    '''

    def updateData(self, lang_dictionary, user_id, phase):
        self.lang_dictionary = {}
        self.curr_userid = user_id
        for e in lang_dictionary:
            if e[1] == phase:
                self.lang_dictionary.update({e[0]: e[2]})

        for row in range(self.rowcount):
            self.table.setItem(row, 0, QTableWidgetItem(""))
            self.table.setItem(row, 1, QTableWidgetItem(""))
            self.table.setItem(row, 2, QTableWidgetItem(""))
            self.table.setItem(row, 3, QTableWidgetItem(""))
            self.table.setItem(row, 4, QTableWidgetItem(""))

        sql = "SELECT user_id, scancode, name, surname, usergroup_id FROM users WHERE usergroup_id <> 'SUPER'"
        value = {}
        records, n_row, err = selectMethod(sql, value, logger)
        row = 0
        if not err and n_row > 0:
            for array in records:
                self.table.setItem(row, 0, QTableWidgetItem(array[0]))
                self.table.setItem(row, 1, QTableWidgetItem(array[1]))
                self.table.setItem(row, 2, QTableWidgetItem(array[2]))
                self.table.setItem(row, 3, QTableWidgetItem(array[3]))
                self.table.setItem(row, 4, QTableWidgetItem(array[4]))
                row = row + 1

        self.table.setHorizontalHeaderLabels([self.lang_dictionary["header_userid"], self.lang_dictionary["header_scancode"],
                                             self.lang_dictionary["header_name"], self.lang_dictionary["header_surname"], self.lang_dictionary["header_permission"]])
        self.title.setText(self.lang_dictionary["label_title"])

    '''
        Rimuove l'utente selezionato
    '''

    def remove_user(self):
        row_select = self.table.currentRow()
        id = self.table.item(row_select, 0).text()
        if id != "" and id != self.curr_userid:
            reply = QMessageBox.question(self, self.lang_dictionary["qmessagebox_information_removal_title"], self.lang_dictionary[
                                         "qmessagebox_information_userremovalquestion"] + str(id) + "]", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                delete_user_query_method(id, logger)
                QMessageBox.information(
                    self, self.lang_dictionary["qmessagebox_information_removal_title"], self.lang_dictionary["qmessagebox_information_removal"])
                self.phase.emit(PHASE_USERS)
        elif id == self.curr_userid:
            QMessageBox.critical(
                self, self.lang_dictionary["qmessagebox_error_title"], self.lang_dictionary["qmessagebox_error_nouserselected"])
        else:
            QMessageBox.critical(
                self, self.lang_dictionary["qmessagebox_error_title"], self.lang_dictionary["qmessagebox_error_nouserselected"])

    def __init__(self, parent):
        super(Users, self).__init__(parent)

        self.parent = parent
        self.rowcount = 30
        self.selectedNewItem = False
        self.lang_dictionary = {}

        self.title = QLabel("", self)
        self.title.setGeometry(0, 75, Style.WIDTH, 50)
        self.title.setStyleSheet(Style.TITLE2_CENTERED_STYLE)

        self.frame = QFrame(self)
        self.frame.setGeometry(0, 125, Style.WIDTH, Style.HEIGHT-225)

        self.table = QTableWidget()
        self.layout1 = QVBoxLayout(self.frame)
        self.layout1.addWidget(self.table)
        self.frame.setLayout(self.layout1)

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(Style.CONF_TABLE)
        self.table.setRowCount(self.rowcount)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["USER ID", "SCANCODE", "NAME", "SURNAME", "PERMISSION"])
        self.table.setColumnWidth(0, 225)
        self.table.setColumnWidth(1, 275)
        self.table.setColumnWidth(2, 225)
        self.table.setColumnWidth(3, 225)
        self.table.setColumnWidth(4, 225)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.buttonHome = QPushButton("", self)
        self.buttonHome.setGeometry(int(Style.BUTTONBAR_X), int(
            Style.BUTTONBAR_Y), int(Style.BUTTONBAR_WIDTH), int(Style.BUTTONBAR_HEIGHT))
        if LINUX:
            homeImage = QIcon(IMG_LINUX_PATH+"home.png")
        else:
            homeImage = QIcon(os.path.join(IMG_WIN_PATH, "home.png"))
        self.buttonHome.setIcon(homeImage)
        self.buttonHome.setIconSize(
            QSize(int(Style.BUTTONBAR_WIDTH - 20), int(Style.BUTTONBAR_HEIGHT - 20)))
        self.buttonHome.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.buttonHome.clicked.connect(lambda: self.phase.emit(PHASE_HOME))

        self.buttonAddUser = QPushButton("", self)
        self.buttonAddUser.setGeometry(int(Style.BUTTONBAR_WIDTH*8+Style.BUTTONBAR_X*8),
                                       Style.BUTTONBAR_Y, Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT)
        if LINUX:
            adduserimg = QIcon(IMG_LINUX_PATH+"add user.png")
        else:
            adduserimg = QIcon(os.path.join(IMG_WIN_PATH, "add user.png"))
        self.buttonAddUser.setIcon(adduserimg)
        self.buttonAddUser.setIconSize(
            QSize(int(Style.BUTTONBAR_WIDTH - 20), int(Style.BUTTONBAR_HEIGHT - 20)))
        self.buttonAddUser.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.buttonAddUser.clicked.connect(
            lambda: self.phase.emit(PHASE_ADD_USER))

        self.buttonRemoveUser = QPushButton("", self)
        self.buttonRemoveUser.setGeometry(int(Style.BUTTONBAR_WIDTH*7+Style.BUTTONBAR_X*7),
                                          Style.BUTTONBAR_Y, Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT)
        self.buttonRemoveUser.setStyleSheet(Style.BUTTONBAR_STYLE)
        if LINUX:
            removeuserimg = QIcon(IMG_LINUX_PATH+"remove user.png")
        else:
            removeuserimg = QIcon(os.path.join(
                IMG_WIN_PATH, "remove user.png"))
        self.buttonRemoveUser.setIcon(removeuserimg)
        self.buttonRemoveUser.setIconSize(
            QSize(int(Style.BUTTONBAR_WIDTH - 20), int(Style.BUTTONBAR_HEIGHT - 20)))
        self.buttonRemoveUser.clicked.connect(self.remove_user)


class Shutdown(QWidget):
    phase = pyqtSignal(int)

    '''
        Compone il dizionario per la classe in questione
    '''

    def updateData(self, lang_dictionary):
        for e in lang_dictionary:
            if e[1] == 8:
                self.lang_dictionary.update({e[0]: e[2]})

    '''
        Funzione che esegue il reboot del pannello
    '''

    def dialogReboot(self):
        reply = QMessageBox.question(self, self.lang_dictionary["qmessagebox_information_reboot_title"],
                                     self.lang_dictionary["qmessagebox_information_reboot"], QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            call("sudo reboot", shell=True)

    # OBSOLETO, NON UTILIZZATO
    def dialog_shutdown(self):
        msg2 = QMessageBox()
        msg2.setIcon(QMessageBox.Information)
        msg2.setText(self.lang_dictionary["qmessagebox_information_shutdown"])
        msg2.setWindowTitle(
            self.lang_dictionary["qmessagebox_information_shutdown_title"])
        msg2.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        reply = msg2.exec_()
        if reply == QMessageBox.Yes:
            call("sudo shutdown -h now", shell=True)

    '''
        Esegue il logout
    '''

    def goBack(self):
        self.phase.emit(PHASE_LOGIN)

    def __init__(self, parent=None):
        super(Shutdown, self).__init__(parent)

        self.lang_dictionary = {}

        self.rebootPushButton = QPushButton(self)
        self.rebootPushButton.setGeometry(350, 175, 580, 150)
        # self.rebootPushButton.setGeometry(350,350,580,150)
        if LINUX:
            rebootImage = QIcon(IMG_LINUX_PATH+"reboot.png")
        else:
            rebootImage = QIcon(os.path.join(IMG_WIN_PATH, "reboot.png"))
        self.rebootPushButton.setIcon(rebootImage)
        self.rebootPushButton.setIconSize(QSize(580, 150))
        self.rebootPushButton.setStyleSheet(Style.BUTTONMENU_STYLE)
        self.rebootPushButton.clicked.connect(self.dialogReboot)

        '''self.shutdownPushButton = QPushButton(self)
        self.shutdownPushButton.setGeometry(350,350,580,150)
        shutdownImage = QIcon("img/shutdown.png")
        self.shutdownPushButton.setIcon(shutdownImage)
        self.shutdownPushButton.setIconSize(QSize(580, 150))
        self.shutdownPushButton.setStyleSheet(Style.BUTTONMENU_STYLE)
        self.shutdownPushButton.clicked.connect(self.dialog_shutdown)'''

        self.backPushButton = QPushButton(self)
        self.backPushButton.setGeometry(int(Style.BUTTONBAR_WIDTH*8+Style.BUTTONBAR_X*8),
                                        Style.BUTTONBAR_Y, Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT)
        if LINUX:
            backImage = QIcon(IMG_LINUX_PATH+"back.png")
        else:
            backImage = QIcon(os.path.join(IMG_WIN_PATH, "back.png"))
        self.backPushButton.setIcon(backImage)
        self.backPushButton.setIconSize(
            QSize(int(Style.BUTTONBAR_WIDTH), int(Style.BUTTONBAR_HEIGHT)))
        self.backPushButton.clicked.connect(self.goBack)
        self.backPushButton.setStyleSheet(Style.BUTTONBAR_STYLE)

# REV. 5.0


class AddUser(QWidget):
    phase = pyqtSignal(int)
    keys = []
    '''
        Svuota tutti i campi della pagina corrente
    '''

    def updateEdit(self):
        for e in self.fields:
            self.fields[e].edit.setText("")
        self.edit_scancode.setText("")

    '''
        Esegue l'updateData della classe AddUser.
        Compone il dizionario per la classe corrente
    '''

    def updateData(self, lang_dictionary, phase):
        self.lang_dictionary = {}
        self.keys = []
        self.updateEdit()
        self.listener = keyboard.Listener(
            on_press=self.on_press, kwargs=self.keys)
        self.listener.start()
        self.scancode = ""

        for e in lang_dictionary:
            if e[1] == phase:
                self.lang_dictionary.update({e[0]: e[2]})

        self.fields["name"].label.setText(self.lang_dictionary["label_name"])
        self.fields["surname"].label.setText(
            self.lang_dictionary["label_surname"])
        self.title.setText(self.lang_dictionary["label_title"])

    '''
        Ritorna in pagina di aggiunta utente
    '''

    def goBack(self):
        self.listener.stop()
        self.listener.join()
        self.phase.emit(PHASE_USERS)

    '''
        Apre la virtual keuboard nel momento in cui una label viene premuta
    '''

    def callKey(self, edit):
        temp = edit.text()
        self.parent.virtualKeyboard.edit.setText("")
        self.parent.virtualKeyboard.exec_()
        self.parent.virtualKeyboard.edit.setFocus()
        text = self.parent.virtualKeyboard.sendDateEnter()
        if len(text.strip()) == 0:
            edit.setText(temp)
        else:
            edit.setText(self.parent.virtualKeyboard.sendDateEnter())
        edit.repaint()

    '''
        Esegue l'aggiunta dell'utente
    '''

    def addUser(self):
        control_message = 0     # Usata per verificare che tutti i campi siano stati compilati
        if str(self.fields["user_id"].edit.text()) == "":
            QMessageBox.warning(
                self, self.lang_dictionary["qmessagebox_information_newuser_title"], self.lang_dictionary["qmessagebox_error_useridempty"])
            control_message = 1
        else:
            user_id = self.fields["user_id"].edit.text()

        # uso una variabile di supporto per evitare sovrapposizione degli interrupt
        '''if str(self.edit_scancode.text()) == "":
            QMessageBox.warning(self, self.lang_dictionary["qmessagebox_information_newuser_title"], self.lang_dictionary["qmessagebox_error_scancodeempty"])
            control_message = 2
        else:
            scancode = self.fields["scancode"].edit.text()'''

        if str(self.fields["name"].edit.text()) == "":
            QMessageBox.warning(
                self, self.lang_dictionary["qmessagebox_information_newuser_title"], self.lang_dictionary["qmessagebox_error_nameempty"])
            control_message = 3
        else:
            name = self.fields["name"].edit.text()

        if str(self.fields["surname"].edit.text()) == "":
            QMessageBox.warning(
                self, self.lang_dictionary["qmessagebox_information_newuser_title"], self.lang_dictionary["qmessagebox_error_surnameempty"])
            control_message = 4
        else:
            surname = self.fields["surname"].edit.text()
            permission = self.comboPermission.currentText()

        if str(self.fields["password"].edit.text()) == "":
            QMessageBox.warning(self, self.lang_dictionary["qmessagebox_information_newuser_title"],
                                self.lang_dictionary["qmessagebox_warning_passwordempty"])
            control_message = 5
        else:
            password = self.fields["password"].edit.text()
            password = encryptString(password)

        if control_message == 0:
            reply = QMessageBox.question(self, self.lang_dictionary["qmessagebox_information_newuser_title"],
                                         self.lang_dictionary["qmessagebox_information_addnewuser"], QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                err = insert_user_query_method(
                    user_id, self.scancode, name, surname, permission, password, logger)
                if not err:
                    QMessageBox.information(
                        self, self.lang_dictionary["qmessagebox_information_newuser_title"], self.lang_dictionary["qmessagebox_information_useradded"])
                    self.listener.stop()
                    self.listener.join()
                    self.phase.emit(PHASE_USERS)
                else:
                    QMessageBox.critical(
                        self, self.lang_dictionary["qmessagebox_information_newuser_title"], self.lang_dictionary['qmessagebox_error_newuser'])
                    self.updateEdit()
            else:
                self.updateEdit()
        else:
            self.updateEdit()

    '''
        Imposta il testo della label per lo scancode rilevato dal lettore di badge
    '''

    def setScancode(self, scancode):
        # il campo scancode è uno specchietto per allodole. il vero valore di cui bisogna tenere conto nella query di insert è il seguente
        self.scancode = scancode
        self.edit_scancode.setText(scancode)

    def on_press(self, key):
        if key == keyboard.Key.esc or key == keyboard.Key.enter:
            self.scancode = self.getKeyStrings(self.keys)
            self.fields["scancode"].edit.setCursorPosition(True)
            self.fields["scancode"].edit.setText(self.scancode)
            print("self.scancode: {}".format(self.scancode))
            self.keys = []
            # return False  # stop listener
        try:
            k = key.char  # single-char keys
            self.keys.append(k)
        except:
            # pass
            k = key.name  # other keys
            # keys.append(k)
        # print('Key pressed: ' + k)

    def getKeyStrings(self, keys):
        keystr = ""
        if keys is not None:
            for entry in keys:
                keystr = keystr + entry

        # print(keystr)
        return keystr

    def __init__(self, parent):
        super(AddUser, self).__init__(parent)

        self.parent = parent
        self.scancode = ""

        self.title = QLabel("", self)
        self.title.setGeometry(0, 75, Style.WIDTH, 50)
        self.title.setStyleSheet(Style.TITLE2_CENTERED_STYLE)

        class Field:
            def __init__(self, parent, text, x, y, flag):
                self.label = QLabel(text, parent)
                self.label.setGeometry(x, y, 200, 50)
                self.label.setStyleSheet(Style.SUBTITLE3_STYLE)
                if flag:
                    self.edit = ClickableLineEdit(parent)
                    self.edit.setGeometry(x+140, y, 250, 50)
                    self.edit.setStyleSheet(Style.TITLE4_LINEEDIT)
                    self.edit.clicked.connect(
                        lambda: parent.callKey(self.edit))
                    self.edit.setReadOnly(True)
                else:
                    self.edit = QLineEdit(parent)
                    self.edit.setGeometry(x+140, y, 250, 50)
                    self.edit.setStyleSheet(Style.TITLE4_LINEEDIT)
                    self.edit.setReadOnly(True)

        self.edit_scancode = QLineEdit(self)
        self.edit_scancode.setGeometry(250, 300, 190, 50)
        self.edit_scancode.setStyleSheet(Style.TITLE4_LINEEDIT)
        self.edit_scancode.setEchoMode(QLineEdit.Password)
        self.edit_scancode.setEnabled(False)

        self.fields = {"user_id": Field(self, "User ID:", 50, 175, True), "scancode": Field(self, "Scancode:", 50, 300, False),
                       "name": Field(self, "Name:", 480, 175, True), "surname": Field(self, "Surname:", 480, 300, True),
                       "password": Field(self, "Password:", 50, 425, True)}
        self.fields["password"].edit.setEchoMode(QLineEdit.Password)

        # self.fields["scancode"].edit.setVisible(True)

        self.permissionLabel = QLabel("Usergroup:", self)
        self.permissionLabel.setGeometry(480, 425, 200, 50)
        self.permissionLabel.setStyleSheet(Style.SUBTITLE3_STYLE)

        self.comboPermission = QComboBox(self)
        sql = "SELECT usergroup_id FROM usersgroup WHERE usergroup_id <> 'SUPER'"
        value = {}
        records, n_row, err = selectMethod(sql, value, logger)
        for list in records:
            self.comboPermission.addItem(list[0])
        self.comboPermission.setStyleSheet(Style.QCOMBOBOX_TITLE5)
        self.comboPermission.setGeometry(620, 425, 250, 50)

        self.goback = QPushButton("", self)
        self.goback.setGeometry(int(Style.BUTTONBAR_X), int(Style.BUTTONBAR_Y), int(
            Style.BUTTONBAR_WIDTH), int(Style.BUTTONBAR_HEIGHT))
        if LINUX:
            backImage = QIcon(IMG_LINUX_PATH+"back.png")
        else:
            backImage = QIcon(os.path.join(IMG_WIN_PATH, "back.png"))
        self.goback.setIcon(backImage)
        self.goback.setIconSize(
            QSize(int(Style.BUTTONBAR_WIDTH - 20), int(Style.BUTTONBAR_HEIGHT - 20)))
        self.goback.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.goback.clicked.connect(self.goBack)

        self.userb = QPushButton("", self)
        self.userb.setGeometry(Style.BUTTONBAR_WIDTH*8+Style.BUTTONBAR_X*8,
                               Style.BUTTONBAR_Y, Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT)
        if LINUX:
            adduserimg = QIcon(IMG_LINUX_PATH+"add user.png")
        else:
            adduserimg = QIcon(os.path.join(IMG_WIN_PATH, "add user.png"))
        self.userb.setIcon(adduserimg)
        self.userb.setIconSize(
            QSize(int(Style.BUTTONBAR_WIDTH - 20), int(Style.BUTTONBAR_HEIGHT - 20)))
        self.userb.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.userb.clicked.connect(self.addUser)

# REV. 5.0


class Configuration(QWidget):
    phase = pyqtSignal(int)

    '''
        Esegue la selezione del prodotto corrente per la produzione
    '''

    def updateCounters(self):
        reply = QMessageBox.question(self, self.lang_dictionary["qmessagebox_configuration"],
                                     self.lang_dictionary["qmessagebox_question_configuration"], QMessageBox.Yes | QMessageBox.No)
        if (reply == QMessageBox.Yes):
            # Aggiornamento prodotto in lavorazione
            reset_counter_selected_query_method(logger)
            update_counter_selected_query_method(
                self.combo.currentText(), logger)
            if self.counter_num != 0:
                self.counter_num = self.result[self.combo.currentText()]
                self.counter_id = self.combo.currentText()
            '''if len(self.boxCustomerCode.text()) == 0 or len(self.boxInternalCode.text()) == 0:
                QMessageBox.critical(self, self.lang_dictionary["qmessagebox_configuration_error"], self.lang_dictionary["qmessagebox_empty_text"])
            else:
                #Aggiornamento customer code e INT code
                error = update_customer_code_sx_query_method(self.combo.currentText(), self.boxInternalCode.text(), self.boxCustomerCode.text())
                if error:
                   QMessageBox.critical(self, self.lang_dictionary["qmessagebox_configuration_error"], self.lang_dictionary["qmessagebox_query_error"])
                else:
                   QMessageBox.information(self, self.lang_dictionary["qmessagebox_configuration"],  self.lang_dictionary["qmessagebox_information_completed"])        
            '''
            error = update_customer_code_sx_query_method(self.combo.currentText(
            ), self.boxInternalCode_sx.text(), self.boxCustomerCode_sx.text(), logger)
            if not error:
                error = update_customer_code_dx_query_method(self.combo.currentText(
                ), self.boxInternalCode_dx.text(), self.boxCustomerCode_dx.text(), logger)
            if error:
                QMessageBox.critical(
                    self, self.lang_dictionary["qmessagebox_configuration_error"], self.lang_dictionary["qmessagebox_query_error"])
            else:
                QMessageBox.information(
                    self, self.lang_dictionary["qmessagebox_configuration"],  self.lang_dictionary["qmessagebox_information_completed"])

    '''
        Metodo getter per il codice interno del prodotto
    '''

    def getCustomerCode(self):
        sql = "SELECT internal_code_sx, customer_code_sx, internal_code_dx, customer_code_dx FROM counters WHERE counter_id = %(counter_id)s"
        value = {'counter_id': self.combo.currentText()}
        records, n_row, err = selectMethod(sql, value, logger)
        if not err and n_row > 0:
            self.boxInternalCode_sx.setText(records[0][0])
            self.boxCustomerCode_sx.setText(records[0][1])
            self.boxInternalCode_dx.setText(records[0][2])
            self.boxCustomerCode_dx.setText(records[0][3])
        else:
            self.boxInternalCode_sx.setText("")
            self.boxCustomerCode_sx.setText("")
            self.boxInternalCode_dx.setText("")
            self.boxCustomerCode_dx.setText("")

    '''
        Apre la virtual keuboard nel momento in cui una label viene premuta
    '''

    def callKey(self, edit):
        temp = edit.text()
        self.parent.virtualKeyboard.edit.setText("")
        self.parent.virtualKeyboard.exec_()
        self.parent.virtualKeyboard.edit.setFocus()
        if len(self.parent.virtualKeyboard.sendDateEnter()) == 0:
            edit.setText(temp)
        else:
            edit.setText(self.parent.virtualKeyboard.sendDateEnter())
        edit.repaint()

    '''
        Metodo getter per il counter id del prodotto
    '''

    def getCounterId(self):
        return self.counter_id

    '''
        Metodo getter per il counter num del prodotto
    '''

    def getCounterNum(self):
        return self.counter_num

    '''
        Metodo getter per il prodotto attualmente selezionato, ovvero il prodotto che ha il campo counter_selected=True
    '''

    def getCurrentProduct(self):
        sql = "SELECT counter_id, counter_num FROM counters WHERE counter_selected = %(selected)s"
        value = {'selected': 'True'}
        records, n_row, err = selectMethod(sql, value, logger)
        if not err and n_row > 0:
            return records[0][0], records[0][1]
        return "", 0

    def getDefaultLang(self):
        sql = "SELECT value FROM configuration WHERE configuration_id='default_lang'"
        value = {}
        records, n_row, err = selectMethod(sql, value, logger)
        if not err and n_row > 0:
            if records[0][0] == 1:
                return "description_IT"
            elif records[0][0] == 2:
                return "description_EN"
            elif records[0][0] == 3:
                return "description_LANG1"
            elif records[0][0] == 4:
                return "description_LANG2"
            else:
                return "description_EN"
        return DEFAULT_DESCRIPTION_LANGUAGE

    '''
        Esegue l'updateData per la classe corrente
    '''

    def updateData(self, lang_dictionary, printer_enabled, enable_manconf, phase):
        self.lang_dictionary = {}
        for e in lang_dictionary:
            if e[1] == phase:
                self.lang_dictionary.update({e[0]: e[2]})

        self.labelModel.setText(self.lang_dictionary["label_model"])
        self.labelDescription.setText(
            self.lang_dictionary["label_description"])
        self.buttonSelectConf.setText(self.lang_dictionary["button_select"])
        self.buttonAdvanced.setText(self.lang_dictionary["button_advanced"])
        self.enable_printer.setText(
            self.lang_dictionary["label_enable_printer"])
        self.labelInternalCode_sx.setText(
            self.lang_dictionary["label_internalcode"] + " SX:")
        self.labelCustomerCode_sx.setText(
            self.lang_dictionary["label_customercode"] + " SX:")
        self.labelInternalCode_dx.setText(
            self.lang_dictionary["label_internalcode"] + " DX:")
        self.labelCustomerCode_dx.setText(
            self.lang_dictionary["label_customercode"] + " DX:")
        self.enable_manconf.setText(self.lang_dictionary["check_conf"])
        self.combo.clear()
        self.result = {}

        sql = "SELECT counter_id, counter_num, counter_selected FROM counters WHERE counter_num > %(num)s AND isEnabled = 1 ORDER BY counter_num"
        value = {'num': DEFAULT_NONE_PRODUCT}
        records, n_row, err = selectMethod(sql, value, logger)

        for e in records:
            self.combo.addItem(e[0])

        for e in records:
            self.result.update({e[0]: e[1]})
            if e[2] == "True":
                self.combo.setCurrentIndex(self.combo.findText(e[0]))

        if enable_manconf == 1:
            self.enable_manconf.setChecked(True)
        else:
            self.enable_manconf.setChecked(False)
        self.doConfActions(self.enable_manconf)

        if printer_enabled == 1:
            self.enable_printer.setChecked(True)
        else:
            self.enable_printer.setChecked(False)

    '''
        Cambio di pagina
    '''

    def changePhase(self, n):
        if self.enable_manconf.isChecked():
            update_configuration_query_method("enable_manconf", 1, logger)
            self.updateCounters()
        else:
            update_configuration_query_method("enable_manconf", 0, logger)
        if self.enable_printer.isChecked():
            update_configuration_query_method("enable_printer", 1, logger)
        else:
            update_configuration_query_method("enable_printer", 0, logger)
        self.phase.emit(n)

    '''
        Gestione del pulsante di configurazione manuale
    '''

    def doConfActions(self, enable_manconf):
        if enable_manconf.isChecked():
            self.boxInternalCode_sx.setEnabled(True)
            self.boxInternalCode_dx.setEnabled(True)
            self.boxCustomerCode_sx.setEnabled(True)
            self.boxCustomerCode_dx.setEnabled(True)
            self.buttonSelectConf.setEnabled(True)
            self.combo.setEnabled(True)
        else:
            self.boxInternalCode_sx.setEnabled(False)
            self.boxInternalCode_dx.setEnabled(False)
            self.boxCustomerCode_sx.setEnabled(False)
            self.boxCustomerCode_dx.setEnabled(False)
            self.buttonSelectConf.setEnabled(False)
            self.combo.setEnabled(False)

    def __init__(self, parent):
        super(Configuration, self).__init__(parent)
        self.parent = parent
        self.counter_id = ""
        self.counter_num = 0
        self.lang_dictionary = {}
        self.result = {}

        self.labelDescription = QLabel("", self)
        self.labelDescription.setGeometry(0, 75, Style.WIDTH, 50)
        self.labelDescription.setStyleSheet(Style.TITLE2_CENTERED_STYLE)

        self.labelModel = QLabel("", self)
        self.labelModel.setGeometry(90, 150, 300, 50)
        self.labelModel.setStyleSheet(Style.TITLE3_CENTERED_STYLE)

        self.combo = QComboBox(self)
        self.combo.setStyleSheet(Style.BODY_BOLD_QCOMBO1)
        self.combo.setGeometry(360, 150, 400, 50)
        self.combo.currentIndexChanged.connect(self.getCustomerCode)

        self.labelInternalCode_sx = QLabel("", self)
        self.labelInternalCode_sx.setGeometry(90, 210, 300, 50)
        self.labelInternalCode_sx.setStyleSheet(Style.TITLE4_CENTERED_STYLE)
        self.labelInternalCode_sx.setVisible(True)
        self.boxInternalCode_sx = ClickableLineEdit(self)
        self.boxInternalCode_sx.setStyleSheet(Style.TITLE4_LINEEDIT)
        self.boxInternalCode_sx.setGeometry(360, 210, 400, 50)
        self.boxInternalCode_sx.clicked.connect(
            lambda: self.callKey(self.boxInternalCode_sx))
        self.boxInternalCode_sx.setVisible(True)

        self.labelCustomerCode_sx = QLabel("", self)
        self.labelCustomerCode_sx.setGeometry(90, 270, 300, 50)
        self.labelCustomerCode_sx.setStyleSheet(Style.TITLE4_CENTERED_STYLE)
        self.labelCustomerCode_sx.setVisible(True)
        self.boxCustomerCode_sx = ClickableLineEdit(self)
        self.boxCustomerCode_sx.setStyleSheet(Style.TITLE4_LINEEDIT)
        self.boxCustomerCode_sx.setGeometry(360, 270, 400, 50)
        self.boxCustomerCode_sx.clicked.connect(
            lambda: self.callKey(self.boxCustomerCode_sx))
        self.boxCustomerCode_sx.setVisible(True)

        self.labelInternalCode_dx = QLabel("", self)
        self.labelInternalCode_dx.setGeometry(90, 330, 300, 50)
        self.labelInternalCode_dx.setStyleSheet(Style.TITLE4_CENTERED_STYLE)
        self.labelInternalCode_dx.setVisible(True)
        self.boxInternalCode_dx = ClickableLineEdit(self)
        self.boxInternalCode_dx.setStyleSheet(Style.TITLE4_LINEEDIT)
        self.boxInternalCode_dx.setGeometry(360, 330, 400, 50)
        self.boxInternalCode_dx.clicked.connect(
            lambda: self.callKey(self.boxInternalCode_dx))
        self.boxInternalCode_dx.setVisible(True)

        self.labelCustomerCode_dx = QLabel("", self)
        self.labelCustomerCode_dx.setGeometry(90, 390, 300, 50)
        self.labelCustomerCode_dx.setStyleSheet(Style.TITLE4_CENTERED_STYLE)
        self.labelCustomerCode_dx.setVisible(True)
        self.boxCustomerCode_dx = ClickableLineEdit(self)
        self.boxCustomerCode_dx.setStyleSheet(Style.TITLE4_LINEEDIT)
        self.boxCustomerCode_dx.setGeometry(360, 390, 400, 50)
        self.boxCustomerCode_dx.clicked.connect(
            lambda: self.callKey(self.boxCustomerCode_dx))
        self.boxCustomerCode_dx.setVisible(True)

        self.buttonSelectConf = QPushButton("", self)
        self.buttonSelectConf.setGeometry(500, 450, 260, 75)
        self.buttonSelectConf.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.buttonSelectConf.clicked.connect(self.updateCounters)

        self.enable_manconf = QCheckBox("", self)
        self.enable_manconf.setGeometry(260, 470, 400, 100)
        self.enable_manconf.setStyleSheet(Style.CHECKBOX_STYLE)
        self.enable_manconf.toggled.connect(
            lambda: self.doConfActions(self.enable_manconf))
        self.enable_manconf.setVisible(False)

        self.enable_printer = QPushButton("", self)
        self.enable_printer.setCheckable(True)
        self.enable_printer.setStyleSheet(
            Style.BUTTON_CONFIGURATION_STYLE_CHECKABLE)
        self.enable_printer.setGeometry(int(
            Style.BUTTONBAR_X*2 + Style.BUTTONBAR_WIDTH), Style.BUTTONBAR_Y, 200, Style.BUTTONBAR_HEIGHT)
        self.enable_printer.setVisible(True)

        self.buttonAdvanced = QPushButton("'", self)
        self.buttonAdvanced.setGeometry(int(Style.BUTTONBAR_WIDTH*8+Style.BUTTONBAR_X*8),
                                        Style.BUTTONBAR_Y, Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT)
        self.buttonAdvanced.clicked.connect(
            lambda: self.phase.emit(PHASE_ADVANCED_CONF))
        self.buttonAdvanced.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.buttonAdvanced.setVisible(False)

        self.buttonHome = QPushButton("", self)
        self.buttonHome.setGeometry(
            Style.BUTTONBAR_X, Style.BUTTONBAR_Y, Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT)
        self.buttonHome.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.buttonHome.clicked.connect(lambda: self.changePhase(PHASE_HOME))
        if LINUX:
            self.buttonHome.setIcon(QIcon(IMG_LINUX_PATH+"home.png"))
        else:
            self.buttonHome.setIcon(
                QIcon(os.path.join(IMG_WIN_PATH, "home.png")))
        self.buttonHome.setIconSize(
            QSize(int(Style.BUTTONBAR_WIDTH - 20), int(Style.BUTTONBAR_HEIGHT - 20)))

        self.ttModbus = ModbusWriter()

# REV. 5.0


class AdvancedConfiguration(QWidget):
    phase = pyqtSignal(int)

    '''
        Esegue l'update data della classe AdvancedConfiguration
    '''

    def updateData(self, lang_dictionary, phase):
        self.lang_dictionary = {}
        for e in lang_dictionary:
            if e[1] == phase:
                self.lang_dictionary.update({e[0]: e[2]})

        # self.labelModel.setText(self.lang_dictionary["label_model"])
        self.labelDescription.setText(
            self.lang_dictionary["label_description"])
        # self.labelInternalCode.setText(self.lang_dictionary["label_internalcode"])
        # self.labelCustomerCode.setText(self.lang_dictionary["label_customercode"])
        # self.buttonSelectConf.setText(self.lang_dictionary["button_select"])

        sql = "SELECT COUNT(counter_id) FROM counters"
        value = {}
        records, n_row, err = selectMethod(sql, value, logger)
        if not err:
            self.max_product = int(records[0][0])

        sql = "SELECT counter_id FROM counters ORDER BY counter_num"
        value = {}
        records, n_row, err = selectMethod(sql, value, logger)
        if not err:
            self.product_name = records

        sql = "SELECT isEnabled FROM counters ORDER BY counter_num"
        value = {}
        records, n_row, err = selectMethod(sql, value, logger)
        if not err:
            self.buttonChecked = records

        for i in range(self.max_product):
            self.stateButton.append(False)
            for j in range(2):
                self.label = QLabel(self)
                self.label.setText(self.product_name[i][0])
                self.checkbox = QCheckBox(self)
                self.label.setStyleSheet(Style.BODY_BOLD_QLABELADVANCED1)
                self.checkbox.setStyleSheet(Style.CHECKBOX_ADVCONFIG_STYLE)
                self.checkbox.stateChanged.connect(self.getCheckboxPressed)
                self.grid.addWidget(self.label, i, 0)
                self.grid.addWidget(self.checkbox, i, 10)
                if self.buttonChecked[i][0] == 1:
                    self.checkbox.setChecked(True)
                elif self.buttonChecked[i][0] == 0:
                    self.checkbox.setChecked(False)

    def getCheckboxPressed(self, checked):
        if checked:
            checkbox = self.sender()
            idx = self.grid.indexOf(checkbox)
            location = self.grid.getItemPosition(idx)
            self.stateButton[location[0]] = True
        else:

            checkbox = self.sender()
            idx = self.grid.indexOf(checkbox)
            location = self.grid.getItemPosition(idx)
            self.stateButton[location[0]] = False

    def change_frame(self):
        reply = QMessageBox.question(self, self.lang_dictionary["qmessagebox_configuration"],
                                     self.lang_dictionary["qmessagebox_question_configuration"], QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            i = 1
            support = []
            for e in self.stateButton:
                support.clear()
                support.extend([e, i])
                self.button_config.append(tuple(support))
                i = i+1

            sql = "UPDATE counters SET isEnabled=%s WHERE counter_num=%s"
            error = executeMultipleQuery(sql, self.button_config, logger)
            if not error:
                self.phase.emit(PHASE_CONFIGURATION)

    def __init__(self, parent):
        super(AdvancedConfiguration, self).__init__(parent)
        self.parent = parent
        self.counter_id = ""
        self.counter_num = 0
        self.lang_dictionary = {}
        self.result = {}
        self.max_product = 0
        self.product_name = []
        self.buttonChecked = []
        self.stateButton = []
        self.button_config = []

        self.labelDescription = QLabel("", self)
        self.labelDescription.setGeometry(0, 75, Style.WIDTH, 50)
        self.labelDescription.setStyleSheet(Style.TITLE2_CENTERED_STYLE)

        self.frame = QFrame(self)
        self.frame.setGeometry(190, 150, 1000, 600)
        self.frame.setStyleSheet(Style.INIT_STYLE)

        self.grid = QGridLayout(self)
        self.frame.setLayout(self.grid)

        self.buttonBack = QPushButton("", self)
        self.buttonBack.setGeometry(
            Style.BUTTONBAR_X, Style.BUTTONBAR_Y, Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT)
        self.buttonBack.setStyleSheet(Style.BUTTONBAR_STYLE)
        # self.buttonBack.clicked.connect(lambda:self.phase.emit(PHASE_CONFIGURATION))
        self.buttonBack.clicked.connect(self.change_frame)
        if LINUX:
            self.buttonBack.setIcon(QIcon(IMG_LINUX_PATH+"back.png"))
        else:
            self.buttonBack.setIcon(
                QIcon(os.path.join(IMG_WIN_PATH, "back.png")))
        self.buttonBack.setIconSize(
            QSize(Style.BUTTONBAR_WIDTH - 20, Style.BUTTONBAR_HEIGHT - 20))

        self.ttModbus = ModbusWriter()
# REV 5.0


class Counters(QWidget):
    phase = pyqtSignal(int)

    '''
        Esegue l'updateData della classe Counters.
        Compone la tabella con i valori dei contatori.
    '''

    def updateData(self):
        if str(self.combo.currentText()) != "":
            sql = "SELECT counter_id, partialPSX, partialrefusePSX, totalrefusePSX, totalPSX, partialPDX, partialrefusePDX, totalrefusePDX, totalPDX FROM counters WHERE counter_id=%(counter_id)s"
            value = {'counter_id': str(self.combo.currentText())}
            records, n_row, err = selectMethod(sql, value, logger)
            if not err and n_row > 0:
                for e in records:
                    self.labelPartial.setText(str(e[1]+e[5]))
                    self.labelPartialRefuse.setText(str(e[2]+e[6]))
                    self.labelTotalRefuse.setText(str(e[3]+e[7]))
                    self.labelTotal.setText(str(e[4]+e[8]))
            else:
                self.labelPartial.setText("")
                self.labelTotal.setText("")
                self.labelPartialRefuse.setText("")
                self.labelTotalRefuse.setText("")
        else:
            self.labelPartial.setText("")
            self.labelTotal.setText("")
            self.labelPartialRefuse.setText("")
            self.labelTotalRefuse.setText("")

    '''
        Imposta i valori per ogni label
    '''

    def updateCombo(self, lang_dictionary, phase):
        self.lang_dictionary = {}
        self.combo.clear()

        sql = "SELECT counter_id FROM counters"
        value = {}
        records, n_row, err = selectMethod(sql, value, logger)

        for e in records:
            self.combo.addItem(e[0])

        sql = "SELECT counter_id, partialPSX, partialrefusePSX, totalrefusePSX, totalPSX, partialPDX, partialrefusePDX, totalrefusePDX, totalPDX FROM counters WHERE counter_id=%(counter_id)s"
        value = {'counter_id': str(self.combo.currentText())}
        records, n_row, err = selectMethod(sql, value, logger)
        if not err:
            if n_row > 0:
                for e in records:
                    self.labelPartial.setText(str(e[1]+e[5]))
                    self.labelPartialRefuse.setText(str(e[2]+e[6]))
                    self.labelTotalRefuse.setText(str(e[3]+e[7]))
                    self.labelTotal.setText(str(e[4]+e[8]))
            else:
                self.labelPartial.setText("0")
                self.labelPartialRefuse.setText("0")
                self.labelTotal.setText("0")
                self.labelTotalRefuse.setText("0")

        for e in lang_dictionary:
            if e[1] == phase:
                self.lang_dictionary.update({e[0]: e[2]})

        self.labelNPartial.setText(self.lang_dictionary["label_partial"])
        self.labelNTotal.setText(self.lang_dictionary["label_total"])
        self.labelDescription.setText(
            self.lang_dictionary["label_description"])
        self.buttonResetPartial.setText(
            self.lang_dictionary["button_resetpartial"])
        self.labelNPartialRefuse.setText(self.lang_dictionary["label_partial"])
        self.labelNTotalRefuse.setText(self.lang_dictionary["label_total"])
        self.labelBuoni.setText(self.lang_dictionary["label_buoni"])
        self.labelScarti.setText(self.lang_dictionary["label_scarti"])

    '''
        Resetta i contatori parziali della macchina
    '''

    def resetPartial(self):
        if str(self.combo.currentText()) != "":
            update_partial_counters_query_method(
                0, 0, 0, 0, str(self.combo.currentText()), logger)
            self.labelPartial.setText("0")
            self.labelPartialRefuse.setText("0")

    '''
    def paintEvent(self, event):
        self.painter = QPainter(self)
        self.painter.begin(self)
        self.painter.setPen(QPen(Qt.white, 2, Qt.SolidLine))
        self.painter.drawLine(50,250,1230,250) #first horizontal
        self.painter.drawLine(50,350,1230,350) #second horizontal
        self.painter.drawLine(50,450,1230,450) #third horizontal
        self.painter.drawLine(280,150,280,550) #first vertical
        self.painter.drawLine(522,150,522,450) #second vertical
        self.painter.drawLine(758,150,758,550) #third vertical
        self.painter.drawLine(994,150,994,550) #fourth vertical
        self.painter.end()
    '''

    def __init__(self, parent):
        super(Counters, self).__init__(parent)
        self.parent = parent
        self.lang_dictionary = {}

        self.frame = QFrame(self)
        self.frame.setGeometry(190, 150, 500, 325)
        self.frame.setStyleSheet(Style.INIT_STYLE)

        self.labelDescription = QLabel("", self)
        self.labelDescription.setGeometry(110, 80, 350, 30)
        self.labelDescription.setStyleSheet(Style.TITLE3_CENTERED_STYLE)

        self.combo = QComboBox(self)
        self.combo.setStyleSheet(Style.BODY_BOLD_QCOMBO1)
        self.combo.setGeometry(470, 80, 400, 40)
        self.combo.currentTextChanged.connect(self.updateData)

        self.labelBuoni = QLabel("", self)
        self.labelBuoni.setStyleSheet(Style.TITLE5_CENTERED_STYLE)
        self.labelBuoni.setGeometry(230, 180, 236, 25)
        self.labelBuoni.setWordWrap(True)

        self.labelScarti = QLabel("", self)
        self.labelScarti.setStyleSheet(Style.TITLE5_CENTERED_STYLE)
        self.labelScarti.setGeometry(450, 180, 236, 25)
        self.labelScarti.setWordWrap(True)

        self.labelNPartial = QLabel("", self)
        self.labelNPartial.setStyleSheet(Style.TITLE5_CENTERED_STYLE)
        self.labelNPartial.setGeometry(230, 210, 236, 55)
        self.labelNPartial.setWordWrap(True)

        self.labelNPartialRefuse = QLabel("", self)
        self.labelNPartialRefuse.setStyleSheet(Style.TITLE5_CENTERED_STYLE)
        self.labelNPartialRefuse.setGeometry(450, 210, 236, 55)
        self.labelNPartialRefuse.setWordWrap(True)

        self.labelPartial = QLabel("", self)
        self.labelPartial.setGeometry(280, 270, 136, 60)
        self.labelPartial.setStyleSheet(Style.BODY4_CENTERED_STYLE)

        self.labelPartialRefuse = QLabel("", self)
        self.labelPartialRefuse.setGeometry(500, 270, 136, 60)
        self.labelPartialRefuse.setStyleSheet(Style.BODY4_CENTERED_STYLE)

        self.labelNTotal = QLabel("", self)
        self.labelNTotal.setStyleSheet(Style.TITLE5_CENTERED_STYLE)
        self.labelNTotal.setGeometry(230, 315, 236, 100)
        self.labelNTotal.setWordWrap(True)

        self.labelNTotalRefuse = QLabel("", self)
        self.labelNTotalRefuse.setStyleSheet(Style.TITLE5_CENTERED_STYLE)
        self.labelNTotalRefuse.setGeometry(450, 315, 236, 100)
        self.labelNTotalRefuse.setWordWrap(True)

        self.labelTotal = QLabel("", self)
        self.labelTotal.setGeometry(280, 395, 136, 60)
        self.labelTotal.setStyleSheet(Style.BODY4_CENTERED_STYLE)

        self.labelTotalRefuse = QLabel("", self)
        self.labelTotalRefuse.setGeometry(500, 395, 136, 60)
        self.labelTotalRefuse.setStyleSheet(Style.BODY4_CENTERED_STYLE)

        self.buttonResetPartial = QPushButton("", self)
        # self.buttonResetPartial.setGeometry(240,515,452,70)
        self.buttonResetPartial.setGeometry(
            Style.BUTTONBAR_X+150, Style.BUTTONBAR_Y, 360, Style.BUTTONBAR_HEIGHT)
        self.buttonResetPartial.setStyleSheet(Style.BUTTONMENU_STYLE)
        self.buttonResetPartial.clicked.connect(self.resetPartial)

        self.buttonHome = QPushButton("", self)
        self.buttonHome.setGeometry(int(Style.BUTTONBAR_X), int(
            Style.BUTTONBAR_Y), int(Style.BUTTONBAR_WIDTH), int(Style.BUTTONBAR_HEIGHT))
        self.buttonHome.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.buttonHome.clicked.connect(lambda: self.phase.emit(PHASE_HOME))
        if LINUX:
            self.buttonHome.setIcon(QIcon(IMG_LINUX_PATH+"home.png"))
        else:
            self.buttonHome.setIcon(
                QIcon(os.path.join(IMG_WIN_PATH, "home.png")))
        self.buttonHome.setIconSize(
            QSize(int(Style.BUTTONBAR_WIDTH - 20), int(Style.BUTTONBAR_HEIGHT - 20)))

# REV 5.0


class Alarms(QWidget):
    phase = pyqtSignal(int)

    '''
        Esegue l'updateData della classe corrente
    '''

    def updateData(self, lang_dictionary, phase, description_language):
        self.lang_dictionary = {}
        self.description_language = description_language

        for e in lang_dictionary:
            if e[1] == phase:
                self.lang_dictionary.update({e[0]: e[2]})

        self.logTable.setHorizontalHeaderLabels([self.lang_dictionary["header_datetime"], self.lang_dictionary["header_product"], self.lang_dictionary["header_n"], self.lang_dictionary["header_status"],
                                                 self.lang_dictionary["header_int"], self.lang_dictionary["header_customer"], self.lang_dictionary["header_side"], self.lang_dictionary["header_user"]])
        self.alarmTable.setHorizontalHeaderLabels([self.lang_dictionary["header_datetime"], self.lang_dictionary["header_warning"],
                                                  self.lang_dictionary["header_message"], self.lang_dictionary["header_user"]])
        self.titleAlarm.setText(self.lang_dictionary["label_alarms"])
        self.titleLog.setText(self.lang_dictionary["label_productionlog"])
        self.info_label.setText(self.lang_dictionary["label_info"])
        self.label_label.setText(self.lang_dictionary["label_label"])
        self.print_button.setText(self.lang_dictionary["button_print"])
        self.device_label.setText(self.lang_dictionary["label_device"])
        self.updateTable()

        self.stopTimer = Event()
        self.timer = ClientTimer(self.stopTimer, 2.0)
        self.timer.signal.connect(self.updateDevices)
        self.timer.start()

    ###
    # Return list of tuples mapping drive letters to drive types
    def getRemovableDrives(self):
        removable_drives = []
        bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        GetVolumeInformationW = ctypes.windll.kernel32.GetVolumeInformationW
        name = ctypes.create_unicode_buffer(64)
        for i in range(26):
            bit = 2 ** i
            if bit & bitmask:
                drive_letter = '%s:' % chr(65 + i)
                drive_type = ctypes.windll.kernel32.GetDriveTypeW(
                    '%s\\' % drive_letter)
                # result.append((drive_letter, drive_type))
                # get name of the drive
                res = GetVolumeInformationW('%s\\' % drive_letter, name, 64, None,
                                            None, None, None, 0)
                if drive_type == DRIVE_REMOVABLE:
                    removable_drives.append(
                        ('%s\\' % drive_letter, name.value, DRIVE_TYPE_MAP[drive_type]))
        # print(removable_drives)
        return removable_drives

    '''
        In base ai dispositivi disponibili si sposta nel path indicata
    '''

    def updateDevices(self):
        removable_drives = self.getRemovableDrives()
        # print('removable_drives = %r' % removable_drives)
        try:
            self.device_combo.clear()
            for e in removable_drives:
                if e != "":
                    if e[1] != "":
                        self.device_combo.addItem(e[1])
                    else:
                        self.device_combo.addItem(e[0])
        except subprocess.SubprocessError as e:
            print(format(e))

    '''
        Aggiorna la tabella della pagina
    '''

    def updateTable(self):
        # Tabella log allarmi
        if self.isAlarmTable == True:
            for row in range(self.rowcount):
                self.alarmTable.setItem(row, 0, QTableWidgetItem(""))
                self.alarmTable.setItem(row, 1, QTableWidgetItem(""))
                self.alarmTable.setItem(row, 2, QTableWidgetItem(""))
                self.alarmTable.setItem(row, 3, QTableWidgetItem(""))

            sql = "select datetimestamp, title, " + self.description_language + \
                ", user_id from alarm_log ORDER BY datetimestamp DESC LIMIT " + \
                str(self.rowcount)
            value = {}
            records, n_row, err = selectMethod(sql, value, logger)
            if not err and n_row > 0:
                row = 0
                for array in records:
                    self.alarmTable.setItem(
                        row, 0, QTableWidgetItem(str(array[0])))
                    self.alarmTable.setItem(row, 1, QTableWidgetItem(array[1]))
                    self.alarmTable.setItem(row, 2, QTableWidgetItem(array[2]))
                    self.alarmTable.setItem(row, 3, QTableWidgetItem(array[3]))
                    row = row + 1

            self.frameAlarm.setVisible(True)
            self.frameLog.setVisible(False)
        # Tabella log produzione
        else:
            for row in range(self.rowcount):
                self.logTable.setItem(row, 0, QTableWidgetItem(""))
                self.logTable.setItem(row, 1, QTableWidgetItem(""))
                self.logTable.setItem(row, 2, QTableWidgetItem(""))
                self.logTable.setItem(row, 3, QTableWidgetItem(""))
                self.logTable.setItem(row, 4, QTableWidgetItem(""))
                self.logTable.setItem(row, 5, QTableWidgetItem(""))
                self.logTable.setItem(row, 6, QTableWidgetItem(""))
                self.logTable.setItem(row, 7, QTableWidgetItem(""))
            sql = "SELECT datetimestamp, counter_id, serial, status_id, internal_code, customer_code, side, user_id FROM prod_log ORDER BY datetimestamp DESC LIMIT " + \
                str(self.rowcount)
            value = {}
            records, n_row, err = selectMethod(sql, value, logger)
            if not err and n_row > 0:
                row = 0
                for array in records:
                    self.logTable.setItem(
                        row, 0, QTableWidgetItem(str(array[0])))
                    self.logTable.setItem(
                        row, 1, QTableWidgetItem(str(array[1])))
                    self.logTable.setItem(
                        row, 2, QTableWidgetItem(str(array[2])))
                    self.logTable.setItem(
                        row, 3, QTableWidgetItem(str(array[3])))
                    self.logTable.setItem(
                        row, 4, QTableWidgetItem(str(array[4])))
                    self.logTable.setItem(
                        row, 5, QTableWidgetItem(str(array[5])))
                    self.logTable.setItem(
                        row, 6, QTableWidgetItem(str(array[6])))
                    self.logTable.setItem(
                        row, 7, QTableWidgetItem(str(array[7])))
                    row = row + 1
            self.frameAlarm.setVisible(False)
            self.frameLog.setVisible(True)

    '''
        Cambio di pagina
    '''

    def changePhase(self, n):
        if n == PHASE_HOME:
            self.stopTimer.set()
        self.phase.emit(n)
        self.isAlarmTable = True

    '''
        Cambia il tipo di tabella da visualizzare
    '''

    def changeTable(self, table):
        if table == "alarm":
            self.isAlarmTable = True
        else:
            self.isAlarmTable = False
        self.updateTable()

    '''
        Scarica la tabella contenente il log degli utenti e salva nel file user_log.csv
    '''

    def downloadUsers(self):
        sql = "SELECT datetimestamp, status_id, user_id, total, totalrefuse FROM users_log ORDER BY datetimestamp DESC"
        value = {}
        records, n_row, err = selectMethod(sql, value, logger)
        if not err and n_row > 0:
            if LINUX:
                with open(FTP_USERLOG_LINUX_PATH, 'w', newline='') as csvfile:
                    fieldnames = ['Timestamp', 'Status',
                                  'User', 'Total', 'Total Refuse']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for e in records:
                        writer.writerow(
                            {'Timestamp': e[0], 'Status': e[1], 'User': e[2], 'Total': e[3], 'Total Refuse': e[4]})
                ftp = FTP(FTP_LOCAL_HOST)
                ftp.login(FTP_LOCAL_USER, FTP_LOCAL_PASSWORD)
                ftp.cwd('/')
                with open(FTP_USERLOG_LINUX_PATH, "rb") as f:
                    ftp.storbinary(
                        'STOR ' + os.path.basename("users_log.csv"), f)
                QMessageBox.information(
                    self, self.lang_dictionary["qmessagebox_information_ftp_title"], self.lang_dictionary["qmessagebox_information_ftp_userslog"])
            else:
                with open(FTP_USERLOG_WIN_PATH, 'w', newline='') as csvfile:
                    fieldnames = ['Timestamp', 'Status',
                                  'User', 'Total', 'Total Refuse']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for e in records:
                        writer.writerow(
                            {'Timestamp': e[0], 'Status': e[1], 'User': e[2], 'Total': e[3], 'Total Refuse': e[4]})
                ftp = FTP(FTP_LOCAL_HOST)
                ftp.login(FTP_LOCAL_USER, FTP_LOCAL_PASSWORD)
                ftp.cwd('/')
                with open(FTP_USERLOG_WIN_PATH, "rb") as f:
                    ftp.storbinary(
                        'STOR ' + os.path.basename("users_log.csv"), f)
                QMessageBox.information(
                    self, self.lang_dictionary["qmessagebox_information_ftp_title"], self.lang_dictionary["qmessagebox_information_ftp_userslog"])
        else:
            QMessageBox.critical(
                self, self.lang_dictionary["qmessagebox_information_ftp_title"], self.lang_dictionary["qmessagebox_error_ftp"])

    '''
        Scarica la tabella contenente il log di produzione e salva nel file prod_log.csv
    '''

    def download_production(self):
        removable_drives = []
        sql = "SELECT datetimestamp, counter_id, serial, status_id, internal_code, customer_code, side, user_id FROM prod_log ORDER BY datetimestamp DESC"
        value = {}
        records, n_row, err = selectMethod(sql, value, logger)
        if not err and n_row > 0:
            if LINUX:
                with open(FTP_PRODLOG_LINUX_PATH, 'w', newline='') as csvfile:
                    fieldnames = ['Timestamp', 'Component', 'Progression',
                                  'Status', 'Internal Code', 'Customer Code', 'Side', 'User']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for e in records:
                        writer.writerow({'Timestamp': e[0], 'Component': e[1], 'Progression': e[2], 'Status': e[3],
                                        'Internal Code': e[4], 'Customer Code': e[5], 'Side': e[6], 'User': e[7]})
                if self.device_combo.currentText() != "":
                    temp = "cp /home/pi/HMI/ControlPanel4/ControlPanel/production_log.csv /media/pi/'" + \
                        self.device_combo.currentText() + "/'production_log_" + DB + "A.csv"
                    call(temp, shell=True)
                else:
                    QMessageBox.critical(
                        self, self.lang_dictionary["qmessagebox_error_title"], self.lang_dictionary["qmessagebox_error_usb"])
                ftp = FTP(FTP_LOCAL_HOST)
                ftp.login(FTP_LOCAL_USER, FTP_LOCAL_PASSWORD)
                ftp.cwd('/')
                with open(FTP_PRODLOG_LINUX_PATH, "rb") as f:
                    ftp.storbinary(
                        'STOR ' + os.path.basename("production_log.csv"), f)
                QMessageBox.information(
                    self, self.lang_dictionary["qmessagebox_information_ftp_title"], self.lang_dictionary["qmessagebox_information_ftp_prodlog"])
            else:
                with open(FTP_PRODLOG_WIN_PATH, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Timestamp', 'Component', 'Progression',
                                  'Status', 'Internal Code', 'Customer Code', 'Side', 'User']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for e in records:
                        writer.writerow({'Timestamp': e[0], 'Component': e[1], 'Progression': e[2], 'Status': e[3],
                                        'Internal Code': e[4], 'Customer Code': e[5], 'Side': e[6], 'User': e[7]})
                removable_drives = self.getRemovableDrives()
                if self.device_combo.currentText() != "":
                    for el in removable_drives:
                        if el[1] != "":
                            if el[1] == self.device_combo.currentText():
                                src_path = os.path.join(
                                    abspath_beginstr, FTP_PRODLOG_WIN_PATH)
                                dst_path = el[0]
                                shutil.copy(src_path, dst_path)
                        else:
                            if el[0] == self.device_combo.currentText():
                                src_path = os.path.join(
                                    abspath_beginstr, FTP_PRODLOG_WIN_PATH)
                                dst_path = el[0]
                                shutil.copy(src_path, dst_path)
                else:
                    QMessageBox.critical(
                        self, self.lang_dictionary["qmessagebox_error_title"], self.lang_dictionary["qmessagebox_error_usb"])
                ftp = FTP(FTP_LOCAL_HOST)
                ftp.login(FTP_LOCAL_USER, FTP_LOCAL_PASSWORD)
                ftp.cwd('/')
                with open(os.path.join(abspath_beginstr, FTP_PRODLOG_WIN_PATH), "rb") as f:
                    ftp.storbinary(
                        'STOR ' + os.path.basename("production_log.csv"), f)
                QMessageBox.information(
                    self, self.lang_dictionary["qmessagebox_information_ftp_title"], self.lang_dictionary["qmessagebox_information_ftp_prodlog"])
        else:
            QMessageBox.critical(
                self, self.lang_dictionary["qmessagebox_information_ftp_title"], self.lang_dictionary["qmessagebox_error_ftp"])

    '''
        Scarica la tabella contenente il log degli allarmi e salva nel file alarms_log.csv
    '''

    def download_alarms(self):
        removable_drives = []
        sql = "SELECT datetimestamp, counter_id, alarm_id, title, description_IT, description_EN, description_LANG1, description_LANG2, user_id FROM alarm_log ORDER BY alarm_log.datetimestamp DESC"
        value = {}
        records, n_row, err = selectMethod(sql, value, logger)
        if not err and n_row > 0:
            if LINUX:
                with open(FTP_ALARMS_LINUX_PATH, 'w', newline='') as csvfile:
                    fieldnames = ['Timestamp', 'Component', 'Alarm ID', 'Alarm Title', 'Alarm Description IT',
                                  'Alarm Description EN', 'Alarm Description LANG1', 'Alarm Description LANG2', 'User']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for e in records:
                        writer.writerow({'Timestamp': e[0], 'Component': e[1], 'Alarm ID': e[2], 'Alarm Title': e[3], 'Alarm Description IT': e[4],
                                        'Alarm Description EN': e[5], 'Alarm Description LANG1': e[6], 'Alarm Description LANG2': e[7], 'User': e[8]})
                if self.device_combo.currentText() != "":
                    temp = "cp /home/pi/HMI/ControlPanel4/ControlPanel/alarms_log.csv /media/pi/'" + \
                        self.device_combo.currentText() + "'/alarms_log_" + DB + "A.csv"
                    call(temp, shell=True)
                else:
                    QMessageBox.critical(
                        self, self.lang_dictionary["qmessagebox_error_title"], self.lang_dictionary["qmessagebox_error_usb"])
                ftp = FTP(FTP_LOCAL_HOST)
                ftp.login(FTP_LOCAL_USER, FTP_LOCAL_PASSWORD)
                ftp.cwd('/')
                with open(FTP_ALARMS_LINUX_PATH, "rb") as f:
                    ftp.storbinary(
                        'STOR ' + os.path.basename("alarms_log.csv"), f)
                QMessageBox.information(
                    self, self.lang_dictionary["qmessagebox_information_ftp_title"], self.lang_dictionary["qmessagebox_information_ftp_alarmslog"])
            else:
                with open(FTP_ALARMS_WIN_PATH, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Timestamp', 'Component', 'Alarm ID', 'Alarm Title', 'Alarm Description IT',
                                  'Alarm Description EN', 'Alarm Description LANG1', 'Alarm Description LANG2', 'User']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for e in records:
                        writer.writerow({'Timestamp': e[0], 'Component': e[1], 'Alarm ID': e[2], 'Alarm Title': e[3], 'Alarm Description IT': e[4],
                                        'Alarm Description EN': e[5], 'Alarm Description LANG1': e[6], 'Alarm Description LANG2': e[7], 'User': e[8]})
                removable_drives = self.getRemovableDrives()
                if self.device_combo.currentText() != "":
                    for el in removable_drives:
                        if el[1] != "":
                            if el[1] == self.device_combo.currentText():
                                src_path = os.path.join(
                                    abspath_beginstr, FTP_ALARMS_WIN_PATH)
                                dst_path = el[0]
                                shutil.copy(src_path, dst_path)
                        else:
                            if el[0] == self.device_combo.currentText():
                                src_path = os.path.join(
                                    abspath_beginstr, FTP_ALARMS_WIN_PATH)
                                dst_path = el[0]
                                shutil.copy(src_path, dst_path)
                else:
                    QMessageBox.critical(
                        self, self.lang_dictionary["qmessagebox_error_title"], self.lang_dictionary["qmessagebox_error_usb"])
                ftp = FTP(FTP_LOCAL_HOST)
                ftp.login(FTP_LOCAL_USER, FTP_LOCAL_PASSWORD)
                ftp.cwd('/')
                with open(os.path.join(abspath_beginstr, FTP_ALARMS_WIN_PATH), "rb") as f:
                    ftp.storbinary(
                        'STOR ' + os.path.basename("alarms_log.csv"), f)
                QMessageBox.information(
                    self, self.lang_dictionary["qmessagebox_information_ftp_title"], self.lang_dictionary["qmessagebox_information_ftp_alarmslog"])
        else:
            QMessageBox.critical(
                self, self.lang_dictionary["qmessagebox_information_ftp_title"], self.lang_dictionary["qmessagebox_error_ftp"])

    '''
        Selezione della riga corrente
    '''

    def selectRow(self):
        row = self.logTable.selectedItems()
        self.label_box.setText(row[2].text())

    '''
        Stampa un etichetta manuale, a patto che ne venga data la possibilità
    '''

    def printLabel(self):
        if self.label_box.text() == "0000000":
            QMessageBox.critical(
                self, self.lang_dictionary["qmessagebox_error_title"], self.lang_dictionary["qmessagebox_error_badprintrequest"])
        elif len(self.label_box.text()) == 0:
            QMessageBox.critical(
                self, self.lang_dictionary["qmessagebox_error_title"], self.lang_dictionary["qmessagebox_error_nolabel"])
        else:
            row = self.logTable.selectedItems()
            res = QMessageBox.question(self, self.lang_dictionary["qmessagebox_info_title"],
                                       self.lang_dictionary["qmessagebox_printer_question"], QMessageBox.Yes | QMessageBox.No)
            if res == QMessageBox.Yes:
                err = printZebraLabel(self.label_buffer, row[0].text(
                ), row[7].text(), row[5].text(), row[2].text())
                if err:
                    QMessageBox.critical(
                        self, self.lang_dictionary["qmessagebox_error_title"], self.lang_dictionary["qmessagebox_printer_error"])

    def __init__(self, parent):
        super(Alarms, self).__init__(parent)
        self.parent = parent
        self.rowcount = 50
        self.lang_dictionary = {}
        self.description_language = ""

        self.label_buffer = ""
        ''' with open("label.zpl","r") as file:
            for line in file:
                self.label_buffer = self.label_buffer + line
                '''

        # Flag che stabilisce la tabella home: in questo caso la tabella allarmi.
        self.isAlarmTable = True

        self.frameLog = QFrame(self)
        self.frameLog.setGeometry(0, 75, Style.WIDTH, Style.HEIGHT-150)
        self.titleLog = QLabel("", self.frameLog)
        self.titleLog.setGeometry(0, 0, Style.WIDTH, 50)
        self.titleLog.setStyleSheet(Style.TITLE2_CENTERED_STYLE)

        self.info_label = QLabel("", self.frameLog)
        self.info_label.setGeometry(10, self.frameLog.height()-140, 650, 100)
        self.info_label.setStyleSheet(Style.SUBTITLE6_STYLE)
        self.info_label.setWordWrap(True)

        self.label_label = QLabel("", self.frameLog)
        self.label_label.setGeometry(750, self.frameLog.height()-140, 350, 45)
        self.label_label.setStyleSheet(Style.TITLE5_CENTERED_STYLE)
        self.label_label.setVisible(False)
        self.label_box = QLabel("", self.frameLog)
        self.label_box.setGeometry(750, self.frameLog.height()-95, 350, 50)
        self.label_box.setStyleSheet(Style.BODY4_CENTERED_STYLE)
        self.label_box.setVisible(False)
        self.print_button = QPushButton("", self.frameLog)
        self.print_button.setGeometry(
            1120, self.frameLog.height()-140, 150, 100)
        self.print_button.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.print_button.clicked.connect(self.printLabel)
        self.print_button.setVisible(False)

        self.frameLogTable = QFrame(self.frameLog)
        self.frameLogTable.setGeometry(
            0, 50, self.frameLog.width(), self.frameLog.height()-75)
        self.logTable = QTableWidget()
        self.layout1 = QVBoxLayout(self.frameLogTable)
        self.layout1.addWidget(self.logTable)

        self.logTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.logTable.setStyleSheet(Style.CONF_TABLE)
        self.logTable.setRowCount(self.rowcount)
        self.logTable.setColumnCount(8)
        self.logTable.setHorizontalHeaderLabels(
            ["DATA/ORA", "PRODOTTO", "PROGRESSIVO N", "STATUS", "SIDE", "INTERNAL CODE", "CUSTOMER", "USER_ID"])
        self.logTable.setColumnWidth(0, 200)
        self.logTable.setColumnWidth(1, 200)
        self.logTable.setColumnWidth(2, 150)
        self.logTable.setColumnWidth(3, 100)
        self.logTable.setColumnWidth(4, 200)
        self.logTable.setColumnWidth(5, 200)
        self.logTable.setColumnWidth(6, 100)
        self.logTable.setColumnWidth(7, 150)
        self.logTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.logTable.itemSelectionChanged.connect(self.selectRow)

        self.frameAlarm = QFrame(self)
        self.frameAlarm.setGeometry(0, 75, Style.WIDTH, Style.HEIGHT-150)
        self.titleAlarm = QLabel("", self.frameAlarm)
        self.titleAlarm.setGeometry(0, 0, Style.WIDTH, 50)
        self.titleAlarm.setStyleSheet(Style.TITLE2_CENTERED_STYLE)

        self.frameAlarmTable = QFrame(self.frameAlarm)
        self.frameAlarmTable.setGeometry(
            0, 50, self.frameAlarm.width(), self.frameAlarm.height()-75)
        self.alarmTable = QTableWidget()
        self.layout2 = QVBoxLayout(self.frameAlarmTable)
        self.layout2.addWidget(self.alarmTable)

        self.alarmTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.alarmTable.setStyleSheet(Style.CONF_TABLE)
        self.alarmTable.setRowCount(self.rowcount)
        self.alarmTable.setColumnCount(4)
        self.alarmTable.setHorizontalHeaderLabels(
            ["DATETIME", "WARNING", "MESSAGE", "USER_ID"])
        self.alarmTable.setColumnWidth(0, 250)
        self.alarmTable.setColumnWidth(1, 300)
        self.alarmTable.setColumnWidth(2, 400)
        self.alarmTable.setColumnWidth(3, 250)
        self.alarmTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.buttonHome = QPushButton(self)
        self.buttonHome.setGeometry(int(Style.BUTTONBAR_X), int(
            Style.BUTTONBAR_Y), int(Style.BUTTONBAR_WIDTH), int(Style.BUTTONBAR_HEIGHT))
        self.buttonHome.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.buttonHome.clicked.connect(lambda: self.changePhase(PHASE_HOME))
        if LINUX:
            self.buttonHome.setIcon(QIcon(IMG_LINUX_PATH+"home.png"))
        else:
            self.buttonHome.setIcon(
                QIcon(os.path.join(IMG_WIN_PATH, "home.png")))
        self.buttonHome.setIconSize(
            QSize(int(Style.BUTTONBAR_WIDTH - 20), int(Style.BUTTONBAR_HEIGHT - 20)))

        self.device_label = QLabel("", self)
        self.device_label.setGeometry(360, 490, 150, 100)
        self.device_label.setStyleSheet(Style.SUBTITLE6_STYLE)
        self.device_label.setWordWrap(True)
        self.device_combo = QComboBox(self)
        self.device_combo.setGeometry(500, 515, 250, 50)
        self.device_combo.setStyleSheet(Style.QCOMBOBOX_TITLE5)
        # self.device_combo.setVisible(True)
        # self.device_combo.addItem("test")

        self.buttonAlarmsLog = QPushButton(self)
        self.buttonAlarmsLog.setGeometry(int(Style.BUTTONBAR_X*2 + Style.BUTTONBAR_WIDTH),
                                         Style.BUTTONBAR_Y, Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT)
        self.buttonAlarmsLog.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.buttonAlarmsLog.clicked.connect(lambda: self.changeTable("alarm"))
        if LINUX:
            self.buttonAlarmsLog.setIcon(
                QIcon(IMG_LINUX_PATH+"alarms_log.png"))
        else:
            self.buttonAlarmsLog.setIcon(
                QIcon(os.path.join(IMG_WIN_PATH, "alarms_log.png")))
        self.buttonAlarmsLog.setIconSize(
            QSize(Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT))

        self.buttonProductionLog = QPushButton(self)
        self.buttonProductionLog.setGeometry(int(
            Style.BUTTONBAR_X*3 + Style.BUTTONBAR_WIDTH*2), Style.BUTTONBAR_Y, Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT)
        self.buttonProductionLog.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.buttonProductionLog.clicked.connect(
            lambda: self.changeTable("production"))
        if LINUX:
            self.buttonProductionLog.setIcon(
                QIcon(IMG_LINUX_PATH+"production_log.png"))
        else:
            self.buttonProductionLog.setIcon(
                QIcon(os.path.join(IMG_WIN_PATH, "production_log.png")))
        self.buttonProductionLog.setIconSize(
            QSize(int(Style.BUTTONBAR_WIDTH), int(Style.BUTTONBAR_HEIGHT)))

        self.buttonDownloadUsers = QPushButton(self)
        self.buttonDownloadUsers.setGeometry(int(
            Style.BUTTONBAR_X*4 + Style.BUTTONBAR_WIDTH*3), Style.BUTTONBAR_Y, Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT)
        self.buttonDownloadUsers.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.buttonDownloadUsers.clicked.connect(self.downloadUsers)
        if LINUX:
            self.buttonDownloadUsers.setIcon(
                QIcon(IMG_LINUX_PATH+"downloadUsers.png"))
        else:
            self.buttonDownloadUsers.setIcon(
                QIcon(os.path.join(IMG_WIN_PATH, "downloadUsers.png")))
        self.buttonDownloadUsers.setIconSize(
            QSize(Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT))
        self.buttonDownloadUsers.setVisible(False)

        self.buttonDownloadAlarms = QPushButton(self)
        self.buttonDownloadAlarms.setGeometry(int(
            Style.BUTTONBAR_X*7 + Style.BUTTONBAR_WIDTH*7), Style.BUTTONBAR_Y, Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT)
        self.buttonDownloadAlarms.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.buttonDownloadAlarms.clicked.connect(self.download_alarms)
        if LINUX:
            self.buttonDownloadAlarms.setIcon(
                QIcon(IMG_LINUX_PATH+"download_alarms.png"))
        else:
            self.buttonDownloadAlarms.setIcon(
                QIcon(os.path.join(IMG_WIN_PATH, "download_alarms.png")))
        self.buttonDownloadAlarms.setIconSize(
            QSize(int(Style.BUTTONBAR_WIDTH), int(Style.BUTTONBAR_HEIGHT)))

        self.buttonDownloadProduction = QPushButton(self)
        self.buttonDownloadProduction.setGeometry(int(
            Style.BUTTONBAR_X*8 + Style.BUTTONBAR_WIDTH*8), Style.BUTTONBAR_Y, Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT)
        self.buttonDownloadProduction.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.buttonDownloadProduction.clicked.connect(self.download_production)
        if LINUX:
            self.buttonDownloadProduction.setIcon(
                QIcon(IMG_LINUX_PATH+"download_production.png"))
        else:
            self.buttonDownloadProduction.setIcon(
                QIcon(os.path.join(IMG_WIN_PATH, "download_production.png")))
        self.buttonDownloadProduction.setIconSize(
            QSize(int(Style.BUTTONBAR_WIDTH), int(Style.BUTTONBAR_HEIGHT)))

# REV 5.0


class Login1(QFrame):
    '''
        Esegue l'updateData della classe Login1
    '''

    def updateData(self, lang_dictionary):
        self.setVisible(True)
        self.user_id = ""
        self.name = ""
        self.surname = ""
        self.permission = {}
        self.lang_dictionary = lang_dictionary

        self.updateEdit()
        self.titleBadgeLabel.setText(
            self.lang_dictionary['descriptionBadgeLabel_alarmtitle'])
        self.titleSuperLabel.setText(
            self.lang_dictionary['descriptionSuperLabel_alarmtitle'])
        self.descriptionBadgeLabel.setText(
            self.lang_dictionary['descriptionBadgeLabel_alarm'])
        self.descriptionSuperLabel.setText(
            self.lang_dictionary['descriptionSuperLabel_alarm'])

        self.badgeLoginFrame.setVisible(True)
        self.superLoginFrame.setVisible(False)

    '''
        Svuota le label
    '''

    def updateEdit(self):
        self.idSuperLineEdit.setText("")
        self.passwordSuperLineEdit.setText("")
        self.idBadgeLineEdit.setText("")

    '''
        Torna indietro, DISABILITATO
    '''

    def goBack(self):
        self.setVisible(False)

    '''
        Torna nella pagina principale
    '''

    def goToMain(self, logintype):
        if logintype == "super":
            voidcounter = 0
            if len(str(self.idSuperLineEdit.text()).strip()) == 0:
                QMessageBox.critical(
                    self, self.lang_dictionary['qmessagebox_error_title'], self.lang_dictionary['qmessagebox_error_userid'])
                voidcounter = voidcounter + 1
            if len(str(self.passwordSuperLineEdit.text()).strip()) == 0:
                QMessageBox.critical(
                    self, self.lang_dictionary['qmessagebox_error_title'], self.lang_dictionary['qmessagebox_error_password'])
                voidcounter = voidcounter + 1
            if voidcounter == 0:
                password = encryptString(
                    str(self.passwordSuperLineEdit.text()).strip())
                sql = "SELECT user_id, name, surname, password, usergroup_id FROM users WHERE user_id = %(user_id)s"
                value = {'user_id': self.idSuperLineEdit.text().strip()}
                res, n_row, err = selectMethod(sql, value, logger)
                if not err:
                    if n_row == 0:
                        QMessageBox.critical(
                            self, self.lang_dictionary['qmessagebox_error_title'], self.lang_dictionary['qmessagebox_error_credentials'])
                        self.updateEdit()
                    else:
                        if res[0][3] == password:
                            sql = "SELECT productionMode, manualMode, configuration, counters, manualCommands, log, users FROM usersgroup WHERE usergroup_id = %(usergroup_id)s"
                            value = {'usergroup_id': res[0][4]}
                            res, n_row, err = selectMethod(sql, value, logger)
                            if not err:
                                if res[0][2] == 'yes':  # Verifica dei permessi dell'utente
                                    self.parent.loginButton.setVisible(False)
                                    self.parent.unlockButton.setVisible(True)
                                    self.setVisible(False)
                                else:
                                    QMessageBox.critical(
                                        self, self.lang_dictionary['permission_denied_title'], self.lang_dictionary['permission_denied_label'])
                                    self.updateEdit()
                            else:
                                QMessageBox.critical(
                                    self, self.lang_dictionary['qmessagebox_error_title'], self.lang_dictionary['qmessagebox_error_credentials_notfound'])
                                self.updateEdit()
                        else:
                            QMessageBox.critical(
                                self, self.lang_dictionary['qmessagebox_error_title'], self.lang_dictionary['qmessagebox_error_credentials'])
                            self.updateEdit()
                else:
                    QMessageBox.critical(
                        self, self.lang_dictionary['qmessagebox_error_title'], self.lang_dictionary['qmessagebox_error_credentials_notfound'])
                    self.updateEdit()
        elif logintype == "badge":
            if len(str(self.idBadgeLineEdit.text()).strip()) == 0:
                QMessageBox.critical(
                    self, self.lang_dictionary['qmessagebox_error_title'], self.lang_dictionary['qmessagebox_error_idnumber'])
            else:
                sql = "SELECT * FROM (SELECT users.user_id, users.name, users.surname, users.scancode, usersgroup.productionMode, usersgroup.manualMode, usersgroup.configuration, usersgroup.counters, usersgroup.manualCommands, usersgroup.log, usersgroup.users FROM users INNER JOIN usersgroup WHERE users.usergroup_id = usersgroup.usergroup_id) AS user WHERE user.scancode = %(scancode)s"
                value = {'scancode': str(self.idBadgeLineEdit.text()).strip()}
                res, n_row, err = selectMethod(sql, value, logger)
                if not err:
                    if n_row == 0:
                        self.idBadgeLineEdit.setText("")
                        QMessageBox.critical(
                            self, self.lang_dictionary['qmessagebox_error_title'], self.lang_dictionary['qmessagebox_error_credentials'])
                    else:
                        if res[0][5] == 'yes':  # se l'operatore ha i permessi richiesti
                            self.parent.loginButton.setVisible(False)
                            self.parent.unlockButton.setVisible(True)
                            self.setVisible(False)
                        else:
                            QMessageBox.critical(
                                self, self.lang_dictionary['permission_denied_title'], self.lang_dictionary['permission_denied_label'])
                else:
                    self.idBadgeLineEdit.setText("")
                    QMessageBox.critical(
                        self, self.lang_dictionary['qmessagebox_error_title'], self.lang_dictionary['qmessagebox_error_credentials_notfound'])

    '''
        Apre la virtual keuboard nel momento in cui una label viene premuta
    '''

    def callKey(self, edit):
        temp = edit.text()
        self.parent.parent.parent.virtualKeyboard.edit.setText("")
        self.parent.parent.parent.virtualKeyboard.exec_()
        self.parent.parent.parent.virtualKeyboard.edit.setFocus()
        if len(self.parent.parent.parent.virtualKeyboard.sendDateEnter()) == 0:
            edit.setText(temp)
        else:
            edit.setText(
                self.parent.parent.parent.virtualKeyboard.sendDateEnter())
        edit.repaint()

    '''
        Cambia tipo di login
    '''

    def changeLogin(self, logintype):
        if logintype == "super":
            self.idSuperLineEdit.setText("")
            self.passwordSuperLineEdit.setText("")
            self.badgeLoginFrame.setVisible(False)
            self.superLoginFrame.setVisible(True)
        elif logintype == "badge":
            self.idBadgeLineEdit.setText("")
            self.badgeLoginFrame.setVisible(True)
            self.superLoginFrame.setVisible(False)

    '''
        Riempie la label dello scancode con ciò che è stato letto dal lettore di badge
    '''

    def setScancode(self, scancode):
        self.idBadgeLineEdit.setEnabled(True)
        self.idBadgeLineEdit.setText(scancode)
        self.idBadgeLineEdit.setEnabled(False)

    def __init__(self, parent):
        super(Login1, self).__init__(parent)

        self.parent = parent
        self.lang_dictionary = {}
        self.user_id = ""
        self.permission = {}

        self.bg = QLabel(self)
        self.bg.setGeometry(0, 0, Style.WIDTH, Style.HEIGHT)
        self.bg.setStyleSheet("QLabel {background-color: rgb(255,255,255)}")
        if LINUX:
            self.bg.setPixmap(
                QPixmap(IMG_LINUX_PATH+"bg.jpeg").scaled(self.bg.width(), self.bg.height()))
        else:
            # self.bg.setPixmap(QPixmap(IMG_WIN_PATH+"bg.jpeg").scaled(self.bg.width(),self.bg.height()))
            self.bg.setPixmap(QPixmap(os.path.join(IMG_WIN_PATH, "bg.jpeg")).scaled(
                self.bg.width(), self.bg.height()))

        ##
        # LOGIN CON BADGE
        '''self.badgeLoginFrame = QFrame(self)
        self.badgeLoginFrame.setGeometry(0,60,Style.WIDTH,Style.HEIGHT-140)

        self.titleBadgeLabel = QLabel("BADGE LOGIN", self.badgeLoginFrame)
        self.titleBadgeLabel.setGeometry(0,150,self.badgeLoginFrame.width(),50)
        self.titleBadgeLabel.setStyleSheet(Style.TITLE_STYLE)
      
        self.descriptionBadgeLabel = QLabel("", self.badgeLoginFrame)
        self.descriptionBadgeLabel.setGeometry(0,275,self.badgeLoginFrame.width(),50)
        self.descriptionBadgeLabel.setStyleSheet(Style.SUBTITLE_CENTERED_RED_STYLE)

        self.idBadgeLineEdit = QLineEdit(self.badgeLoginFrame)
        self.idBadgeLineEdit.setGeometry(300,350,self.badgeLoginFrame.width()-600,50)
        self.idBadgeLineEdit.setStyleSheet(Style.TITLE3_LINEEDIT)
        self.idBadgeLineEdit.setEchoMode(QLineEdit.Password)
        if LINUX:
            self.idBadgeLineEdit.setEnabled(False)

        self.okButtonBadge = QPushButton("OK", self.badgeLoginFrame)
        self.okButtonBadge.setGeometry((int(self.badgeLoginFrame.width()/2)-125),450,100,75)
        self.okButtonBadge.setStyleSheet(Style.BUTTONMENU_STYLE)
        self.okButtonBadge.clicked.connect(lambda:self.goToMain("badge"))
        
        self.changeFrameFromBadgeButton = QPushButton("", self.badgeLoginFrame)
        self.changeFrameFromBadgeButton.setGeometry((int(self.badgeLoginFrame.width()/2) + 25),450,100,75)
        self.changeFrameFromBadgeButton.setStyleSheet(Style.BUTTONMENU_STYLE)
        if LINUX:
            changeFrameFromBadgeIcon = QIcon(IMG_LINUX_PATH+"key.png")
        else:
            changeFrameFromBadgeIcon = QIcon(os.path.join(IMG_WIN_PATH,"key.png"))
        self.changeFrameFromBadgeButton.setIcon(changeFrameFromBadgeIcon)
        self.changeFrameFromBadgeButton.setIconSize(QSize(self.changeFrameFromBadgeButton.width()-25, self.changeFrameFromBadgeButton.height()-25))
        self.changeFrameFromBadgeButton.clicked.connect(lambda:self.changeLogin("super"))'''

        # LOGIN CON BADGE

        self.badgeLoginFrame = QFrame(self)
        self.badgeLoginFrame.setGeometry(0, 60, Style.WIDTH, Style.HEIGHT-140)

        self.titleBadgeLabel = QLabel("BADGE LOGIN", self.badgeLoginFrame)
        self.titleBadgeLabel.setGeometry(
            0, 100, self.badgeLoginFrame.width(), 50)
        self.titleBadgeLabel.setStyleSheet(Style.TITLE_STYLE)

        self.descriptionBadgeLabel = QLabel("", self.badgeLoginFrame)
        self.descriptionBadgeLabel.setGeometry(
            0, 210, self.badgeLoginFrame.width(), 50)
        self.descriptionBadgeLabel.setStyleSheet(Style.SUBTITLE_CENTERED_STYLE)

        self.idBadgeLineEdit = QLineEdit(self.badgeLoginFrame)
        self.idBadgeLineEdit.setGeometry(
            300, 275, self.badgeLoginFrame.width()-600, 50)
        self.idBadgeLineEdit.setStyleSheet(Style.TITLE3_LINEEDIT)
        self.idBadgeLineEdit.setEchoMode(QLineEdit.Password)

        if LINUX:
            self.idBadgeLineEdit.setEnabled(False)

        self.okButtonBadge = QPushButton("OK", self.badgeLoginFrame)
        self.okButtonBadge.setGeometry(
            int((self.badgeLoginFrame.width()/2)-125), 350, 100, 75)
        self.okButtonBadge.setStyleSheet(Style.BUTTONMENU_STYLE)
        self.okButtonBadge.clicked.connect(lambda: self.goToMain("badge"))

        self.changeFrameFromBadgeButton = QPushButton("", self.badgeLoginFrame)
        self.changeFrameFromBadgeButton.setGeometry(
            int((self.badgeLoginFrame.width()/2) + 25), 350, 100, 75)
        self.changeFrameFromBadgeButton.setStyleSheet(Style.BUTTONMENU_STYLE)
        if LINUX:
            changeFrameFromBadgeIcon = QIcon(IMG_LINUX_PATH+"key.png")
        else:
            changeFrameFromBadgeIcon = QIcon(
                os.path.join(IMG_WIN_PATH, "key.png"))
        self.changeFrameFromBadgeButton.setIcon(changeFrameFromBadgeIcon)
        self.changeFrameFromBadgeButton.setIconSize(QSize(
            self.changeFrameFromBadgeButton.width()-25, self.changeFrameFromBadgeButton.height()-25))
        self.changeFrameFromBadgeButton.clicked.connect(
            lambda: self.changeLogin("super"))

        ##
        # LOGIN MANUALE
        '''self.superLoginFrame = QFrame(self)
        self.superLoginFrame.setGeometry(0,60,Style.WIDTH,Style.HEIGHT-140)

        self.titleSuperLabel = QLabel("USER LOGIN", self.superLoginFrame)
        self.titleSuperLabel.setGeometry(0,150,self.superLoginFrame.width(),50)
        self.titleSuperLabel.setStyleSheet(Style.TITLE_STYLE)

        self.descriptionSuperLabel = QLabel("", self.superLoginFrame)
        self.descriptionSuperLabel.setGeometry(0,225,self.superLoginFrame.width(),50)
        self.descriptionSuperLabel.setStyleSheet(Style.SUBTITLE_CENTERED_RED_STYLE)

        self.idSuperLabel = QLabel("User ID", self.superLoginFrame)
        self.idSuperLabel.setGeometry(0,300,int(self.superLoginFrame.width()/3),50)
        self.idSuperLabel.setStyleSheet(Style.TITLE2_CENTERED_STYLE)

        self.idSuperLineEdit = ClickableLineEdit(self.superLoginFrame)
        self.idSuperLineEdit.setGeometry(int(self.superLoginFrame.width()/3),300,int(self.superLoginFrame.width()/3*1.7-50),50)
        self.idSuperLineEdit.setStyleSheet(Style.TITLE3_LINEEDIT)
        self.idSuperLineEdit.clicked.connect(lambda:self.callKey(self.idSuperLineEdit))

        self.passwordSuperLabel = QLabel("Password", self.superLoginFrame)
        self.passwordSuperLabel.setGeometry(0,375,int(self.superLoginFrame.width()/3),50)
        self.passwordSuperLabel.setStyleSheet(Style.TITLE2_CENTERED_STYLE)

        self.passwordSuperLineEdit = ClickableLineEdit(self.superLoginFrame)
        self.passwordSuperLineEdit.setGeometry(int(self.superLoginFrame.width()/3),375,int(self.superLoginFrame.width()/3*1.7-50),50)
        self.passwordSuperLineEdit.setStyleSheet(Style.TITLE3_LINEEDIT)
        self.passwordSuperLineEdit.clicked.connect(lambda:self.callKey(self.passwordSuperLineEdit))
        self.passwordSuperLineEdit.setEchoMode(QLineEdit.Password)

        self.changeFrameFromSuperButton = QPushButton("", self.superLoginFrame)
        self.changeFrameFromSuperButton.setGeometry(int(self.superLoginFrame.width()/3),450,100,75)
        self.changeFrameFromSuperButton.setStyleSheet(Style.BUTTONMENU_STYLE)
        if LINUX:
            changeFrameFromSuperIcon = QIcon(IMG_LINUX_PATH+"hid.png")
        else:
            changeFrameFromSuperIcon = QIcon(os.path.join(IMG_WIN_PATH,"hid.png"))
        self.changeFrameFromSuperButton.setIcon(changeFrameFromSuperIcon)
        self.changeFrameFromSuperButton.setIconSize(QSize(int(self.changeFrameFromSuperButton.width()-25), int(self.changeFrameFromSuperButton.height()-25)))
        self.changeFrameFromSuperButton.clicked.connect(lambda:self.changeLogin("badge"))

        self.okButtonSuper = QPushButton("OK", self.superLoginFrame)
        self.okButtonSuper.setGeometry(int(self.superLoginFrame.width()/3 + 120),450,100,75)
        self.okButtonSuper.setStyleSheet(Style.BUTTONMENU_STYLE)
        self.okButtonSuper.clicked.connect(lambda:self.goToMain("super"))'''
        self.superLoginFrame = QFrame(self)
        self.superLoginFrame.setGeometry(0, 60, Style.WIDTH, Style.HEIGHT-140)

        self.titleSuperLabel = QLabel("USER LOGIN", self.superLoginFrame)
        self.titleSuperLabel.setGeometry(
            0, 75, self.superLoginFrame.width(), 50)
        self.titleSuperLabel.setStyleSheet(Style.TITLE_STYLE)

        self.descriptionSuperLabel = QLabel("", self.superLoginFrame)
        self.descriptionSuperLabel.setGeometry(
            0, 150, self.superLoginFrame.width(), 50)
        self.descriptionSuperLabel.setStyleSheet(Style.SUBTITLE_CENTERED_STYLE)

        self.idSuperLabel = QLabel("User ID", self.superLoginFrame)
        self.idSuperLabel.setGeometry(
            0, 225, int(self.superLoginFrame.width()/3), 50)
        self.idSuperLabel.setStyleSheet(Style.TITLE2_CENTERED_STYLE)

        self.idSuperLineEdit = ClickableLineEdit(self.superLoginFrame)
        self.idSuperLineEdit.setGeometry(int(self.superLoginFrame.width(
        )/3), 225, int(self.superLoginFrame.width()/3*1.7-50), 50)
        self.idSuperLineEdit.setStyleSheet(Style.TITLE3_LINEEDIT)
        self.idSuperLineEdit.clicked.connect(
            lambda: self.callKey(self.idSuperLineEdit))

        self.passwordSuperLabel = QLabel("Password", self.superLoginFrame)
        self.passwordSuperLabel.setGeometry(
            0, 300, int(self.superLoginFrame.width()/3), 50)
        self.passwordSuperLabel.setStyleSheet(Style.TITLE2_CENTERED_STYLE)

        self.passwordSuperLineEdit = ClickableLineEdit(self.superLoginFrame)
        self.passwordSuperLineEdit.setGeometry(int(self.superLoginFrame.width(
        )/3), 300, int(self.superLoginFrame.width()/3*1.7-50), 50)
        self.passwordSuperLineEdit.setStyleSheet(Style.TITLE3_LINEEDIT)
        self.passwordSuperLineEdit.clicked.connect(
            lambda: self.callKey(self.passwordSuperLineEdit))
        self.passwordSuperLineEdit.setEchoMode(QLineEdit.Password)

        self.changeFrameFromSuperButton = QPushButton("", self.superLoginFrame)
        self.changeFrameFromSuperButton.setGeometry(
            int(self.superLoginFrame.width()/3), 375, 100, 75)
        self.changeFrameFromSuperButton.setStyleSheet(Style.BUTTONMENU_STYLE)
        if LINUX:
            changeFrameFromSuperIcon = QIcon(IMG_LINUX_PATH+"hid.png")
        else:
            changeFrameFromSuperIcon = QIcon(
                os.path.join(IMG_WIN_PATH, "hid.png"))
        self.changeFrameFromSuperButton.setIcon(changeFrameFromSuperIcon)
        self.changeFrameFromSuperButton.setIconSize(QSize(int(
            self.changeFrameFromSuperButton.width()-25), self.changeFrameFromSuperButton.height()-25))
        self.changeFrameFromSuperButton.clicked.connect(
            lambda: self.changeLogin("badge"))
        # self.changeFrameFromSuperButton.setVisible(False)

        self.okButtonSuper = QPushButton("OK", self.superLoginFrame)
        self.okButtonSuper.setGeometry(
            int(self.superLoginFrame.width()/3 + 120), 375, 100, 75)
        # self.okButtonSuper.setGeometry(self.superLoginFrame.width()/3,450,100,75)
        self.okButtonSuper.setStyleSheet(Style.BUTTONMENU_STYLE)
        self.okButtonSuper.clicked.connect(lambda: self.goToMain("super"))

        ##
        # ALTRI OGGETTI
        self.badgeLoginFrame.setVisible(True)
        self.superLoginFrame.setVisible(False)

        self.setVisible(False)

# REV. 5.0


class Alarm(QFrame):
    '''
        Esegue l'updateData del frame Alarm
    '''

    def updateData(self, lang_dictionary, description_language, user_id, counter_id):
        self.user_id = user_id
        self.counter_id = counter_id
        self.lang_dictionary = {}
        self.description_language = description_language

        for e in lang_dictionary:
            if e[1] == 0:
                self.lang_dictionary.update({e[0]: e[2]})

        self.unlockButton.setText(self.lang_dictionary["button_alarmunlock"])
        self.reprocessButton.setText(self.lang_dictionary["button_reprocess"])

    '''
        Gestione del pulsante di sblocco allarme
    '''

    def unlockMachine(self):
        self.setVisible(False)
        '''if self.flag: # pezzo scarto
            self.ttModbus.setRegister((OUTPUT_ALARM_RESET1, 1))
            self.parent.flag_alarms = True #ripristino la possibilità di visualizzare schermate di allarme
        else: #torno in HOME
            self.ttModbus.setRegister((OUTPUT_ALARM_RESET1, 1))
            self.parent.flag_alarms = True
            self.parent.stopProduction()'''
        self.ttModbus.setRegister(
            (OUTPUT_ALARM_SHOWN, 0))      # Registro allarme mostrato a 0, dopo che allarme è accettato
        self.ttModbus.setRegister((OUTPUT_ALARM_ACCEPTED[0], 1))
        # ripristino la possibilità di visualizzare schermate di allarme
        self.parent.flag_alarms = True
        self.timer_dropOut.start(400)                       # timer di 400 ms

    '''
        Gestione del pulsante che permette all'amministratore di riprocessare un componente
    '''

    def reprocess(self):
        self.setVisible(False)
        # Registro allarme mostrato a 0, dopo che allarme è accettato
        self.ttModbus.setRegister((OUTPUT_ALARM_SHOWN, 0))
        self.ttModbus.setRegister((OUTPUT_ALARM_RETRY, 1))
        self.timer_dropOut.start(400)                       # timer di 400 ms
        # ripristino la possibilità di visualizzare schermate di allarme
        self.parent.flag_alarms = True

    '''
        Mostra la pagina di login per gli utenti non amministratori
    '''

    def loginMachine(self):
        self.login1.updateData(self.lang_dictionary)

    '''
        Visualizza l'errore e lo inserisce nella tabella di log
    '''

    def setError(self, alarm_id, switch):
        # alarm_id = str(alarm_id)
        # self.alarm_index2 = alarm_index2 # indici di allarmi più specifici
        self.setVisible(True)
        sql = "SELECT alarm_id,title,description_IT,description_EN,description_LANG1,description_LANG2,usergroup_id FROM alarms WHERE alarm_id = %(alarm_id)s"
        value = {'alarm_id': alarm_id}
        alarm, n_row, err = selectMethod(sql, value, logger)
        if err or n_row == 0:
            alarm = [('default', 'default', 'default', 'default', 'default')]
        print("alarm list:", alarm)

        '''sql = "SELECT * FROM specific_alarm_index WHERE alarm_index = %(alarm_index)s"
        value = {'alarm_index': self.alarm_index2}
        alarm_index, n_row, err = selectMethod(sql, value, logger)'''

        for e in alarm:
            self.alarm_id = e[0]
            self.title = e[1]
            self.description_IT = e[2]
            self.description_EN = e[3]
            self.description_LANG1 = e[4]
            self.description_LANG2 = e[5]
            self.usergroup_id = e[6]

        '''for i in alarm_index:
            self.index = i[0]
            self.desc_IT = i[1]
            self.desc_EN = i[2]
            self.desc_LANG1 = i[3]
            self.desc_LANG2 = i[4]'''

        # if self.flag == True:
        pattern = ""
        sql = "SELECT bitmap_id, bitmap_label, label FROM bitmap"
        value = {}
        self.bitmap_pattern, n_row, err = selectMethod(sql, value, logger)
        if len(switch) > 0:
            for e in self.bitmap_pattern:
                if e[0] in switch:
                    if e[2] == "sensor":
                        if e[0] != switch[-1]:  # se ci sono più elementi
                            pattern = pattern + e[1] + "/"
                        else:
                            pattern = pattern + e[1]
                        # print(pattern)
            if "{sensor}" in self.title:
                self.title = self.title.replace("{sensor}", pattern)
            if "{sensor}" in self.description_IT:
                self.description_IT = self.description_IT.replace(
                    "{sensor}", pattern)
            if "{sensor}" in self.description_EN:
                self.description_EN = self.description_EN.replace(
                    "{sensor}", pattern)
            if "{sensor}" in self.description_LANG1:
                self.description_LANG1 = self.description_LANG1.replace(
                    "{sensor}", pattern)
            if "{sensor}" in self.description_LANG2:
                self.description_LANG2 = self.description_LANG2.replace(
                    "{sensor}", pattern)

            # FARE QUI ANALISI DEI CODICI ERRORE
            '''
            try:
                if "{pos}" in self.title:
                    self.title = self.title.replace("{pos}", positioner)
                if "{pos}" in self.description_IT:
                    self.description_IT = self.description_IT.replace("{pos}", positioner)
                if "{pos}" in self.description_EN:
                    self.description_EN = self.description_EN.replace("{pos}", positioner)
            except KeyError as e:
                print(format(e))

            try:
                if "{counter_id}" in self.title:
                    self.title = self.title.replace("{counter_id}", self.counter_id)
                if "{counter_id}" in self.description_IT:
                    self.description_IT = self.description_IT.replace("{counter_id}", self.counter_id)
                if "{counter_id}" in self.description_EN:
                    self.description_EN = self.description_EN.replace("{counter_id}", self.counter_id)
            except KeyError as e:
                print(format(e))
        '''

        # self.desc si riferisce agli indici più specifici di allarme, ad esempio era stato usato per le 21028S, avendo anche il saldatore
        if self.description_language == "description_EN":
            self.description = self.description_EN
            # self.desc = self.desc_EN
        elif self.description_language == "description_IT":
            self.description = self.description_IT
            # self.desc = self.desc_IT
        elif self.description_language == "description_LANG1":
            self.description = self.description_LANG1
            # self.desc = self.desc_LANG1
        elif self.description_language == "description_LANG2":
            self.description = self.description_LANG2
            # self.desc = self.desc_LANG2

        insert_alarmlog_query_method(self.counter_id, alarm_id, self.title, self.description_IT,
                                     self.description_EN, self.description_LANG1, self.description_LANG2, self.user_id, logger)
        self.titleLabel.setText(
            "(Error: " + str(self.alarm_id) + ") " + self.title)
        self.descriptionLabel.setText(self.description)

        ''' ALLARMI SPECIFICI
        if self.alarm_id == 8 or self.alarm_id == 9:
            self.titleLabel.setText("(Error: " + str(self.alarm_id) + ") " + self.title)
            self.descriptionLabel.setText(self.description + "\n" + self.desc)
        else:
            self.titleLabel.setText("(Error: " + str(self.alarm_id) + ") " + self.title)
            self.descriptionLabel.setText(self.description)
        '''
        if self.parent.parent.permission["manualMode"] == 'no' and self.usergroup_id != "OPERATOR":
            self.unlockButton.setVisible(False)
            self.reprocessButton.setVisible(False)
            self.loginButton.setVisible(True)
        else:
            self.unlockButton.setVisible(True)
            self.reprocessButton.setVisible(False)
            self.loginButton.setVisible(False)

        self.repaint()

    '''
        Inserisce nell'apposito campo il valore ricevuto dal lettore
    '''

    def setScancode(self, scancode):
        self.idLineEdit.setText(scancode)

    '''
        Abbassa il bit del registro che indica che l'allarme è stato accettato
    '''

    def dropOut(self):
        self.ttModbus.setRegister((OUTPUT_ALARM_ACCEPTED[0], 0))
        self.ttModbus.setRegister((OUTPUT_ALARM_RETRY, 0))
        self.timer_dropOut.stop()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.alarm_id = ""
        self.title = ""
        self.description_IT = ""
        self.lang_dictionary = {}
        self.timer_dropOut = QtCore.QTimer()
        self.timer_dropOut.timeout.connect(self.dropOut)

        self.setGeometry(0, 0, Style.WIDTH, Style.HEIGHT)
        self.setStyleSheet("QFrame {background-color: rgba(255,255,255,0)}")

        self.panel = QFrame(self)
        self.panel.setGeometry(30, 75, Style.WIDTH-60, Style.HEIGHT-100)
        self.panel.setStyleSheet(
            "QFrame {background-color: rgb(255,0,0); border-radius: 16px}")

        self.alertLabel = QLabel(self.panel)
        self.alertLabel.setGeometry(25, 25, 150, 150)
        if LINUX:
            self.alertLabel.setPixmap(QPixmap(
                IMG_LINUX_PATH+"alert.png").scaled(self.alertLabel.width(), self.alertLabel.height()))
        else:
            self.alertLabel.setPixmap(QPixmap(os.path.join(IMG_WIN_PATH, "alert.png")).scaled(
                self.alertLabel.width(), self.alertLabel.height()))

        self.titleLabel = QLabel("", self.panel)
        self.titleLabel.setGeometry(145, 25, self.panel.width()-170, 150)
        self.titleLabel.setStyleSheet(Style.TITLE2_CENTERED_STYLE)
        self.titleLabel.setText(
            "(Error: " + str(self.alarm_id) + ") " + self.title)
        self.titleLabel.setWordWrap(True)

        self.descriptionLabel = QLabel(self.panel)
        self.descriptionLabel.setGeometry(25, 100, self.panel.width()-50, 400)
        self.descriptionLabel.setStyleSheet(
            "QLabel {background-color: rgb(255,255,0)}")
        self.descriptionLabel.setStyleSheet(Style.SUBTITLE3_CENTERED_STYLE)
        self.descriptionLabel.setWordWrap(True)
        self.descriptionLabel.setText(self.description_IT)

        self.login1 = Login1(self)

        self.unlockButton = QPushButton("", self.panel)
        self.unlockButton.setGeometry(
            self.panel.width()-300, self.panel.height()-140, 275, 120)
        self.unlockButton.setStyleSheet(Style.BUTTONALARM_STYLE)
        self.unlockButton.clicked.connect(self.unlockMachine)

        self.reprocessButton = QPushButton("", self.panel)
        self.reprocessButton.setGeometry(
            self.panel.width()-600, self.panel.height()-140, 275, 120)
        self.reprocessButton.setStyleSheet(Style.BUTTONALARM_STYLE)
        self.reprocessButton.clicked.connect(self.reprocess)
        self.reprocessButton.setVisible(False)

        self.loginButton = QPushButton("LOGIN", self.panel)
        self.loginButton.setGeometry(
            self.panel.width()-300, self.panel.height()-140, 275, 120)
        self.loginButton.setStyleSheet(Style.BUTTONALARM_STYLE)
        self.loginButton.clicked.connect(self.loginMachine)

        self.ttModbus = ModbusWriter()

        self.show()
        self.setVisible(False)

# REV 5.0


class Production(QWidget):
    phase = pyqtSignal(int)

    '''
        Stampa l'etichetta
    '''

    def printLabel(self, datetime):
        side = "RIGHT"
        if side == "LEFT":
            err = printZebraLabel(self.label_buffer, datetime, self.user_id,
                                  self.customer_code_sx, self.serial, self.counter_id)

        elif side == "RIGHT":
            err = printZebraLabel(self.label_buffer, datetime, self.user_id,
                                  self.customer_code_dx, self.serial, self.counter_id)

        if err:
            QMessageBox.critical(
                self, self.lang_dictionary["qmessagebox_error_title"], self.lang_dictionary["qmessagebox_printer_error"])
            self.ttModbus.setRegister((OUTPUT_ALARM_PRINTER_1, 1))
        else:
            self.ttModbus.setRegister((OUTPUT_ALARM_PRINTER_1, 0))

    '''
        Get the HEARTBIT error
    '''

    def getHBError(self, plcError):
        if self.flag_alarms:
            self.alarm.setError(PLC_LOST_ALARM_INDEX, "")
            print("PLC LOST")

    '''
        Dovrebbe non essere più utilizzato
    '''

    def getPlcEmergency(self, plcEmergency):
        if plcEmergency == 1:
            self.emergency.setText(self.lang_dictionary["label_emergency"])
            self.emergency.setStyleSheet(Style.EMERGENCY_NOK)
            self.emergency.setVisible(True)
        elif plcEmergency == 2:
            self.emergency.setText(self.lang_dictionary["label_airpressure"])
            self.emergency.setStyleSheet(Style.AIR_NOK)
            self.emergency.setVisible(True)
        else:
            self.emergency.setVisible(False)

    '''
        Terminate the production phase
    '''

    def stopProduction(self):
        # self.ttModbus.setRegister((OUTPUT_START_PRODUCTION, 1))
        self.stopModbusTimer.set()
        # self.stopTimer.set()
        self.canvas.fill(Qt.transparent)
        self.photo_cover.setPixmap(self.canvas)
        self.tModbus.wait()
        self.phase.emit(PHASE_HOME)

    '''
        Esegue l'update della foto
    '''

    def updatePhoto(self):
        try:
            # C11 C12 C13 O11 PP11 PP12 PM11 PM12 PM13 PM14 PM15 PF11 PF12 PF13
            bitmap = [self.switch_sensor[0], self.switch_sensor[1], self.switch_sensor[2], self.switch_sensor[3],
                      self.switch_sensor[4], self.switch_sensor[5], self.switch_sensor[6], self.switch_sensor[7], self.switch_sensor[8],
                      self.switch_sensor[9], self.switch_sensor[10], self.switch_sensor[11], self.switch_sensor[12]]
            # draw_cover(self.photo_cover, bitmap)
            self.photo_cover.update()
        except IndexError:
            pass

    '''
        Elabora gli INPUT ricevuti da PLC
    '''

    def getPlc(self, modbusDict):
        bitmapDict = {}

        for e in modbusDict:
            temp_bitmap = getBitmap(modbusDict[e])
            bitmapDict.update({e: temp_bitmap})

        yellow_sensora = getBitmap(modbusDict[INPUT_PROD_YELLOWA])
        red_sensora = getBitmap(modbusDict[INPUT_PROD_REDA])
        green_sensora = getBitmap(modbusDict[INPUT_PROD_GREENA])

        start_flag = getBitmap(modbusDict[INPUT_STOP_PROD_BUTTON[0]])
        start_flag = start_flag[0]
        synoptic_index = modbusDict[INPUT_PANEL_PHRASE1]
        bunner_customization = modbusDict[INPUT_CUSTOMIZATION_BANNER]
        self.number_screw = modbusDict[INPUT_NUMER_SCREW_REG]
        # self.screw_label.setText(str(self.number_screw))

        alarm = getBitmap(modbusDict[INPUT_SHOW_ALARM[0]])
        alarm = alarm[0]
        alarm_index = modbusDict[INPUT_ALARM_INDEXES]

        self.switch_sensor = getSemaphoreArray(
            yellow_sensora, red_sensora, green_sensora)

        t = 0
        temp = {}
        for e in self.switch_sensor:
            temp.update({t: e})
            t = t + 1

        if start_flag == 1:
            self.stop_production.setEnabled(False)
        elif start_flag == 0:
            self.stop_production.setEnabled(True)

        try:
            # BANNER trasparente
            if bunner_customization == 0:
                self.photoDescriptionLabel.setText(
                    self.synoptic_strings[synoptic_index])
                self.emergency.setVisible(False)
            # EMERGENZA
            elif bunner_customization == 1:
                self.emergency.setText(self.synoptic_strings[synoptic_index])
                self.emergency.setStyleSheet(Style.RED_BANNER)
                self.emergency.setVisible(True)
            # MANCANZA ARIA
            elif bunner_customization == 2:
                self.emergency.setText(self.synoptic_strings[synoptic_index])
                self.emergency.setStyleSheet(Style.ORANGE_BANNER)
                self.emergency.setVisible(True)
            # BANNER VERDE
            elif bunner_customization == 3:
                self.emergency.setText(self.synoptic_strings[synoptic_index])
                self.emergency.setStyleSheet(Style.GREEN_BANNER)
                self.emergency.setVisible(True)
        except KeyError:
            pass

        # INCREMENTO CONTATORI
        if bitmapDict[INPUT_INCREASE_COUNTER[0]][INPUT_INCREASE_COUNTER[1]] == 0:
            self.flag_counters = True  # abilita la possibilità di incrementare il contatore
        else:  # se in scarico pezzo
            if self.flag_counters:
                self.flag_counters = False
                # se il pezzo GOOD
                if bitmapDict[INPUT_INCREASE_COUNTER_GOOD[0]][INPUT_INCREASE_COUNTER_GOOD[1]]:
                    # AGGIORNAMENTO DEI CONTATORI
                    side = "LEFT"
                    if side == "LEFT":
                        update_counters_psx_query_method(
                            self.psx[0] + 1, self.psx[1], self.psx[2], self.psx[3] + 1, self.counter_id, logger)
                        self.internal_code = self.internal_code_sx
                        self.customer_code = self.customer_code_sx
                        t_prodlog = Thread(target=insert_prodlog_query_method(
                            self.serial, self.counter_id, self.internal_code, self.customer_code, side, 'OK', self.user_id, logger))
                        t_prodlog.start()
                    elif side == "RIGHT":
                        update_counters_pdx_query_method(
                            self.pdx[0] + 1, self.pdx[1], self.pdx[2], self.pdx[3] + 1, self.counter_id, logger)
                        self.internal_code = self.internal_code_dx
                        self.customer_code = self.customer_code_dx
                        t_prodlog = Thread(target=insert_prodlog_query_method(
                            self.serial, self.counter_id, self.internal_code, self.customer_code, side, 'OK', self.user_id, logger))
                        t_prodlog.start()
                    else:
                        QMessageBox.critical(
                            self, self.lang_dictionary["qmessagebox_counter_update_error_title"], self.lang_dictionary["qmessagebox_counter_update_error"])

                # se pezzo BAD
                elif bitmapDict[INPUT_INCREASE_COUNTER_BAD[0]][INPUT_INCREASE_COUNTER_BAD[1]]:
                    # AGGIORNAMENTO DEI CONTATORI
                    side = "LEFT"
                    if side == "LEFT":
                        update_counters_psx_query_method(
                            self.psx[0], self.psx[1] + 1, self.psx[2] + 1, self.psx[3], self.counter_id, logger)
                        self.internal_code = self.internal_code_sx
                        self.customer_code = self.customer_code_sx
                        t_prodlog = Thread(target=insert_prodlog_query_method(
                            "0000000", self.counter_id, self.internal_code, self.customer_code, side, 'NOK', self.user_id, logger))
                        t_prodlog.start()
                    elif side == "RIGHT":
                        update_counters_pdx_query_method(
                            self.pdx[0], self.pdx[1] + 1, self.pdx[2] + 1, self.pdx[3], self.counter_id, logger)
                        self.internal_code = self.internal_code_dx
                        self.customer_code = self.customer_code_dx
                        t_prodlog = Thread(target=insert_prodlog_query_method(
                            "0000000", self.counter_id, self.internal_code, self.customer_code, side, 'NOK', self.user_id, logger))
                        t_prodlog.start()
                    else:
                        QMessageBox.critical(
                            self, self.lang_dictionary["qmessagebox_counter_update_error_title"], self.lang_dictionary["qmessagebox_counter_update_error"])
                self.updateCounters()

        # STAMPO ETICHETTA CON DEVICE 1 E CONFERMO LA STAMPA
        if bitmapDict[INPUT_PRINT_LABEL1[0]][INPUT_PRINT_LABEL1[1]] == 1 and self.enable_printer == 1 and not self.flag_printer:
            self.printLabel(getCurrentDateTimePrinter())
            self.ttModbus.setRegister((OUTPUT_PRINT_LABEL1_ACK, 1))
            self.flag_printer = True

        # RIPORTO IL BIT DI CONFERMA A 0 QUANDO IL PLC MI RIPORTA A 0 IL BIT DI STAMPA
        if bitmapDict[INPUT_PRINT_LABEL1[0]][INPUT_PRINT_LABEL1[1]] == 0 and self.enable_printer == 1 and self.flag_printer:
            self.ttModbus.setRegister((OUTPUT_PRINT_LABEL1_ACK, 0))
            self.flag_printer = False

        # GESTIRE GLI ALLARMI e i LOG di ALLARMI
        if alarm == 1:
            if self.flag_alarms:
                # impedisce che vengano mostrati continuamente allarmi
                self.flag_alarms = False
                temp_switch = []
                n = 0
                for e in self.switch_sensor:  # per ogni elemento nella bitmap
                    if e == 1:  # se quell'elemento è uguale a 1
                        temp_switch.append(n)  # appendo l'indice dell'elemento
                    n = n + 1
                self.alarm.setError(alarm_index, temp_switch)
                # Registro allarme mostrato a 1
                self.ttModbus.setRegister((OUTPUT_ALARM_SHOWN, 1))

    '''
        Incremento dei contatori
    '''

    def updateCounters(self):
        self.counter_id = self.parent.counter_id
        self.psx = ()
        self.pdx = ()
        sql = "SELECT partialPSX, partialrefusePSX, totalrefusePSX, totalPSX FROM counters WHERE counter_id=%(counter_id)s"
        value = {'counter_id': self.counter_id}
        records, n_row, err = selectMethod(sql, value, logger)
        self.totalGoodpsx = records[0][3]
        self.totalRefusepsx = records[0][2]
        for sx in records:
            self.psx = self.psx + sx
        # for self.psx in records:
            # print("PSX:",self.psx)

        sql = "SELECT partialPDX, partialrefusePDX, totalrefusePDX, totalPDX FROM counters WHERE counter_id=%(counter_id)s"
        value = {'counter_id': self.counter_id}
        records, n_row, err = selectMethod(sql, value, logger)
        self.totalGoodpdx = records[0][3]
        self.totalRefusepdx = records[0][2]
        for dx in records:
            self.pdx = self.pdx + dx
        # for self.pdx in records:
            # print("PDX:",self.pdx)

        self.totalGood = self.totalGoodpsx + self.totalGoodpdx
        self.totalRefuse = self.totalRefusepsx + self.totalRefusepdx

        '''
        sql = "SELECT value FROM configuration WHERE configuration_id = %s"
        err, res = new_select_query_method(sql, ("totalGood",))
        self.totalGood = res[0][0]

        sql = "SELECT value FROM configuration WHERE configuration_id = %s"
        err, res = new_select_query_method(sql, ("totalRefuse",))
        self.totalRefuse = res[0][0]
        '''

        sql = "SELECT serial FROM prod_log ORDER by serial DESC LIMIT 1"
        value = {}
        records, n_row, err = selectMethod(sql, value, logger)
        if err == True or n_row == 0:
            self.serial = "0000001"
        else:
            self.serial = int(records[0][0]) + 1
            temp = ""
            for i in range(7-len(str(self.serial))):
                temp = temp + "0"
            self.serial = temp + str(self.serial)

        # self.partial_box.setText(str(int(self.psx[0]) + int(self.psx[1]) + int(self.pdx[0]) + int(self.pdx[1])))
        # self.total_box.setText(str(self.totalGood + self.totalRefuse))
        # self.total_boxSX.setText(str(self.totalGood + self.totalRefuse))
        # self.total_boxDX.setText(str(self.totalGood + self.totalRefuse))
        # self.totalGood_boxSX.setText(str(int(self.psx[3])))
        # self.totalRefuse_boxSX.setText(str(int(self.psx[2])))
        # self.totalGood_boxDX.setText(str(int(self.pdx[3])))
        # self.totalRefuse_boxDX.setText(str(int(self.pdx[2])))

    '''
        Esegue l'updateData della classe Production
    '''

    def updateData(self, lang_dictionary, description_language, synoptic_strings, user_id, counter_id, phase, printer_enabled):
        self.counter_id = counter_id
        self.enable_printer = printer_enabled
        self.user_id = user_id
        self.internal_code_sx = ""
        self.customer_code_sx = ""
        self.internal_code_dx = ""
        self.customer_code_dx = ""

        self.updateCounters()

        sql = "SELECT counter_num, internal_code_sx, customer_code_sx, counter_photo_sx, counter_photo_dx, internal_code_dx, customer_code_dx FROM counters WHERE counter_id = %(counter_id)s"
        value = {'counter_id': self.counter_id}
        records, n_row, err = selectMethod(sql, value, logger)

        if not err:
            self.counter_num = int(records[0][0])
            self.internal_code_sx = records[0][1]
            self.customer_code_sx = records[0][2]
            if LINUX:
                self.photo_sx = IMG_LINUX_PATH+records[0][3]
                self.photo_dx = IMG_LINUX_PATH+records[0][4]
            else:
                self.photo_sx = os.path.join(IMG_WIN_PATH, records[0][3])
                self.photo_dx = os.path.join(IMG_WIN_PATH, records[0][4])
            self.internal_code_dx = records[0][5]
            self.customer_code_dx = records[0][6]

        self.photoLabel.setPixmap(QPixmap(self.photo_sx).scaled(
            self.photoLabel.width(), self.photoLabel.height()))

        '''
        if self.counter_num != 1 and self.counter_num != 2 and self.counter_num != 3:
            self.central_rect.setVisible(False)
        else:
            self.central_rect.setVisible(True)
        '''

        self.counterid_label.setText(self.counter_id)
        # self.internalcode_box_sx.setText(self.internal_code_sx)
        # self.internalcode_box_dx.setText(self.internal_code_dx)
        self.lang_dictionary = {}
        self.synoptic_strings = {}
        self.description_language = description_language
        self.alarm.updateData(
            lang_dictionary, description_language, user_id, counter_id)

        for e in lang_dictionary:
            if e[1] == phase:
                self.lang_dictionary.update({e[0]: e[2]})

        for e in synoptic_strings:
            self.synoptic_strings.update({int(e[0]): e[1]})

        self.stop_production.setText(
            self.lang_dictionary["button_stopproduction"])
        self.title.setText(self.lang_dictionary["label_title"])
        # self.title_screw.setText(self.lang_dictionary["label_screw"])

        # self.stopTimer.clear()
        # self.timer.start()
        self.stopModbusTimer.clear()
        self.tModbus.start()

    def __init__(self, parent):
        super(Production, self).__init__(parent)

        self.parent = parent

        self.lang_dictionary = {}
        self.switch_sensor = []

        self.photo_sx = ""
        self.photo_dx = ""
        self.dest_photo_sx = ""
        self.dest_photo_dx = ""

        self.serial = 0                 # progressivo log
        self.totalGood = 0
        self.totalRefuse = 0
        self.counter_id = ""
        self.counter_num = 0
        self.number_screw = 0
        self.internal_code_sx = ""
        self.customer_code_sx = ""
        self.internal_code = ""
        self.customer_code = ""
        # per evitare i duplicati nei contatori. DIVENTERA' OBSOLETO CON LA NUOVA GESTIONE
        self.flag_counters = True
        # per evitare loop schermate allarme che impallano il sistema
        self.flag_alarms = True
        self.enable_printer = 0
        self.label_buffer = ""
        self.flag_printer = False
        try:
            if LINUX:
                with open(LABEL_LINUX_PATH, "r") as file:
                    for line in file:
                        self.label_buffer = self.label_buffer + line
            else:
                with open(LABEL_WIN_PATH, "r") as file:
                    for line in file:
                        self.label_buffer = self.label_buffer + line
        except Exception:
            pass
        except OSError as ose:
            pass

        self.title = QLabel("", self)
        self.title.setGeometry(50, 75, 550, 50)
        self.title.setStyleSheet(Style.TITLE3_CENTERED_STYLE)
        self.counterid_label = QLabel("", self)
        self.counterid_label.setGeometry(580, 75, 350, 50)
        self.counterid_label.setStyleSheet(Style.BODY5_CENTERED_STYLE)
        # self.counterid_label.setStyleSheet("QLabel {background-color: rgb(0,0,0)}")

        '''self.title_screw = QLabel("", self)
        self.title_screw.setGeometry(260,175,100,50)
        self.title_screw.setStyleSheet(Style.TITLE6_CENTERED_STYLE)
        self.screw_label = QLabel("", self)
        self.screw_label.setGeometry(380,175,50,50)
        self.screw_label.setStyleSheet(Style.BODY5_CENTERED_STYLE)'''

        self.photoLabel = QLabel("", self)
        self.photoLabel.setGeometry(
            int((Style.WIDTH-COVER_WIDTH)/2), 135, COVER_WIDTH, COVER_HEIGHT)
        self.photoLabel.setVisible(True)

        self.photo_cover = QLabel("", self)
        self.photo_cover.setGeometry(
            int((Style.WIDTH-COVER_WIDTH)/2), 135, COVER_WIDTH, COVER_HEIGHT)
        self.photo_cover.setVisible(True)
        self.canvas = QPixmap(COVER_WIDTH, COVER_HEIGHT)
        self.canvas.fill(Qt.transparent)
        self.photo_cover.setPixmap(self.canvas)

        self.photoDescriptionLabel = QLabel("", self)
        # self.photoDescriptionLabel.setWordWrap(True)
        self.photoDescriptionLabel.setGeometry(50, 640, 550, 100)
        self.photoDescriptionLabel.setStyleSheet(
            Style.SUBTITLE4_CENTERED_STYLE)
        self.photoDescriptionLabel.setVisible(True)

        # self.stopTimer = Event()
        # self.timer = ClientTimer(self.stopTimer, 0.5)
        # self.timer.signal.connect(self.updatePhoto)

        self.emergency = QLabel("", self)
        self.emergency.setWordWrap(True)
        self.emergency.setGeometry(20, Style.HEIGHT-110, 700, 100)
        self.emergency.setVisible(False)

        self.stop_production = QPushButton("", self)
        self.stop_production.setGeometry(725, Style.HEIGHT-110, 280, 100)
        self.stop_production.setStyleSheet(Style.BUTTONMENU_STYLE)
        self.stop_production.clicked.connect(self.stopProduction)

        self.stopModbusTimer = Event()
        self.tModbus = ModbusReader(self.stopModbusTimer, MODBUS_TIMER)
        self.tModbus.setRegisters(PRODUCTION_REGISTERS)
        self.tModbus.modbusSignal.connect(self.getPlc)
        self.tModbus.heartbitSignal.connect(self.getHBError)
        # self.tModbus.emergencySignal.connect(self.getPlcEmergency)

        self.ttModbus = ModbusWriter()

        self.alarm = Alarm(self)

# REV 4.0


class Manual(QWidget):
    phase = pyqtSignal(int)

    def updateData(self, lang_dictionary, phase, user_id):
        self.tModbus.setRegisters(MANUAL_REGISTERS)
        self.stopModbusTimer.clear()
        self.tModbus.start()

        # Usato come flag per mostrare una sola volta l'allarme di PLC perso
        self.flag = True

        self.lang_dictionary = {}

        for e in lang_dictionary:
            if e[1] == phase:
                self.lang_dictionary.update({e[0]: e[2]})
        # self.change_frame(0)

        self.user_id = user_id
        self.stopTimer.clear()
        # self.timer.start()         non ricordo per cosa viene utilizzato
        self.title.setText(self.lang_dictionary["label_title"])

        self.sensor["b00"].label.setText(
            "B00 : "+self.lang_dictionary["label_riposo"])
        self.sensor["b2"].label.setText(
            "B2 : "+self.lang_dictionary["label_riposo"])
        self.sensor["b3"].label.setText(
            "B3 : "+self.lang_dictionary["label_riposo"])
        self.sensor["b4"].label.setText(
            "B4 : "+self.lang_dictionary["label_riposo"])
        self.sensor["b22"].label.setText(
            "B22 : "+self.lang_dictionary["label_riposo"])
        self.sensor["b33"].label.setText(
            "B33 : "+self.lang_dictionary["label_riposo"])
        self.sensor["b44"].label.setText(
            "B44 : "+self.lang_dictionary["label_riposo"])
        self.sensor["b00_p"].label.setText(
            "B00 : "+self.lang_dictionary["label_bu"])
        self.sensor["b1sx_p"].label.setText(
            "B1"+self.lang_dictionary["label_side_sx"]+" : "+self.lang_dictionary["label_bu"])
        self.sensor["b2_p"].label.setText(
            "B2 : "+self.lang_dictionary["label_bu"])
        self.sensor["b3_p"].label.setText(
            "B3 : "+self.lang_dictionary["label_bu"])
        self.sensor["b4_p"].label.setText(
            "B4 : "+self.lang_dictionary["label_bu"])
        self.sensor["b1dx_p"].label.setText(
            "B1"+self.lang_dictionary["label_side_dx"]+" : "+self.lang_dictionary["label_bu"])
        self.sensor["b22_p"].label.setText(
            "B22 : "+self.lang_dictionary["label_bu"])
        self.sensor["b33_p"].label.setText(
            "B33 : "+self.lang_dictionary["label_bu"])
        self.sensor["b44_p"].label.setText(
            "B44 : "+self.lang_dictionary["label_bu"])
        self.sensor["pp1"].label.setText(
            "PP1 : "+self.lang_dictionary["label_pp"])
        self.sensor["pp2"].label.setText(
            "PP2 : "+self.lang_dictionary["label_pp"])
        self.sensor["avv_e"].label.setText(
            self.lang_dictionary["label_screwdriver_error"])
        self.sensor["avv_vok"].label.setText(
            self.lang_dictionary["label_screwingok"])
        self.sensor["airpressure"].label.setText(
            self.lang_dictionary["airpressure"])

        self.valve["b1sx"].valv.setText(
            self.lang_dictionary["button_ins"] + " B1 \n"+self.lang_dictionary["label_side_sx"])
        self.valve["b1dx"].valv.setText(
            self.lang_dictionary["button_ins"] + " B1 \n"+self.lang_dictionary["label_side_dx"])
        self.valve["insertion"].valv.setText(
            self.lang_dictionary["button_ins"] + " \nB00 - B44")
        self.valve["slitta"].valv.setText(self.lang_dictionary["button_slide"])
        self.valve["ogg"].valv.setText(self.lang_dictionary["button_oc"])
        self.valve["motor"].valv.setText(
            self.lang_dictionary["valv_screwdriver"])
        self.valve["b1sx"].label.setText(
            "B1"+self.lang_dictionary["label_side_sx"]+" : "+self.lang_dictionary["label_riposo"])
        self.valve["b1dx"].label.setText(
            "B1"+self.lang_dictionary["label_side_dx"]+" : "+self.lang_dictionary["label_riposo"])
        self.valve["insertion"].led.setVisible(False)
        self.valve["ogg"].label.setText(self.lang_dictionary["label_lavoro"])
        self.valve["motor"].label.setText(
            self.lang_dictionary["label_screwdriver_motor"])
        self.valve["slitta"].home_label.setText(
            self.lang_dictionary["label_riposo"])
        self.valve["slitta"].end_label.setText(
            self.lang_dictionary["label_lavoro"])

    def getPlcEmergency(self, plcEmergency):
        if plcEmergency > 0:
            '''if plcEmergency == 1:
                QMessageBox.information(self, self.lang_dictionary["qmessagebox_info_emergency_title"], self.lang_dictionary["qmessagebox_info_emergency"])
            else:
                QMessageBox.information(self, self.lang_dictionary["qmessagebox_info_emergency_title"], self.lang_dictionary["qmessagebox_info_emergency"])'''
            if self.valve["b1sx"].valv.isChecked():
                self.valve["b1sx"].valv.toggle()
                self.writeOutputRegisters(
                    self.valve["b1sx"].valv, self.valve["b1sx"].register, self.valve["b1sx"].bit)
            if self.valve["b1dx"].valv.isChecked():
                self.valve["b1dx"].valv.toggle()
                self.writeOutputRegisters(
                    self.valve["b1dx"].valv, self.valve["b1dx"].register, self.valve["b1dx"].bit)
            if self.valve["insertion"].valv.isChecked():
                self.valve["insertion"].valv.toggle()
                self.writeOutputRegisters(
                    self.valve["insertion"].valv, self.valve["insertion"].register, self.valve["insertion"].bit)
            if self.valve["slitta"].valv.isChecked():
                self.valve["slitta"].valv.toggle()
                self.writeOutputRegisters(
                    self.valve["slitta"].valv, self.valve["slitta"].register, self.valve["slitta"].bit)
            if self.valve["ogg"].valv.isChecked():
                self.valve["ogg"].valv.toggle()
                self.writeOutputRegisters(
                    self.valve["ogg"].valv, self.valve["ogg"].register, self.valve["ogg"].bit)
            if self.valve["motor"].valv.isChecked():
                self.valve["motor"].valv.toggle()
                self.writeOutputRegisters(
                    self.valve["motor"].valv, self.valve["motor"].register, self.valve["motor"].bit)

    def getHBError(self, heartbitSignal):
        if LINUX and self.flag:
            self.flag = False
            QMessageBox.critical(
                self, self.lang_dictionary["qmessagebox_error_title"], self.lang_dictionary["qmessagebox_error_plclost"])
            # self.changePhase(PHASE_HOME)
        # else:
        #    print("PLC LOST")

    def getPlc(self, modbusDict):
        bitmapDict = {}

        for e in modbusDict:
            temp_bitmap = getBitmap(modbusDict[e])
            bitmapDict.update({e: temp_bitmap})

        self.outputDict.update({"150": bitmapDict["150"]})

        self.bitmap = bitmapDict["200"] + bitmapDict["201"] + bitmapDict["250"]

        self.sensor["b00"].led.setValue(
            LED_STATUS[bitmapDict[INPUT_MAN_B00_END[0]][INPUT_MAN_B00_END[1]]])
        self.sensor["b2"].led.setValue(
            LED_STATUS[bitmapDict[INPUT_MAN_B2_END[0]][INPUT_MAN_B2_END[1]]])
        self.sensor["b3"].led.setValue(
            LED_STATUS[bitmapDict[INPUT_MAN_B3_END[0]][INPUT_MAN_B3_END[1]]])
        self.sensor["b4"].led.setValue(
            LED_STATUS[bitmapDict[INPUT_MAN_B4_END[0]][INPUT_MAN_B4_END[1]]])
        self.sensor["b22"].led.setValue(
            LED_STATUS[bitmapDict[INPUT_MAN_B22_END[0]][INPUT_MAN_B22_END[1]]])
        self.sensor["b33"].led.setValue(
            LED_STATUS[bitmapDict[INPUT_MAN_B33_END[0]][INPUT_MAN_B33_END[1]]])
        self.sensor["b44"].led.setValue(
            LED_STATUS[bitmapDict[INPUT_MAN_B44_END[0]][INPUT_MAN_B44_END[1]]])
        self.sensor["b00_p"].led.setValue(
            LED_STATUS[bitmapDict[INPUT_MAN_B00_PRES[0]][INPUT_MAN_B00_PRES[1]]])
        self.sensor["b1sx_p"].led.setValue(
            LED_STATUS[bitmapDict[INPUT_MAN_B1SX_PRES[0]][INPUT_MAN_B1SX_PRES[1]]])
        self.sensor["b2_p"].led.setValue(
            LED_STATUS[bitmapDict[INPUT_MAN_B2_PRES[0]][INPUT_MAN_B2_PRES[1]]])
        self.sensor["b3_p"].led.setValue(
            LED_STATUS[bitmapDict[INPUT_MAN_B3_PRES[0]][INPUT_MAN_B3_PRES[1]]])
        self.sensor["b4_p"].led.setValue(
            LED_STATUS[bitmapDict[INPUT_MAN_B4_PRES[0]][INPUT_MAN_B4_PRES[1]]])
        self.sensor["b1dx_p"].led.setValue(
            LED_STATUS[bitmapDict[INPUT_MAN_B1DX_PRES[0]][INPUT_MAN_B1DX_PRES[1]]])
        self.sensor["b22_p"].led.setValue(
            LED_STATUS[bitmapDict[INPUT_MAN_B22_PRES[0]][INPUT_MAN_B22_PRES[1]]])
        self.sensor["b33_p"].led.setValue(
            LED_STATUS[bitmapDict[INPUT_MAN_B33_PRES[0]][INPUT_MAN_B33_PRES[1]]])
        self.sensor["b44_p"].led.setValue(
            LED_STATUS[bitmapDict[INPUT_MAN_B44_PRES[0]][INPUT_MAN_B44_PRES[1]]])
        self.sensor["pp1"].led.setValue(
            LED_STATUS[bitmapDict[INPUT_MAN_PP1[0]][INPUT_MAN_PP1[1]]])
        self.sensor["pp2"].led.setValue(
            LED_STATUS[bitmapDict[INPUT_MAN_PP2[0]][INPUT_MAN_PP2[1]]])
        self.sensor["avv_e"].led.setValue(
            LED_STATUS[bitmapDict[INPUT_MAN_ERR_AV[0]][INPUT_MAN_ERR_AV[1]]])
        self.sensor["avv_vok"].led.setValue(
            LED_STATUS[bitmapDict[INPUT_MAN_OK_AV[0]][INPUT_MAN_OK_AV[1]]])

        self.valve["b1sx"].led.setValue(
            LED_STATUS[bitmapDict[INPUT_MAN_B1SX_END[0]][INPUT_MAN_B1SX_END[1]]])
        self.valve["b1dx"].led.setValue(
            LED_STATUS[bitmapDict[INPUT_MAN_B1DX_END[0]][INPUT_MAN_B1DX_END[1]]])
        self.valve["slitta"].end_led.setValue(
            LED_STATUS[bitmapDict[INPUT_MAN_S_END[0]][INPUT_MAN_S_END[1]]])
        self.valve["slitta"].home_led.setValue(
            LED_STATUS[bitmapDict[INPUT_MAN_S_HOME[0]][INPUT_MAN_S_HOME[1]]])
        self.valve["ogg"].led.setValue(
            LED_STATUS[bitmapDict[INPUT_MAN_OGG_END[0]][INPUT_MAN_OGG_END[1]]])
        self.valve["motor"].led.setValue(
            LED_STATUS[bitmapDict[INPUT_MAN_ONOFF_AV[0]][INPUT_MAN_ONOFF_AV[1]]])

        try:
            self.sensor["airpressure"].led.setOnColour(
                LED_COLOUR[modbusDict[INPUT_MAN_AIRPRESSURE]])
            self.sensor["airpressure"].led.setValue(
                LED_STATUS[modbusDict[INPUT_MAN_AIRPRESSURE]])
        except KeyError as ke:
            pass
        except Exception:
            pass

    '''
    def updatePhoto(self):
        try:
            print(self.bitmap)
            draw_cover_manual(self.photo_cover, self.bitmap)
            self.photo_cover.update()
        except IndexError:
            pass
    '''

    def changePhase(self, n):
        something_checked = False

        if self.valve["b1sx"].valv.isChecked():
            something_checked = True
        if self.valve["b1dx"].valv.isChecked():
            something_checked = True
        if self.valve["insertion"].valv.isChecked():
            something_checked = True
        if self.valve["slitta"].valv.isChecked():
            something_checked = True
        if self.valve["ogg"].valv.isChecked():
            something_checked = True
        if self.valve["motor"].valv.isChecked():
            something_checked = True

        if something_checked:
            QMessageBox.critical(
                self, self.lang_dictionary["qmessagebox_error_title"], self.lang_dictionary["qmessagebox_error_exit"])
        else:
            self.stopModbusTimer.set()
            self.tModbus.start()
            self.tModbus.wait()
            self.phase.emit(n)

    def change_frame(self, n):
        self.page_counter = self.page_counter + n
        if self.page_counter == 0:
            try:
                self.stopTimer.clear()
                # self.timer.start()
            except RuntimeError:
                pass
            self.frame_1.setVisible(False)
            # self.frame_2.setVisible(False)
            self.frame_0.setVisible(True)
            self.buttonBack.setEnabled(False)
            self.buttonFor.setEnabled(True)
        elif self.page_counter == 1:
            self.stopTimer.set()
            self.frame_0.setVisible(False)
            # self.frame_2.setVisible(False)
            self.frame_1.setVisible(True)
            self.buttonFor.setEnabled(False)
            self.buttonBack.setEnabled(True)
        '''elif self.page_counter == 2:
            self.stopTimer.set()
            self.frame_0.setVisible(False)
            self.frame_1.setVisible(False)
            self.frame_2.setVisible(True)
            self.buttonFor.setEnabled(False)
            self.buttonBack.setEnabled(True)'''

    '''
    def paintEvent(self, event):
        self.painter = QPainter(self)
        self.painter.begin(self)
        self.painter.setPen(QPen(Qt.white, 2, Qt.SolidLine))
        self.painter.drawLine(Style.WIDTH/2,135,Style.WIDTH/2,680) #first vertical
        self.painter.end()
    '''

    def writeOutputRegisters(self, button, register, bit, timed):
        temp_value = 0
        if timed:
            self.timer.start(200)
            self.outputDict[register][bit] = 1
            self.registerTimed = register
            self.bitTimed = bit
        elif button.isChecked():
            self.outputDict[register][bit] = 1
        else:
            self.outputDict[register][bit] = 0

        for i in range(15, -1, -1):
            if self.outputDict[register][i] == 1:
                temp_value = temp_value + pow(2, i)

        self.ttModbus.setRegister((int(register), temp_value))

    def timeout_valve(self):
        temp_value = 0
        self.timer.stop()
        self.outputDict[self.registerTimed][self.bitTimed] = 0
        for i in range(15, -1, -1):
            if self.outputDict[self.registerTimed][i] == 1:
                temp_value = temp_value + pow(2, i)

        self.ttModbus.setRegister((int(self.registerTimed), temp_value))

    def __init__(self, parent):
        super(Manual, self).__init__(parent)

        self.lang_dictionary = {}
        self.parent = parent
        self.page_counter = 0
        self.bitmap = []

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timeout_valve)
        self.registerTimed = {}
        self.bitTimed = {}

        self.ttModbus = ModbusWriter()
        self.outputDict = {}
        self.title = QLabel("", self)
        self.title.setGeometry(0, 20, Style.WIDTH, 50)
        self.title.setStyleSheet(Style.TITLE2_CENTERED_STYLE)

        self.frame_0 = QFrame(self)
        self.frame_0.setGeometry(0, 75, Style.WIDTH, Style.HEIGHT)
        self.frame_gsx_0 = QFrame(self.frame_0)
        self.frame_gsx_0.setGeometry(
            0, 0, int(Style.WIDTH/2), self.frame_0.height())
        self.frame_gdx_0 = QFrame(self.frame_0)
        self.frame_gdx_0.setGeometry(
            int(Style.WIDTH/2), 0, int(Style.WIDTH/2), int(self.frame_0.height()))

        self.frame_1 = QFrame(self)
        self.frame_1.setGeometry(0, 75, Style.WIDTH, Style.HEIGHT)
        self.frame_gsx_1 = QFrame(self.frame_1)
        self.frame_gsx_1.setGeometry(
            0, 0, int(Style.WIDTH/2), int(self.frame_1.height()))
        self.frame_gdx_1 = QFrame(self.frame_1)
        self.frame_gdx_1.setGeometry(
            int(Style.WIDTH/2), 0, int(Style.WIDTH/2), int(self.frame_1.height()))
        self.frame_1.setVisible(False)

        '''
        self.frame_0 = QFrame(self)
        self.frame_0.setGeometry(0,75,Style.WIDTH,560)
        self.frame_gsx_0 = QFrame(self.frame_0)
        self.frame_gsx_0.setGeometry(0,0,Style.WIDTH/3,self.frame_0.height())
        self.frame_center_0 = QFrame(self.frame_0)
        self.frame_center_0.setGeometry(Style.WIDTH/3,0,Style.WIDTH/3,self.frame_0.height())
        self.frame_gdx_0 = QFrame(self.frame_0)
        self.frame_gdx_0.setGeometry(Style.WIDTH/3*2,0,Style.WIDTH/3,self.frame_0.height())
        '''

        '''
        self.frame_2 = QFrame(self)
        self.frame_2.setGeometry(0,75,Style.WIDTH,560)
        self.frame_gsx_2 = QFrame(self.frame_2)
        self.frame_gsx_2.setGeometry(0,0,Style.WIDTH/3,self.frame_2.height())
        self.frame_center_2 = QFrame(self.frame_2)
        self.frame_center_2.setGeometry(Style.WIDTH/3,0,Style.WIDTH/3,self.frame_2.height())
        self.frame_gdx_2 = QFrame(self.frame_2)
        self.frame_gdx_2.setGeometry(Style.WIDTH/3*2,0,Style.WIDTH/3,self.frame_2.height())
        '''

        self.sensor = {
            "b00": PresenceSensor(self.frame_gsx_0, "", 20, 0),
            "b2": PresenceSensor(self.frame_gsx_0, "", 20, 1),
            "b3": PresenceSensor(self.frame_gsx_0, "", 20, 2),
            "b4": PresenceSensor(self.frame_gsx_0, "", 20, 3),
            "b22": PresenceSensor(self.frame_gsx_0, "", 20, 4),
            "b33": PresenceSensor(self.frame_gsx_0, "", 20, 5),
            "b44": PresenceSensor(self.frame_gsx_0, "", 20, 6),
            "b00_p": PresenceSensor(self.frame_gdx_1, "", 20, 0),
            "b1sx_p": PresenceSensor(self.frame_gdx_1, "", 20, 1),
            "b2_p": PresenceSensor(self.frame_gdx_1, "", 20, 2),
            "b3_p": PresenceSensor(self.frame_gdx_1, "", 20, 3),
            "b4_p": PresenceSensor(self.frame_gdx_1, "", 20, 4),
            "b1dx_p": PresenceSensor(self.frame_gdx_1, "", 20, 5),
            "b22_p": PresenceSensor(self.frame_gdx_1, "", 20, 6),
            "b33_p": PresenceSensor(self.frame_gdx_1, "", 20, 7),
            "b44_p": PresenceSensor(self.frame_gdx_1, "", 20, 8),
            "airpressure": PresenceSensor(self.frame_gsx_1, "", 20, 0),
            "pp1": PresenceSensor(self.frame_gsx_1, "", 20, 1),
            "pp2": PresenceSensor(self.frame_gsx_1, "", 20, 2),
            "avv_e": PresenceSensor(self.frame_gsx_1, "", 20, 5),
            "avv_vok": PresenceSensor(self.frame_gsx_1, "", 20, 6)

        }

        self.valve = {
            "b1sx": SingleValveControl(self.frame_gdx_0, "", "", 10, 0, self.ttModbus, OUTPUT_MAN_VALV_B1SX[0], OUTPUT_MAN_VALV_B1SX[1]),
            "b1dx": SingleValveControl(self.frame_gdx_0, "", "", 10, 110, self.ttModbus, OUTPUT_MAN_VALV_B1DX[0], OUTPUT_MAN_VALV_B1DX[1]),
            "insertion": SingleValveControl(self.frame_gsx_0, "", "", 10, 265, self.ttModbus, OUTPUT_MAN_VALV_B00_B44[0], OUTPUT_MAN_VALV_B00_B44[1]),
            "slitta": ValveControl(self.frame_gdx_0, "", "", "", 10, 220, self.ttModbus, OUTPUT_MAN_S[0], OUTPUT_MAN_S[1]),
            "ogg": SingleValveControl(self.frame_gdx_0, "", "", 10, 330, self.ttModbus, OUTPUT_MAN_OGG[0], OUTPUT_MAN_OGG[1]),
            "motor": SingleValveControlRedGreen(self.frame_gsx_1, "", "", 10, 265, self.ttModbus, OUTPUT_MAN_STOP_MOTOR[0], OUTPUT_MAN_STOP_MOTOR[1]),
        }

        self.valve["b1sx"].valv.clicked.connect(lambda: self.writeOutputRegisters(
            self.valve["b1sx"].valv, self.valve["b1sx"].register, self.valve["b1sx"].bit, False))
        self.valve["b1dx"].valv.clicked.connect(lambda: self.writeOutputRegisters(
            self.valve["b1dx"].valv, self.valve["b1dx"].register, self.valve["b1dx"].bit, False))
        self.valve["insertion"].valv.clicked.connect(lambda: self.writeOutputRegisters(
            self.valve["insertion"].valv, self.valve["insertion"].register, self.valve["insertion"].bit, False))
        self.valve["slitta"].valv.clicked.connect(lambda: self.writeOutputRegisters(
            self.valve["slitta"].valv, self.valve["slitta"].register, self.valve["slitta"].bit, False))
        self.valve["ogg"].valv.clicked.connect(lambda: self.writeOutputRegisters(
            self.valve["ogg"].valv, self.valve["ogg"].register, self.valve["ogg"].bit, False))
        self.valve["motor"].valv.clicked.connect(lambda: self.writeOutputRegisters(
            self.valve["motor"].valv, self.valve["motor"].register, self.valve["motor"].bit, False))

        self.stopTimer = Event()
        # self.timer = ClientTimer(self.stopTimer, 1.0)
        # self.timer.signal.connect(self.updatePhoto)

        self.stopModbusTimer = Event()
        self.tModbus = ModbusReader(self.stopModbusTimer, MODBUS_TIMER)
        self.tModbus.modbusSignal.connect(self.getPlc)
        self.tModbus.heartbitSignal.connect(self.getHBError)
        # self.tModbus.emergencySignal.connect(self.getPlcEmergency)

        self.buttonBack = QPushButton(self)
        self.buttonBack.setGeometry(int(Style.BUTTONBAR_X * 2 + Style.BUTTONBAR_WIDTH),
                                    Style.BUTTONBAR_Y, Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT)
        self.buttonBack.setStyleSheet(Style.BUTTONBAR_STYLE)
        if LINUX:
            self.buttonBack.setIcon(QIcon(IMG_LINUX_PATH+"back.png"))
        else:
            self.buttonBack.setIcon(
                QIcon(os.path.join(IMG_WIN_PATH, "back.png")))
        self.buttonBack.setIconSize(
            QSize(int(Style.BUTTONBAR_WIDTH - 20), int(Style.BUTTONBAR_HEIGHT - 20)))
        self.buttonBack.clicked.connect(lambda: self.change_frame(-1))
        self.buttonBack.setEnabled(False)
        self.buttonBack.setVisible(True)

        self.buttonFor = QPushButton(self)
        self.buttonFor.setGeometry(int(Style.BUTTONBAR_X * 3 + Style.BUTTONBAR_WIDTH * 2),
                                   Style.BUTTONBAR_Y, Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT)
        self.buttonFor.setStyleSheet(Style.BUTTONBAR_STYLE)
        if LINUX:
            self.buttonFor.setIcon(QIcon(IMG_LINUX_PATH+"for.png"))
        else:
            self.buttonFor.setIcon(
                QIcon(os.path.join(IMG_WIN_PATH, "for.png")))
        self.buttonFor.setIconSize(
            QSize(int(Style.BUTTONBAR_WIDTH - 20), int(Style.BUTTONBAR_HEIGHT - 20)))
        self.buttonFor.clicked.connect(lambda: self.change_frame(+1))
        self.buttonFor.setVisible(True)

        self.buttonHome = QPushButton(self)
        self.buttonHome.setGeometry(int(Style.BUTTONBAR_X), int(
            Style.BUTTONBAR_Y), int(Style.BUTTONBAR_WIDTH), int(Style.BUTTONBAR_HEIGHT))
        self.buttonHome.setStyleSheet(Style.BUTTONBAR_STYLE)
        if LINUX:
            self.buttonHome.setIcon(QIcon(IMG_LINUX_PATH+"home.png"))
        else:
            self.buttonHome.setIcon(
                QIcon(os.path.join(IMG_WIN_PATH, "home.png")))
        self.buttonHome.setIconSize(
            QSize(int(Style.BUTTONBAR_WIDTH - 20), int(Style.BUTTONBAR_HEIGHT - 20)))
        self.buttonHome.clicked.connect(lambda: self.changePhase(PHASE_HOME))

# REV. 4.0


class ChangeDateTime(QWidget):
    phase = pyqtSignal(int)

    def updateData(self, lang_dictionary, phase):
        self.lang_dictionary = {}

        for e in lang_dictionary:
            if e[1] == phase:
                self.lang_dictionary.update({e[0]: e[2]})

        self.title.setText(self.lang_dictionary['label_title'])
        self.fields["year"].title.setText(self.lang_dictionary["label_year"])
        self.fields["month"].title.setText(self.lang_dictionary["label_month"])
        self.fields["day"].title.setText(self.lang_dictionary["label_day"])
        self.fields["hours"].title.setText(self.lang_dictionary["label_hours"])
        self.fields["minutes"].title.setText(
            self.lang_dictionary["label_minutes"])
        self.setButton.setText(self.lang_dictionary['label_modify'])

        self.datetime = QDateTime.currentDateTime()

        self.updateDateTime(self.datetime)

    def change(self):
        # systemctl disable systemd-timesyncd.service ////Disattiva sincro automatica data/ora sistema

        # call("sudo date --set " + self.fields["year"].label.text() + "-" + self.fields["month"].label.text() + "-" + self.fields["day"].label.text(), shell=True)
        # call("sudo date --set " + self.fields["hours"].label.text() + ":" + self.fields["minutes"].label.text() + ":00", shell=True)
        # call("sudo hwclock -w", shell=True)

        os.system("time "+self.fields["hours"].label.text() +
                  ":" + self.fields["minutes"].label.text() + ":00")
        os.system("date "+self.fields["day"].label.text() + "-" +
                  self.fields["month"].label.text() + "-" + self.fields["year"].label.text())

    def updateDateTime(self, datetime):
        self.datetime = datetime
        datetime = datetime.toString(Qt.ISODate)
        d = datetime.split("T")[0]
        t = datetime.split("T")[1]

        self.fields["year"].label.setText(str(d.split("-")[0]))
        self.fields["month"].label.setText(str(d.split("-")[1]))
        self.fields["day"].label.setText(str(d.split("-")[2]))
        self.fields["hours"].label.setText(str(t.split(":")[0]))
        self.fields["minutes"].label.setText(str(t.split(":")[1]))

    def __init__(self, parent=None):
        super(ChangeDateTime, self).__init__(parent)

        self.lang_dictionary = {}

        self.datetime = QDateTime.currentDateTime()

        self.title = QLabel("Impostazioni Data e Ora", self)
        self.title.setGeometry(0, 50, Style.WIDTH, 50)
        self.title.setStyleSheet(Style.TITLE2_CENTERED_STYLE)

        class Field:
            def __init__(self, parent, text, x, y):
                self.title = QLabel(text, parent)
                self.title.setGeometry(x, y, 325, 50)
                self.title.setStyleSheet(Style.TITLE3_CENTERED_STYLE)
                self.label = QLabel("", parent)
                self.label.setGeometry(x+80, y+50, 165, 50)
                self.label.setStyleSheet(Style.BODY_BG_HOME)
                self.sub = QPushButton("", parent)
                self.sub.setGeometry(x, y+50, 70, 50)
                if LINUX:
                    self.sub.setIcon(QIcon(IMG_LINUX_PATH+"back.png"))
                else:
                    self.sub.setIcon(
                        QIcon(os.path.join(IMG_WIN_PATH, "back.png")))
                self.sub.setIconSize(
                    QSize(self.sub.width() - 20, self.sub.height() - 20))
                self.sub.setStyleSheet(Style.BUTTONBAR_STYLE)
                self.add = QPushButton("", parent)
                self.add.setGeometry(x+255, y+50, 70, 50)
                if LINUX:
                    self.add.setIcon(QIcon(IMG_LINUX_PATH+"for.png"))
                else:
                    self.add.setIcon(
                        QIcon(os.path.join(IMG_WIN_PATH, "for.png")))
                self.add.setIconSize(
                    QSize(self.add.width() - 20, self.add.height() - 20))
                self.add.setStyleSheet(Style.BUTTONBAR_STYLE)

        self.fields = {"year": Field(self, "ANNO", 150, 125), "month": Field(self, "MESE", 150, 250), "day": Field(self, "GIORNO", 150, 375),
                       "hours": Field(self, "ORE", 505, 125), "minutes": Field(self, "MINUTI", 505, 250)}

        self.fields["year"].sub.clicked.connect(
            lambda: self.updateDateTime(self.datetime.addYears(-1)))
        self.fields["year"].add.clicked.connect(
            lambda: self.updateDateTime(self.datetime.addYears(1)))
        self.fields["month"].sub.clicked.connect(
            lambda: self.updateDateTime(self.datetime.addMonths(-1)))
        self.fields["month"].add.clicked.connect(
            lambda: self.updateDateTime(self.datetime.addMonths(1)))
        self.fields["day"].sub.clicked.connect(
            lambda: self.updateDateTime(self.datetime.addDays(-1)))
        self.fields["day"].add.clicked.connect(
            lambda: self.updateDateTime(self.datetime.addDays(1)))
        self.fields["hours"].sub.clicked.connect(
            lambda: self.updateDateTime(self.datetime.addSecs(-3600)))
        self.fields["hours"].add.clicked.connect(
            lambda: self.updateDateTime(self.datetime.addSecs(3600)))
        self.fields["minutes"].sub.clicked.connect(
            lambda: self.updateDateTime(self.datetime.addSecs(-60)))
        self.fields["minutes"].add.clicked.connect(
            lambda: self.updateDateTime(self.datetime.addSecs(60)))

        self.setButton = QPushButton(" ", self)
        self.setButton.setGeometry(int(Style.BUTTONBAR_WIDTH*8+Style.BUTTONBAR_X*8),
                                   Style.BUTTONBAR_Y, Style.BUTTONBAR_WIDTH, Style.BUTTONBAR_HEIGHT)
        self.setButton.setStyleSheet(Style.BUTTONBAR_STYLE)
        self.setButton.clicked.connect(self.change)

        self.buttonHome = QPushButton(self)
        self.buttonHome.setGeometry(int(Style.BUTTONBAR_X), int(
            Style.BUTTONBAR_Y), int(Style.BUTTONBAR_WIDTH), int(Style.BUTTONBAR_HEIGHT))
        self.buttonHome.setStyleSheet(Style.BUTTONBAR_STYLE)
        if LINUX:
            homeImage = QIcon(IMG_LINUX_PATH+"home.png")
        else:
            homeImage = QIcon(os.path.join(IMG_WIN_PATH, "home.png"))
        self.buttonHome.setIcon(homeImage)
        self.buttonHome.setIconSize(
            QSize(int(Style.BUTTONBAR_WIDTH - 20), int(Style.BUTTONBAR_HEIGHT - 20)))
        self.buttonHome.clicked.connect(lambda: self.phase.emit(PHASE_HOME))


class MainWindow(QMainWindow):
    '''
        Imposta come widget principale la classe specificata dal parametro @phase
    '''

    def settaFase(self, phase):
        self.counter_id, self.counter_num = self.configuration.getCurrentProduct()
        self.description_language = self.configuration.getDefaultLang()

        if phase == PHASE_LOGIN:
            self.errPhase = False
            # print("Phase 0 (Login) is running.")
            self.login.updateData(self.lang_dictionary, phase)
            self.centralWidget.setCurrentWidget(self.login)
        if phase == PHASE_HOME:
            self.errPhase = False
            # print("Phase 1 (Home) is running.")
            self.centralWidget.setCurrentWidget(self.home)
            self.user_id, self.permission = self.login.getCredentials()
            self.home.updateData(self.lang_dictionary, phase,
                                 self.user_id, self.counter_id, self.counter_num)
        if phase == PHASE_PRODUCTION:
            printer_enabled = self.home.getEnabledPrinter()
            if self.permission["productionMode"] == 'yes':
                self.errPhase = False
                # print("Phase 2 (Production) is running.")
                self.centralWidget.setCurrentWidget(self.production)
                self.production.updateData(self.lang_dictionary, self.description_language,
                                           self.synoptic_strings, self.user_id, self.counter_id, phase, printer_enabled)
            else:
                self.errPhase = True
                QMessageBox.critical(self, self.home.getLangDict()[
                                     "qmessagebox_error_accessdenied_title"], self.home.getLangDict()["qmessagebox_error_accessdenied"])
        if phase == PHASE_CONFIGURATION:
            if self.permission["configuration"] == 'yes':
                self.errPhase = False
                # print ("Phase 3 (Configuration) is running.")
                printer_enabled = self.home.getEnabledPrinter()
                enable_manconf = self.home.getEnabledManConf()
                self.configuration.updateData(
                    self.lang_dictionary, printer_enabled, enable_manconf, phase)
                self.centralWidget.setCurrentWidget(self.configuration)
            else:
                self.errPhase = True
                QMessageBox.critical(self, self.home.getLangDict()[
                                     "qmessagebox_error_accessdenied_title"], self.home.getLangDict()["qmessagebox_error_accessdenied"])
        if phase == PHASE_COUNTERS:
            if self.permission["counters"] == 'yes':
                self.errPhase = False
                # print ("Phase 4 (Counters) is running.")
                self.counters.updateCombo(self.lang_dictionary, phase)
                self.centralWidget.setCurrentWidget(self.counters)
            else:
                self.errPhase = True
                QMessageBox.critical(self, self.home.getLangDict()[
                                     "qmessagebox_error_accessdenied_title"], self.home.getLangDict()["qmessagebox_error_accessdenied"])
        if phase == PHASE_MANUAL:
            if self.permission["manualCommands"] == 'yes':
                self.errPhase = False
                # print ("Phase 5 (Manual Commands) is running.")
                self.manual.updateData(
                    self.lang_dictionary, phase, self.user_id)
                self.centralWidget.setCurrentWidget(self.manual)
            else:
                self.errPhase = True
                QMessageBox.critical(self, self.home.getLangDict()[
                                     "qmessagebox_error_accessdenied_title"], self.home.getLangDict()["qmessagebox_error_accessdenied"])
        if phase == PHASE_LOG:
            if self.permission["log"] == 'yes':
                self.errPhase = False
                # print ("Phase 6 (Log and Alarms) is running.")
                self.alarms.updateData(
                    self.lang_dictionary, phase, self.description_language)
                self.centralWidget.setCurrentWidget(self.alarms)
            else:
                self.errPhase = True
                QMessageBox.critical(self, self.home.getLangDict()[
                                     "qmessagebox_error_accessdenied_title"], self.home.getLangDict()["qmessagebox_error_accessdenied"])
        if phase == PHASE_USERS:
            if self.permission["users"] == 'yes':
                self.errPhase = False
                # print("Phase 7 (Users) is running.")
                self.user_id, self.permission = self.login.getCredentials()
                self.users.updateData(
                    self.lang_dictionary, self.user_id, phase)
                self.centralWidget.setCurrentWidget(self.users)
            else:
                self.errPhase = True
                QMessageBox.critical(self, self.home.getLangDict()[
                                     "qmessagebox_error_accessdenied_title"], self.home.getLangDict()["qmessagebox_error_accessdenied"])
        if phase == PHASE_SHUTDOWN:
            # print("Phase 8 (Shutdown) is running.")
            self.errPhase = False
            self.shutdown.updateData(self.lang_dictionary)
            self.centralWidget.setCurrentWidget(self.shutdown)
        if phase == PHASE_ADD_USER:
            # print("Phase 9 (Add User) is running.")
            self.errPhase = False
            self.adduser.updateData(self.lang_dictionary, phase)
            self.centralWidget.setCurrentWidget(self.adduser)
        if phase == PHASE_DATETIME:
            # print("Phase 10 (Change Date/Time) is running.")
            self.errPhase = False
            self.changeDateTime.updateData(self.lang_dictionary, phase)
            self.centralWidget.setCurrentWidget(self.changeDateTime)
        if phase == PHASE_LANG:
            # print("Phase 11 (Lang) is running.")
            self.errPhase = False
            self.lang.updateData(self.lang_dictionary, phase)
            self.centralWidget.setCurrentWidget(self.lang)
        if phase == PHASE_IT:
            # print("Phase 12 (Italian) is running.")
            self.errPhase = False
            sql = "SELECT international_id, phase, it FROM international"
            value = {}
            self.lang_dictionary, n_row, err = selectMethod(sql, value, logger)
            self.description_language = "description_IT"
            update_configuration_query_method("default_lang", 1, logger)
            sql = "SELECT synoptic_id, it FROM synoptic"
            value = {}
            self.synoptic_strings, n_row, err = selectMethod(
                sql, value, logger)
            self.settaFase(PHASE_LANG)
        if phase == PHASE_EN:
            # print("Phase 13 (English) is running.")
            self.errPhase = False
            sql = "SELECT international_id, phase, en FROM international"
            value = {}
            self.lang_dictionary, n_row, err = selectMethod(sql, value, logger)
            self.description_language = "description_EN"
            update_configuration_query_method("default_lang", 2, logger)
            sql = "SELECT synoptic_id, en FROM synoptic"
            value = {}
            self.synoptic_strings, n_row, err = selectMethod(
                sql, value, logger)
            self.settaFase(PHASE_LANG)
        if phase == PHASE_LANG1:
            # print("Phase 14 (LANG1) is running.")
            self.errPhase = False
            sql = "SELECT international_id, phase, LANG1 FROM international"
            value = {}
            self.lang_dictionary, n_row, err = selectMethod(sql, value, logger)
            self.description_language = "description_LANG1"
            update_configuration_query_method("default_lang", 3, logger)
            sql = "SELECT synoptic_id, LANG1 FROM synoptic"
            value = {}
            self.synoptic_strings, n_row, err = selectMethod(
                sql, value, logger)
            self.settaFase(PHASE_LANG)
        if phase == PHASE_LANG2:
            # print("Phase 15 (LANG2) is running.")
            self.errPhase = False
            sql = "SELECT international_id, phase, LANG2 FROM international"
            value = {}
            self.lang_dictionary, n_row, err = selectMethod(sql, value, logger)
            self.description_language = "description_LANG2"
            update_configuration_query_method("default_lang", 4, logger)
            sql = "SELECT synoptic_id, LANG2 FROM synoptic"
            value = {}
            self.synoptic_strings, n_row, err = selectMethod(
                sql, value, logger)
            self.settaFase(PHASE_LANG)
        if phase == PHASE_IDT:
            # print("Phase 16 (IDT) is running.")
            self.errPhase = False
            self.idt.updateData(self.lang_dictionary, phase)
            self.centralWidget.setCurrentWidget(self.idt)
        if phase == PHASE_ADVANCED_CONF:
            # ADMINISTRATOR --> non ha policy dedicata
            if self.permission['users'] == 'yes':
                # print("Phase 17 (Advanced Priority Configuration) is running.")
                self.errPhase = False
                self.advancedConf.updateData(self.lang_dictionary, phase)
                self.centralWidget.setCurrentWidget(self.advancedConf)
            else:
                self.errPhase = True
                QMessageBox.critical(self, self.home.getLangDict()[
                                     "qmessagebox_error_accessdenied_title"], self.home.getLangDict()["qmessagebox_error_accessdenied"])

        if not self.errPhase:
            self.ttModbus.setRegister((OUTPUT_PHASE, phase))

    '''
        Start HMI e instanza classi ed oggetti
    '''

    def startPanel(self, check_sig):
        if check_sig:
            self.initFrame.finishMe()
            self.lang_dictionary = self.initFrame.getLangDict()
            self.synoptic_strings = self.initFrame.getSynopticString()
            self.permission = {}

            self.login = Login(self)
            self.login.phase.connect(self.settaFase)
            self.centralWidget.addWidget(self.login)

            self.shutdown = Shutdown(self)
            self.shutdown.phase.connect(self.settaFase)
            self.centralWidget.addWidget(self.shutdown)

            self.home = Home(self)
            self.centralWidget.addWidget(self.home)
            self.home.phase.connect(self.settaFase)

            self.configuration = Configuration(self)
            self.centralWidget.addWidget(self.configuration)
            self.configuration.phase.connect(self.settaFase)

            self.advancedConf = AdvancedConfiguration(self)
            self.centralWidget.addWidget(self.advancedConf)
            self.advancedConf.phase.connect(self.settaFase)

            self.counters = Counters(self)
            self.centralWidget.addWidget(self.counters)
            self.counters.phase.connect(self.settaFase)

            self.alarms = Alarms(self)
            self.centralWidget.addWidget(self.alarms)
            self.alarms.phase.connect(self.settaFase)

            self.users = Users(self)
            self.centralWidget.addWidget(self.users)
            self.users.phase.connect(self.settaFase)

            self.adduser = AddUser(self)
            self.centralWidget.addWidget(self.adduser)
            self.adduser.phase.connect(self.settaFase)

            self.changeDateTime = ChangeDateTime(self)
            self.centralWidget.addWidget(self.changeDateTime)
            self.changeDateTime.phase.connect(self.settaFase)

            self.production = Production(self)
            self.centralWidget.addWidget(self.production)
            self.production.phase.connect(self.settaFase)

            self.manual = Manual(self)
            self.centralWidget.addWidget(self.manual)
            self.manual.phase.connect(self.settaFase)

            self.idt = IDT(self)
            self.centralWidget.addWidget(self.idt)
            self.idt.phase.connect(self.settaFase)

            self.lang = Lang(self)
            self.centralWidget.addWidget(self.lang)
            self.lang.phase.connect(self.settaFase)

            self.description_language = self.configuration.getDefaultLang()

            ##
            # FIRST WIDGET TO BE SHOWN
            self.login.updateData(self.lang_dictionary, PHASE_LOGIN)
            self.centralWidget.setCurrentWidget(self.login)

            # Forza il valore del registro indicante la pagina del pannello corrente a 0
            self.ttModbus.setRegister((OUTPUT_PHASE, PHASE_LOGIN))
        else:
            QMessageBox.critical(self.initFrame, "Error",
                                 "Bad startup sequence. Press OK to try again.")
            self.initFrame.initMe()

    # Dovrebbe essere obsoleto ora che la lettura dei dispositivi di input viene fatta per ogni dispositivo collegato e non uno specifico
    def setHidDevice(self, hid):
        self.hid = hid

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.virtualKeyboard = VirtualKeyboard(self)
        self.lang_dictionary = []
        self.description_language = DEFAULT_DESCRIPTION_LANGUAGE
        self.user_id = ""
        self.name = ""
        self.surname = ""
        self.permission = {}
        self.counter_id = ""
        self.errPhase = False
        self.centralWidget = QStackedWidget()
        self.setCentralWidget(self.centralWidget)

        self.setWindowTitle(TITLE)
        self.resize(Style.WIDTH, Style.HEIGHT)

        self.logoLabel = QLabel("", self)
        if LINUX:
            self.logoLabel.setPixmap(QPixmap(IMG_LINUX_PATH+"idt.png"))
        else:
            self.logoLabel.setPixmap(
                QPixmap(os.path.join(IMG_WIN_PATH, "idt.png")))
        self.logoLabel.setGeometry(25, 25, 200, 50)

        if LINUX:
            bg = QImage(IMG_LINUX_PATH +
                        "bg.jpeg").scaled(QSize(Style.WIDTH, Style.HEIGHT))
        else:
            # bg = QImage(IMG_WIN_PATH+"bg.jpeg").scaled(QSize(Style.WIDTH, Style.HEIGHT))
            bg = QImage(os.path.join(IMG_WIN_PATH, "bg.jpeg")).scaled(
                QSize(Style.WIDTH, Style.HEIGHT))

        palette = QPalette()
        palette.setBrush(10, QBrush(bg))
        self.setPalette(palette)

        self.initFrame = InitFrame(self)
        self.initFrame.check_sig.connect(self.startPanel)
        self.initFrame.hid_sig.connect(self.setHidDevice)
        self.initFrame.initMe()

        self.ttModbus = ModbusWriter()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # window.showFullScreen()
    sys.exit(app.exec_())
