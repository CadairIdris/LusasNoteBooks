from tkinter import *
from PIL import ImageTk, Image      # pip install pillow
import win32com.client as win32
lusas = win32.gencache.EnsureDispatch("Lusas.Modeller.22.0")


def set_support_size(size:int):
    lusas.view().insertAttributesLayer()
    lusas.view().getAttributesLayer().visualiseAll("Supports")
    lusas.view().getAttributesLayer().setMaxArrowSize("Supports", size)


def set_load_arrow_size(size:int):
    lusas.view().insertAttributesLayer()
    lusas.view().getAttributesLayer().visualiseAll("Loading")
    lusas.view().getAttributesLayer().setMaxArrowSize("Loading", size)


def set_deformed_mesh_size(size:int):
    lusas.view().insertDeformLayer()
    lusas.view().setDeformationMagnitude(size, False, True)




root = Tk()
root.title('Sliders')
root.geometry("400x400")

Label(root, text='Support Size').pack()
Scale(root, from_=0, to=20, orient=HORIZONTAL, length=200, command=set_support_size).pack()

Label(root, text='Load Size').pack()
Scale(root, from_=0, to=20, orient=HORIZONTAL, length=200, command=set_load_arrow_size).pack()

Label(root, text='Deformed Mesh Size').pack()
Scale(root, from_=0, to=20, orient=HORIZONTAL, length=200, command=set_deformed_mesh_size).pack()

root.mainloop()