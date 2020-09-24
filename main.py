'''
function: Plugin for edit the gcode given by user
author:Yu Shengnan, Qiu Wen, Gong Yuchen, Xu Zhe, Chen Ting
date:2020-7-22
type:Gcode
return:Gcode
'''
import os
import json
import re
import sys
import time
from functools import partial

from PyQt5 import QtWidgets, QtCore, sip
from PyQt5.QtCore import Qt,QTimer

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLineEdit, QLabel, QMessageBox, QHBoxLayout
from pathlib import Path
from untitled import Ui_MainWindow
import locales
import Color_Setting
import untitled
import Color_Select
import resource_rc

global d
#global info1
info1 = [
    {'C': 0, 'M': 0, 'Y': 0, 'R': 0, 'G': 0, 'B': 0},
    {'C': 0, 'M': 0, 'Y': 0, 'R': 0, 'G': 0, 'B': 0},
    {'C': 0, 'M': 0, 'Y': 0, 'R': 0, 'G': 0, 'B': 0},
    {'C': 0, 'M': 0, 'Y': 0, 'R': 0, 'G': 0, 'B': 0},
    {'C': 0, 'M': 0, 'Y': 0, 'R': 0, 'G': 0, 'B': 0},
    {'C': 0, 'M': 0, 'Y': 0, 'R': 0, 'G': 0, 'B': 0},
    {'C': 0, 'M': 0, 'Y': 0, 'R': 0, 'G': 0, 'B': 0},
    {'C': 0, 'M': 0, 'Y': 0, 'R': 0, 'G': 0, 'B': 0},
    {'C': 0, 'M': 0, 'Y': 0, 'R': 0, 'G': 0, 'B': 0},
    {'C': 0, 'M': 0, 'Y': 0, 'R': 0, 'G': 0, 'B': 0},
    {'C': 0, 'M': 0, 'Y': 0, 'R': 0, 'G': 0, 'B': 0},
    {'C': 0, 'M': 0, 'Y': 0, 'R': 0, 'G': 0, 'B': 0},
    {'C': 0, 'M': 0, 'Y': 0, 'R': 0, 'G': 0, 'B': 0},
    {'C': 0, 'M': 0, 'Y': 0, 'R': 0, 'G': 0, 'B': 0},
    {'C': 0, 'M': 0, 'Y': 0, 'R': 0, 'G': 0, 'B': 0},
    {'C': 0, 'M': 0, 'Y': 0, 'R': 0, 'G': 0, 'B': 0},
    {'C': 0, 'M': 0, 'Y': 0, 'R': 0, 'G': 0, 'B': 0},
    {'C': 0, 'M': 0, 'Y': 0, 'R': 0, 'G': 0, 'B': 0},
    {'C': 0, 'M': 0, 'Y': 0, 'R': 0, 'G': 0, 'B': 0},
    {'C': 0, 'M': 0, 'Y': 0, 'R': 0, 'G': 0, 'B': 0},
    {'C': 0, 'M': 0, 'Y': 0, 'R': 0, 'G': 0, 'B': 0},
    {'C': 0, 'M': 0, 'Y': 0, 'R': 0, 'G': 0, 'B': 0},
    {'C': 0, 'M': 0, 'Y': 0, 'R': 0, 'G': 0, 'B': 0},
    {'C': 0, 'M': 0, 'Y': 0, 'R': 0, 'G': 0, 'B': 0}]

colorflag = [""]
def Prusagetvalue(layer,key,default= None):
    if key not in layer :
        return default
    subPart = layer[(layer.find(key) + len(key)):]
    m = re.search("^[-]?[0-9]*\.?[0-9]*",subPart)

    if m == None:
        return default
    try:
        return float(m.group(0))
    except:
        return default

def getValue(layer, key, default=None):  # replace default getvalue due to comment-reading feature
    if not key in layer or (";" in layer and layer.find(key) > layer.find(";") and not ";ChangeAtZ" in key and not ";LAYER:" in key):
        return default
    subPart = layer[layer.find(key) + len(key):]
    m = re.search("^[-]?[0-9]*\.?[0-9]*", subPart)

    if m == None:
        return default
    try:
        return float(m.group(0))
    except:
        return default

def Prusafindtotalheight(layerData):
    if "G1" in layerData and "Z" in layerData:
        foundZ = Prusagetvalue(layerData,"Z",-1)
        if foundZ != -1:
            return float(foundZ)
    return -1

def findTotalHeight(layerData):
    if ("G1" in layerData or "G0" in layerData) and "Z" in layerData :
        foundZ = getValue(layerData,"Z",-1)
        if foundZ != -1:
            return  float(foundZ)
    return -1

def material_chose(user_R,user_G,user_B):
    """挤料比例模块"""
    info = [{'C': 98, 'M': 1, 'Y': 1, 'R': 128, 'G': 199, 'B': 217},
            {'C': 89, 'M': 10, 'Y': 1, 'R': 153, 'G': 185, 'B': 215},
            {'C': 79, 'M': 20, 'Y': 1, 'R': 160, 'G': 144, 'B': 191},
            {'C': 69, 'M': 30, 'Y': 1, 'R': 172, 'G': 136, 'B': 188},
            {'C': 59, 'M': 40, 'Y': 1, 'R': 175, 'G': 112, 'B': 172},
            {'C': 49, 'M': 50, 'Y': 1, 'R': 179, 'G': 94, 'B': 161},
            {'C': 39, 'M': 60, 'Y': 1, 'R': 190, 'G': 92, 'B': 165},
            {'C': 29, 'M': 70, 'Y': 1, 'R': 195, 'G': 93, 'B': 167},
            {'C': 19, 'M': 80, 'Y': 1, 'R': 210, 'G': 95, 'B': 170},
            {'C': 9, 'M': 90, 'Y': 1, 'R': 225, 'G': 104, 'B': 181},

            {'C': 1, 'M': 98, 'Y': 1, 'R': 244, 'G': 104, 'B': 193},
            {'C': 1, 'M': 89, 'Y': 10, 'R': 232, 'G': 112, 'B': 163},
            {'C': 1, 'M': 79, 'Y': 20, 'R': 227, 'G': 107, 'B': 142},
            {'C': 1, 'M': 69, 'Y': 30, 'R': 223, 'G': 101, 'B': 129},
            {'C': 1, 'M': 59, 'Y': 40, 'R': 225, 'G': 109, 'B': 128},
            {'C': 1, 'M': 49, 'Y': 50, 'R': 224, 'G': 118, 'B': 127},
            {'C': 1, 'M': 39, 'Y': 60, 'R': 223, 'G': 124, 'B': 120},
            {'C': 1, 'M': 29, 'Y': 70, 'R': 223, 'G': 137, 'B': 116},
            {'C': 1, 'M': 19, 'Y': 80, 'R': 225, 'G': 159, 'B': 113},
            {'C': 1, 'M': 9, 'Y': 90, 'R': 226, 'G': 179, 'B': 96},

            {'C':1, 'M':1, 'Y':98, 'R':223, 'G':215, 'B':89},
            {'C':10, 'M':1, 'Y':89, 'R':214, 'G':213, 'B':88},
            {'C':20, 'M':1, 'Y':79, 'R':194, 'G':211, 'B':105},
            {'C':30, 'M':1, 'Y':69, 'R':177, 'G':202, 'B':108},
            {'C':40, 'M':1, 'Y':59, 'R':169, 'G':203, 'B':126},
            {'C':50, 'M':1, 'Y':49, 'R':161, 'G':200, 'B':138},
            {'C':60, 'M':1, 'Y':39, 'R':153, 'G':195, 'B':145},
            {'C':70, 'M':1, 'Y':29, 'R':140, 'G':191, 'B':154},
            {'C':80, 'M':1, 'Y':19, 'R':141, 'G':197, 'B':168},
            {'C':90, 'M':1, 'Y':9, 'R':137, 'G':199, 'B':190},

            {'C':80, 'M':10, 'Y':10, 'R':138, 'G':145, 'B':129},
            {'C':70, 'M':20, 'Y':10, 'R':141, 'G':111, 'B':113},
            {'C':60, 'M':30, 'Y':10, 'R':149, 'G':91, 'B':106},
            {'C':50, 'M':40, 'Y':10, 'R':154, 'G':71, 'B':94},
            {'C':40, 'M':50, 'Y':10, 'R':163, 'G':63, 'B':89},
            {'C':30, 'M':60, 'Y':10, 'R':168, 'G':54, 'B':80},
            {'C':20, 'M':70, 'Y':10, 'R':178, 'G':50, 'B':77},
            {'C':10, 'M':80, 'Y':10, 'R':187, 'G':44, 'B':77},
            {'C':70, 'M':10, 'Y':20, 'R':152, 'G':150, 'B':110},

            {'C': 60, 'M': 20, 'Y': 20, 'R': 158, 'G': 131, 'B': 117},
            {'C': 50, 'M': 30, 'Y': 20, 'R': 173, 'G': 120, 'B': 118},
            {'C': 40, 'M': 40, 'Y': 20, 'R': 181, 'G': 110, 'B': 116},
            {'C': 30, 'M': 50, 'Y': 20, 'R': 177, 'G': 88, 'B': 98},
            {'C': 20, 'M': 60, 'Y': 20, 'R': 187, 'G': 76, 'B': 92},
            {'C': 10, 'M': 70, 'Y': 20, 'R': 193, 'G': 69, 'B': 90},
            {'C': 60, 'M': 10, 'Y': 30, 'R': 160, 'G': 161, 'B': 114},
            {'C': 50, 'M': 20, 'Y': 30, 'R': 171, 'G': 131, 'B': 106},
            {'C': 40, 'M': 30, 'Y': 30, 'R': 183, 'G': 122, 'B': 101},

            {'C': 30, 'M': 40, 'Y': 30, 'R': 173, 'G': 88, 'B': 80},
            {'C': 20, 'M': 50, 'Y': 30, 'R': 184, 'G': 84, 'B': 80},
            {'C': 10, 'M': 60, 'Y': 30, 'R': 182, 'G': 74, 'B': 80},
            {'C': 50, 'M': 10, 'Y': 40, 'R': 158, 'G': 155, 'B': 86},
            {'C': 40, 'M': 20, 'Y': 40, 'R': 171, 'G': 129, 'B': 83},
            {'C': 30, 'M': 30, 'Y': 40, 'R': 178, 'G': 104, 'B': 78},
            {'C': 20, 'M': 40, 'Y': 40, 'R': 182, 'G': 93, 'B': 70},
            {'C': 10, 'M': 50, 'Y': 40, 'R': 192, 'G': 82, 'B': 72},
            {'C': 40, 'M': 10, 'Y': 50, 'R': 172, 'G': 152, 'B': 65},

            {'C': 30, 'M': 20, 'Y': 50, 'R': 174, 'G': 126, 'B': 85},
            {'C': 20, 'M': 30, 'Y': 50, 'R': 179, 'G': 108, 'B': 86},
            {'C': 10, 'M': 40, 'Y': 50, 'R': 188, 'G': 91, 'B': 78},
            {'C': 30, 'M': 10, 'Y': 60, 'R': 168, 'G': 146, 'B': 78},
            {'C': 20, 'M': 20, 'Y': 60, 'R': 179, 'G': 120, 'B': 76},
            {'C': 10, 'M': 30, 'Y': 60, 'R': 190, 'G': 104, 'B': 74},
            {'C': 20, 'M': 10, 'Y': 70, 'R': 187, 'G': 149, 'B': 65},
            {'C': 10, 'M': 20, 'Y': 70, 'R': 197, 'G': 128, 'B': 63},
            {'C': 10, 'M': 10, 'Y': 80, 'R': 206, 'G': 162, 'B': 59}]
    for i in info:
        if  user_R == i['R'] and user_G == i['G'] and user_B == i['B']:
            materials = "M165 A{} B{} C{}".format(i['C'], i['M'], i['Y'])
            materials2 = "{},{},{}".format(i['C'], i['M'], i['Y'])
            materials3 = [materials,materials2]
            return  materials3

