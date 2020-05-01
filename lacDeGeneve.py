# *********************************************************
# Laboratoire   : 3 - Leman Map
# Élèves        : Crüll Loris, Jaquet David, Lagier Elodie
# Date          : 4 mai 2020
# *********************************************************
import vtk

START = 0


def scale_dimensions(w, h):
    return 100000 / w, 100000 / h


# Si les points autour d'un point défini sont égaux à lui, alors il s'agit d'une aire plate -> présence d'un lac.
def test_flat_area(point, matrix_row, points, line_index, column_index):
    pass
    return point \
           == points[line_index - 1][column_index] \
           == points[line_index + 1][column_index] \
           == matrix_row[column_index - 1] \
           == matrix_row[column_index + 1] \
           == points[line_index - 1][column_index + 1] \
           == points[line_index - 1][column_index - 1] \
           == points[line_index + 1][column_index + 1] \
           == points[line_index + 1][column_index - 1]


def build_mapper(mapper_to_build):
    mapper_to_build.SetInputConnection(filter.GetOutputPort())
    mapper_to_build.SetLookupTable(lookupTable)
    mapper_to_build.UseLookupTableScalarRangeOn()


# source : https://github.com/Kitware/VTK/blob/master/Examples/Rendering/Python/rainbow.py
def build_lookuptable(table):
    table.SetTableRange(100, 1000)
    table.SetHueRange(0.3, 0)  # portion de l'arc-en-ciel
    table.SetSaturationRange(0.5, 0)  # l'intensité des couleurs
    table.SetValueRange(0.55, 1)  # luminosité
    table.SetBelowRangeColor(63 / 255, 147 / 255, 232 / 255, 1)  # couleur du lac
    table.UseBelowRangeColorOn()  # active la couleur de la coordonnée la plus basse
    table.Build()


def transform_and_filter(transform, filter):
    filter.SetInputData(leman_map)
    filter.SetTransform(transform)
    transform.RotateZ(-90)
    filter.Update()


def build_map(points, strip, scalars):
    leman_map.SetPoints(points)
    leman_map.SetStrips(strip)
    leman_map.GetPointData().SetScalars(scalars)


file = open('altitudes.txt', 'r')
(width, height) = file.readline().split()
width = int(width)
height = int(height)

map_points = []
horizontal_limit = width - 1
vertical_limit = height - 1
(width_scaling, height_scaling) = scale_dimensions(width, height)

# On créé les différentes structures de données qui vont nous servir à réaliser la map
leman_map = vtk.vtkPolyData()
points = vtk.vtkPoints()
strip = vtk.vtkCellArray()
scalars = vtk.vtkFloatArray()

# INSERTION POINT SELON ALTITUDE
for x in range(START, width):
    row = list(map(int, file.readline().split()))
    map_points.append(row)
    for y in range(START, height):
        points.InsertNextPoint((height_scaling * x, width_scaling * y, row[y]))
        scalars.InsertTuple1(height * x + y, row[y])
file.close()

for x_coordinate in range(START, horizontal_limit):
    strip.InsertNextCell(vertical_limit * 2)
    for y_coordinate in range(START, vertical_limit):
        strip.InsertCellPoint(height * (x_coordinate + 1) + y_coordinate)
        strip.InsertCellPoint(height * x_coordinate + y_coordinate)

# CHECK POUR LES LACS
for i, row in enumerate(map_points):
    for j, val in enumerate(row):
        if (horizontal_limit > i > 0) and (vertical_limit > j > 0) and test_flat_area(val, row, map_points, i, j):
            scalars.SetValue(height * i + j, 0)  # on set les points du lac à une valeur scalaire de 0.

build_map(points, strip, scalars)

transform = vtk.vtkTransform()
filter = vtk.vtkTransformPolyDataFilter()
transform_and_filter(transform, filter)

lookupTable = vtk.vtkLookupTable()
build_lookuptable(lookupTable)

mapper = vtk.vtkPolyDataMapper()
build_mapper(mapper)

actor = vtk.vtkActor()
actor.SetMapper(mapper)

renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(232 / 255, 210 / 255, 252 / 255)  # superbe background mauve (^w^)

# source : https://www.programcreek.com/python/example/14847/vtk.vtkInteractorStyleTrackballCamera
trackball_interactor = vtk.vtkInteractorStyleTrackballCamera()
win_interactor = vtk.vtkRenderWindowInteractor()
ren_win = vtk.vtkRenderWindow()
ren_win.AddRenderer(renderer)
ren_win.SetSize(600, 600)
win_interactor.SetRenderWindow(ren_win)
win_interactor.SetInteractorStyle(trackball_interactor)
win_interactor.Initialize()
win_interactor.Render()
win_interactor.Start()
