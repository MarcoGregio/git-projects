from PyQt5.QtWidgets import QSizePolicy, QApplication, QMainWindow, QWidget, QStackedWidget, QLabel, QPushButton, QLineEdit, QMessageBox, QComboBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QAbstractItemView, QFrame, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon, QPalette, QBrush, QImage, QPixmap, QFontMetrics, QMovie, QPainter, QPen
from PyQt5.QtCore import QSize, Qt, QThread, pyqtSignal, QObject, QCoreApplication, QDateTime, QDate, QTime, QTimer
from IO_Constants import *
import Style
from QLed import *

class MyQLabel(QLabel):
    def __init__(self, text, parent):
        super(MyQLabel, self).__init__(text, parent)
        self.setText(text)
        self.setStyleSheet(Style.SUBTITLE5_STYLE)

class PresenceSensor:
    def setVisible(self, flag):
        self.led.setVisible(flag)
        self.label.setVisible(flag)
                
    def __init__(self, parent, label, x, y):
        self.led = QLed(parent, onColour=QLed.Green, shape=QLed.Circle, value=False)
        self.led.setGeometry(x,40*y,34,34)
        self.label = MyQLabel(label, parent)
        self.label.setGeometry(x+40,40*y,500,35)        

class ProdPresenceSensor:
    def setVisible(self, flag):
        self.led.setVisible(flag)
        self.label.setVisible(flag)
                
    def __init__(self, parent, label, x, y):
        self.led = QLed(parent, onColour=QLed.Green, shape=QLed.Circle, value=False)
        self.led.setGeometry(x,10+55*y,30,30)
        self.label = MyQLabel(label, parent)
        self.label.setGeometry(x+5,10+55*y,250,30)
        self.label.setStyleSheet(Style.SUBTITLE6_CENTERED_STYLE)

class SingleValveControl:
    def valv_operation(self):
        if self.valv.isChecked():
            self.ttModbus.setRegister((self.register, 1))
        else:
            self.ttModbus.setRegister((self.register, 0))

    def __init__(self, parent, valv_label, label, x, y, ttModbus, register, bit):
        self.ttModbus = ttModbus
        self.register = register
        self.bit = bit
        self.valv = QPushButton(valv_label, parent)
        self.valv.setCheckable(True)
        #self.valv.clicked.connect(self.valv_operation)
        self.valv.setStyleSheet(Style.BUTTON_MANUAL_STYLE_CHECKABLE)
        self.valv.setGeometry(x,y+25,130,60)
        self.led = QLed(parent, onColour=QLed.Green, shape=QLed.Circle, value=False)
        self.led.setGeometry(x+140,y+35,34,34)
        self.label = MyQLabel(label, parent)
        self.label.setGeometry(x+180,y+35,500,45)

class SingleValveControlRedGreen:
    def valv_operation(self):
        if self.valv.isChecked():
            self.ttModbus.setRegister((self.register, 1))
        else:
            self.ttModbus.setRegister((self.register, 0))

    def __init__(self, parent, valv_label, label, x, y, ttModbus, register, bit):
        self.ttModbus = ttModbus
        self.register = register
        self.bit = bit
        self.valv = QPushButton(valv_label, parent)
        self.valv.setCheckable(True)
        #self.valv.clicked.connect(self.valv_operation)
        self.valv.setStyleSheet(Style.BUTTON_MANUAL_STYLE_REDGREEN_CHECKABLE)
        self.valv.setGeometry(x,y+25,130,60)
        self.led = QLed(parent, onColour=QLed.Green, shape=QLed.Circle, value=False)
        self.led.setGeometry(x+140,y+35,34,34)
        self.label = MyQLabel(label, parent)
        self.label.setGeometry(x+180,y+35,500,45)
        
