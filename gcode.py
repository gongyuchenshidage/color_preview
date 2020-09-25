import re

from params import InclineXValue, PlaneCenter


class GCode:
    def __init__(self, layers, rotations, lays2rots,color=None,divide = None,center = None):
        self.layers = layers
        self.rotations = rotations
        self.lays2rots = lays2rots
        self.color = color
        self.divide = divide
        self.center = center
        # self.color = color


class Rotation:
    def __init__(self, x, z):
        self.x_rot = x
        self.z_rot = z

    def __str__(self):
        return " x:" + str(self.x_rot) + " z:" + str(self.z_rot)


def parseArgs(args, x, y, z, absolute=True):
    xr, yr, zr = 0, 0, 0
    z_rot = None
    if absolute:
        xr, yr, zr = x, y, z

    for arg in args:
        if len(arg) == 0:
            continue
        if arg[0] == "X":
            xr = float(arg[1:])
        elif arg[0] == "Y":
            yr = float(arg[1:])
        elif arg[0] == "Z":
            zr = float(arg[1:])
        elif arg[0] == "A":
            z_rot = -float(arg[1:])
        elif arg[0] == ";":
            break
        else:
            pass
    if absolute:
        return xr, yr, zr, z_rot
    return xr + x, yr + y, zr + z, z_rot


def parseRotation(args):
    x, _, z, _ = parseArgs(args, 0, 0, 0)
    return Rotation(-x, -z)


def readGCode(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f]
    return parseGCode(lines)

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

def parseGCode(lines):
    path = []
    layer = []
    layers = []#位置信息（源码中的，包含一些其他参数）
    rotations = []
    lays2rots = []
    color = []#颜色信息
    floor = 0#层数
    divide = []#分层信息
    center = None#模型中心位置
    plane = []#位置信息（自己写的，只有xyz坐标值）
    stop = False


    rotations.append(Rotation(0, 0))
    x, y, z = 0, 0, 0
    w,e,r = 0,0,0
    abs_pos = True  # absolute positioning

    def finishLayer():
        nonlocal path, layer
        if len(path) > 1:
            layer.append(path)
        path = [[x, y, z]]
        if len(layer) > 0:
            layers.append(layer)
            lays2rots.append(len(rotations) - 1)
        layer = []

    for line in lines:
        if len(line) == 0:
            continue
        if line.startswith(";LAYER:1"):
            stop = True

        if line.startswith(';'):  # comment
            if line.startswith(";LAYER:"):
                finishLayer()
                floor += 1
            # elif line.startswith(";End"):
            #     break
        # if line.startswith(";LAYER:"):

        if stop is True:
            for i in range(len(plane)):
                w += plane[i][0]
                e += plane[i][1]
                r += plane[i][2]
            w = w / len(plane)
            e = e / len(plane)
            r = r / len(plane)
            stop = False #归位
            if center is None:#保证center只有一个值
                center = [w, e, r]
        else:
            if "G1" in line or "G0" in line:
                a = float(getValue(line, "X", -1))
                b = float(getValue(line, "Y", -1))
                c = float(getValue(line, "Z", -1))
                if a != -1 and b != -1 and c != -1:
                    plane.append([a, -b,-c])
                else:
                    plane.append([a, -b, 0])

            args = line.split(" ")
            if args[0] == "G0" :  # move to (or rotate)
                if len(path) > 1:  # finish path and start new
                    layer.append(path)
                x, y, z, z_rot = parseArgs(args[1:], x, y, z, abs_pos)
                path = [[x, y, z]]
                if z_rot is not None:
                    finishLayer()
                    rotations.append(Rotation(rotations[-1].x_rot, z_rot))
            elif args[0] == "M165":
                 divide.append(floor)
                 a = float(getValue(line, "A", -1))
                 b = float(getValue(line, "B", -1))
                 c = float(getValue(line, "C", -1))
                 color.append(material_chose(a,b,c))

            elif args[0] == "G1" :  # draw to
                x, y, z, _ = parseArgs(args[1:], x, y, z, abs_pos)
                path.append([x, y, z])

            elif args[0] == "G62":  # rotate plate
                finishLayer()  # rotation could not be inside the layer
                rotations.append(parseRotation(args[1:]))
            elif args[0] == "M43":  # incline X
                finishLayer()  # rotation could not be inside the layer
                rotations.append(Rotation(-InclineXValue, rotations[-1].z_rot))
            elif args[0] == "M42":  # incline X BACK
                finishLayer()  # rotation could not be inside the layer
                rotations.append(Rotation(0, rotations[-1].z_rot))
            elif args[0] == "G90":  # absolute positioning
                abs_pos = True
            elif args[0] == "G91":  # relative positioning
                abs_pos = False
            else:
                pass  # skip

    # finishLayer()  # not forget about last layer
    divide.append(floor)
    print(len(divide),floor,len(color),center)


    layers.append(layer)  # add dummy layer for back rotations
    lays2rots.append(len(rotations) - 1)
    # print(layers)
    return GCode(layers, rotations, lays2rots,color,divide,center)#这些应该是每一层单独存储

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