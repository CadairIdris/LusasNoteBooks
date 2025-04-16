import User_Tools_Library as lib
from tkinter import *
import sys; sys.path.append('../') # Reference modules in parent directory
from LPI_22_0 import *
lusas = get_lusas_modeller()

root = Tk()
root.title('User Tools')
root.geometry("400x400")

Button(root, text='Match Surface Assignments', command=lambda:lib.match_assignments_surface(copy_mesh=True)).pack(padx=20, pady=20)

Button(root, text='Match Line Assignments', command=lambda:lib.match_assignments_line(copy_mesh=True)).pack(padx=20, pady=20)

Button(root, text='Show Shell Table Results', command=lambda:lib.show_shell_results()).pack(padx=20, pady=20)

Button(root, text='Show Line Table Results', command=lambda:lib.show_beam_results()).pack(padx=20, pady=20)

Button(root, text='Print Reactions', command=lambda:lib.plot_reactions()).pack(padx=20, pady=20)

root.mainloop()
