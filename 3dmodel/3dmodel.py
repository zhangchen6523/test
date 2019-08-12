#!/usr/bin/env python

import vtk

# Create the importer and read a file
importer = vtk.vtk3DSImporter()
# importer.ComputeNormalsOn()
importer.SetFileName("3d.3ds")
importer.Read()

# Here we let the importer create a renderer and a render window for
# us. We could have also create and assigned those ourselves like so:
# renWin = vtk.vtkRenderWindow()
# importer.SetRenderWindow(renWin)

# Assign an interactor.
# We have to ask the importer for it's render window.
renWin = importer.GetRenderWindow()
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
# iren.SetRotation(45)

# Set the render window's size
renWin.SetSize(1700, 700)

# Set some properties on the renderer.
# We have to ask the importer for it's renderer.

ren = importer.GetRenderer()
ren.SetBackground(0.1, 0.2, 0.4)

iren.Initialize()
iren.Start()

