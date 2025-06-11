# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'searchIFsfKY.ui'
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

class Ui_SearchWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(640, 480)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.userid_textbox = QLineEdit(self.centralwidget)
        self.userid_textbox.setObjectName(u"userid_textbox")
        self.userid_textbox.setGeometry(QRect(100, 80, 211, 51))
        font = QFont()
        font.setPointSize(20)
        self.userid_textbox.setFont(font)
        self.name_textbox = QLineEdit(self.centralwidget)
        self.name_textbox.setObjectName(u"name_textbox")
        self.name_textbox.setGeometry(QRect(100, 170, 211, 51))
        self.name_textbox.setFont(font)
        self.search_api_button = QPushButton(self.centralwidget)
        self.search_api_button.setObjectName(u"search_api_button")
        self.search_api_button.setGeometry(QRect(280, 350, 141, 61))
        self.combo_box = QComboBox(self.centralwidget)
        self.combo_box.addItem("")
        self.combo_box.addItem("")
        self.combo_box.addItem("")
        self.combo_box.addItem("")
        self.combo_box.setObjectName(u"combo_box")
        self.combo_box.setGeometry(QRect(290, 280, 111, 31))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 640, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.back_button = QPushButton(self.centralwidget)
        self.back_button.setObjectName(u"back_button")
        self.back_button.setGeometry(QRect(450, 400, 75, 23))

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.userid_textbox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"User ID", None))
        self.name_textbox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Name", None))
        self.search_api_button.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.combo_box.setItemText(0, QCoreApplication.translate("MainWindow", u"health_record", None))
        self.combo_box.setItemText(1, QCoreApplication.translate("MainWindow", u"research_record", None))
        self.combo_box.setItemText(2, QCoreApplication.translate("MainWindow", u"medicine_record", None))
        self.combo_box.setItemText(3, QCoreApplication.translate("MainWindow", u"financial_record", None))

        self.back_button.setText(QCoreApplication.translate("ManiWindow", u"Back", None))