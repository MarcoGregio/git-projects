import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizeGrip, QWidget, QPushButton, QLineEdit, QGridLayout, QDialog, QSizePolicy
from PyQt5.QtGui import QMouseEvent, QIcon
from PyQt5.QtCore import QSize, pyqtSignal, Qt
from PyQt5 import QtGui
from IO_Constants import *
import Style

class VirtualKeyboard(QDialog):
    signal = pyqtSignal(str)

    def sendData(self, b):
        t = self.edit.text()
        self.edit.setText(t + b.text())
        self.edit.repaint()

    def sendDateCanc(self):
        var = self.edit.text()
        long = (len(var)) - 1
        self.edit.setText(var[0:long])
        self.edit.repaint()

    def sendDateCancALL(self):
        var = ""
        self.edit.setText(var)
        self.edit.repaint()

    def sendDateSpace(self):
        var = self.edit.text()
        long = (len(var))
        var = var[0:long] + " "
        self.edit.setText(var[0:long + 1])
        self.edit.repaint()

    def sendDataApostrophe(self):
        t = self.edit.text()
        self.edit.setText(t + str("\\'"))
        self.edit.repaint()
        
    def sendDateEnter(self):
        var = self.edit.text()
        self.close()
        return var

    def sendShift(self):
        if self.shift.text().isupper():
            self.shift.setText(self.shift.text().lower())
        else:
            self.shift.setText(self.shift.text().upper())
            
        if self.letQ.text().isupper():
            self.letQ.setText(self.letQ.text().lower())
        else:
            self.letQ.setText(self.letQ.text().upper())

        if self.letW.text().isupper():
            self.letW.setText(self.letW.text().lower())
        else:
            self.letW.setText(self.letW.text().upper())

        if self.letE.text().isupper():
            self.letE.setText(self.letE.text().lower())
        else:
            self.letE.setText(self.letE.text().upper())

        if self.letR.text().isupper():
            self.letR.setText(self.letR.text().lower())
        else:
            self.letR.setText(self.letR.text().upper())

        if self.letT.text().isupper():
            self.letT.setText(self.letT.text().lower())
        else:
            self.letT.setText(self.letT.text().upper())

        if self.letY.text().isupper():
            self.letY.setText(self.letY.text().lower())
        else:
            self.letY.setText(self.letY.text().upper())

        if self.letU.text().isupper():
            self.letU.setText(self.letU.text().lower())
        else:
            self.letU.setText(self.letU.text().upper())

        if self.letI.text().isupper():
            self.letI.setText(self.letI.text().lower())
        else:
            self.letI.setText(self.letI.text().upper())

        if self.letO.text().isupper():
            self.letO.setText(self.letO.text().lower())
        else:
            self.letO.setText(self.letO.text().upper())

        if self.letP.text().isupper():
            self.letP.setText(self.letP.text().lower())
        else:
            self.letP.setText(self.letP.text().upper())

        if self.letA.text().isupper():
            self.letA.setText(self.letA.text().lower())
        else:
            self.letA.setText(self.letA.text().upper())

        if self.letS.text().isupper():
            self.letS.setText(self.letS.text().lower())
        else:
            self.letS.setText(self.letS.text().upper())

        if self.letD.text().isupper():
            self.letD.setText(self.letD.text().lower())
        else:
            self.letD.setText(self.letD.text().upper())

        if self.letF.text().isupper():
            self.letF.setText(self.letF.text().lower())
        else:
            self.letF.setText(self.letF.text().upper())

        if self.letG.text().isupper():
            self.letG.setText(self.letG.text().lower())
        else:
            self.letG.setText(self.letG.text().upper())

        if self.letH.text().isupper():
            self.letH.setText(self.letH.text().lower())
        else:
            self.letH.setText(self.letH.text().upper())
            
        if self.letJ.text().isupper():
            self.letJ.setText(self.letJ.text().lower())
        else:
            self.letJ.setText(self.letJ.text().upper())

        if self.letK.text().isupper():
            self.letK.setText(self.letK.text().lower())
        else:
            self.letK.setText(self.letK.text().upper())

        if self.letL.text().isupper():
            self.letL.setText(self.letL.text().lower())
        else:
            self.letL.setText(self.letL.text().upper())

        if self.letZ.text().isupper():
            self.letZ.setText(self.letZ.text().lower())
        else:
            self.letZ.setText(self.letZ.text().upper())

        if self.letX.text().isupper():
            self.letX.setText(self.letX.text().lower())
        else:
            self.letX.setText(self.letX.text().upper())

        if self.letC.text().isupper():
            self.letC.setText(self.letC.text().lower())
        else:
            self.letC.setText(self.letC.text().upper())

        if self.letV.text().isupper():
            self.letV.setText(self.letV.text().lower())
        else:
            self.letV.setText(self.letV.text().upper())

        if self.letB.text().isupper():
            self.letB.setText(self.letB.text().lower())
        else:
            self.letB.setText(self.letB.text().upper())

        if self.letN.text().isupper():
            self.letN.setText(self.letN.text().lower())
        else:
            self.letN.setText(self.letN.text().upper())

        if self.letM.text().isupper():
            self.letM.setText(self.letM.text().lower())
        else:
            self.letM.setText(self.letM.text().upper())
            
    def __init__(self, parent=None):
        super(VirtualKeyboard,self).__init__()

        self.setWindowTitle("VirtualKeyboard")
        self.setGeometry(200, 200, 650, 300)
        self.edit = ClickableLineEdit(self)
        self.setFixedSize(self.size())

        class MyQPushButton(QPushButton):
            def __init__(self, text):
                super(MyQPushButton, self).__init__(text)
                self.setText(text)
                self.setStyleSheet(Style.BUTTONMENU_STYLE)
                self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

        self.layout = QGridLayout(self)
        self.num1 = MyQPushButton("1")
        self.num1.clicked.connect(lambda:self.sendData(self.num1))

        self.num2 = MyQPushButton("2")
        self.num2.clicked.connect(lambda:self.sendData(self.num2))

        self.num3 = MyQPushButton("3")
        self.num3.clicked.connect(lambda:self.sendData(self.num3))

        self.num4 = MyQPushButton("4")
        self.num4.clicked.connect(lambda:self.sendData(self.num4))

        self.num5 = MyQPushButton("5")
        self.num5.clicked.connect(lambda:self.sendData(self.num5))

        self.num6 = MyQPushButton("6")
        self.num6.clicked.connect(lambda:self.sendData(self.num6))

        self.num7 = MyQPushButton("7")
        self.num7.clicked.connect(lambda:self.sendData(self.num7))

        self.num8 = MyQPushButton("8")
        self.num8.clicked.connect(lambda:self.sendData(self.num8))

        self.num9 = MyQPushButton("9")
        self.num9.clicked.connect(lambda:self.sendData(self.num9))

        self.num0 = MyQPushButton("0")
        self.num0.clicked.connect(lambda:self.sendData(self.num0))

        self.apostrophe = MyQPushButton("'")
        self.apostrophe.clicked.connect(self.sendDataApostrophe)

        self.backspace = QPushButton("")
        self.backspace.clicked.connect(self.sendDateCanc)
        if LINUX:
            backspaceIcon = QtGui.QIcon(IMG_LINUX_PATH + "backspace.png")
        else:
            backspaceIcon = QtGui.QIcon(os.path.join(IMG_WIN_PATH,"backspace.png"))
        self.backspace.setIcon(backspaceIcon)
        self.backspace.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.backspace.setIconSize(QSize(45, 45))
        self.backspace.setStyleSheet(Style.BUTTONMENU_STYLE)
        #self.backspace = MyQPushButton("<---")
        #self.backspace.clicked.connect(self.sendDateCanc)

        self.cancALL = QPushButton("")
        self.cancALL.clicked.connect(self.sendDateCancALL)
        if LINUX:
            cancAllIcon = QtGui.QIcon(IMG_LINUX_PATH +"cancel.png")
        else:
            cancAllIcon = QtGui.QIcon(os.path.join(IMG_WIN_PATH,"cancel.png"))
        self.cancALL.setIcon(cancAllIcon)
        self.cancALL.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.cancALL.setStyleSheet(Style.BUTTONMENU_STYLE)
        #self.cancALL = MyQPushButton("><")
        #self.cancALL.clicked.connect(self.sendDateCancALL)

        self.space=MyQPushButton("SPACE")
        self.space.clicked.connect(self.sendDateSpace)

        self.enter = QPushButton("")
        self.enter.clicked.connect(self.sendDateEnter)
        if LINUX:
            enterIcon = QtGui.QIcon(IMG_LINUX_PATH + "enter.png")
        else:
            enterIcon = QtGui.QIcon(os.path.join(IMG_WIN_PATH,"enter.png"))
        self.enter.setIcon(enterIcon)
        self.enter.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.enter.setIconSize(QSize(80, 80))
        self.enter.setStyleSheet(Style.BUTTONMENU_STYLE)
        #self.enter=MyQPushButton("ENTER")
        #self.enter.clicked.connect(self.sendDateEnter)


        # LETTERE PRIMA FILA//////////////////////////////////////////////////////////////////
        self.letQ = MyQPushButton("q")
        self.letQ.clicked.connect(lambda:self.sendData(self.letQ))

        self.letW = MyQPushButton("w")
        self.letW.clicked.connect(lambda:self.sendData(self.letW))

        self.letE = MyQPushButton("e")
        self.letE.clicked.connect(lambda:self.sendData(self.letE))
        
        self.letR = MyQPushButton("r")
        self.letR.clicked.connect(lambda:self.sendData(self.letR))

        self.letT = MyQPushButton("t")
        self.letT.clicked.connect(lambda:self.sendData(self.letT))

        self.letY = MyQPushButton("y")
        self.letY.clicked.connect(lambda:self.sendData(self.letY))

        self.letU = MyQPushButton("u")
        self.letU.clicked.connect(lambda:self.sendData(self.letU))

        self.letI = MyQPushButton("i")
        self.letI.clicked.connect(lambda:self.sendData(self.letI)) 

        self.letO = MyQPushButton("o")
        self.letO.clicked.connect(lambda:self.sendData(self.letO))

        self.letP = MyQPushButton("p")
        self.letP.clicked.connect(lambda:self.sendData(self.letP))

        # LETTERE SECONDA FILA//////////////////////////////////////////////////////////////////

        self.letA = MyQPushButton("a")
        self.letA.clicked.connect(lambda:self.sendData(self.letA))

        self.letS = MyQPushButton("s")
        self.letS.clicked.connect(lambda:self.sendData(self.letS))

        self.letD = MyQPushButton("d")
        self.letD.clicked.connect(lambda:self.sendData(self.letD))

        self.letF = MyQPushButton("f")
        self.letF.clicked.connect(lambda:self.sendData(self.letF))

        self.letG = MyQPushButton("g")
        self.letG.clicked.connect(lambda:self.sendData(self.letG))

        self.letH = MyQPushButton("h")
        self.letH.clicked.connect(lambda:self.sendData(self.letH))

        self.letJ = MyQPushButton("j")
        self.letJ.clicked.connect(lambda:self.sendData(self.letJ))

        self.letK = MyQPushButton("k")
        self.letK.clicked.connect(lambda:self.sendData(self.letK))

        self.letL = MyQPushButton("l")
        self.letL.clicked.connect(lambda:self.sendData(self.letL))

        # LETTERE Terza FILA//////////////////////////////////////////////////////////////////

        self.letZ = MyQPushButton("z")
        self.letZ.clicked.connect(lambda:self.sendData(self.letZ))

        self.letX = MyQPushButton("x")
        self.letX.clicked.connect(lambda:self.sendData(self.letX))

        self.letC = MyQPushButton("c")
        self.letC.clicked.connect(lambda:self.sendData(self.letC))

        self.letV = MyQPushButton("v")
        self.letV.clicked.connect(lambda:self.sendData(self.letV))

        self.letB = MyQPushButton("b")
        self.letB.clicked.connect(lambda:self.sendData(self.letB))

        self.letN = MyQPushButton("n")
        self.letN.clicked.connect(lambda:self.sendData(self.letN))

        self.letM = MyQPushButton("m")
        self.letM.clicked.connect(lambda:self.sendData(self.letM))

        self.shift = QPushButton("")
        self.shift.clicked.connect(self.sendShift)
        if LINUX:
            shiftIcon = QtGui.QIcon(IMG_LINUX_PATH + "shift.png")
        else:
            shiftIcon = QtGui.QIcon(os.path.join(IMG_WIN_PATH,"shift.png"))
        self.shift.setIcon(shiftIcon)
        self.shift.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.shift.setIconSize(QSize(30, 40))
        self.shift.setStyleSheet(Style.BUTTONMENU_STYLE)
        #self.shift = MyQPushButton("shift")
        #self.shift.clicked.connect(self.sendShift)

        self.layout.addWidget(self.edit,0,1,1,11)
        self.layout.addWidget(self.num1, 2, 1)
        self.layout.addWidget(self.num2, 2, 2)
        self.layout.addWidget(self.num3, 2, 3)
        self.layout.addWidget(self.num4, 2, 4)
        self.layout.addWidget(self.num5, 2, 5)
        self.layout.addWidget(self.num6, 2, 6)
        self.layout.addWidget(self.num7, 2, 7)
        self.layout.addWidget(self.num8, 2, 8)
        self.layout.addWidget(self.num9, 2, 9)
        self.layout.addWidget(self.num0, 2, 10)
        self.layout.addWidget(self.backspace, 2, 11)
        #self.layout.addWidget(self.apostrophe, 2, 11)
        # LETTERE PRIMA FILA///////////////////////////////////////////////////////////
        self.layout.addWidget(self.letQ, 3, 1)
        self.layout.addWidget(self.letW, 3, 2)
        self.layout.addWidget(self.letE, 3, 3)
        self.layout.addWidget(self.letR, 3, 4)
        self.layout.addWidget(self.letT, 3, 5)
        self.layout.addWidget(self.letY, 3, 6)
        self.layout.addWidget(self.letU, 3, 7)
        self.layout.addWidget(self.letI, 3, 8)
        self.layout.addWidget(self.letO, 3, 9)
        self.layout.addWidget(self.letP, 3, 10)
        self.layout.addWidget(self.cancALL, 3, 11)

        # LETTERE SECONDA FILA///////////////////////////////////////////////////////////
        self.layout.addWidget(self.letA, 4, 1)
        self.layout.addWidget(self.letS, 4, 2)
        self.layout.addWidget(self.letD, 4, 3)
        self.layout.addWidget(self.letF, 4, 4)
        self.layout.addWidget(self.letG, 4, 5)
        self.layout.addWidget(self.letH, 4, 6)
        self.layout.addWidget(self.letJ, 4, 7)
        self.layout.addWidget(self.letK, 4, 8)
        self.layout.addWidget(self.letL, 4, 9)
        self.layout.addWidget(self.enter,4,10,3,2)

        # LETTERE TERZA  FILA///////////////////////////////////////////////////////////

        self.layout.addWidget(self.letZ, 5, 1)
        self.layout.addWidget(self.letX, 5, 2)
        self.layout.addWidget(self.letC, 5, 3)
        self.layout.addWidget(self.letV, 5, 4)
        self.layout.addWidget(self.letB, 5, 5)
        self.layout.addWidget(self.letN, 5, 6)
        self.layout.addWidget(self.letM, 5, 7)
        self.layout.addWidget(self.shift, 5, 8, 1, 2)
        self.layout.addWidget(self.space,6,1,1,7)
        self.setLayout(self.layout)

class ClickableLineEdit(QLineEdit):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        QLineEdit.mousePressEvent(self, event)
