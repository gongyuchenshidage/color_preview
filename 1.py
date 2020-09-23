#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re

def readGCode2(filename):
    with open(filename) as f:
        # print(f)
        lines = [line.strip() for line in f]
        color = []
        for line in lines:
            if "G1" in  line or "G0":
                x = float(getValue(line, "X", -1))
                y = float(getValue(line, "Y", -1))
                z = float(getValue(line, "Z", -1))
                if x != -1 and  y != -1 and  z != -1:
                    color.append([x,y,z])
            if len(color) == 1 :
                break
        print(color)



def readGCode1(filename):
    with open(filename) as f:
        # print(f)
        lines = [line.strip() for line in f]
        layer = 0
        d = []
        color = []
        for line in lines:
            if line.startswith(";LAYER:"):
                layer +=1
            if line.startswith("M165"):
                d.append(layer)
                a = float(getValue(line, "A", -1))
                b = float(getValue(line, "B", -1))
                c = float(getValue(line, "C", -1))
                color.append(material_chose(a, b, c))
        d.append(layer)
        print(d,color)


def material_chose(user_a,user_b,user_c):
    """挤料比例模块"""
    color = []
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
        if  user_a == i['C'] and user_b == i['M'] and user_c == i['Y']:
            color = [i['R'],i['G'],i['B']]
    if len(color) == 0:
        total = user_a + user_b + user_c
        color = [255-255*user_a/total,255-255*user_b/total,255-255*user_c/total]
    return color

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


readGCode1(r"G:\360MoveData\Users\Administrator\Desktop\stl_file\gongyuchen.gcode")