def one_color_printing_active(linestoedit, R, G, B, color_back_number):
    instruction = ""
    j = 0
    if color_back_number[0] == 1:
        for ii in info1:
            if int(R) == ii["R"] and int(G) == ii["G"] and int(B) == ii["B"]:
                instruction = "M165 A{} B{} C{}".format(ii['C'], ii['M'], ii['Y'])
    else:
        instruction = material_chose(R, G, B)[0]
    for i in range(len(linestoedit)):
        if (";LAYER" in linestoedit[i] and "COUNT" not in linestoedit[i]):
            j += 1
            if (j == 2):
                break
            linestoedit[i] = linestoedit[i].replace(linestoedit[i], instruction + "\n" + linestoedit[i])
            QApplication.processEvents()
    m = len(linestoedit)
    savefile(linestoedit)

def mutiple_color_printing_active(linestoedit,number,color_back_number):
#    print(color_back_number)
    instruction = ""
    layer = 0
    a = [0 for _ in range(len(number))]
    color_index = 0
    flag = 1
    number_count = 1
    for i in range(len(linestoedit)):
        if (";LAYER" in linestoedit[i] and "COUNT" not in linestoedit[i]):
            if color_back_number[color_index] == 1:
                for ii in info1:
                    if float(number[color_index][2]) == ii["R"] and float(number[color_index][3]) == ii["G"] and float(
                            number[color_index][4]) == ii["B"]:
                        instruction = "M165 A{} B{} C{}".format(ii['C'], ii['M'], ii['Y'])
            else:
                instruction = material_chose(float(number[color_index][2]), float(number[color_index][3]),
                                             float(number[color_index][4]))[0]
            flag += 1
            if flag == number[number_count][0]:
                color_index += 1
                number_count += 1
                if number_count == len(number):
                    number_count = len(number) - 1
            for item in range(len(number)):
                if (layer >= int(number[item][0]) and layer <= int(number[item][1])):
                    a[item] += 1
                    if (a[item] >= 2):
                        continue
                    # instruction = material_chose(int(number[item][2]), int(number[item][3]), int(number[item][4]))[0]
                    linestoedit[i] = linestoedit[i].replace(linestoedit[i], instruction + "\n" + linestoedit[i])
                    QApplication.processEvents()
            layer += 1
    m = len(linestoedit)
    savefile(linestoedit)

def Gradientprinting_active(linestoedit,color_start, color_stop,color_start_10,color_stop_10):
    gradient_line = ""
    global total
    start_time = time.process_time()
    n = len(linestoedit)#源文件行数
        #RGB2CMY
    color_back_number = [color_start_10,color_stop_10]
    color_all = [color_start,color_stop]
    for i in range(len(color_back_number)):
        for ii in range(len(color_back_number[i])):
            if color_back_number[i][ii] == 1:
                for i3 in info1:
                    if color_all[i][ii][0] == i3['R'] and color_all[i][ii][1] == i3['G'] and color_all[i][ii][2] == i3['B']:
                        materials2 = "{},{},{}".format(i3['C'], i3['M'], i3['Y'])
                        instruction = materials2.split(",")
                        a = [float(instruction[0]), float(instruction[1]), float(instruction[2])]
                        color_all[i][ii] = list(map(lambda x: x / sum(a), a))
            else:
                instruction_1 = material_chose(color_all[i][ii][0], color_all[i][ii][1], color_all[i][ii][2])[1].split(",")
                b = [float(instruction_1[0]), float(instruction_1[1]), float(instruction_1[2])]
                color_all[i][ii] = list(map(lambda x: x / sum(b), b))
    totalHeight = -1
    current_layer = len(linestoedit) - 1
    while totalHeight == -1:
        layer_1 = linestoedit[current_layer]
        totalHeight = findTotalHeight(layer_1)
        if (totalHeight > -1):
            break
        current_layer -= 1
    height_step = totalHeight / len(color_start)
    color_index = 0
    z = 0
    x = None
    y = None
    current_z = 0
    z_changed = False
    insert_gradient = True
    for i in range(len(linestoedit)):
        total = 0
        z_changed = False
        line_index = i
        if ("G0" in linestoedit[i] or "G1" in linestoedit[i]) and "Z" in linestoedit[i]:
            newZ = getValue(linestoedit[i], "Z", z)
            current_z = newZ
            x = getValue(linestoedit[i], "X", None)
            y = getValue(linestoedit[i], "Y", None)
            if (newZ != z) and (x is not None) and (y is not None):
                z = newZ
                z_changed = True
        if ("G1" in linestoedit[i] or "G0" in linestoedit[i]) and (z_changed):
            if z > color_index * height_step:
                color_index += 1
                if color_index > len(color_all[0]):
                    color_index = len(color_all[0])
                    insert_gradient = False
            if insert_gradient and z_changed is True:
                color_from = color_all[0][color_index -1]
                color_to = color_all[1][color_index -1]
                gradient_line = "M165 A{0} B{1} C{2}".format(
                    color_from[0] + (color_to[0] - color_from[0]) * (
                    (current_z - (color_index - 1) * height_step) / height_step),
                    color_from[1] + (color_to[1] - color_from[1]) * (
                    (current_z - (color_index - 1) * height_step) / height_step),
                    color_from[2] + (color_to[2] - color_from[2]) * (
                    (current_z - (color_index - 1) * height_step) / height_step))
                linestoedit[i] = linestoedit[i].replace(linestoedit[i], linestoedit[i]+ gradient_line + "\n")
                QApplication.processEvents()
        m = len(linestoedit)
    savefile(linestoedit)
        #start_time = time.process_time()
        #for line in range(0, m):
            # line_correct += lines[line]  将数组内容集中
        #end_time = time.process_time()

def PrusaGradient_active( linestoedit,color_start, color_stop,color_start_10,color_stop_10):
    global total
    gradient_line = ""
    n = len(linestoedit)#源文件行数
        #  rgb - cmy
    color_back_number = [color_start_10, color_stop_10]
    color_all = [color_start, color_stop]

    for i in range(len(color_back_number)):
        for ii in range(len(color_back_number[i])):
            if color_back_number[i][ii] == 1:
                for i3 in info1:
                    if color_all[i][ii][0] == i3['R'] and color_all[i][ii][1] == i3['G'] and color_all[i][ii][2] == \
                            i3['B']:
                        # materials = "M165 A{} B{} C{}".format(i3['C'], i3['M'], i3['Y'])
                        materials2 = "{},{},{}".format(i3['C'], i3['M'], i3['Y'])
                        instruction = materials2.split(",")
                        a = [float(instruction[0]), float(instruction[1]), float(instruction[2])]
                        color_all[i][ii] = list(map(lambda x: x / sum(a), a))

            else:
                instruction_1 = material_chose(color_all[i][ii][0], color_all[i][ii][1], color_all[i][ii][2])[
                    1].split(",")
                b = [float(instruction_1[0]), float(instruction_1[1]), float(instruction_1[2])]
                color_all[i][ii] = list(map(lambda x: x / sum(b), b))

    totalHeight = -1
    current_layer = len(linestoedit) - 1
    while totalHeight == -1:
        layer_1 = linestoedit[current_layer]
        totalHeight = Prusafindtotalheight(layer_1)

        if (totalHeight > -1):
            break
        current_layer -= 1


    height_step = totalHeight / len(color_start)

    x = None
    y = None
    current_z = 0
    z_changed = False
    insert_gradient = True
    z = 0

    color_index = 0
    print("155")
    for i in range(len(linestoedit)):
        total = 0
        z_changed = False
        line_index = i
        if ("G0" in linestoedit[i] or "G1" in linestoedit[i]) and "Z" in linestoedit[i] and "nozzle" not in linestoedit[i]:
            newZ = Prusagetvalue(linestoedit[i], "Z", z)
            current_z = newZ
            if newZ != z:
                z = newZ
                z_changed = True
        if ("G1" in linestoedit[i]) and (z_changed):
            if z > color_index * height_step:
                color_index += 1
                if color_index > len(color_all[0]):
                    color_index = len(color_all[0])
                    insert_gradient = False
                    # insert_gradient = False
            if insert_gradient and z_changed is True:
                color_from = color_all[0][color_index - 1]
                color_to = color_all[1][color_index - 1]
                gradient_line = "M165 A{0} B{1} C{2}".format(
                    color_from[0] + (color_to[0] - color_from[0]) * (
                            (current_z - (color_index - 1) * height_step) / height_step),
                    color_from[1] + (color_to[1] - color_from[1]) * (
                            (current_z - (color_index - 1) * height_step) / height_step),
                    color_from[2] + (color_to[2] - color_from[2]) * (
                            (current_z - (color_index - 1) * height_step) / height_step))
                linestoedit[i] = linestoedit[i].replace(linestoedit[i], gradient_line + "\n" + linestoedit[i])
                print(linestoedit[i])
                QApplication.processEvents()


    print("156")
    m = len(linestoedit)
    global lineprocess
    lineprocess = True
    savefile(linestoedit)# 处理后文件行数
    # print(m, n)

