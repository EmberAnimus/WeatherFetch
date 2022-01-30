# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLayout, QPushButton, QSizePolicy,
    QSpacerItem, QTableView, QVBoxLayout, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.setWindowModality(Qt.NonModal)
        Widget.resize(525, 592)
        self.layoutWidget = QWidget(Widget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 0, 524, 591))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelImg = QLabel(self.layoutWidget)
        self.labelImg.setObjectName(u"labelImg")
        self.labelImg.setMinimumSize(QSize(49, 57))
        self.labelImg.setMaximumSize(QSize(16777215, 16777215))
        self.labelImg.setScaledContents(True)

        self.horizontalLayout.addWidget(self.labelImg)

        self.labelCurTemp = QLabel(self.layoutWidget)
        self.labelCurTemp.setObjectName(u"labelCurTemp")
        font = QFont()
        font.setPointSize(14)
        self.labelCurTemp.setFont(font)
        self.labelCurTemp.setScaledContents(True)

        self.horizontalLayout.addWidget(self.labelCurTemp)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelCurTime = QLabel(self.layoutWidget)
        self.labelCurTime.setObjectName(u"labelCurTime")
        self.labelCurTime.setScaledContents(True)

        self.verticalLayout.addWidget(self.labelCurTime)

        self.labelLoc = QLabel(self.layoutWidget)
        self.labelLoc.setObjectName(u"labelLoc")
        self.labelLoc.setFont(font)
        self.labelLoc.setScaledContents(True)

        self.verticalLayout.addWidget(self.labelLoc)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelFeelsLike = QLabel(self.layoutWidget)
        self.labelFeelsLike.setObjectName(u"labelFeelsLike")
        self.labelFeelsLike.setScaledContents(True)

        self.gridLayout.addWidget(self.labelFeelsLike, 0, 0, 1, 2)

        self.labelHumidity = QLabel(self.layoutWidget)
        self.labelHumidity.setObjectName(u"labelHumidity")
        self.labelHumidity.setScaledContents(True)

        self.gridLayout.addWidget(self.labelHumidity, 1, 0, 1, 1)

        self.labelWind = QLabel(self.layoutWidget)
        self.labelWind.setObjectName(u"labelWind")
        self.labelWind.setScaledContents(True)

        self.gridLayout.addWidget(self.labelWind, 1, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 1)


        self.horizontalLayout_3.addLayout(self.gridLayout_2)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.pushButtonEnterLoc = QPushButton(self.layoutWidget)
        self.pushButtonEnterLoc.setObjectName(u"pushButtonEnterLoc")

        self.gridLayout_4.addWidget(self.pushButtonEnterLoc, 0, 0, 1, 1)

        self.pushButtonQuit = QPushButton(self.layoutWidget)
        self.pushButtonQuit.setObjectName(u"pushButtonQuit")

        self.gridLayout_4.addWidget(self.pushButtonQuit, 0, 1, 1, 1)

        self.tableWeatherAlerts = QTableView(self.layoutWidget)
        self.tableWeatherAlerts.setObjectName(u"tableWeatherAlerts")
        self.tableWeatherAlerts.verticalHeader().setVisible(False)

        self.gridLayout_4.addWidget(self.tableWeatherAlerts, 1, 0, 1, 2)


        self.horizontalLayout_3.addLayout(self.gridLayout_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tableViewHourly = QTableView(self.layoutWidget)
        self.tableViewHourly.setObjectName(u"tableViewHourly")
        self.tableViewHourly.verticalHeader().setVisible(False)

        self.horizontalLayout_2.addWidget(self.tableViewHourly)

        self.tableViewMin = QTableView(self.layoutWidget)
        self.tableViewMin.setObjectName(u"tableViewMin")
        self.tableViewMin.setAlternatingRowColors(True)
        self.tableViewMin.verticalHeader().setVisible(False)

        self.horizontalLayout_2.addWidget(self.tableViewMin)


        self.gridLayout_3.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        self.tableViewDaily = QTableView(self.layoutWidget)
        self.tableViewDaily.setObjectName(u"tableViewDaily")
        self.tableViewDaily.verticalHeader().setVisible(False)

        self.gridLayout_3.addWidget(self.tableViewDaily, 0, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_3)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Weather App", None))
        self.labelImg.setText(QCoreApplication.translate("Widget", u"TextLabel", None))
        self.labelCurTemp.setText(QCoreApplication.translate("Widget", u"127 F", None))
        self.labelCurTime.setText(QCoreApplication.translate("Widget", u"Jan 10, 00:00 (If you see this, an error occured)", None))
        self.labelLoc.setText(QCoreApplication.translate("Widget", u"Bowling Green, US", None))
        self.labelFeelsLike.setText(QCoreApplication.translate("Widget", u"Feels like 119 F. Overcast Clouds. Gentle Breeze.", None))
        self.labelHumidity.setText(QCoreApplication.translate("Widget", u"Humidity: 66%", None))
        self.labelWind.setText(QCoreApplication.translate("Widget", u"Wind: 8.1 Mph", None))
        self.pushButtonEnterLoc.setText(QCoreApplication.translate("Widget", u"Enter New Location", None))
        self.pushButtonQuit.setText(QCoreApplication.translate("Widget", u"Quit", None))
    # retranslateUi

