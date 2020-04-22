# *********************************************************
# Laboratoire   : 3 - Leman Map
# Élèves        : Crüll Loris, Jaquet David, Lagier Elodie
# Date          : 4 mai 2020
# *********************************************************

import vtk

# LECTURE DONNEES
with open('altitudes.txt', 'r') as file:
    data_array = file.readlines()
file.close()

# on récupère les dimensions de la map
(map_width, map_height) = data_array[0].split()

# CREATION DE LA MAP DU LEMAN
leman_map = vtk.vtkPolyData()
points = vtk.vtkPoints()
strips = vtk.vtkCellArray()
scalars = vtk.vtkFloatArray()