def Custom_Gradientprinting_active( linestoedit,color_start, color_stop,custom_layer,color_start_10,color_stop_10):
    gradient_line = ""
    n = len(linestoedit)  # 源文件行数
    #  rgb - cmy
    color_back_number = [color_start_10, color_stop_10]
    color_all = [color_start, color_stop]
    for i in range(len(color_back_number)):
        for ii in range(len(color_back_number[i])):
            if color_back_number[i][ii] == 1:
                for i3 in info1:
                    if color_all[i][ii][0] == i3['R'] and color_all[i][ii][1] == i3['G'] and color_all[i][ii][2] == i3[
                        'B']:
                        # materials = "M165 A{} B{} C{}".format(i3['C'], i3['M'], i3['Y'])
                        materials2 = "{},{},{}".format(i3['C'], i3['M'], i3['Y'])
                        instruction = materials2.split(",")
                        a = [float(instruction[0]), float(instruction[1]), float(instruction[2])]
                        color_all[i][ii] = list(map(lambda x: x / sum(a), a))

            else:
                instruction_1 = material_chose(color_all[i][ii][0], color_all[i][ii][1], color_all[i][ii][2])[1].split(
                    ",")
                b = [float(instruction_1[0]), float(instruction_1[1]), float(instruction_1[2])]
                color_all[i][ii] = list(map(lambda x: x / sum(b), b))
    totalHeight = -1
    current_layer = len(linestoedit) - 1
    while totalHeight == -1:
        layer_1 = linestoedit[current_layer]
        totalHeight = findTotalHeight(layer_1)

        if (totalHeight > -1):
            break
        current_layer -= 1
    z = 0
    x = None
    y = None
    current_z = 0
    z_changed = False
    insert_gradient = True
    color_index = 0
    layer = 0
    layer_step = 0
    height_step = []
    for i in range(len(linestoedit)):
        layer = linestoedit[i]
        if "Layer height" in layer:
            layer_height = re.search("[0-9]*\.[0-9]", layer)
            layer_height = float(layer_height.group(0))
            break
    for i in range(len(linestoedit)):
        layer = linestoedit[i]
        if ";MINZ" in layer:
            first_z = re.search("[0-9]*\.[0-9]", layer)
            first_z = float(first_z.group(0))
            break
    for i in range(len(custom_layer[0])):
        if i == 0:
            b = (int(custom_layer[1][i]) - int(custom_layer[0][i]) + 1) * layer_height + first_z
            height_step.append(b)
        else:
            b = (int(custom_layer[1][i]) - int(custom_layer[0][i]) + 1) * layer_height
            height_step.append(b)
    for i in range(len(linestoedit)):
        total = 0
        z_changed = False
        line_index = i
        if ("G0" in linestoedit[i] or "G1" in linestoedit[i]) and "Z" in linestoedit[i]:
            newZ = getValue(linestoedit[i], "Z", z)
            current_z = newZ
            x = getValue(linestoedit[i], "X", None)
            y = getValue(linestoedit[i], "Y", None)
            if (newZ != z) and (x is not None) and (y is not None):
                z = newZ
                z_changed = True
        if ("G1" in linestoedit[i] or "G0" in linestoedit[i]) and (z_changed):
            if z >= ((int(custom_layer[0][layer_step]) - 1) * (layer_height) + first_z) and z <= (
                    int(custom_layer[1][layer_step]) * (layer_height) + first_z):
                color_index += 1
                layer_step += 1
                if layer_step >= len(color_all[0]):
                    layer_step = len(color_all[0]) - 1
                if color_index > len(color_all[0]):
                    color_index = len(color_all[0])

                #  insert_gradient = False
            if insert_gradient and z_changed is True:
                color_from = color_all[0][color_index - 1]
                color_to = color_all[1][color_index - 1]
                gradient_line = "M165 A{0} B{1} C{2}".format(
                    color_from[0] + (color_to[0] - color_from[0]) * (
                            (current_z - sum(height_step[:color_index - 1])) / height_step[color_index - 1]),
                    color_from[1] + (color_to[1] - color_from[1]) * (
                            (current_z - sum(height_step[:color_index - 1])) / height_step[color_index - 1]),
                    color_from[2] + (color_to[2] - color_from[2]) * (
                            (current_z - sum(height_step[:color_index - 1])) / height_step[color_index - 1]))
                linestoedit[i] = linestoedit[i].replace(linestoedit[i], gradient_line + "\n" + linestoedit[i])
                QApplication.processEvents()

    m = len(linestoedit)  # 处理后文件行数
    # print(m, n)
    # start_time = time.process_time()
    # for line in range(0, m):
    # line_correct += lines[line]  将数组内容集中
    # end_time = time.process_time()
    global lineprocess
    lineprocess = True
    savefile(linestoedit)

def PrusaCustom_Gradientprinting_active(linestoedit,color_start, color_stop,custom_layer,color_start_10,color_stop_10):
    gradient_line = ""
    n = len(linestoedit)  # 源文件行数
    #  rgb - cmy
    color_back_number = [color_start_10, color_stop_10]
    color_all = [color_start, color_stop]
    for i in range(len(color_back_number)):
        for ii in range(len(color_back_number[i])):
            if color_back_number[i][ii] == 1:
                for i3 in info1:
                    if color_all[i][ii][0] == i3['R'] and color_all[i][ii][1] == i3['G'] and color_all[i][ii][2] == \
                            i3['B']:
                        # materials = "M165 A{} B{} C{}".format(i3['C'], i3['M'], i3['Y'])
                        materials2 = "{},{},{}".format(i3['C'], i3['M'], i3['Y'])
                        instruction = materials2.split(",")
                        a = [float(instruction[0]), float(instruction[1]), float(instruction[2])]
                        color_all[i][ii] = list(map(lambda x: x / sum(a), a))

            else:
                instruction_1 = material_chose(color_all[i][ii][0], color_all[i][ii][1], color_all[i][ii][2])[
                    1].split(",")
                b = [float(instruction_1[0]), float(instruction_1[1]), float(instruction_1[2])]
                color_all[i][ii] = list(map(lambda x: x / sum(b), b))
    totalHeight = -1
    current_layer = n - 1
    while totalHeight == -1:
        layer_1 = linestoedit[current_layer]
        totalHeight = Prusafindtotalheight(layer_1)

        if (totalHeight > -1):
            break
        current_layer -= 1
    print(totalHeight)
    z = 0
    x = None
    y = None
    current_z = 0
    z_changed = False
    insert_gradient = True
    color_index = 0
    layer_step = 0
    # 找到第一层高度
    for i in range(len(linestoedit)):
        layer = linestoedit[~i]
        if "; first_layer_height" in layer:
            first_z = re.search("[0-9]*\.[0-9]*", layer)
            first_z = float(first_z.group(0))
            break
    # 找到层高
    for i in range(len(linestoedit)):
        layer = linestoedit[~i]
        if "; layer_height" in layer:
            layer_height = re.search("[0-9]*\.[0-9]", layer)
            layer_height = float(layer_height.group(0))
            break
    height_step = []
    for i in range(len(custom_layer[0])):
        if i == 0:
            b = (int(custom_layer[1][i]) - int(custom_layer[0][i]) + 1) * layer_height + first_z
            height_step.append(b)
        else:
            b = (int(custom_layer[1][i]) - int(custom_layer[0][i]) + 1) * layer_height
            height_step.append(b)
    for i in range(len(linestoedit)):
        total = 0
        z_changed = False
        if ("G1" in linestoedit[i]) and "Z" in linestoedit[i]:
            newZ = Prusagetvalue(linestoedit[i], "Z", z)
            current_z = newZ
            if newZ != z:
                z = newZ
                z_changed = True
        if ("G1" in linestoedit[i]) and (z_changed):
            if z >= ((int(custom_layer[0][layer_step]) - 1) * (layer_height) + first_z) and z <= (
                    int(custom_layer[1][layer_step]) * (layer_height) + first_z):
                color_index += 1
                layer_step += 1
                if layer_step == len(color_all[0]):
                    layer_step = len(color_all[0]) - 1
                if color_index > len(color_all[0]):
                    color_index = len(color_all[0])
                #  insert_gradient = False
            if insert_gradient and z_changed is True:
                color_from = color_all[0][color_index - 1]
                color_to = color_all[1][color_index - 1]
                gradient_line = "M165 A{0} B{1} C{2}".format(
                    color_from[0] + (color_to[0] - color_from[0]) * (
                            (current_z - sum(height_step[:(color_index - 1)])) / height_step[color_index - 1]),
                    color_from[1] + (color_to[1] - color_from[1]) * (
                            (current_z - sum(height_step[:(color_index - 1)])) / height_step[color_index - 1]),
                    color_from[2] + (color_to[2] - color_from[2]) * (
                            (current_z - sum(height_step[:(color_index - 1)])) / height_step[color_index - 1]))
                linestoedit[i] = linestoedit[i].replace(linestoedit[i], gradient_line + "\n" + linestoedit[i])
                QApplication.processevents()


    m = len(linestoedit)
    global lineprocess
    lineprocess = True
    savefile(linestoedit)  # 处理后文件行数
    # print(m, n)
    # start_time = time.process_time()
    # for line in range(0, m):
    # line_correct += lines[line]  将数组内容集中
    # end_time = time.process_time()

def layer_add(input_file_name,linestoedit):
    if 'PrusaSlicer' in linestoedit:
        j = -1
        for i in range(len(linestoedit)):
            if ";LAYER:" in linestoedit[i]:
                break
            if 'G1' in linestoedit[i] and 'Z' in linestoedit[i] and 'F' in linestoedit[i] and 'nozzle'not in linestoedit[i]:
                j += 1
                linestoedit[i] = linestoedit[i].replace(linestoedit[i], ";LAYER:" + "{}".format(j) + "\n" + linestoedit[i])
        count = "LAYER_COUNT:{}".format(j)
        m=len(linestoedit)
        with open(input_file_name) as fw:
            for i in range(m):
                fw.write(linestoedit[i])
            fw.write('\n' + ';' + count)
            fw.close()

def soft_choose(input_file):
    with open(input_file,"r+") as f:
        lines2 = f.readlines()
        for i in range(len(lines2)):

            if "PrusaSlicer" in lines2[i]:
                return 1
            else:
                return 0


#单色打印
def one_color_printing(input_file_name,linestoedit,R,G,B,color_back_number):
    soft_number = soft_choose(input_file_name)
    if soft_number == 0:
        one_color_printing_active(linestoedit,R,G,B,color_back_number)
    if soft_number == 1:
        # layer_add(input_file_name)
        one_color_printing_active(linestoedit, R,G,B, color_back_number)

# 多层打印
def mutiple_color_printing(input_file_name,linestoedit,number,color_back_number):
    soft_number = soft_choose(input_file_name)
    if soft_number == 0:
        mutiple_color_printing_active(linestoedit, number, color_back_number)
    if soft_number == 1:
        # layer_add(input_file_name)
        mutiple_color_printing_active(linestoedit, number, color_back_number)