class ValveControl:
    def valv_operation(self):
        if self.valv.isChecked():
            self.ttModbus.setRegister((self.register, 1))
        else:
            self.ttModbus.setRegister((self.register, 0))

    def __init__(self, parent, valv_label, label_end, label_home, x, y, ttModbus, register, bit):
        self.ttModbus = ttModbus
        self.register = register
        self.bit = bit
        self.valv = QPushButton(valv_label, parent)
        self.valv.setCheckable(True)
        #self.valv.clicked.connect(self.valv_operation)
        self.valv.setStyleSheet(Style.BUTTON_MANUAL_STYLE_CHECKABLE)
        self.valv.setGeometry(x,y+25,130,60)
        self.home_led = QLed(parent, onColour=QLed.Green, shape=QLed.Circle, value=False)
        self.home_led.setGeometry(x+140,y+6,34,34)
        self.home_label = MyQLabel(label_home, parent)
        self.home_label.setGeometry(x+180,y+6,500,45)
        self.end_led = QLed(parent, onColour=QLed.Green, shape=QLed.Circle, value=False)
        self.end_led.setGeometry(x+140,y+57,34,34)
        self.end_label = MyQLabel(label_end, parent)
        self.end_label.setGeometry(x+180,y+57,500,45)

class ValveControlNotCheckable:
    def valv_operation(self):
        if self.valv.isChecked():
            self.ttModbus.setRegister((self.register, 1))

    def __init__(self, parent, valv_label, label_end, label_home, x, y, ttModbus, register, bit):
        self.ttModbus = ttModbus
        self.register = register
        self.bit = bit
        self.valv = QPushButton(valv_label, parent)
        #self.valv.setCheckable(True)
        #self.valv.clicked.connect(self.valv_operation)
        self.valv.setStyleSheet(Style.BUTTON_MANUAL_STYLE_CHECKABLE)
        self.valv.setGeometry(x,y+25,130,60)
        self.home_led = QLed(parent, onColour=QLed.Green, shape=QLed.Circle, value=False)
        self.home_led.setGeometry(x+140,y+6,34,34)
        self.home_label = MyQLabel(label_home, parent)
        self.home_label.setGeometry(x+180,y+6,500,45)
        self.end_led = QLed(parent, onColour=QLed.Green, shape=QLed.Circle, value=False)
        self.end_led.setGeometry(x+140,y+57,34,34)
        self.end_label = MyQLabel(label_end, parent)
        self.end_label.setGeometry(x+180,y+57,500,45)

class TripleValveControl:
    def valv_operation(self, register, bit):
        if self.valv.isChecked():
            self.ttModbus.setRegister((self.register, 1))
        else:
            self.ttModbus.setRegister((self.register, 0))

    def __init__(self, parent, valv_label, label_end, label_home, label_end1, label_home1, label_home2, label_end2, x, y, ttModbus, register, bit):
        self.ttModbus = ttModbus
        self.register = register
        self.bit = bit
        self.valv = QPushButton(valv_label, parent)
        self.valv.setCheckable(True)
        #self.valv.clicked.connect(self.valv_operation)
        self.valv.setStyleSheet(Style.BUTTON_MANUAL_STYLE_CHECKABLE)
        self.valv.setGeometry(x,y+51,150,60)
        self.home_led = QLed(parent, onColour=QLed.Green, shape=QLed.Circle, value=False)
        self.home_led.setGeometry(x+160,y+6,45,45)
        self.home_label = MyQLabel(label_home, parent)
        self.home_label.setGeometry(x+215,y+6,180,45)
        self.home_led1 = QLed(parent, onColour=QLed.Green, shape=QLed.Circle, value=False)
        self.home_led1.setGeometry(x+160,y+57,45,45)
        self.home_label1 = MyQLabel(label_home1, parent)
        self.home_label1.setGeometry(x+215,y+57,180,45)
        self.home_led2 = QLed(parent, onColour=QLed.Green, shape=QLed.Circle, value=False)
        self.home_led2.setGeometry(x+160,y+108,45,45)
        self.home_label2 = MyQLabel(label_home2, parent)
        self.home_label2.setGeometry(x+215,y+108,180,45)
        self.end_led = QLed(parent, onColour=QLed.Green, shape=QLed.Circle, value=False)
        self.end_led.setGeometry(x+365,y+6,45,45)
        self.end_label = MyQLabel(label_end, parent)
        self.end_label.setGeometry(x+420,y+6,180,45)
        self.end_led1 = QLed(parent, onColour=QLed.Green, shape=QLed.Circle, value=False)
        self.end_led1.setGeometry(x+365,y+57,45,45)
        self.end_label1 = MyQLabel(label_end1, parent)
        self.end_label1.setGeometry(x+420,y+57,180,45)
        self.end_led2 = QLed(parent, onColour=QLed.Green, shape=QLed.Circle, value=False)
        self.end_led2.setGeometry(x+365,y+108,45,45)
        self.end_label2 = MyQLabel(label_end2, parent)
        self.end_label2.setGeometry(x+420,y+108,180,45)

