

lusas  : 'IFModeller' = None
db : "IFDatabase"     = None

def initialise(modellr):
	global lusas, db 
	lusas = modellr
	db = lusas.database()


# %% 
''' Match Assignments '''


def __copy_assignments(geoms:list, attrType:str) -> None:
	# Get a list of the assignments for the given attribute
	primary_assignments = geoms[0].getAssignments(attrType)
	# For each assignment get the corresponding attribute
	for a in range(0, len(primary_assignments)):
		attr = primary_assignments[a].getAttribute()
		# and assign it to the remaining selected surfaces, using the original assignment details
		for i in range(1, len(geoms)):
			attr.assignTo(geoms[i], primary_assignments[a])
			
def __copy_groups(geoms:list) -> None:
	for g in db.getObjects("Group"):
		if geoms[0].isMemberOfGroup(g):
			for i in range(1, len(geoms)):
				g.add(geoms[i])
				
def __cycle_relative():
	tempSetA = lusas.newObjectSet()
	tempSetA.add(lusas.selection(), "Surface")
	tempSetA.cycleRelative(lusas.geometryData().setAllDefaults())
	

def match_assignments_surface(copy_mesh:bool):
    if lusas.selection().countSurfaces() < 2:
        lusas.AfxMsgBox("You must select at least two surfaces")
    else:
        # get the list of selected surfaces
        surfaces = lusas.selection().getObjects("Surface")

        __copy_assignments(surfaces, "Geometric")
        __copy_assignments(surfaces, "Material")
        __copy_assignments(surfaces, "Loading")
        __copy_assignments(surfaces, "Supports")
        __copy_assignments(surfaces, "Search Area")
        __copy_assignments(surfaces, "Wood-Armer")
        __copy_assignments(surfaces, "Design")
        __copy_groups(surfaces)
        if copy_mesh: # Causes re-mesh
            __cycle_relative()
            __copy_assignments(surfaces, "Mesh")	


def match_assignments_line(copy_mesh:bool):
    if lusas.selection().countLines() < 2:
        lusas.AfxMsgBox("You must select at least two lines")
    else:
        # get the list of selected surfaces
        lines = lusas.selection().getObjects("Lines")

        __copy_assignments(lines, "Geometric")
        __copy_assignments(lines, "Material")
        __copy_assignments(lines, "Loading")
        __copy_assignments(lines, "Supports")
        __copy_assignments(lines, "Search Area")
        __copy_assignments(lines, "Wood-Armer")
        __copy_assignments(lines, "Design")

        if copy_mesh: # Causes re-mesh
            __copy_assignments(lines, "Mesh")	
			


# %%
''' Next Section '''