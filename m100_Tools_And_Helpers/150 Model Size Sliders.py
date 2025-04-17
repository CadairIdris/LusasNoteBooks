from tkinter import *
import sys; sys.path.append('../') # Reference modules in parent directory
from LPI_22_0 import *
lusas = get_lusas_modeller()


def set_support_size(size:int):
    lusas.view().insertAttributesLayer()
    lusas.view().getAttributesLayer().visualiseAll("Supports")
    lusas.view().getAttributesLayer().setMaxArrowSize("Supports", int(size))


def set_load_arrow_size(size:int):
    lusas.view().insertAttributesLayer()
    lusas.view().getAttributesLayer().visualiseAll("Loading")
    lusas.view().getAttributesLayer().setMaxArrowSize("Loading", int(size))
    lusas.view().getAttributesLayer().setArrowHeadSize("Loading", int(size)/3)


def set_deformed_mesh_size(size:int):
    lusas.view().insertDeformLayer()
    lusas.view().setDeformationMagnitude(size, False, True)


def set_diagrams_size(size:int):
    lusas.view().insertDiagramsLayer()
    lusas.view().getDiagramsLayer().setScaleMagnitude(size)


def set_values_size(size:int):
    lusas.view().insertValuesLayer()
    lusas.view().getValuesLayer().setShowLabels(True, 6, f"Arial;{10*int(size)};Normal;NoItalic;NoUnderline;NoStrikeOut;0;")


root = Tk()
root.title('Scale visualisations')
root.geometry("400x400")

Label(root, text='Support Size').pack()
Scale(root, from_=0, to=20, orient=HORIZONTAL, length=200, command=set_support_size).pack()

Label(root, text='Load Size').pack()
Scale(root, from_=0, to=20, orient=HORIZONTAL, length=200, command=set_load_arrow_size).pack()

Label(root, text='Deformed Mesh Size').pack()
Scale(root, from_=0, to=20, orient=HORIZONTAL, length=200, command=set_deformed_mesh_size).pack()

Label(root, text='Diagrams Size').pack()
Scale(root, from_=0, to=20, orient=HORIZONTAL, length=200, command=set_diagrams_size).pack()

Label(root, text='Values Font Size').pack()
Scale(root, from_=6, to=36, orient=HORIZONTAL, length=200, command=set_values_size).pack()

root.mainloop()