# 平均渐变
def Gradientprinting(input_file_name, linestoedit, color_start, color_stop,color_start_10,color_stop_10):
    soft_number = soft_choose(input_file_name)
    if soft_number == 0:
        Gradientprinting_active( linestoedit, color_start, color_stop, color_start_10,color_stop_10)
    if soft_number == 1:
        PrusaGradient_active( linestoedit, color_start, color_stop, color_start_10, color_stop_10)

# 自定义层数渐变
def Custom_Gradientprinting(input_file_name, linestoedit, color_start, color_stop,custom_layer,color_start_10,color_stop_10):
    soft_number = soft_choose(input_file_name)
    if soft_number == 0:
        Custom_Gradientprinting_active(linestoedit, color_start, color_stop, custom_layer,color_start_10, color_stop_10)
    if soft_number == 1:
        PrusaCustom_Gradientprinting_active(linestoedit, color_start, color_stop, custom_layer,color_start_10, color_stop_10)

#def openfile():
#    print("Open file is ok")
#    global name
 #   global nameout
  #  global layerm
   # global file1
    #global lines
#    layerm = 0
 #   name = QFileDialog.getOpenFileName()[0]
  #  if(name !=""):
   #     with open(name) as file1:
    #        lines = file1.readlines()
     #       for i in range(len(lines)):
      #          if (";LAYER" in lines[i] and "COUNT" not in lines[i]):
       #             layerm += 1
#        ui.one_color_radio.setEnabled(True)
 #       ui.much_layers_radio.setEnabled(True)
  #      ui.mix_colors_radio.setEnabled(True)
#    ui.one_color_item.setEnabled(True)
#    ui.layers_num.setEnabled(True)
#    ui.mix_colors_num.setEnabled(True)
#    ui.handle.setEnabled(True)
   #     _translate = QtCore.QCoreApplication.translate
    #    ui.totalHeight.setText(_translate("MainWindow","您选择的Gcode共有%i层" %layerm))
     #   ui.namein.setText(_translate("MainWindow","%s" %name))
    #else:
#        ui.one_color_radio.setEnabled(False)
 #       ui.much_layers_radio.setEnabled(False)
  #      ui.mix_colors_radio.setEnabled(False)
   #     ui.one_color_item.setEnabled(False)
    #    ui.handle.setEnabled(False)
     #   _translate = QtCore.QCoreApplication.translate
      #  ui.totalHeight.setText(_translate("MainWindow", ""))
       # ui.namein.setText(_translate("MainWindow", ""))

def colorselect(objectname):#颜色选择
    for i in Color_Select.selfcolor:
        if(i !=""):
            z = Color_Select.selfcolor.index(i)
            info1[z]['R'] = int(getRGB(i)[0])
            info1[z]['G'] = int(getRGB(i)[1])
            info1[z]['B'] = int(getRGB(i)[2])
            info1[z]['C'] = int(Color_Select.selfcmya[z][0])
            info1[z]['M'] = int(Color_Select.selfcmya[z][1])
            info1[z]['Y'] = int(Color_Select.selfcmya[z][2])
            # print(info1[2]["C"])
            # print(type(info1[2]["C"]))
            #print(info1)
#    print(info1)
    global d
    d = QtWidgets.QDialog()
    ui2 = Color_Select.Ui_Color_Select()
    ui2.setupUi(d)
    d.exec()
    c = ""
    f = ""
    try:
        c = Color_Select.abcde()   #获取颜色RGB
        f = Color_Select.fghij()   #获取""
#        print(info1)
        if(c != ""):
            ysn = MainWindow.findChild((QPushButton,), objectname)
            ysn.setStyleSheet("QPushButton{background:%s}" % c)
            ysn.setText(str(f))
        elif(c == ""):
            ysn = MainWindow.findChild((QPushButton,), objectname)
            ysn.setStyleSheet("QPushButton{background:}")
            ysn.setText("请选择颜色")
            return
        else:
            pass
    except:#点击取消按钮后执行函数
        ysn = MainWindow.findChild((QPushButton,), objectname)
        ysn.setStyleSheet("QPushButton{background:}")
        ysn.setText("请选择颜色")
    h = Color_Select.pqrst()
    if( h != ""):
        if(h.startswith("self")):
            ss =1
        else:
            ss = 0
    if ui.one_color_radio.isChecked():
        global coloronelayer
        coloronelayer = ["#000000"]
        coloronelayer[0] = c
#        print(c)
        colorflag[0] = ss
        # print(colorflag)
#        print(colorflag)
#        print(coloronelayer)
    elif ui.much_layers_radio.isChecked():
#        qw = MainWindow.findChild((QLineEdit,),objectname.replace("color","height"))
#        print(qw)
#        heightdata = qw.text()
#        print(heightdata)
        index =  int(re.search('[0-9]\d{1,2}|\d',objectname).group(0))
#        heightdata_total1[index] = heightdata
        colormuchlayers[index] = c
        muchcolorflag[index] = ss
        # print(muchcolorflag)
#        print(muchcolorflag)
#        print(heightdata_total1)
#        print(colormuchlayers)
    elif ui.mix_colors_radio.isChecked():
        if(objectname.startswith("mix_layers_color_stop_item")):
            if(int(re.search('[0-9]\d{1,2}|\d',objectname).group(0))) < (int(ui.mix_colors_num.text())-1):
#            qw = MainWindow.findChild((QLineEdit,),objectname.replace("color_stop_","height_"))
#            heightdata = qw.text()
                index =  int(re.search('[0-9]\d{1,2}|\d',objectname).group(0))
#            heightdata_total2[index] = heightdata
#            print(heightdata_total2)
                colorstop[index] = c
                mixcolorstopflag[index] =ss
#                print(mixcolorstopflag)
                objectname3 = objectname.replace("stop_item%s" % str(index), "start_item%s" % str(index +1))
                ysn2 = MainWindow.findChild((QPushButton,), objectname3)
                ysn2.setStyleSheet("QPushButton{background:%s}" % c)
                ysn2.setText(str(f))
                colorstart[index+1] = c
                mixcolorstartflag[index+1] = ss
                # print(mixcolorstartflag)
                # print(mixcolorstopflag)
#                print(colorstart)
#                print(colorstop)
#            print(colorstop)
            else:
                index = int(re.search('[0-9]\d{1,2}|\d', objectname).group(0))
                colorstop[index] = c
                mixcolorstopflag[index] = ss
                # print(mixcolorstartflag)
                # print(mixcolorstopflag)
        elif(objectname.startswith("mix_layers_color_start_item")):
#            qw = MainWindow.findChild((QLineEdit,), objectname.replace("color_start_", "height_"))
#            heightdata = qw.text()
            index = int(re.search('[0-9]\d{1,2}|\d',objectname).group(0))
#            heightdata_total2[index] =heightdata
#            print(heightdata_total2)
            colorstart[index] = c
            mixcolorstartflag[index] = ss
            # print(mixcolorstartflag)
            # print(mixcolorstopflag)
#            print(colorstart)
#            print(colorstop)
            pass

def heightselect(objectname1):#上一层的终止层高+1为下一层的起始层高
    qw = MainWindow.findChild((QLineEdit,),objectname1)
#    print(qw)
    if(qw.text() == ""):
        return 0
    heightdata = int(qw.text())
#    print(heightdata)
    index = int(re.search('[0-9]\d{1,2}|\d',objectname1).group(0))
    if(objectname1.startswith("much_layers_height_start") or objectname1.startswith("mix_layers_height_start")):
        if(re.search('[0-9]\d{1,2}|\d',objectname1).group(0) != "0"):
            heightdata_total_start[index] = heightdata
            #print(heightdata_total_start)
            heightdata_total_stop[index-1] = heightdata-1
            #print(heightdata_total_stop)
            objectname2 = objectname1.replace("start_item%s" % str(index), "stop_item%s" % str(index-1))
            qw1 = MainWindow.findChild((QLineEdit,), objectname2)
            qw1.setText(str(heightdata_total_stop[index-1]))
        else:
            heightdata_total_start[index] = heightdata
           # print(heightdata_total_start)

    else:
        if(ui.layers_num.text()!=""):
            if (int(re.search('[0-9]\d{1,2}|\d', objectname1).group(0))) < (int(ui.layers_num.text()) - 1):
                heightdata_total_stop[index] = heightdata
                # print(heightdata_total_stop)
                heightdata_total_start[index + 1] = heightdata + 1
                # print(heightdata_total_start)
                objectname2 = objectname1.replace("stop_item%s" % str(index), "start_item%s" % str(index + 1))
                # print(objectname2)
                qw1 = MainWindow.findChild((QLineEdit,), objectname2)
                qw1.setText(str(heightdata_total_start[index + 1]))
            else:
                heightdata_total_stop[index] = heightdata
                # print(heightdata_total_stop)
        else:
            if ((int(re.search('[0-9]\d{1,2}|\d', objectname1).group(0))) < (int(ui.mix_colors_num.text()) - 1)):
                heightdata_total_stop[index] = heightdata
                # print(heightdata_total_stop)
                heightdata_total_start[index + 1] = heightdata + 1
                # print(heightdata_total_start)
                objectname2 = objectname1.replace("stop_item%s" % str(index), "start_item%s" % str(index + 1))
                # print(objectname2)
                qw1 = MainWindow.findChild((QLineEdit,), objectname2)
                qw1.setText(str(heightdata_total_start[index + 1]))
            else:
                heightdata_total_stop[index] = heightdata
                # print(heightdata_total_stop)

def getRGB(str):
    output = []
    color_1 = str[1:][:2]
    color_1_final = hex2dec(color_1)
    output.append(color_1_final)
    color_2 = str[1:][2:4]
    color_2_final = hex2dec(color_2)
    output.append(color_2_final)
    color_3 = str[1:][4:]
    color_3_final = hex2dec(color_3)
    output.append(color_3_final)
    return output

def hex2dec(str):
    return int(str, 16)

def process_change():#处理进度条
    global count
    global lineprocess
    global writeprocess
    global set
    global process
    global timer
    if (count == 0):
        for i in range(3333):
            process.setValue(i)
        count += 1
    if (lineprocess == True):
        for i in range(3333, 6666):
            process.setValue(i)
        lineprocess = False
    if(writeprocess == True):
        for i in range(6666,10001):
            process.setValue(i)
        writeprocess = False
        count =0
        timer.stop()
        proob = MainWindow.findChild((QtWidgets.QProgressBar),"process2")
        proob.setParent(None)
        _translate = QtCore.QCoreApplication.translate
        ui.suggestion.setText(_translate("MainWindow","当前处理已完成"))

    #for i in range(9999):
    #process.setValue(i)

