# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loginduDxgn.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QTextEdit, QWidget, QLineEdit)

class Ui_LoginWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(640, 480)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(280, 340, 111, 51))
        self.username_textbox = QLineEdit(self.centralwidget)
        self.username_textbox.setObjectName(u"username_textbox")
        self.username_textbox.setGeometry(QRect(200, 110, 281, 61))
        font = QFont()
        font.setPointSize(25)
        self.username_textbox.setFont(font)
        self.password_textbox = QLineEdit(self.centralwidget)
        self.password_textbox.setObjectName(u"password_textbox")
        self.password_textbox.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_textbox.setGeometry(QRect(200, 220, 281, 61))
        self.password_textbox.setFont(font)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 640, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.username_textbox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Username", None))
        self.password_textbox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Password", None))
