# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'menuOwAupO.ui'
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
    QSizePolicy, QStatusBar, QWidget, QLabel)

class Ui_MenuWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(640, 480)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.search_button = QPushButton(self.centralwidget)
        self.search_button.setObjectName(u"search_button")
        self.search_button.setGeometry(QRect(200, 30, 271, 61))
        self.view_button = QPushButton(self.centralwidget)
        self.view_button.setObjectName(u"view_button")
        self.view_button.setGeometry(QRect(200, 130, 271, 61))
        self.upload_button = QPushButton(self.centralwidget)
        self.upload_button.setObjectName(u"upload_button")
        self.upload_button.setGeometry(QRect(200, 230, 271, 61))
        self.update_button = QPushButton(self.centralwidget)
        self.update_button.setObjectName(u"update_button")
        self.update_button.setGeometry(QRect(200, 330, 271, 61))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 640, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.text_label = QLabel(self.centralwidget)
        self.text_label.setObjectName(u"text_label")
        self.text_label.setGeometry(QRect(200, 430, 271, 31))

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.search_button.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.view_button.setText(QCoreApplication.translate("MainWindow", u"View", None))
        self.upload_button.setText(QCoreApplication.translate("MainWindow", u"Upload", None))
        self.update_button.setText(QCoreApplication.translate("MainWindow", u"Update", None))