def loading():#设置进度条
    global process
    global timer
#    process.setWindowFlags(QtCore.Qt.WindowCloseButtonHint|QtCore.Qt.WindowContextHelpButtonHint)
    process=QtWidgets.QProgressBar(MainWindow)
    process.setObjectName("process2")
    process.setGeometry(300,900,200,25)
    timer =QTimer(process)
    process.setRange(0,10000)
    process.show()
    timer.start(1000)
    timer.timeout.connect(process_change)

def postprocessingplugin():#获得数据，进行处理
    with open(untitled.filename,'r') as fa:
        lines1 = fa.readlines()
    global nameout
    global heightdata_total_start
    global heightdata_total_stop
    nameout = QFileDialog.getSaveFileName()[0]
    if(nameout ==""):
        msg_box3 = QMessageBox(QMessageBox.Warning, '提示', '请输入正确文件名！')
        msg_box3.exec_()
        return
    global process
    if mode == "one_color":#单色处理
        try:
            for i in coloronelayer:
                index = coloronelayer.index(i)
                coloronelayer[index] = getRGB(i)
            color_R = coloronelayer[0][0]
            color_G = coloronelayer[0][1]
            color_B = coloronelayer[0][2]
            loading()
            one_color_printing(untitled.filename,lines1,color_R,color_G,color_B,colorflag)
            openGcodeModel()#重新载入处理后的gcode文件进行预览
        except:
            ui.exception_handling("单色处理失败")
    elif mode == "much_layers":
        try:
            colors_num = int(ui.layers_num.text())
            if ui.checkBox_4.isChecked():
                if (heightdata_total_start[0] > heightdata_total_stop[0]) or (
                        heightdata_total_stop[colors_num - 1] < heightdata_total_start[colors_num - 1]):
                    msg_box4 = QMessageBox(QMessageBox.Warning, '警告', '亲爱的用户，您所输入的数值存在终止层大于起始层错误，请重新检查后输入！')
                    msg_box4.exec_()
                    return
                muchlayersoptions = [0] * int(colors_num)
                heightdata_total11 = [0] * int(ui.layers_num.text())
                # 判断TRUEifturelayerm/shuru
                for i in range(0, colors_num):
                    muchlayerslist = [0] * 5
                    #                heightdata_total11[i] = int(heightdata_total1[i])+ int(heightdata_total11[i-1])
                    muchlayerslist[0] = heightdata_total_start[i]
                    muchlayerslist[1] = heightdata_total_stop[i]
                    muchlayerslist[2] = getRGB(colormuchlayers[i])[0]
                    muchlayerslist[3] = getRGB(colormuchlayers[i])[1]
                    muchlayerslist[4] = getRGB(colormuchlayers[i])[2]
                    #                print(muchlayerslist)
                    muchlayersoptions[i] = muchlayerslist
                #            print(muchlayersoptions)
                if (int(heightdata_total11[colors_num - 1]) <= untitled.layerm):
                    #            print("yes ok!")
                    loading()
                    mutiple_color_printing(untitled.filename, lines1, muchlayersoptions, muchcolorflag)
                else:
                    msg_box = QMessageBox(QMessageBox.Warning, '警告', '亲爱的用户，您所已输入层高已超限制，请检查后重新输入')
                    msg_box.exec_()

            elif ui.checkBox_3.isChecked():#平均分层
                #ui.layers_num.setEnabled(True)
                if (heightdata_total_start[0] > heightdata_total_stop[0]) or (heightdata_total_stop[colors_num - 1] < heightdata_total_start[colors_num - 1]):
                    msg_box4 = QMessageBox(QMessageBox.Warning, '警告', '亲爱的用户，您所输入的数值存在终止层大于起始层错误，请重新检查后输入！')
                    msg_box4.exec_()
                    return
                muchlayersoptions = [0] * int(colors_num)
                heightdata_total11 = [0] * int(ui.layers_num.text())
                v=untitled.layerm//colors_num
                for i in range(0, colors_num):
                    muchlayerslist = [0] * 5
                    muchlayerslist[0] = i * v
                    muchlayerslist[1] = (i + 1) * v - 1
                    muchlayerslist[2] = getRGB(colormuchlayers[i])[0]
                    muchlayerslist[3] = getRGB(colormuchlayers[i])[1]
                    muchlayerslist[4] = getRGB(colormuchlayers[i])[2]
                    muchlayersoptions[i] = muchlayerslist
                if (int(heightdata_total11[colors_num - 1]) <= untitled.layerm):
                    #            print("yes ok!")
                    loading()
                    mutiple_color_printing(untitled.filename, lines1, muchlayersoptions, muchcolorflag)
                else:
                    msg_box = QMessageBox(QMessageBox.Warning, '警告', '亲爱的用户，您所已输入层高已超限制，请检查后重新输入')
                    msg_box.exec_()
            openGcodeModel()
        except:
            ui.exception_handling("分层处理失败")
    elif mode == "mix_colors":
        try:
            colors_num = int(ui.mix_colors_num.text())
            colorstartoptions = ["#000000"] * mix_colors_num
            colorstopoptions = ["#000000"] * mix_colors_num
            h = [0] * int(ui.mix_colors_num.text())
            j = [0] * int(ui.mix_colors_num.text())
            aa = [h, j]
            if ui.checkBox.isChecked():#自定义渐变
                for i in range(0, colors_num):
                    colorstartoptions[i] = getRGB(colorstart[i])
                    colorstopoptions[i] = getRGB(colorstop[i])
                    aa[0][i] = heightdata_total_start[i]
                    aa[1][i] = heightdata_total_stop[i]
                Custom_Gradientprinting(untitled.filename, lines1, colorstartoptions, colorstopoptions, aa,
                                        mixcolorstartflag, mixcolorstopflag)
            elif ui.checkBox_2.isChecked():#平均渐变
                v = untitled.layerm // colors_num
                for i in range(0, colors_num):
                    colorstartoptions[i] = getRGB(colorstart[i])
                    colorstopoptions[i] = getRGB(colorstop[i])
                    aa[0][i] = i*v
                    aa[1][i] = (i+1)*v-1
                print("111")
                Gradientprinting(untitled.filename, lines1, colorstartoptions, colorstopoptions,
                                        mixcolorstartflag, mixcolorstopflag)


    #            print(colorstartoptions)
    #            print(colorstopoptions)
            loading()
            openGcodeModel()
        except:
            ui.exception_handling("渐变处理失败")

#        print(time.process_time())
#        end1 = time.process_time()
#        print(end1 - start1)
    else:
        pass
    ui.handle.setEnabled(False)
    ui.checkBox_3.setChecked(False)
    ui.checkBox_4.setChecked(False)
    ui.checkBox_2.setChecked(False)
    ui.checkBox.setChecked(False)
    ui.checkBox_3.setEnabled(False)
    ui.checkBox_4.setEnabled(False)
    ui.checkBox_2.setEnabled(False)
    ui.checkBox.setEnabled(False)
    ui.mix_colors_radio.setChecked(False)
    ui.much_layers_radio.setChecked(False)
    ui.one_color_radio.setChecked(False)
    ui.layers_num.setText("")
    ui.mix_colors_num.setText("")
    ui.layers_num.setEnabled(False)
    ui.mix_colors_num.setEnabled(False)
    ysn = MainWindow.findChild((QPushButton,),"one_color_item")
    ysn.setStyleSheet("QPushButton{background:}")
    ysn.setText("请选择颜色")
#    ysn = MainWindow.findChild((QtWidgets.QHBoxLayout,), "one_color_choose")
#    ysn1 = MainWindow.findChild((QtWidgets.QPushButton,), "one_color_item")
#    ysn.setParent(None)
#    ysn.deleteLater()
#    sip.delete(ysn)
#    ysn1.setParent(None)
    if(ui.mix_colors_options.findChild((QtWidgets.QHBoxLayout), "mix_layers_list0") != None):
        for i in range(0, 30):
            ysn21 = ui.mix_colors_options.findChild((QtWidgets.QHBoxLayout,), "mix_layers_list%s" % str(i))
            if (ysn21 != None):
                ysn211 = MainWindow.findChild((QPushButton,), "mix_layers_color_start_item%s" % str(i))
                ysn212 = MainWindow.findChild((QPushButton,), "mix_layers_color_stop_item%s" % str(i))
                ysn213 = MainWindow.findChild((QLabel,), "mix_layers_color_start_label%s" % str(i))
                ysn214 = MainWindow.findChild((QLabel,), "mix_layers_color_stop_label%s" % str(i))
                ysn216 = MainWindow.findChild((QLineEdit,), "mix_layers_height_start_item%s" % str(i))
                ysn215 = MainWindow.findChild((QLabel,), "mix_layers_height_start_label%s" % str(i))
                ysn218 = MainWindow.findChild((QLineEdit,), "mix_layers_height_stop_item%s" % str(i))
                ysn217 = MainWindow.findChild((QLabel,), "mix_layers_height_stop_label%s" % str(i))
                if (ysn211 != None) and (ysn212 != None):
                    ysn21.setParent(None)
                    ysn21.deleteLater()
                    sip.delete(ysn21)
                    ysn211.setParent(None)
                    ysn212.setParent(None)
                    ysn213.setParent(None)
                    ysn214.setParent(None)
                    ysn215.setParent(None)
                    ysn216.setParent(None)
                    ysn217.setParent(None)
                    ysn218.setParent(None)
                else:
                    ysn21.setParent(None)
                    ysn21.deleteLater()
                    #        ui.mix_layers_options.setParent(None)
                    #        ui.mix_layers_options.deleteLater()
    if(ui.much_layers_options.findChild((QtWidgets.QHBoxLayout), "much_layers_list0") != None):
        for i in range(0, 30):
            ysn21 = ui.much_layers_options.findChild((QtWidgets.QHBoxLayout,), "much_layers_list%s" % str(i))
            if (ysn21 != None):
                ysn211 = MainWindow.findChild((QLabel,), "much_layers_height_start_label%s" % str(i))
                ysn212 = MainWindow.findChild((QLineEdit,), "much_layers_height_start_item%s" % str(i))
                ysn215 = MainWindow.findChild((QLabel,), "much_layers_height_stop_label%s" % str(i))
                ysn216 = MainWindow.findChild((QLineEdit,), "much_layers_height_stop_item%s" % str(i))
                ysn213 = MainWindow.findChild((QLabel,), "much_layers_color_label%s" % str(i))
                ysn214 = MainWindow.findChild((QPushButton,), "much_layers_color_item%s" % str(i))
                if (ysn211 != None):
                    ysn21.setParent(None)
                    ysn21.deleteLater()
                    sip.delete(ysn21)
                    ysn211.setParent(None)
                    ysn212.setParent(None)
                    ysn213.setParent(None)
                    ysn214.setParent(None)
                    ysn215.setParent(None)
                    ysn216.setParent(None)
                else:
                    ysn21.setParent(None)
                    ysn21.deleteLater()

