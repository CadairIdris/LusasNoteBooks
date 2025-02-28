from tkinter import *
import win32com.client as win32
lusas = win32.gencache.EnsureDispatch("Lusas.Modeller.22.0")


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



root = Tk()
root.title('Sliders')
root.geometry("400x400")

Label(root, text='Support Size').pack()
Scale(root, from_=0, to=20, orient=HORIZONTAL, length=200, command=set_support_size).pack()

Label(root, text='Load Size').pack()
Scale(root, from_=0, to=20, orient=HORIZONTAL, length=200, command=set_load_arrow_size).pack()

Label(root, text='Deformed Mesh Size').pack()
Scale(root, from_=0, to=20, orient=HORIZONTAL, length=200, command=set_deformed_mesh_size).pack()

Label(root, text='Diagrams Size').pack()
Scale(root, from_=0, to=20, orient=HORIZONTAL, length=200, command=set_diagrams_size).pack()

root.mainloop()