import m150_User_Tools_Library as lib
from tkinter import *
import win32com.client as win32
lusas = win32.gencache.EnsureDispatch("Lusas.Modeller.22.0")
lib.initialise(lusas)


root = Tk()
root.title('User Tools')
root.geometry("400x600")

Button(root, text='Match Surface Assignments', command=lib.match_assignments_surface(copy_mesh=True)).pack(padx=20, pady=20)

Button(root, text='Match Line Assignments', command=lib.match_assignments_line(copy_mesh=True)).pack(padx=20, pady=80)


root.mainloop()
