# This file provides the functionality behind the dialog in #150

import ctypes  # An included library with Python install.
from LPI_22_0 import *

def msgbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

lusas  : 'IFModeller' = None
db : "IFDatabase"     = None

def initialise(modellr):
	global lusas, db 
	lusas = modellr
	db = lusas.database()


# %% 
''' Match Assignments '''


def __copy_assignments(geoms:list[IFGeometry], attrType:str) -> None:
	# Get a list of the assignments for the given attribute
	primary_assignments : list[IFAssignment] = geoms[0].getAssignments(attrType)
	# For each assignment get the corresponding attribute
	for a in range(0, len(primary_assignments)):
		attr = primary_assignments[a].getAttribute()
		# and assign it to the remaining selected surfaces, using the original assignment details
		for i in range(1, len(geoms)):
			attr.assignTo(geoms[i], primary_assignments[a])
			
def __copy_groups(geoms:list[IFGeometry]) -> None:
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
''' Shell results Tables '''


def __get_display_components_shells(entity: str) -> list:
    # We just want the "Standard" components without the additional energy or UDRs
    if entity == "Force/Moment - Thick Shell": 
        return["Nx","Ny","Nxy","Mx","My","Mxy","Sx","Sy"]

    # Default to everything
    return lusas.view().getResultsComponentNames(entity)



def __create_shell_table():

    # Get the result being displayed
    entity, component = None
    lusas.view().contours().getResults(entity, component)
    # And the transformation
    sType, rXYAngle, extraInfo1, extraInfo2 = None
    lusas.view().contours().getResultsTransformData(sType, rXYAngle, extraInfo1, extraInfo2)	

    # Get the primary component being used - if any
    hasPrimary, primaryEntity, primaryComponent = None
    hasPrimary = lusas.view().getActiveLoadset().hasPrimaryComponent(primaryEntity, primaryComponent)

    # Create the PRW
    attr = db.createPrintResultsWizard("___TEMPORARY___")
    attr.setUnits(None)
    attr.setResultsType("Components")
    attr.setResultsOrder("Mesh")
    attr.setResultsContent("Tabular")
    attr.setExtent("Selection", "")
    attr.setLoadcasesOption("Active")
	
    # Reported Entity and Components
    attr.setResultsEntity(entity)	
    attr.setComponents(__get_display_components_shells(entity))
    # Transformation
    match sType:
        case "Global":
            attr.setResultsTransformGlobal()
        case "Feature":
            attr.setResultsTransformFeature()
        case "Local Coords":
            attr.setResultsTransformLocal(extraInfo1, extraInfo2)
        case _:
            msgbox(f"Un Transformed results -> {sType} {rXYAngle} {extraInfo1} {extraInfo2}")


    if entity == "Reactions":
        attr.setResultsLocation("Nodal")
    else:
        attr.setResultsLocation("ElementNodal")


    # Primary Components
    if hasPrimary: 
        attr.setPrimaryResultsData(list(primaryComponent), list(primaryEntity))

    # Options
    attr.setAnalysisResultTypes(None)
    attr.showCoordinates(False)
    attr.showExtremeResults(False)
    attr.setSlice(False)
    attr.setAllowDerived(False)
    attr.setDisplayNow(True)

    # TODO - get model precision
    if 0 :	
        attr.setSigFig(6, False)
        attr.setThreshold(None)
    else :
        attr.setDecimalPlaces(1)
        attr.setThreshold(0.05)

    # Display
    if 0 :
        attr.showResults() # Debug save to treeview
    else:
        attr.showResults(True)	


def show_shell_results():
     
    if lusas.selection().countelements() < 1:
        msgbox("Select a element")
        return

    if not lusas.view().existsContoursLayer():
        msgbox("No contours")
        return

    __create_shell_table()





# %%
''' Beam results Tables '''


def __get_display_components_beams(entity: str) -> list:
    # We just want the "Standard" components without the additional energy or UDRs
    if entity == "Force/Moment - Thick 2D Beam": 
        return["Fx","Fy","Mz"]
    if entity == "Force/Moment - Thick 3D Beam": 
        return ["Fx","Fy","Fz","Mx","My","Mz"]

    # Default to everything
    return lusas.view().getResultsComponentNames(entity)



def __create_beam_table():

    # Get the result being displayed
    entity, component = None
    lusas.view().contours().getResults(entity, component)

    # Get the primary component being used - if any
    hasPrimary, primaryEntity, primaryComponent = None
    hasPrimary = lusas.view().getActiveLoadset().hasPrimaryComponent(primaryEntity, primaryComponent)

    # Create the PRW
    attr = db.createPrintResultsWizard("___TEMPORARY___")
    attr.setUnits(None)
    attr.setResultsType("Components")
    attr.setResultsOrder("Mesh")
    attr.setResultsContent("Tabular")
    attr.setExtent("Selection", "")
    attr.setLoadcasesOption("Active")
	
    attr.setResultsLocation("Element Nodal")	

    # Reported Entity and Components
    attr.setResultsEntity(entity)	
    attr.setComponents(__get_display_components_beams(entity))

    # Primary Components
    if hasPrimary: 
        attr.setPrimaryResultsData(list(primaryComponent), list(primaryEntity))

    # Options
    attr.setAnalysisResultTypes(None)
    attr.showCoordinates(True)
    attr.showExtremeResults(False)
    attr.setSlice(False)
    attr.setAllowDerived(False)
    attr.setDisplayNow(True)

    # TODO - get model precision
    if 0 :	
        attr.setSigFig(6, False)
        attr.setThreshold(None)
    else :
        attr.setDecimalPlaces(1)
        attr.setThreshold(0.05)

    # Display
    if 0 :
        attr.showResults() # Debug save to treeview
    else:
        attr.showResults(True)	


def show_beam_results():
     
    if lusas.selection().countelements() < 1:
        msgbox("Select a line")
        return

    if not lusas.view().existsDiagramsLayer():
        msgbox("No diagrams")
        return

    __create_beam_table()



















# %%
''' Reactions '''
def plot_reactions():
    fx, fy, fz = 0, 0, 0
    for n in lusas.database().getObjects("Node"):
        fx += n.getResults("Reaction", "FX")[0] if n.hasResults("Reaction", "FX") else 0
        fy += n.getResults("Reaction", "FY")[0] if n.hasResults("Reaction", "FY") else 0
        fz += n.getResults("Reaction", "FZ")[0] if n.hasResults("Reaction", "FZ") else 0

    lusas.getTextWindow().writeLine(f"Total reactions : {fx:.2f}, {fy:.2f}, {fz:.2f}")




# %%
''' Next Section '''