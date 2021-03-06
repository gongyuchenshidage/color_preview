# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import os

import vtkmodules.all as vtk
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
# from PyQt5.QtWidgets import QGridLayout, QFileDialog, QSlider
from pathlib import Path
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

import gcode
import gui_utils
import locales
import params
lines=[]
layerm=0
filename=""


class Ui_MainWindow(object):
    one_color_radio = None
    much_layers_radio = None
    mix_colors_radio = None
    one_color_item = None
    handle = None
    totalHeight = None
    namein = None
    slider = None
    def setupUi(self, MainWindow):
        global trans
        trans = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 1000)

        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("QWidge{background-color: rgb(213, 214, 255);}\n"
"")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.Layoutin = QtWidgets.QHBoxLayout()
        self.Layoutin.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.Layoutin.setSpacing(7)
        self.Layoutin.setObjectName("Layoutin")
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setStyleSheet("")
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap(":/png/icon/1137264.png"))
        self.label_7.setObjectName("label_7")
        self.Layoutin.addWidget(self.label_7)
        self.name_label = QtWidgets.QLabel(self.frame)
        self.name_label.setStyleSheet("font: 11pt \"宋体\";")
        self.name_label.setObjectName("name_label")
        self.Layoutin.addWidget(self.name_label)
        Ui_MainWindow.namein = QtWidgets.QLabel(self.frame)
        Ui_MainWindow.namein.setWordWrap(True)
        Ui_MainWindow.namein.setObjectName("namein")
        self.Layoutin.addWidget(Ui_MainWindow.namein)
        self.selectnamein = QtWidgets.QPushButton(self.frame)
        self.selectnamein.setStyleSheet("background-color: rgb(167, 210, 222);\n"
"font: 11pt \"宋体\";")
        self.selectnamein.setObjectName("selectnamein")
        _translate = QtCore.QCoreApplication.translate
        self.selectnamein.clicked.connect(self.openFile)
        self.selectnamein.setText(_translate("MainWindow", "文件目录"))
        self.Layoutin.addWidget(self.selectnamein)
        #处理进度条


        Ui_MainWindow.totalHeight = QtWidgets.QLabel(self.frame)
        Ui_MainWindow.totalHeight.setWordWrap(True)
        Ui_MainWindow.totalHeight.setObjectName("Heightshow")
        self.Layoutin.addWidget(Ui_MainWindow.totalHeight)

        self.suggestion1 = QtWidgets.QLabel(self.frame)
        self.suggestion1.setObjectName("")
        # self.suggestion1.setGeometry(1160, 35, 150, 25)
        self.suggestion1.setStyleSheet("font: 11pt \"宋体\";")
        self.Layoutin.addWidget(self.suggestion1)
        self.Layoutin.setStretch(1, 1)
        self.Layoutin.setStretch(2, 2)
        self.Layoutin.setStretch(3, 1)
        self.Layoutin.setStretch(4, 2)
        self.Layoutin.setStretch(5, 1)

        self.gridLayout_3.addLayout(self.Layoutin, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 2)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.frame_5 = QtWidgets.QFrame(self.centralwidget)
        self.frame_5.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setMidLineWidth(0)
        self.frame_5.setObjectName("frame_5")
        self.gridLayout_5.addWidget(self.frame_5, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout_5, 2, 1, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setStyleSheet("")
        self.label_11.setText("")
        self.label_11.setPixmap(QtGui.QPixmap(":/png/icon/preview.png"))
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_4.addWidget(self.label_11)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("font: 13pt \"黑体\";")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.horizontalLayout_4.setStretch(1, 19)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 1, 1, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setStyleSheet("border-color: rgb(255, 255,255);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setLineWidth(1)
        self.frame_2.setMidLineWidth(0)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        Ui_MainWindow.one_color_radio = QtWidgets.QRadioButton(self.frame_2)
        Ui_MainWindow.one_color_radio.setMouseTracking(False)
        Ui_MainWindow.one_color_radio.setStyleSheet("font: 11pt \"宋体\";")
        Ui_MainWindow.one_color_radio.setCheckable(True)
        Ui_MainWindow.one_color_radio.setChecked(False)
        Ui_MainWindow.one_color_radio.setEnabled(False)
        Ui_MainWindow.one_color_radio.setAutoRepeatInterval(99)
        Ui_MainWindow.one_color_radio.setObjectName("one_color_radio")
        self.verticalLayout.addWidget(Ui_MainWindow.one_color_radio)
        self.one_color_choose = QtWidgets.QHBoxLayout()
        self.one_color_choose.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.one_color_choose.setObjectName("one_color_choose")
        #self.one_color_choose.setEnabled(False)
        self.label_select_one_color = QtWidgets.QLabel(self.frame_2)
        self.label_select_one_color.setStyleSheet("font: 10pt \"宋体\";")
        self.label_select_one_color.setObjectName("label_select_one_color")
        self.one_color_choose.addWidget(self.label_select_one_color)
        Ui_MainWindow.one_color_item = QtWidgets.QPushButton(self.frame_2)
        Ui_MainWindow.one_color_item.setStyleSheet("\n"
"font: 10pt \"宋体\";\n")
        Ui_MainWindow.one_color_item.setObjectName("one_color_item")
        Ui_MainWindow.one_color_item.setEnabled(False)

        self.one_color_choose.addWidget(Ui_MainWindow.one_color_item)
        self.verticalLayout.addLayout(self.one_color_choose)
        self.verticalLayout.setStretch(1, 2)
        self.gridLayout_7.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_2, 0, 0, 1, 1)
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.much_layers_choose = QtWidgets.QVBoxLayout()
        self.much_layers_choose.setObjectName("much_layers_choose")
        Ui_MainWindow.much_layers_radio = QtWidgets.QRadioButton(self.frame_3)
        Ui_MainWindow.much_layers_radio.setEnabled(True)
        Ui_MainWindow.much_layers_radio.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        Ui_MainWindow.much_layers_radio.setStyleSheet("border-color: rgb(0, 0, 255);font: 11pt \"宋体\";")
        Ui_MainWindow.much_layers_radio.setAutoExclusive(False)
        Ui_MainWindow.much_layers_radio.setObjectName("much_layers_radio")
        Ui_MainWindow.much_layers_radio.setEnabled(False)
        self.much_layers_choose.addWidget(Ui_MainWindow.much_layers_radio)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.checkBox_3 = QtWidgets.QCheckBox(self.frame_3)
        self.checkBox_3.setStyleSheet("")
        self.checkBox_3.setObjectName("checkBox_3")
        self.horizontalLayout_3.addWidget(self.checkBox_3)
        self.checkBox_4 = QtWidgets.QCheckBox(self.frame_3)
        self.checkBox_4.setObjectName("checkBox_4")
        self.horizontalLayout_3.addWidget(self.checkBox_4)
        self.checkBox_3.setEnabled(False)
        self.checkBox_4.setEnabled(False)
        self.much_layers_choose.addLayout(self.horizontalLayout_3)
        self.layers_num_input = QtWidgets.QHBoxLayout()
        self.layers_num_input.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.layers_num_input.setObjectName("layers_num_input")
        self.layers_num_label = QtWidgets.QLabel(self.frame_3)
        self.layers_num_label.setStyleSheet("font: 10pt \"宋体\";")
        self.layers_num_label.setObjectName("layers_num_label")
        self.layers_num_input.addWidget(self.layers_num_label)
        self.layers_num = QtWidgets.QLineEdit(self.frame_3)
        self.layers_num.setStyleSheet("border-radius:5px;\n"
"border: 1px solid black")
        self.layers_num.setEnabled(False)
        self.layers_num.setText("")
        self.layers_num.setObjectName("layers_num")
        self.layers_num_input.addWidget(self.layers_num)
        self.much_layers_choose.addLayout(self.layers_num_input)
        self.much_layers_choose.setStretch(2, 1)

        self.much_layers_option = QtWidgets.QVBoxLayout()
        self.much_layers_choose.addLayout(self.much_layers_option)
        self.much_layers_options1 = QtWidgets.QWidget()
        self.much_layers_options1.setMinimumSize(450, 1200)
        self.scroll1 = QtWidgets.QScrollArea()
        self.much_layers_option.addWidget(self.scroll1)  # vbox.addwidget(scroll)
        self.scroll1.setWidget(self.much_layers_options1)
        self.much_layers_options = QtWidgets.QVBoxLayout()

        self.gridLayout_8.addLayout(self.much_layers_choose, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_3, 1, 0, 1, 1)
        self.frame_4 = QtWidgets.QFrame(self.centralwidget)
        self.frame_4.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.frame_4)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.mix_color_choose = QtWidgets.QVBoxLayout()
        self.mix_color_choose.setObjectName("mix_color_choose")
        Ui_MainWindow.mix_colors_radio = QtWidgets.QRadioButton(self.frame_4)
        Ui_MainWindow.mix_colors_radio.setEnabled(False)
        Ui_MainWindow.mix_colors_radio.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        Ui_MainWindow.mix_colors_radio.setStyleSheet("font: 11pt \"宋体\";")
        Ui_MainWindow.mix_colors_radio.setAutoExclusive(False)
        Ui_MainWindow.mix_colors_radio.setObjectName("mix_colors_radio")
        self.mix_color_choose.addWidget(Ui_MainWindow.mix_colors_radio)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkBox_2 = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_2.setObjectName("checkBox_2")
        self.horizontalLayout_2.addWidget(self.checkBox_2)
        self.checkBox = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_2.addWidget(self.checkBox)
        self.checkBox_2.setEnabled(False)
        self.checkBox.setEnabled(False)
        self.mix_color_choose.addLayout(self.horizontalLayout_2)
        self.mix_colors_input = QtWidgets.QHBoxLayout()
        self.mix_colors_input.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.mix_colors_input.setObjectName("mix_colors_input")
        self.mix_colors_num_label = QtWidgets.QLabel(self.frame_4)
        self.mix_colors_num_label.setStyleSheet("font: 10pt \"宋体\";")
        self.mix_colors_num_label.setObjectName("mix_colors_num_label")
        self.mix_colors_input.addWidget(self.mix_colors_num_label)
        self.mix_colors_num = QtWidgets.QLineEdit(self.frame_4)
        self.mix_colors_num.setStyleSheet("border-radius:5px;\n"
"border: 1px solid black")
        self.mix_colors_num.setText("")
        self.mix_colors_num.setObjectName("mix_colors_num")
        self.mix_colors_num.setEnabled(False)
        self.mix_colors_input.addWidget(self.mix_colors_num)
        self.mix_color_choose.addLayout(self.mix_colors_input)
        self.mix_color_choose.setStretch(2, 1)

        self.mix_colors_option = QtWidgets.QVBoxLayout()
        self.mix_color_choose.addLayout(self.mix_colors_option)  # 滚动条
        self.mix_colors_options1 = QtWidgets.QWidget()
        self.mix_colors_options1.setMinimumSize(450, 1200)
        self.scroll2 = QtWidgets.QScrollArea()
        self.mix_colors_option.addWidget(self.scroll2)  # vbox.addwidget(scroll)
        self.scroll2.setWidget(self.mix_colors_options1)
        self.mix_colors_options = QtWidgets.QVBoxLayout()

        self.gridLayout_9.addLayout(self.mix_color_choose, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_4, 2, 0, 1, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(2, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setStyleSheet("")
        self.label_9.setText("")
        self.label_9.setTextFormat(QtCore.Qt.MarkdownText)
        self.label_9.setPixmap(QtGui.QPixmap(":/png/icon/set.png"))
        self.label_9.setObjectName("label_9")
        self.horizontalLayout.addWidget(self.label_9)

        self.locale = locales.getLocale()
        self.main_grid = QVBoxLayout(self.frame_5)
        self.main_grid.addWidget(self.init3dWidget())
        Ui_MainWindow.slider = QSlider(Qt.Horizontal)
        Ui_MainWindow.slider.setEnabled(False)
        self.main_grid.addWidget(Ui_MainWindow.slider)

        self.label_8 = QLabel("0")
        # self.label_11.setFont(QFont('Arial Black', 20))
        self.label_8.setAlignment(Qt.AlignCenter)
        self.main_grid.addWidget(self.label_8)

        self.planeActor = gui_utils.createPlaneActorCircle(params.PlaneCenter)
        self.planeTransform = vtk.vtkTransform()
        self.render.AddActor(self.planeActor)
        self.render.ResetCamera()

        self.planes = []
        self.planesActors = []


        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setStyleSheet("font: 13pt \"黑体\";\n"
"font: 13pt \"黑体\";")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.horizontalLayout.setStretch(1, 19)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")



        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_6.addWidget(self.label)
        self.suggestion = QtWidgets.QLabel(self.centralwidget)
        #self.suggestion.setObjectName("label_10")
        self.horizontalLayout_6.addWidget(self.suggestion)
        self.suggestion.setStyleSheet("font: 11pt \"宋体\";")
        Ui_MainWindow.handle = QtWidgets.QPushButton(self.centralwidget)
        Ui_MainWindow.handle.setLayoutDirection(QtCore.Qt.LeftToRight)
        Ui_MainWindow.handle.setStyleSheet("font: 12pt \"宋体\";\n"
"background-color: rgb(167, 210, 222);\n"
"\n"
"\n"
"border-radius:25px")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/png/icon/deal small.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.handle.setIcon(icon)
        self.handle.setObjectName("handle")
        self.horizontalLayout_6.addWidget(Ui_MainWindow.handle)
        Ui_MainWindow.handle.setEnabled(False)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_6.addWidget(self.label_2)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_6.addWidget(self.label_6)
        self.gridLayout_2.addLayout(self.horizontalLayout_6, 4, 0, 1, 2)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 968, 26))
        self.menubar.setStyleSheet("background-color: rgb(85, 170, 255,180);")
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setStyleSheet("background-color: rgb(234, 234, 234);")
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setStyleSheet("background-color: rgb(234, 234, 234);")
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setStyleSheet("background-color: rgb(234, 234, 234);")
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setStyleSheet("background-color: rgb(234, 234, 234);")
        self.menu_4.setObjectName("menu_4")
        self.menu_CMY = QtWidgets.QMenu(self.menubar)
        self.menu_CMY.setStyleSheet("background-color: rgb(234, 234, 234);")
        self.menu_CMY.setObjectName("menu_CMY")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        # self.actionOpen = QtWidgets.QAction(MainWindow)
        # self.actionOpen.setObjectName("actionOpen")
        # self.actionClose = QtWidgets.QAction(MainWindow)
        # self.actionClose.setObjectName("actionClose")
        # self.actionSave = QtWidgets.QAction(MainWindow)
        # self.actionSave.setObjectName("actionSave")
        # self.actionQuit = QtWidgets.QAction(MainWindow)
        # self.actionQuit.setObjectName("actionQuit")
        # self.actionPath = QtWidgets.QAction(MainWindow)
        # self.actionPath.setObjectName("actionPath")
        # self.actionAbout_Us = QtWidgets.QAction(MainWindow)
        # self.actionAbout_Us.setObjectName("actionAbout_Us")
        self.actionColor_Select = QtWidgets.QAction(MainWindow)
        self.actionColor_Select.setObjectName("actionColor_Select")
        # self.menu.addAction(self.actionOpen)
        # self.menu.addAction(self.actionClose)
        # self.menu.addAction(self.actionSave)
        # self.menu.addAction(self.actionQuit)
        # self.menu_2.addAction(self.actionPath)
        # self.menu_4.addAction(self.actionAbout_Us)
        self.menu_CMY.addAction(self.actionColor_Select)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menubar.addAction(self.menu_CMY.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "3D打印切片后处理应用软件"))
        MainWindow.setToolTip(_translate("MainWindow", "Designed By Yu"))
        Ui_MainWindow.one_color_radio.setText(_translate("MainWindow", "单色打印"))
        self.label_select_one_color.setText(_translate("MainWindow", "选择的颜色"))
        Ui_MainWindow.one_color_item.setText(_translate("MainWindow", "选择的颜色"))
        self.much_layers_radio.setText(_translate("MainWindow", "分层彩色打印"))
        self.checkBox_3.setText(_translate("MainWindow", "平均分层"))
        self.checkBox_4.setText(_translate("MainWindow", "自定义分层"))
        self.layers_num_label.setText(_translate("MainWindow", "分段数"))
        Ui_MainWindow.mix_colors_radio.setText(_translate("MainWindow", "渐变打印"))
        self.checkBox_2.setText(_translate("MainWindow", "平均渐变"))
        self.checkBox.setText(_translate("MainWindow", "自定义渐变"))
        self.mix_colors_num_label.setText(_translate("MainWindow", "渐变次数"))
        Ui_MainWindow.handle.setText(_translate("MainWindow", " 处理"))
        self.name_label.setText(_translate("MainWindow", "选择的文件"))
        Ui_MainWindow.namein.setText(_translate("MainWindow", ""))
        Ui_MainWindow.totalHeight.setText(_translate("MainWindow", ""))
        self.label_4.setText(_translate("MainWindow", "打印模式"))
        self.label_5.setText(_translate("MainWindow", "模型预览"))
        # self.pushButton.setText(_translate("MainWindow", "预览"))
        # self.menu.setTitle(_translate("MainWindow", "开始"))
        # self.menu_2.setTitle(_translate("MainWindow", "设置"))
        # self.menu_3.setTitle(_translate("MainWindow", "帮助"))
        # self.menu_4.setTitle(_translate("MainWindow", "关于"))
        self.menu_CMY.setTitle(_translate("MainWindow", "自定义CMY"))
        # self.actionOpen.setText(_translate("MainWindow", "Open"))
        # self.actionClose.setText(_translate("MainWindow", "Close"))
        # self.actionSave.setText(_translate("MainWindow", "Save"))
        # self.actionQuit.setText(_translate("MainWindow", "Quit"))
        # self.actionPath.setText(_translate("MainWindow", "Path"))
        # self.actionAbout_Us.setText(_translate("MainWindow", "About Us"))
        self.actionColor_Select.setText(_translate("MainWindow", "Color_Setting"))

    def init3dWidget(self):
        widget3d = QVTKRenderWindowInteractor()
        widget3d.Initialize()
        widget3d.Start()
        self.render = vtk.vtkRenderer()
        self.render.SetBackground(params.BackgroundColor)
        widget3d.GetRenderWindow().AddRenderer(self.render)
        self.interactor = widget3d.GetRenderWindow().GetInteractor()
        self.interactor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()
        self.axesWidget = gui_utils.createAxes(self.interactor)
        return widget3d

    def loadSTL(self, filename, method=gui_utils.createStlActorInOrigin):
        self.stlActor, self.stlTranslation, self.stlBounds = method(filename)
        # self.xPosition_value.setText(str(self.stlTranslation[0])[:10])
        # self.yPosition_value.setText(str(self.stlTranslation[1])[:10])
        # self.zPosition_value.setText(str(self.stlTranslation[2])[:10])

        self.clearScene()
        self.planeActor = gui_utils.createPlaneActorCircle(params.PlaneCenter)
        self.render.AddActor(self.planeActor)

        self.render.AddActor(self.stlActor)
        # self.bottom_panel.setEnabled(True)
        # self.loadPlanes()
        # self.stateStl()
        self.openedStl = filename
        self.render.ResetCamera()
        self.reloadScene()

    def process_change1(self):  # 导入文件进度条
        global count1
        global vv1
        global vv2
        global fileopen
        global set
        global timer1
        global step
        global trans
        # global rm
        # global rm1

        #count1 = 0
        step += 1
        if (count1 == 0):
            for i in range(3333):
                fileopen.setValue(i)
            count1 += 1
        if (vv1 == True):
            for i in range(3333, 6666):
                fileopen.setValue(i)
            vv1 = False
        if (vv2 == True):
            for i in range(6666, 10001):
                fileopen.setValue(i)
            vv2 = False
            count1 = 0
            rm1 = trans.findChild((QProgressBar,), "fileopen")
            rm1.setParent(None)
            timer1.stop()
            _translate = QtCore.QCoreApplication.translate
            self.suggestion1.setText(_translate("MainWindow", "导入文件成功！"))
        if step > 10:
            timer1.stop()
            self.suggestion1.setText(_translate("MainWindow", "导入文件失败！"))
            rm = trans.findChild((QProgressBar,), "fileopen")
            rm.setParent(None)
            step = 0

        # for i in range(9999):
        # process.setValue(i)

    def loading1(self):
        global fileopen
        global timer1
        global step
        global count1
        count1 = 0
        step = 0

        fileopen = QtWidgets.QLabel(self.frame)
        fileopen = QProgressBar(trans)
        fileopen.setObjectName("fileopen")

        # fileopen= QtWidgets.QLabel(self.frame)

        fileopen.setGeometry(200, 115, 300, 20)
        # self.fileopen.setGeometry(220, 20, 921, 61)
        # print(trans)
        #    process.setWindowFlags(QtCore.Qt.WindowCloseButtonHint|QtCore.Qt.WindowContextHelpButtonHint)
        timer1 = QTimer(fileopen)
        fileopen.setRange(0, 10000)
        # fileopen.setAutoClose(True)
        fileopen.show()
        timer1.start(1000)
        timer1.timeout.connect(self.process_change1)

    def openFile(self):
        base = False
        base1 = False
        base2 = False
        base3 = False
        base4 = False
        base5 = False
        base6 = False

        global lines
        global layerm
        global filename
        global process
        global fileopen
        global vv1
        global vv2
        vv1 = False
        vv2 = False

        filename = str(
            QFileDialog.getOpenFileName(None, self.locale.OpenModel, ",",
                                        "GCODE(*.gcode);;STL(*.stl)")[0])  # TODO: fix path

        if filename != "":
            layerm = 0
            # self.planes = []
            fileExt = os.path.splitext(filename)[1].upper()
            filename = str(Path(filename))
            if fileExt == ".STL":
                try:
                    self.loadSTL(filename)
                    QApplication.processEvents()
                    Ui_MainWindow.one_color_radio.setEnabled(False)
                    Ui_MainWindow.much_layers_radio.setEnabled(False)
                    Ui_MainWindow.mix_colors_radio.setEnabled(False)
                    Ui_MainWindow.one_color_item.setEnabled(False)
                    Ui_MainWindow.handle.setEnabled(False)
                    _translate = QtCore.QCoreApplication.translate
                    Ui_MainWindow.totalHeight.setText(_translate("MainWindow", ""))
                    Ui_MainWindow.namein.setText(_translate("MainWindow", ""))
                except:
                    self.exception_handling("stl文件导入失败")

                    # global fileopen
            elif fileExt == ".GCODE":
                try:
                    self.suggestion1.setText(" ")
                    self.suggestion.setText(" ")

                    self.loading1()
                    self.layer_add(filename)
                    vv1 = True
                    #self.loading1()

                    print("loading")
                    self.loadGCode(filename, False)
                    QApplication.processEvents()
                    vv2 = True
                    print("loading")
                    with open(filename) as file1:
                        lines = file1.readlines()
                        for i in range(len(lines)):
                            if (";LAYER" in lines[i] and "COUNT" not in lines[i]):
                                layerm += 1
                                base = True
                            if ("Generated with Cura_SteamEngine" in lines[i]):
                                base1 = True
                                indexa = i
                            if ("PrusaSlicer" in lines[i]):
                                base2 = True
                            if base2:
                                if (lines[i].startswith("; layer_height")):
                                    base5 = True
                                if (lines[i].startswith("; first_layer_height")):
                                    base6 = True

                        for i in range(len(lines)):
                            if base1:
                                # print(i)
                                if (";MINZ:" in lines[i]):
                                    # print(i)
                                    base3 = True
                                    continue
                                if (";Layer height:" in lines[i]):
                                    base4 = True
                    #vv2 = True
                    if not ((base2 and base5 and base6) or (base3 and base4)):
                        raise Exception


                    Ui_MainWindow.one_color_radio.setEnabled(True)
                    Ui_MainWindow.much_layers_radio.setEnabled(True)
                    Ui_MainWindow.mix_colors_radio.setEnabled(True)
                    _translate = QtCore.QCoreApplication.translate
                    Ui_MainWindow.totalHeight.setText(_translate("MainWindow", "您选择的Gcode共有%i层" % layerm))

                    Ui_MainWindow.namein.setText(_translate("MainWindow", "%s" % filename))
                    Ui_MainWindow.slider.setEnabled(True)
                    Ui_MainWindow.slider.setMinimum(1)
                    Ui_MainWindow.slider.setMaximum(layerm)
                    Ui_MainWindow.slider.setSingleStep(1)
                    Ui_MainWindow.slider.setValue(1)
                    Ui_MainWindow.slider.valueChanged.connect(self.valueChange)

                    # Ui_MainWindow.slider.valueChanged.connect(self.loading1)

                except:
                    self.exception_handling("gcode文件导入失败")

            else:
                print("This file format isn't supported:", fileExt)
        # except IOError as e:
        # print("Error during file opening:", e)

    def exception_handling(self, suggestion):
        _translate = QtCore.QCoreApplication.translate
        self.suggestion1.setText(_translate("MainWindow", suggestion))
        self.handle.setEnabled(False)
        self.checkBox_4.setChecked(False)
        self.checkBox.setChecked(False)
        self.checkBox_2.setChecked(False)
        self.checkBox_3.setChecked(False)
        self.checkBox_3.setEnabled(False)
        self.checkBox.setEnabled(False)
        self.checkBox_2.setEnabled(False)
        self.checkBox_4.setEnabled(False)
        Ui_MainWindow.one_color_radio.setChecked(False)
        Ui_MainWindow.one_color_radio.setEnabled(False)
        Ui_MainWindow.much_layers_radio.setChecked(False)
        Ui_MainWindow.much_layers_radio.setEnabled(False)
        Ui_MainWindow.mix_colors_radio.setChecked(False)
        Ui_MainWindow.mix_colors_radio.setEnabled(False)
        self.layers_num.setText("")
        self.mix_colors_num.setText("")
        self.layers_num.setEnabled(False)
        self.mix_colors_num.setEnabled(False)
        self.slider.setEnabled(False)
        Ui_MainWindow.totalHeight.setText(_translate("MainWindow", " "))
        Ui_MainWindow.namein.setText(_translate("MainWindow", " "))

    def open_gcode(self, nameout):
        layerm1 = 0
        self.loadGCode(nameout, False)
        with open(nameout) as file1:
            lines = file1.readlines()
            for i in range(len(lines)):
                if (";LAYER" in lines[i] and "COUNT" not in lines[i]):
                    layerm1 += 1
        # print(layerm1)
        Ui_MainWindow.one_color_radio.setEnabled(True)
        Ui_MainWindow.much_layers_radio.setEnabled(True)
        Ui_MainWindow.mix_colors_radio.setEnabled(True)
        _translate = QtCore.QCoreApplication.translate
        Ui_MainWindow.totalHeight.setText(_translate("MainWindow", "您选择的Gcode共有%i层" % layerm1))
        Ui_MainWindow.namein.setText(_translate("MainWindow", "%s" % nameout))
        Ui_MainWindow.slider.setEnabled(True)
        Ui_MainWindow.slider.setMinimum(1)
        Ui_MainWindow.slider.setMaximum(layerm1)
        Ui_MainWindow.slider.setSingleStep(1)
        Ui_MainWindow.slider.setValue(1)
        Ui_MainWindow.slider.valueChanged.connect(self.valueChange)

    def valueChange(self):
        try:
            size = Ui_MainWindow.slider.value()
            self.label_8.setText(str(size))
            # layers2 = []
            # color2 = []
            # divide = []
            actors2 = []

            for i in range(size):
                actors2.append(self.actors[i])
            for a in range(len(actors2)):
                if len(self.gode.color) == 0:
                    actors2[a].GetProperty().SetColor(params.LastLayerColor)
                elif len(self.gode.color) == 1:
                    actors2[a].GetProperty().SetColor(self.gode.color[0][0] / 255, self.gode.color[0][1] / 255,
                                                      self.gode.color[0][2] / 255)
                elif len(self.gode.color) > 1:
                    for i in range(len(self.gode.color)):
                        if self.gode.divide[i] <= a < self.gode.divide[i + 1]:
                            actors2[a].GetProperty().SetColor(self.gode.color[i][0] / 255, self.gode.color[i][1] / 255,
                                                              self.gode.color[i][2] / 255)

            actors2[-1].GetProperty().SetColor(params.LayerColor)
            # if len(self.gode.color) == 0:
            #     blocks2 = gui_utils.makeBlocks(layers2)
            #     self.actors = gui_utils.wrapWithActors(blocks2, self.gode.rotations, self.gode.lays2rots,color2)#None不能使用len方法
            # if len(self.gode.color) == 1:
            #     color2.append(self.gode.color[0])
            #     blocks2 = gui_utils.makeBlocks(layers2)
            #     self.actors = gui_utils.wrapWithActors(blocks2, self.gode.rotations, self.gode.lays2rots,color2)
            # if len(self.gode.color)>1:
            #     for i in range(len(self.gode.color)):
            #         for layer in range (self.gode.divide[i],self.gode.divide[i+1]):
            #             if layer == size-1:
            #                 for a in range(i+1):
            #                     color2.append(self.gode.color[a])
            #                     divide.append(self.gode.divide[a])
            #                 divide.append(self.gode.divide[i+1])
            #                 print(color2,divide,size)
            #     blocks2 = gui_utils.makeBlocks(layers2)
            #     self.actors = gui_utils.wrapWithActors(blocks2, self.gode.rotations, self.gode.lays2rots, color2,divide)

            self.clearScene()
            self.render.AddActor(self.planeActor)

            for actor in actors2:
                self.render.AddActor(actor)

            # self.loadPlanes()
            # self.bottom_panel.setEnabled(False)

            # if addStl:
            #     self.stateBoth(len(self.actors))
            # else:
            #     self.stateGcode(len(self.actors))

            self.openedGCode = filename
            self.reloadScene()
            QApplication.processEvents()
        except:
            self.exception_handling("分层预览失败")

    def loadGCode(self, filename, addStl):
        QApplication.processEvents()
        try:
            gode = gcode.readGCode(filename)
            print("++++++*******")
            self.gode = gode
        except:
            self.exception_handling("gcode文件解析失败")

        try:
            blocks = gui_utils.makeBlocks(self.gode.layers)
            self.blocks = blocks
            print(len(blocks))
        except:
            self.exception_handling("面片生成失败")
        try:
            self.actors = gui_utils.wrapWithActors(self.blocks, self.gode.rotations, self.gode.lays2rots,
                                                   self.gode.color, self.gode.divide)
            self.clearScene()
            self.planeActor = gui_utils.createPlaneActorCircle(self.gode.center)
            self.render.AddActor(self.planeActor)
            if addStl:
                self.render.AddActor(self.stlActor)

            self.rotatePlane(self.gode.rotations[-1])
            for actor in self.actors:
                self.render.AddActor(actor)

            # self.loadPlanes()
            # self.bottom_panel.setEnabled(False)

            # if addStl:
            #     self.stateBoth(len(self.actors))
            # else:
            #     self.stateGcode(len(self.actors))

            self.openedGCode = filename
            self.render.ResetCamera()
            self.reloadScene()
        except:
            self.exception_handling("文件渲染失败")

    def clearScene(self):
        self.render.RemoveAllViewProps()

    def reloadScene(self):
        self.render.Modified()
        self.interactor.Render()

    def rotatePlane(self, rotation):
        transform = vtk.vtkTransform()
        transform.PostMultiply()
        transform.RotateZ(rotation.z_rot)
        transform.PostMultiply()
        transform.RotateX(rotation.x_rot)
        self.planeActor.SetUserTransform(transform)
        self.planeTransform = transform

    def layer_add(self, input_file_name):
        with open(input_file_name, "r+") as f:
            linestoedit = f.readlines()
            j = -1

            for i in range(len(linestoedit)):
                if "Generated with Cura_SteamEngine" in linestoedit[i]:
                    break
                if linestoedit[i].startswith("G1") and 'E' not in linestoedit[i]:
                    linestoedit[i] = linestoedit[i].replace("G1", "G0")
                if 'G0' in linestoedit[i] and 'Z' in linestoedit[i] and 'F' in linestoedit[i] and 'nozzle' not in \
                        linestoedit[i]:
                    j += 1
                    linestoedit[i] = linestoedit[i].replace(linestoedit[i],
                                                            ";LAYER:" + "{}".format(j) + "\n" + linestoedit[i])
            #count = "LAYER_COUNT:{}".format(j)
            m = len(linestoedit)
            self.save_3rfile(input_file_name, linestoedit, m)
    def save_3rfile(self, inputfilename, linestoedit,m):
        with open(inputfilename, "w+") as fw:
            for i in range(m):
                fw.write(linestoedit[i])
            # fw.write('\n' + ';' + count)
            # f.close()
import resource_rc