def modeselect(zz):#打印模式选择
    global mode
    aa = False
    bb = False
    cc = False
    if (zz=="aa"):
        aa = True
    elif (zz=="bb"):
        bb =True
    elif (zz=="cc"):
        cc =True
    if (ui.one_color_radio.isChecked() and aa==True):
        mode = "one_color"
        ui.mix_colors_radio.setChecked(False)
        #ui.mix_colors_radio.setEnabled(False)
        ui.much_layers_radio.setChecked(False)
        #ui.much_layers_radio.setEnabled(False)
        ui.one_color_item.setEnabled(True)
        ui.layers_num.setEnabled(False)
        ui.mix_colors_num.setEnabled(False)
        ui.checkBox_3.setEnabled(False)
        ui.checkBox_4.setEnabled(False)
        ui.checkBox_2.setEnabled(False)
        ui.checkBox.setEnabled(False)
        ui.handle.setEnabled(True)
        ui.mix_colors_num.setText("")
        ui.layers_num.setText("")
        if (ui.mix_colors_options.findChild((QtWidgets.QHBoxLayout), "mix_layers_list0") != None):
            for i in range(0, 30):
                ysn21 = ui.mix_colors_options.findChild((QtWidgets.QHBoxLayout,), "mix_layers_list%s" % str(i))
                if (ysn21 != None):
                    ysn211 = MainWindow.findChild((QPushButton,), "mix_layers_color_start_item%s" % str(i))
                    ysn212 = MainWindow.findChild((QPushButton,), "mix_layers_color_stop_item%s" % str(i))
                    ysn213 = MainWindow.findChild((QLabel,), "mix_layers_color_start_label%s" % str(i))
                    ysn214 = MainWindow.findChild((QLabel,), "mix_layers_color_stop_label%s" % str(i))
                    ysn216 = MainWindow.findChild((QLineEdit,), "mix_layers_height_start_item%s" % str(i))
                    ysn215 = MainWindow.findChild((QLabel,), "mix_layers_height_start_label%s" % str(i))
                    ysn218 = MainWindow.findChild((QLineEdit,), "mix_layers_height_stop_item%s" % str(i))
                    ysn217 = MainWindow.findChild((QLabel,), "mix_layers_height_stop_label%s" % str(i))
                    if (ysn211 != None) and (ysn212 != None):
                        ysn21.setParent(None)
                        ysn21.deleteLater()
                        sip.delete(ysn21)
                        ysn211.setParent(None)
                        ysn212.setParent(None)
                        ysn213.setParent(None)
                        ysn214.setParent(None)
                        ysn215.setParent(None)
                        ysn216.setParent(None)
                        ysn217.setParent(None)
                        ysn218.setParent(None)
                    else:
                        ysn21.setParent(None)
                        ysn21.deleteLater()
                        #        ui.mix_layers_options.setParent(None)
                        #        ui.mix_layers_options.deleteLater()
        if (ui.much_layers_options.findChild((QtWidgets.QHBoxLayout), "much_layers_list0") != None):
            for i in range(0, 30):
                ysn21 = ui.much_layers_options.findChild((QtWidgets.QHBoxLayout,), "much_layers_list%s" % str(i))
                if (ysn21 != None):
                    ysn211 = MainWindow.findChild((QLabel,), "much_layers_height_start_label%s" % str(i))
                    ysn212 = MainWindow.findChild((QLineEdit,), "much_layers_height_start_item%s" % str(i))
                    ysn215 = MainWindow.findChild((QLabel,), "much_layers_height_stop_label%s" % str(i))
                    ysn216 = MainWindow.findChild((QLineEdit,), "much_layers_height_stop_item%s" % str(i))
                    ysn213 = MainWindow.findChild((QLabel,), "much_layers_color_label%s" % str(i))
                    ysn214 = MainWindow.findChild((QPushButton,), "much_layers_color_item%s" % str(i))
                    if (ysn211 != None):
                        ysn21.setParent(None)
                        ysn21.deleteLater()
                        sip.delete(ysn21)
                        ysn211.setParent(None)
                        ysn212.setParent(None)
                        ysn213.setParent(None)
                        ysn214.setParent(None)
                        ysn215.setParent(None)
                        ysn216.setParent(None)
                    else:
                        ysn21.setParent(None)
                        ysn21.deleteLater()
    elif (ui.much_layers_radio.isChecked() and bb==True):
        mode = "much_layers"
        ui.mix_colors_radio.setChecked(False)
        #ui.mix_colors_radio.setEnabled(False)
        ui.one_color_radio.setChecked(False)
        #ui.one_color_radio.setEnabled(False)
        ui.layers_num.setEnabled(False)
        ui.one_color_item.setEnabled(False)
        ui.mix_colors_num.setEnabled(False)
        ui.handle.setEnabled(True)
        ui.checkBox_3.setEnabled(True)
        ui.checkBox_4.setEnabled(True)
        ui.checkBox_2.setEnabled(False)
        ui.checkBox.setEnabled(False)
        #ui.checkBox_3.setChecked(False)
        #ui.checkBox_4.setChecked(False)
        ui.mix_colors_num.setText("")
        ysn = MainWindow.findChild((QPushButton,),"one_color_item")
        ysn.setStyleSheet("QPushButton{background:}")
        ysn.setText("请选择颜色")
        if (ui.mix_colors_options.findChild((QtWidgets.QHBoxLayout), "mix_layers_list0") != None):
            for i in range(0, 30):
                ysn21 = ui.mix_colors_options.findChild((QtWidgets.QHBoxLayout,), "mix_layers_list%s" % str(i))
                if (ysn21 != None):
                    ysn211 = MainWindow.findChild((QPushButton,), "mix_layers_color_start_item%s" % str(i))
                    ysn212 = MainWindow.findChild((QPushButton,), "mix_layers_color_stop_item%s" % str(i))
                    ysn213 = MainWindow.findChild((QLabel,), "mix_layers_color_start_label%s" % str(i))
                    ysn214 = MainWindow.findChild((QLabel,), "mix_layers_color_stop_label%s" % str(i))
                    ysn216 = MainWindow.findChild((QLineEdit,), "mix_layers_height_start_item%s" % str(i))
                    ysn215 = MainWindow.findChild((QLabel,), "mix_layers_height_start_label%s" % str(i))
                    ysn218 = MainWindow.findChild((QLineEdit,), "mix_layers_height_stop_item%s" % str(i))
                    ysn217 = MainWindow.findChild((QLabel,), "mix_layers_height_stop_label%s" % str(i))
                    if (ysn211 != None) and (ysn212 != None):
                        ysn21.setParent(None)
                        ysn21.deleteLater()
                        sip.delete(ysn21)
                        ysn211.setParent(None)
                        ysn212.setParent(None)
                        ysn213.setParent(None)
                        ysn214.setParent(None)
                        ysn215.setParent(None)
                        ysn216.setParent(None)
                        ysn217.setParent(None)
                        ysn218.setParent(None)
                    else:
                        ysn21.setParent(None)
                        ysn21.deleteLater()
        else:
            pass
    elif (ui.mix_colors_radio.isChecked() and cc==True):
        mode = "mix_colors"
        ui.one_color_radio.setChecked(False)
        #ui.one_color_radio.setEnabled(False)
        ui.much_layers_radio.setChecked(False)
        #ui.much_layers_radio.setEnabled(False)
        ui.mix_colors_num.setEnabled(False)
        ui.one_color_item.setEnabled(False)
        ui.layers_num.setEnabled(False)
        ui.handle.setEnabled(True)
        ui.checkBox_2.setEnabled(True)
        ui.checkBox.setEnabled(True)
        ui.checkBox_3.setEnabled(False)
        ui.checkBox_4.setEnabled(False)
        ui.layers_num.setText("")
        ysn = MainWindow.findChild((QPushButton,),"one_color_item")
        ysn.setStyleSheet("QPushButton{background:}")
        ysn.setText("请选择颜色")
        if (ui.much_layers_options.findChild((QtWidgets.QHBoxLayout), "much_layers_list0") != None):
            for i in range(0, 30):
                ysn21 = ui.much_layers_options.findChild((QtWidgets.QHBoxLayout,), "much_layers_list%s" % str(i))
                if (ysn21 != None):
                    ysn211 = MainWindow.findChild((QLabel,), "much_layers_height_start_label%s" % str(i))
                    #                    print(ysn211)
                    ysn212 = MainWindow.findChild((QLineEdit,), "much_layers_height_start_item%s" % str(i))
                    #                    print(ysn212)
                    ysn215 = MainWindow.findChild((QLabel,), "much_layers_height_stop_label%s" % str(i))
                    #                    print(ysn215)
                    ysn216 = MainWindow.findChild((QLineEdit,), "much_layers_height_stop_item%s" % str(i))
                    #                    print(ysn216)
                    ysn213 = MainWindow.findChild((QLabel,), "much_layers_color_label%s" % str(i))
                    #                    print(ysn213)
                    ysn214 = MainWindow.findChild((QPushButton,), "much_layers_color_item%s" % str(i))
                    #                    print(ysn214)
                    if (ysn211 != None):
                        ysn21.setParent(None)
                        ysn21.deleteLater()
                        sip.delete(ysn21)
                        ysn211.setParent(None)
                        ysn212.setParent(None)
                        ysn213.setParent(None)
                        ysn214.setParent(None)
                        ysn215.setParent(None)
                        ysn216.setParent(None)
                    else:
                        ysn21.setParent(None)
                        ysn21.deleteLater()
        else:
            pass

def openGcodeModel():
    global nameout
    fileExt = os.path.splitext(nameout)[1].upper()
    if fileExt == ".GCODE":
        ui.loadGCode(nameout,False)

def addmuchLayers():#分层打印 动态添加删除控件
    #when user'sedit finished,connect this
#    print("Layers input finished")
    if(ui.layers_num.text()== ""):
        return 0
    if(int(ui.layers_num.text())<= 30):
        global much_colors_num
        much_colors_num = int(ui.layers_num.text())
        global heightdata_total_start
        global heightdata_total_stop
        global colormuchlayers
        global muchcolorflag
        heightdata_total_start = [0] * much_colors_num
        heightdata_total_stop = [0] * much_colors_num
        colormuchlayers = ["#000000"] * much_colors_num
        muchcolorflag = [""] * much_colors_num
