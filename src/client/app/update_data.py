# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pushdatanEjIvS.ui'
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
from PyQt5.QtWidgets import (QApplication, QComboBox, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QLineEdit,
    QWidget)

class Ui_UpdateWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(741, 589)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.UID = QLineEdit(self.centralwidget)
        self.UID.setObjectName(u"UID")
        self.UID.setGeometry(QRect(210, 120, 141, 41))
        self.NAME = QLineEdit(self.centralwidget)
        self.NAME.setObjectName(u"NAME")
        self.NAME.setGeometry(QRect(210, 180, 321, 61))
        self.FileName = QLineEdit(self.centralwidget)
        self.FileName.setObjectName(u"FileName")
        self.FileName.setGeometry(QRect(210, 260, 321, 41))
        self.update_api_button = QPushButton(self.centralwidget)
        self.update_api_button.setObjectName(u"update_api_button")
        self.update_api_button.setGeometry(QRect(230, 370, 281, 51))
        self.collection = QComboBox(self.centralwidget)
        self.collection.addItem("")
        self.collection.addItem("")
        self.collection.addItem("")
        self.collection.addItem("")
        self.collection.setObjectName(u"collection")
        self.collection.setGeometry(QRect(290, 320, 171, 31))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 741, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.back_button = QPushButton(self.centralwidget)
        self.back_button.setObjectName(u"back_button")
        self.back_button.setGeometry(QRect(550, 450, 75, 23))

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.UID.setPlaceholderText(QCoreApplication.translate("MainWindow", u"UID", None))
        self.NAME.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Name", None))
        self.FileName.setPlaceholderText(QCoreApplication.translate("MainWindow", u"FileName", None))
        self.update_api_button.setText(QCoreApplication.translate("MainWindow", u"UPDATE", None))
        self.collection.setItemText(0, QCoreApplication.translate("MainWindow", u"health_record", None))
        self.collection.setItemText(1, QCoreApplication.translate("MainWindow", u"research_record", None))
        self.collection.setItemText(2, QCoreApplication.translate("MainWindow", u"medicine_record", None))
        self.collection.setItemText(3, QCoreApplication.translate("MainWindow", u"financial_record", None))

        self.back_button.setText(QCoreApplication.translate("ManiWindow", u"Back", None))