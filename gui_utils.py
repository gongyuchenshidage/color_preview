import vtk
import params


def findStlOrigin(vtkBlock):
    bound = [0, 0, 0, 0, 0, 0]
    vtkBlock.GetBounds(bound)
    x_mid = (bound[0] + bound[1]) / 2
    y_mid = (bound[2] + bound[3]) / 2
    return x_mid, y_mid, bound[4]


def getBounds(vtkBlock):
    bound = [0, 0, 0, 0, 0, 0]
    vtkBlock.GetBounds(bound)
    return bound


def createPlaneActorCircle(x):
    return createPlaneActorCircleByCenter(x)


def createPlaneActorCircleByCenter(center):
    cylinder = vtk.vtkCylinderSource()#形状
    cylinder.SetResolution(50)
    cylinder.SetRadius(params.PlaneDiameter / 2)#大小
    cylinder.SetHeight(0.1)#高度
    cylinder.SetCenter(center[0], center[2] - 0.1, center[1])#中心
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(cylinder.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(params.PlaneColor)#颜色
    actor.RotateX(90)
    return actor


def createPlaneActorCircleByCenterAndRot(center, x_rot, z_rot):  # TODO: rename me
    cylinder = vtk.vtkCylinderSource()
    cylinder.SetResolution(50)
    cylinder.SetRadius(params.PlaneDiameter / 3)  # TODO: remove hardcode
    cylinder.SetHeight(0.1)
    # cylinder.SetCenter(center[0], center[2] - 0.1, center[1])  # WHAT? vtk :(
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(cylinder.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(params.PlaneColor)
    actor.GetProperty().SetOpacity(0.3)
    actor.RotateX(90)
    # actor.RotateX(x_rot)
    # actor.SetPosition(center[0], center[1],center[2] - 0.1)
    # actor.RotateY(x_rot)
    # actor.GetUserTransform()
    transform = vtk.vtkTransform()
    transform.PostMultiply()
    transform.RotateX(x_rot)
    transform.PostMultiply()
    transform.RotateZ(z_rot)
    transform.Translate(center[0], center[1], center[2] - 0.1)
    actor.SetUserTransform(transform)
    return actor


def createAxes(interactor):
    axesWidget = vtk.vtkOrientationMarkerWidget()
    rgba = [0] * 4
    vtk.vtkNamedColors().GetColor("Carrot", rgba)
    axesWidget.SetOutlineColor(rgba[0], rgba[1], rgba[2])
    axesWidget.SetOrientationMarker(vtk.vtkAxesActor())
    axesWidget.SetInteractor(interactor)
    axesWidget.SetViewport(0.0, 0.0, 0.3, 0.3)
    axesWidget.SetEnabled(1)
    axesWidget.InteractiveOff()
    return axesWidget


def createStlActor(filename):
    reader = vtk.vtkSTLReader()
    reader.SetFileName(filename)
    reader.Update()
    return build_actor(reader), reader


def createStlActorInOriginWithColorize(filename):
    # actor, reader = createStlActor(filename)
    # output = reader.GetOutput()
    # actor = colorizeSTL(output)
    # origin = findStlOrigin(output)
    # print(origin)
    # return actor, (0,0,0)
    return createStlActorInOrigin(filename, colorize=True)


def createStlActorInOrigin(filename, colorize=False):
    actor, reader = createStlActor(filename)
    output = reader.GetOutput()

    if colorize:
        actor = colorizeSTL(output)

    origin = findStlOrigin(output)
    transform = vtk.vtkTransform()
    c = params.PlaneCenter
    transform.Translate(-origin[0] + c[0], -origin[1] + c[1], -origin[2] + c[2])
    actor.SetUserTransform(transform)
    return actor, (-origin[0], -origin[1], -origin[2]), getBounds(output)  # return not origin but applied translation


def makeBlocks(layers):#将离散点变成面片信息
    blocks = []
    for layer in layers:
        points = vtk.vtkPoints()#点云
        lines = vtk.vtkCellArray()
        block = vtk.vtkPolyData()
        points_count = 0
        for path in layer:
            line = vtk.vtkLine()
            for k in range(len(path) - 1):
                points.InsertNextPoint(path[k])
                line.GetPointIds().SetId(0, points_count + k)
                line.GetPointIds().SetId(1, points_count + k + 1)
                lines.InsertNextCell(line)
            points.InsertNextPoint(path[-1])  # not forget to add last point
            points_count += len(path)
        block.SetPoints(points)
        block.SetLines(lines)
        blocks.append(block)
    return blocks


def wrapWithActors(blocks, rotations, lays2rots,color = None,divide = None):
    actors = []
    for i in range(len(blocks)):
        block = blocks[i]
        actor = build_actor(block, True)
        transform = vtk.vtkTransform()
        # rotate to abs coords firstly and then apply last rotation
        transform.PostMultiply()
        transform.RotateX(-rotations[lays2rots[i]].x_rot)
        transform.PostMultiply()
        transform.RotateZ(-rotations[lays2rots[i]].z_rot)

        transform.PostMultiply()
        transform.RotateZ(rotations[-1].z_rot)
        transform.PostMultiply()
        transform.RotateX(rotations[-1].x_rot)
        actor.SetUserTransform(transform)
        if len(color) == 0:
            actor.GetProperty().SetColor(params.LastLayerColor)
        elif len(color) == 1:
            actor.GetProperty().SetColor(color[0][0]/255,color[0][1]/255,color[0][2]/255)
        actors.append(actor)
    if len(color) >1:
        if len(color) == len(actors)-2:
            for i in range(len(color)):
                actors[i].GetProperty().SetColor(color[i][0]/255,color[i][1]/255,color[i][2]/255)
        else:
            for i in range(len(color)):
                for layer in range(divide[i], divide[i + 1]):
                    if len(actors) - 1>=divide[i+1]:
                        actors[layer + 1].GetProperty().SetColor(color[i][0]/255,color[i][1]/255,color[i][2]/255)
                    else:
                        for layer in range(divide[i+1],len(actors)-1):
                            actors[layer + 1].GetProperty().SetColor(color[i][0] / 255, color[i][1] / 255,color[i][2] / 255)
    print(len(actors))
    actors[-1].GetProperty().SetColor(params.LayerColor)
    return actors


def colorizeSTL(output):
    polys = output.GetPolys()
    allpoints = output.GetPoints()

    tocolor = []
    with open(params.ColorizeResult, "rb") as f:
        content = f.read()
        for b in content:
            if b == 1:
                tocolor.append(True)
            else:
                tocolor.append(False)

    triangles = vtk.vtkCellArray()
    triangles2 = vtk.vtkCellArray()
    for i in range(polys.GetSize()):
        idList = vtk.vtkIdList()
        polys.GetNextCell(idList)
        num = idList.GetNumberOfIds()
        if num != 3:
            break

        triangle = vtk.vtkTriangle()
        triangle.GetPointIds().SetId(0, idList.GetId(0))
        triangle.GetPointIds().SetId(1, idList.GetId(1))
        triangle.GetPointIds().SetId(2, idList.GetId(2))

        if tocolor[i]:
            triangles.InsertNextCell(triangle)
        else:
            triangles2.InsertNextCell(triangle)

    trianglePolyData = vtk.vtkPolyData()
    trianglePolyData.SetPoints(allpoints)
    trianglePolyData.SetPolys(triangles)
    trianglePolyData2 = vtk.vtkPolyData()
    trianglePolyData2.SetPoints(allpoints)
    trianglePolyData2.SetPolys(triangles2)

    actor = build_actor(trianglePolyData, True)
    actor.GetProperty().SetColor(params.ColorizeColor)
    actor2 = build_actor(trianglePolyData2, True)

    assembly = vtk.vtkAssembly()
    assembly.AddPart(actor)
    assembly.AddPart(actor2)

    return assembly


def build_actor(source, as_is=False):#source就是面片信息，gcode需要得到面片信息
    mapper = vtk.vtkPolyDataMapper()# 2. 建图（将点拼接成立方体）
    if as_is:
        mapper.SetInputData(source)#gcode信息需要用另外的方法提取
    else:
        mapper.SetInputData(source.GetOutput())#提取解析stl结果的面片信息
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)# 3. 根据2创建执行单元
    return actor


class Plane:
    def __init__(self, tilt, rot, point):
        self.tilted = tilt
        self.x = point[0]
        self.y = point[1]
        self.z = point[2]
        self.rot = rot

    def toFile(self):
        return "X" + str(self.x) + " Y" + str(self.y) + " Z" + str(self.z) + \
               " T" + str(self.tilted).lower() + " R" + str(self.rot)


def read_planes():
    planes = []
    with open(params.AnalyzeResult) as fp:
        for line in fp:
            v = line.strip().split(' ')
            planes.append(Plane(v[3][1:] == "true", float(v[4][1:]),
                                (float(v[0][1:]), float(v[1][1:]), float(v[2][1:]))))
    return planes
