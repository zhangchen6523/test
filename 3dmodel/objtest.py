#!/usr/bin/env python
import threading
import time
import vtk

dt = 1  # degree step in rotation
aNum = 0

uActor = None
dActor = None

class MyInteractor(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, parent=None):
        self.AddObserver("CharEvent", self.OnCharEvent)
        self.AddObserver("KeyPressEvent", self.OnKeyPressEvent)

    def OnCharEvent(self, obj, event):
        pass

    def OnKeyPressEvent(self, obj, event):
        global aNum
        key = self.GetInteractor().GetKeySym()

        if (key == "Left"):
            uActor.AddPosition(-dt, 0, 0)

        if (key == "Right"):
            uActor.AddPosition(dt, 0, 0)

        if (key == "Up"):
            print("dt=======" + str(dActor.GetPosition()))
            if (aNum == 0):
                dActor.RotateZ(45)
                aNum = aNum + 1
            else:
                dActor.AddPosition(-dt, dt, 0)

        if (key == "Down"):
            dActor.AddPosition(dt, -dt, 0)

        renWin.Render()
        return


# Create points
p1 = [5.0, 0.0, 0.0]
p2 = [-110.0, 110.0, 0.0]
p3 = [-106.0, 100.0, 0.0]
p4 = [-90.0, 40.0, 0.0]

# LineSource:画两个点的线
def CreateLine():
    lineSource = vtk.vtkLineSource()
    lineSource.SetPoint1(p1)
    lineSource.SetPoint2(p2)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(lineSource.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor

def CreateCurve():
    curvepoints = vtk.vtkPoints()
    curvepoints.InsertNextPoint(p1)
    curvepoints.InsertNextPoint(p2)
    curvepoints.InsertNextPoint(p3)
    curvepoints.InsertNextPoint(p4)

    spline = vtk.vtkParametricSpline()
    spline.SetPoints(curvepoints)

    functionsource = vtk.vtkParametricFunctionSource()
    functionsource.SetParametricFunction(spline)
    functionsource.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(functionsource.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor


def CreateGround():
    # create plane source
    plane = vtk.vtkPlaneSource()
    plane.SetXResolution(50)
    plane.SetYResolution(50)
    plane.SetCenter(0, 0, 0)
    plane.SetNormal(0, 1, 1)
    # mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(plane.GetOutputPort())

    # actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetRepresentationToWireframe()
    # actor.GetProperty().SetOpacity(0.4) # 1.0 is totally opaque and 0.0 is completely transparent
    actor.GetProperty().SetColor(1, 1, 1)

    transform = vtk.vtkTransform()
    transform.Scale(100, 100, 1)
    actor.SetUserTransform(transform)
    return actor


def CreateObj(filePath):
    reader = vtk.vtkOBJReader()
    reader.SetFileName(filePath)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    # print(vtk.VTK_MAJOR_VERSION)
    # if vtk.VTK_MAJOR_VERSION <= 5:
    #     mapper.SetInput(reader.GetOutput())
    # else:
    #     mapper.SetInputConnection(reader.GetOutputPort())

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    r = 0.91
    g = 0.59
    b = 0.48
    actor.GetProperty().SetDiffuseColor(r, g, b)
    return actor


ColorBackground = [.2, .2, .2]
uPath = "u.obj"
dPath = "d.obj"

ren = vtk.vtkRenderer()
ren.SetBackground(ColorBackground)

uActor = CreateObj(uPath)
ren.AddActor(uActor)
dActor = CreateObj(dPath)
ren.AddActor(dActor)

# ren.AddActor(CreateLine())
ren.AddActor(CreateCurve())


renWin = vtk.vtkRenderWindow()
renWin.SetWindowName("Test")
renWin.AddRenderer(ren)
renWin.SetSize(700, 700)
# Create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

style = MyInteractor(CreateObj(uPath))
style.SetDefaultRenderer(ren)
iren.SetInteractorStyle(style)
iren.Initialize()
iren.Start()