class DoubleValveControl:
    def valv_operation(self):
        if self.valv.isChecked():
            self.ttModbus.setRegister((self.register, 1))
        else:
            self.ttModbus.setRegister((self.register, 0))

    def __init__(self, parent, valv_label, label_end, label_home, label_end1, label_home1, x, y, ttModbus, register, bit):
        self.ttModbus = ttModbus
        self.register = register
        self.bit = bit
        self.valv = QPushButton(valv_label, parent)
        self.valv.setCheckable(True)
        #self.valv.clicked.connect(self.valv_operation)
        self.valv.setStyleSheet(Style.BUTTON_MANUAL_STYLE_CHECKABLE)
        self.valv.setGeometry(x,y+25,130,60)
        self.home_led = QLed(parent, onColour=QLed.Green, shape=QLed.Circle, value=False)
        self.home_led.setGeometry(x+140,y+6,34,34)
        self.home_label = MyQLabel(label_home, parent)
        self.home_label.setGeometry(x+180,y+6,300,45)
        self.home_led1 = QLed(parent, onColour=QLed.Green, shape=QLed.Circle, value=False)
        self.home_led1.setGeometry(x+140,y+57,34,34)
        self.home_label1 = MyQLabel(label_home1, parent)
        self.home_label1.setGeometry(x+180,y+57,300,45)     
        self.end_led = QLed(parent, onColour=QLed.Green, shape=QLed.Circle, value=False)
        self.end_led.setGeometry(x+320,y+6,34,34)
        self.end_label = MyQLabel(label_end, parent)
        self.end_label.setGeometry(x+360,y+6,300,45)
        self.end_led1 = QLed(parent, onColour=QLed.Green, shape=QLed.Circle, value=False)
        self.end_led1.setGeometry(x+320,y+57,34,34)
        self.end_label1 = MyQLabel(label_end1, parent)
        self.end_label1.setGeometry(x+360,y+57,300,45)

class VerticalDoubleValveControl:
    def valv_operation(self):
        if self.valv.isChecked():
            self.ttModbus.setRegister((self.register, 1))
        else:
            self.ttModbus.setRegister((self.register, 0))

    def __init__(self, parent, valv_label, label_end, label_home, label_end1, label_home1, x, y, ttModbus, register, bit):
        self.ttModbus = ttModbus
        self.register = register
        self.bit = bit
        self.valv = QPushButton(valv_label, parent)
        self.valv.setCheckable(True)
        #self.valv.clicked.connect(self.valv_operation)
        self.valv.setStyleSheet(Style.BUTTON_MANUAL_STYLE_CHECKABLE)
        self.valv.setGeometry(x,y+85,150,60)
        self.home_led = QLed(parent, onColour=QLed.Green, shape=QLed.Circle, value=False)
        self.home_led.setGeometry(x+160,y+6,45,45)
        self.home_label = MyQLabel(label_home, parent)
        self.home_label.setGeometry(x+215,y+6,350,45)
        self.home_led1 = QLed(parent, onColour=QLed.Green, shape=QLed.Circle, value=False)
        self.home_led1.setGeometry(x+160,y+57,45,45)
        self.home_label1 = MyQLabel(label_home1, parent)
        self.home_label1.setGeometry(x+215,y+57,350,45)     
        self.end_led = QLed(parent, onColour=QLed.Green, shape=QLed.Circle, value=False)
        self.end_led.setGeometry(x+160,y+108,45,45)
        self.end_label = MyQLabel(label_end, parent)
        self.end_label.setGeometry(x+215,y+108,350,45)
        self.end_led1 = QLed(parent, onColour=QLed.Green, shape=QLed.Circle, value=False)
        self.end_led1.setGeometry(x+160,y+159,45,45)
        self.end_label1 = MyQLabel(label_end1, parent)
        self.end_label1.setGeometry(x+215,y+159,350,45)