#    ui.much_layers_options.deleteLater()
#    ui.much_layers_options.setParent(None)
#    ui.much_layers_options.deleteLater()
#    ui.much_layers_options = QtWidgets.QVBoxLayout()
#    ui.much_layers_choose.addLayout(ui.much_layers_options)
        if (ui.much_layers_options.findChild((QtWidgets.QHBoxLayout), "much_layers_list0") != None):
            for i in range(0, 30):
                ysn21 = ui.much_layers_options.findChild((QtWidgets.QHBoxLayout,), "much_layers_list%s" % str(i))
                if (ysn21 != None):
                    ysn211 = MainWindow.findChild((QLabel,), "much_layers_height_start_label%s" % str(i))
                    ysn212 = MainWindow.findChild((QLineEdit,), "much_layers_height_start_item%s" % str(i))
                    ysn215 = MainWindow.findChild((QLabel,), "much_layers_height_stop_label%s" % str(i))
                    ysn216 = MainWindow.findChild((QLineEdit,), "much_layers_height_stop_item%s" % str(i))
                    ysn213 = MainWindow.findChild((QLabel,), "much_layers_color_label%s" % str(i))
                    ysn214 = MainWindow.findChild((QPushButton,), "much_layers_color_item%s" % str(i))
                    if (ysn211 != None):
                        ysn21.setParent(None)
                        ysn21.deleteLater()
                        sip.delete(ysn21)
                        ysn211.setParent(None)
                        ysn212.setParent(None)
                        ysn213.setParent(None)
                        ysn214.setParent(None)
                        ysn215.setParent(None)
                        ysn216.setParent(None)
                    else:
                        ysn21.setParent(None)
                        ysn21.deleteLater()
        else:
            ui.much_layers_options1.setParent(None)
            ui.much_layers_options1.deleteLater()
#            ui.much_layers_option.add(ui.much_layers_option)
#            ui.much_layers_choose.addLayout(ui.much_layers_option)
            ui.much_layers_options1 = QtWidgets.QWidget()  # topFiller
            ui.much_layers_options1.setMinimumSize(600, 80)
#            ui.scroll1 = QtWidgets.QScrollArea()  # scroll
            ui.much_layers_option.addWidget(ui.scroll1)  # vbox.addwidget(scroll)
            ui.scroll1.setWidget(ui.much_layers_options1)  # scroll.setwidget(topFiller)
            ui.much_layers_options = QtWidgets.QVBoxLayout()  # vbox
#            ui.much_layers_options = QtWidgets.QVBoxLayout()
#            ui.much_layers_options1.setLayout(ui.much_layers_options)
        for i in range(0,much_colors_num):
            m = str(i)
            much_layers_list = QtWidgets.QHBoxLayout()
            ui.much_layers_options1.resize(600,80*i)
            much_layers_height_start_label = QtWidgets.QLabel(ui.much_layers_options1)
            much_layers_list.addWidget(much_layers_height_start_label)
#            ui.much_layers_options1.addWidget(much_layers_height_start_label)
            much_layers_height_start_item = QtWidgets.QLineEdit(ui.much_layers_options1)
            much_layers_list.addWidget(much_layers_height_start_item)
#            ui.much_layers_options1.addWidget(much_layers_height_start_item)
            much_layers_height_stop_label = QtWidgets.QLabel(ui.much_layers_options1)
            much_layers_list.addWidget(much_layers_height_stop_label)
#            ui.much_layers_options1.addWidget(much_layers_height_stop_label)
            much_layers_height_stop_item = QtWidgets.QLineEdit(ui.much_layers_options1)
            much_layers_list.addWidget(much_layers_height_stop_item)
#            ui.much_layers_options1.addWidget(much_layers_height_stop_item)
            much_layers_color_label = QtWidgets.QLabel(ui.much_layers_options1)
            much_layers_list.addWidget(much_layers_color_label)
#            ui.much_layers_options1.addWidget(much_layers_color_label)
            much_layers_color_item = QtWidgets.QPushButton(ui.much_layers_options1)
            much_layers_list.addWidget(much_layers_color_item)
#            ui.much_layers_options1.addWidget(much_layers_color_item)
            ui.much_layers_options.addLayout(much_layers_list)
            _translate = QtCore.QCoreApplication.translate
            much_layers_color_label.setText(_translate("MainWindow","颜色%s" %m))
            much_layers_height_start_label.setText(_translate("MainWindow","分段%s开始" %m))
            much_layers_height_stop_label.setText(_translate("MainWindow", "分段%s结束" % m))
            much_layers_color_item.setText(_translate("MainWindow","选择的颜色"))
            much_layers_list.setObjectName("much_layers_list%s" %m)
            much_layers_height_start_label.setObjectName("much_layers_height_start_label%s" %m)
            much_layers_height_start_item.setObjectName("much_layers_height_start_item%s" %m)
            much_layers_height_stop_label.setObjectName("much_layers_height_stop_label%s" %m)
            much_layers_height_stop_item.setObjectName("much_layers_height_stop_item%s" %m)
            much_layers_color_label.setObjectName("much_layers_color_label%s" %m)
            much_layers_color_item.setObjectName("much_layers_color_item%s" %m)
            if ui.checkBox_3.isChecked():#自定义分层or平均分层
                for i in range(0,30):
                    ysn21 = ui.much_layers_options.findChild((QtWidgets.QHBoxLayout,), "much_layers_list%s" % str(i))
                    if (ysn21 != None):
                        ysn211 = MainWindow.findChild((QLabel,), "much_layers_height_start_label%s" % str(i))
                        ysn212 = MainWindow.findChild((QLineEdit,), "much_layers_height_start_item%s" % str(i))
                        ysn215 = MainWindow.findChild((QLabel,), "much_layers_height_stop_label%s" % str(i))
                        ysn216 = MainWindow.findChild((QLineEdit,), "much_layers_height_stop_item%s" % str(i))
                        #ysn213 = MainWindow.findChild((QLabel,), "much_layers_color_label%s" % str(i))
                        #ysn214 = MainWindow.findChild((QPushButton,), "much_layers_color_item%s" % str(i))
                        ysn211.setEnabled(False)
                        ysn212.setEnabled(False)
                        ysn215.setEnabled(False)
                        ysn216.setEnabled(False)


            much_layers_color_item.clicked.connect(partial(colorselect,"much_layers_color_item%s" %m))
            much_layers_height_start_item.textChanged.connect(partial(heightselect,"much_layers_height_start_item%s" %m))
            much_layers_height_stop_item.textChanged.connect(partial(heightselect,"much_layers_height_stop_item%s" %m))
        ui.much_layers_options1.setLayout(ui.much_layers_options)
    else:
        msg_box1 = QMessageBox(QMessageBox.Warning, '提示', '亲爱的用户，本软件目前仅支持30层以下分层数，请输入不大于30的分层数！')
        msg_box1.exec_()

def savefile(linesa):#保存
    global nameout
#    nameout = QFileDialog.getSaveFileName()[0]
#    print(nameout)
    if not (nameout.endswith(".gcode")) or not (nameout.endswith(".GCODE")):
        nameout = nameout + ".gcode"
    m = len(linesa)
    with open(nameout, "w+")as fw:
        for i in range(m):
            fw.write(linesa[i])
    global writeprocess
    writeprocess = True

def addmixLayers():#渐变打印 根据用户输入动态添加控件
    if(ui.mix_colors_num.text() == ""):
        return 0
    if (int(ui.mix_colors_num.text())<= 30):
        global mix_colors_num
        mix_colors_num = int(ui.mix_colors_num.text())
        global mixcolorstartflag
        global mixcolorstopflag
        global heightdata_total_start
        global heightdata_total_stop
        global colorstart
        global colorstop
        mixcolorstartflag = [""] * mix_colors_num
        mixcolorstopflag = [""] * mix_colors_num
        heightdata_total_start = [0] * mix_colors_num
        heightdata_total_stop = [0] * mix_colors_num
        colorstart = ["#000000"] * mix_colors_num
        colorstop = ["#000000"] * mix_colors_num
#    print(ui.mix_layers_options.findChild((QtWidgets.QHBoxLayout),"mix_layers_list0"))
        if(ui.mix_colors_options.findChild((QtWidgets.QHBoxLayout),"mix_layers_list0") != None):
            for i in range(0,30):
                global ysn21
                ysn21 = ui.mix_colors_options.findChild((QtWidgets.QHBoxLayout,),"mix_layers_list%s" %str(i))
#            print(ysn21)
                if(ysn21 != None):
                    ysn211 = MainWindow.findChild((QPushButton,),"mix_layers_color_start_item%s" %str(i))
#                    print(ysn211)
                    ysn212 = MainWindow.findChild((QPushButton,),"mix_layers_color_stop_item%s" %str(i))
#                    print(ysn212)
                    ysn213 = MainWindow.findChild((QLabel,), "mix_layers_color_start_label%s" % str(i))
#                    print(ysn213)
                    ysn214 = MainWindow.findChild((QLabel,), "mix_layers_color_stop_label%s" % str(i))
#                    print(ysn214)
                    ysn216 = MainWindow.findChild((QLineEdit,), "mix_layers_height_start_item%s" % str(i))
                    ysn215 = MainWindow.findChild((QLabel,), "mix_layers_height_start_label%s" % str(i))
                    ysn218 = MainWindow.findChild((QLineEdit,), "mix_layers_height_stop_item%s" % str(i))
                    ysn217 = MainWindow.findChild((QLabel,), "mix_layers_height_stop_label%s" % str(i))
#                ysn213 = MainWindow.findChild((QPushButton,),"mix_layers_color_start_label%s" %str(i))
#                print(ysn213)
#                ysn214 = MainWindow.findChild((QPushButton,),"mix_layers_color_stop_label%s" %str(i))
#                print(ysn214)
                    if (ysn211 != None) and (ysn212 != None):
                        ysn21.setParent(None)
                        ysn21.deleteLater()
                        sip.delete(ysn21)
                        ysn211.setParent(None)
                        ysn212.setParent(None)
                        ysn213.setParent(None)
                        ysn214.setParent(None)
                        ysn215.setParent(None)
                        ysn216.setParent(None)
                        ysn217.setParent(None)
                        ysn218.setParent(None)
#                    ysn21.removeWidget(ysn211)
#                    ysn211.deleteLater()
#                    sip.delete(ysn211)
#                    ysn212.setParent(None)
#                    ysn21.removeWidget(ysn212)
#                    ysn212.deleteLater()
#                    sip.delete(ysn212)
                    else:
                        ysn21.setParent(None)
                        ysn21.deleteLater()
