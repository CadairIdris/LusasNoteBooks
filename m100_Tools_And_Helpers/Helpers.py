import win32com.client as win32



def initialise(modeller:'IFModeller'):
    global lusas
    lusas = modeller





# Define a useful helper function to create a point from coordinates
def create_point(x:float, y:float, z:float) -> 'IFPoint':
    # geometryData object contains all the settings to perform a geometry creation
    geom_data = lusas.geometryData().setAllDefaults() 
    # set the options for creating points from coordinates
    geom_data.setLowerOrderGeometryType("coordinates")
    # Add the coordinates
    geom_data.addCoords(x, y, z)
    # Create the point and return it. 
    # Note that createPoint returns and IFObjectSet from which we can get the point.
    return win32.CastTo(lusas.database().createPoint(geom_data).getObject("Point"), "IFPoint")


# Define a useful helper function to create a line from two point objects
# Note that we expect two IFPoint objects, these are references to points already created in the model
def create_line_from_points(p1:'IFPoint', p2:'IFPoint') -> 'IFLine':
    # geometryData object contains all the settings to perform a geometry creation
    geom_data = lusas.geometryData().setAllDefaults()         
    # set the options for creating straight lines from points
    geom_data.setCreateMethod("straight")        
    geom_data.setLowerOrderGeometryType("points")

    # Create an object set to contain the points and use this set to create the line
    obs = lusas.newObjectSet()                 
    obs.add(p1)
    obs.add(p2)

    # Create the line, get the line object array from the returned object set
    return win32.CastTo(obs.createLine(geom_data).getObject("Line"), "IFLine")


# Define a useful helper function to create a line from two point coordinates
def create_line(p1:list, p2:list) -> 'IFLine':
    # geometryData object contains all the settings to perform a geometry creation
    geom_data = lusas.geometryData().setAllDefaults()  
    # set the options for creating straight lines from coordinates
    geom_data.setCreateMethod("straight")        
    geom_data.setLowerOrderGeometryType("coordinates")        
    
    # Add the cordinates, lines directions will follow the order of the coordinates
    geom_data.addCoords(p1[0], p1[1], p1[2])    # Set the coordinates of the first point X,Y,Z
    geom_data.addCoords(p2[0], p2[1], p2[2])    # Set the coordinates of the second point X,Y,Z

    # Create the line, get the line objects from the returned object set
    return win32.CastTo(lusas.database().createLine(geom_data).getObject("Line"), "IFLine")


def delete_all_database_contents(db:'IFDatabase'):
    # Close any previous results
    db.closeAllResults()

    # Delete all previous model data
    db.deleteLoadsets("Envelopes")
    db.deleteLoadsets("Smart Combinations")
    db.deleteLoadsets("Basic Combinations")
    db.deleteAllAnalyses()
    db.deleteAllNoGroups()
    db.deleteAllAttributes()
    db.deleteAllUtilities()
    db.deleteAll()

    db.createAnalysisStructural("Analysis 1")



def create_reinforcing_bar_attributes(db:'IFDatabase', diameters:list) -> list:
    names = []
    for dia in diameters:
        name = f"Bar {dia}"
        util = db.createParametricSection(name)
        util.setType("Circular Solid")
        util.setDimensions(['D'], [dia])

        attr = db.createGeometricLine(name)
        attr.setFromLibrary("Utilities", "", name, 0, 0, 0)
        names.append(name)
    return names



def create_circular_section(db:'IFDatabase', name:str, dia:float) -> 'IFAttribute':
    util = db.createParametricSection(name)
    util.setType("Circular Solid")
    util.setDimensions(['D'], [dia])

    attr = db.createGeometricLine(name)
    attr.setFromLibrary("Utilities", "", name, 0, 0, 0)
    return attr
    

def create_rectangular_section(db:'IFDatabase', name:str, breadth:float, depth:float) -> 'IFAttribute':
    util = db.createParametricSection(name)
    util.setType("Rectangular Solid")
    util.setDimensions(['B', 'D'], [breadth, depth])

    attr = db.createGeometricLine(name)
    attr.setFromLibrary("Utilities", "", name, 0, 0, 0)
    return attr
    