class MinusPlusMiniWidget:
    def setVisible(self, flag):
        if flag:
            self.box.setVisible(True)
            self.minus.setVisible(True)
            self.plus.setVisible(True)
        else:
            self.box.setVisible(False)
            self.minus.setVisible(False)
            self.plus.setVisible(False)    
                    
    def __init__(self, parent, title, x, y, width, height):
        self.box = QLabel(title, parent)
        self.box.setGeometry(x+75,y,width-150,height)
        self.box.setStyleSheet(Style.BODY4_CENTERED_STYLE)
        self.minus = QPushButton("", parent)
        self.minus.setGeometry(x+20,y,50,50)
        self.minus.setStyleSheet(Style.MINUS_PLUS)
        minusImage = QIcon("img/minus.png")
        self.minus.setIcon(minusImage)
        self.minus.setIconSize(QSize(self.minus.width() - 5, self.minus.height() - 25))
        self.plus = QPushButton("", parent)
        self.plus.setGeometry(x+80+self.box.width(),y,50,50)
        self.plus.setStyleSheet(Style.MINUS_PLUS)
        plusImage = QIcon("img/plus.png")
        self.plus.setIcon(plusImage)
        self.plus.setIconSize(QSize(self.minus.width() - 5, self.minus.height() - 25))

class MinusPlusWidget:
    def setVisible(self, flag):
        if flag:
            self.label.setVisible(True)
            self.box.setVisible(True)
            self.minus.setVisible(True)
            self.plus.setVisible(True)
        else:
            self.label.setVisible(False)
            self.box.setVisible(False)
            self.minus.setVisible(False)
            self.plus.setVisible(False)

    def set_values_offset(self, subtraction, element):
        try:
            value = float(element.text())
            if subtraction:
                if value > self.default_zero:
                    value = value - self.unit
            else: 
                if value < self.default_max:
                    value = value + self.unit
            element.setText(str("{0:.1f}".format(round(value,1))))
        except ValueError:
            print("errore")

    def set_values(self, subtraction, element):
        try:
            value = int(element.text())
            if subtraction:
                if value > self.default_zero:
                    value = value - self.unit
            else: 
                if value < self.default_max:
                    value = value + self.unit
            element.setText(str(value))
        except ValueError:
            print("errore")

    def __init__(self, parent, title, x, y, width, height, value, default_zero, default_max, unit):
        self.default_zero = default_zero
        self.default_max = default_max
        self.unit = unit
        self.label = QLabel(title, parent)
        self.label.setGeometry(x, y, width, height)
        self.label.setStyleSheet(Style.SUBTITLE6_CENTERED_STYLE)
        self.box = QLabel(str(value), parent)
        self.box.setGeometry(x+60,y+height,width-120,height)
        self.box.setStyleSheet(Style.BODY4_CENTERED_STYLE)
        self.minus = QPushButton("", parent)
        self.minus.setGeometry(x+5,y+height,50,50)
        self.minus.setStyleSheet(Style.MINUS_PLUS)
        minusImage = QIcon("img/minus.png")
        self.minus.setIcon(minusImage)
        self.minus.setIconSize(QSize(self.minus.width() - 5, self.minus.height() - 25))
        self.plus = QPushButton("", parent)
        self.plus.setGeometry(x+65+self.box.width(),y+height,50,50)
        self.plus.setStyleSheet(Style.MINUS_PLUS)
        plusImage = QIcon("img/plus.png")
        self.plus.setIcon(plusImage)
        self.plus.setIconSize(QSize(self.minus.width() - 5, self.minus.height() - 25))