#        ui.mix_layers_options.setParent(None)
#        ui.mix_layers_options.deleteLater()
        else:
            ui.mix_colors_options1.setParent(None)
            ui.mix_colors_options1.deleteLater()
            ui.mix_colors_options1 = QtWidgets.QWidget()
            ui.mix_colors_options1.setMinimumSize(600,80)
            ui.mix_colors_option.addWidget(ui.scroll2)
            ui.scroll2.setWidget(ui.mix_colors_options1)
            ui.mix_colors_options = QtWidgets.QVBoxLayout()
        for i in range(0,mix_colors_num):
            m = str(i)
            mix_layers_list = QtWidgets.QHBoxLayout()#H是水平布局，V是垂直布局
            ui.mix_colors_options1.resize(600,80*i)
#        mix_layers_height_label = QtWidgets.QLabel(ui.verticalLayoutWidget)
#        mix_layers_list.addWidget(mix_layers_height_label)
#        mix_layers_height_item = QtWidgets.QLineEdit(ui.verticalLayoutWidget)
#        mix_layers_list.addWidget(mix_layers_height_item)
            mix_layers_height_start_label = QtWidgets.QLabel(ui.mix_colors_options1)
            mix_layers_height_start_item = QtWidgets.QLineEdit(ui.mix_colors_options1)
            mix_layers_list.addWidget(mix_layers_height_start_label)
            mix_layers_list.addWidget(mix_layers_height_start_item)
            mix_layers_height_stop_label = QtWidgets.QLabel(ui.mix_colors_options1)
            mix_layers_height_stop_item = QtWidgets.QLineEdit(ui.mix_colors_options1)
            mix_layers_list.addWidget(mix_layers_height_stop_label)
            mix_layers_list.addWidget(mix_layers_height_stop_item)

            mix_layers_color_start_label = QtWidgets.QLabel(ui.mix_colors_options1)
            mix_layers_list.addWidget(mix_layers_color_start_label)
#        mix_layers_color_start_item = QtWidgets.QComboBox(ui.verticalLayoutWidget)
            mix_layers_color_start_item = QtWidgets.QPushButton(ui.mix_colors_options1)
            mix_layers_list.addWidget(mix_layers_color_start_item)
#        mix_layers_color_start_item.addItems(dict)
            mix_layers_color_stop_label = QtWidgets.QLabel(ui.mix_colors_options1)
            mix_layers_list.addWidget(mix_layers_color_stop_label)
            mix_layers_color_stop_item = QtWidgets.QPushButton(ui.mix_colors_options1)
#        mix_layers_color_stop_item = QtWidgets.QComboBox(ui.verticalLayoutWidget)
            mix_layers_list.addWidget(mix_layers_color_stop_item)
#        mix_layers_color_stop_item.addItems(dict)
            ui.mix_colors_options.addLayout(mix_layers_list)
            _translate = QtCore.QCoreApplication.translate
            mix_layers_color_start_label.setText(_translate("MainWindow","起始颜色%s" %m))
#        mix_layers_height_label.setText(_translate("MainWindow","层高%s" %m))
            mix_layers_color_start_item.setText(_translate("MainWindow","选择的颜色"))
            mix_layers_color_stop_label.setText(_translate("MainWindow", "终止颜色%s" % m))
            mix_layers_color_stop_item.setText(_translate("MainWindow", "选择的颜色"))
            mix_layers_height_stop_item.setText(_translate("MainWindow", ""))
            mix_layers_height_start_item.setText(_translate("MainWindow", ""))
            mix_layers_height_start_label.setText(_translate("MainWindow", "分段%s开始" % m))
            mix_layers_height_stop_label.setText(_translate("MainWindow", "分段%s结束" % m))
            mix_layers_list.setObjectName("mix_layers_list%s" %m)
#        mix_layers_height_label.setObjectName("mix_layers_height_label%s" %m)
#        mix_layers_height_item.setObjectName("mix_layers_height_item%s" %m)
            mix_layers_height_start_label.setObjectName("mix_layers_height_start_label%s" % m)
            mix_layers_height_start_item.setObjectName("mix_layers_height_start_item%s" % m)
            mix_layers_height_stop_label.setObjectName("mix_layers_height_stop_label%s" % m)
            mix_layers_height_stop_item.setObjectName("mix_layers_height_stop_item%s" % m)
            mix_layers_color_start_label.setObjectName("mix_layers_color_start_label%s" %m)
            mix_layers_color_start_item.setObjectName("mix_layers_color_start_item%s" %m)
            mix_layers_color_stop_label.setObjectName("mix_layers_color_stop_label%s" %m)
            mix_layers_color_stop_item.setObjectName("mix_layers_color_stop_item%s" %m)
            if ui.checkBox_2.isChecked():#自定义渐变or平均渐变
                for i in range(0, 30):
                    ysn21 = ui.mix_colors_options.findChild((QtWidgets.QHBoxLayout,), "mix_layers_list%s" % str(i))
                    if (ysn21 != None):
                        ysn216 = MainWindow.findChild((QLineEdit,), "mix_layers_height_start_item%s" % str(i))
                        ysn215 = MainWindow.findChild((QLabel,), "mix_layers_height_start_label%s" % str(i))
                        ysn218 = MainWindow.findChild((QLineEdit,), "mix_layers_height_stop_item%s" % str(i))
                        ysn217 = MainWindow.findChild((QLabel,), "mix_layers_height_stop_label%s" % str(i))
                        ysn215.setEnabled(False)
                        ysn216.setEnabled(False)
                        ysn217.setEnabled(False)
                        ysn218.setEnabled(False)
            mix_layers_color_start_item.clicked.connect(partial(colorselect,"mix_layers_color_start_item%s" %m))
            mix_layers_color_stop_item.clicked.connect(partial(colorselect,"mix_layers_color_stop_item%s" %m))
            mix_layers_height_start_item.textChanged.connect(partial(heightselect, "mix_layers_height_start_item%s" % m))
            mix_layers_height_stop_item.textChanged.connect(partial(heightselect, "mix_layers_height_stop_item%s" % m))
        ui.mix_colors_options1.setLayout(ui.mix_colors_options)
    else:
        msg_box2 = QMessageBox(QMessageBox.Warning, '提示', '亲爱的用户，本软件目前仅支持30层以下分层数，请输入不大于30的分层数！')
        msg_box2.exec_()

def settings():#自定义颜色
    n = QtWidgets.QDialog()
    ui4 = Color_Setting.Ui_Color_Setting()
    ui4.setupUi(n)
    n.exec()
    startpart = '''
    {
    "colors":[
    '''
    endpart = '''
    ]
    }'''
    a = addsomething()
    with open("setting.json","w+") as f:
        l =startpart + a +endpart
        f.write(l)

def addsomething():
    items = []
    for i in range(24):
#        print("start" + str(i))
        t = gotit(i)
        if(t == ""):
            continue
        else:
            items.append(t)
#        print("end" + str(i))
    return ",".join(items)

def gotit(index):
#    print("mid" + str(index))
    if (Color_Select.selfcmya[index] != ""):
        x = Color_Select.selfcmya[index][0]
        y = Color_Select.selfcmya[index][1]
        z = Color_Select.selfcmya[index][2]
        if (Color_Select.selfcolor[index] != ""):
            t = Color_Select.selfcolor[index]
            u = getRGB(Color_Select.selfcolor[index])[0]
            v = getRGB(Color_Select.selfcolor[index])[1]
            w = getRGB(Color_Select.selfcolor[index])[2]
        else:
            t = Color_Select.selfcolor[index]
            u = 0
            v = 0
            w = 0
        return """
            {{
                "colorname":"{0}",
                "R":{1},
                "G":{2},
                "B":{3},
                "C":{4},
                "M":{5},
                "Y":{6}
            }}
            """.format(t,u,v,w,x,y,z)
    else:
        return ""

def change(cbname):#平均or自定义互斥选择
    cb = MainWindow.findChild((QtWidgets.QCheckBox,),cbname)
    if ui.much_layers_radio.isChecked():
        ui.layers_num.setEnabled(True)
        ui.layers_num.setText("0")
        ui.checkBox_4.setChecked(False)
        ui.checkBox_3.setChecked(False)
    elif ui.mix_colors_radio.isChecked():
        ui.mix_colors_num.setEnabled(True)
        ui.mix_colors_num.setText("0")
        ui.checkBox.setChecked(False)
        ui.checkBox_2.setChecked(False)
    cb.setChecked(True)



if __name__ == '__main__':
    d = None
    mode = None
    c = ""
    name = None
    global set
    set = True
    global line_correct
    global colorprocess
    global lineprocess
    global writeprocess
    global count
    count = 0
    writeprocess = False
    lineprocess = False
    colorprocess = False
    app = 0  # 解决方案
    with open("setting.json", "r") as f:
        data = json.load(f)
        selfsetting = data['colors']
#        print(data['colors'])  #[{'R':255,'G':255,'B':255,'C':1,'M':1,'Y':1},{the same as below},{}]
        for i in range(len(selfsetting)):
            selfobject = selfsetting[i]
#            print(type(selfobject))
            Color_Select.selfcolor[i] = selfobject["colorname"]
            Color_Select.selfcmya[i] = [selfobject["C"],selfobject["M"],selfobject["Y"]]
            Color_Select.selfprint[i] = "{0}:{1}:{2}".format(selfobject["C"],selfobject["M"],selfobject["Y"])
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = untitled.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.handle.clicked.connect(postprocessingplugin)
    ui.mix_colors_radio.clicked.connect(partial(modeselect,"cc"))
    ui.much_layers_radio.clicked.connect(partial(modeselect,"bb"))
    ui.one_color_radio.clicked.connect(partial(modeselect,"aa"))
    ui.one_color_item.clicked.connect(partial(colorselect,"one_color_item"))
    ui.checkBox.clicked.connect(partial(change,ui.checkBox.objectName()))
    ui.checkBox_2.clicked.connect(partial(change, ui.checkBox_2.objectName()))
    ui.checkBox_3.clicked.connect(partial(change, ui.checkBox_3.objectName()))
    ui.checkBox_4.clicked.connect(partial(change, ui.checkBox_4.objectName()))
    #ui.selectnamein.clicked.connect(loading1)
#    ui.actionOpen.triggered.connect(openfile)
#    ui.actionSave.triggered.connect(savefile)
   # ui.selectnamein.clicked.connect(openfile)
    ui.layers_num.textChanged.connect(addmuchLayers)
    ui.mix_colors_num.textChanged.connect(addmixLayers)
    ui.actionColor_Select.triggered.connect(settings)
    sys.exit(app.exec_())