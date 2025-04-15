from LPI_22_0 import *



def initialise(modeller:'IFModeller'):
    global lusas
    lusas = modeller





def create_point(x:float, y:float, z:float) -> 'IFPoint':
    """Helper function to create a point from coordinates

    Args:
        x (float): Global X coordinate
        y (float): Global Y coordinate
        z (float): Global Z coordinate

    Returns:
        IFPoint: Point in the IFDatabase
    """    
    # geometryData object contains all the settings to perform a geometry creation
    geom_data = lusas.geometryData().setAllDefaults() 
    # set the options for creating points from coordinates
    geom_data.setLowerOrderGeometryType("coordinates")
    # Add the coordinates
    geom_data.addCoords(x, y, z)
    # Create the point and return it. 
    # Note that createPoint returns and IFObjectSet from which we can get the point.
    return win32.CastTo(lusas.database().createPoint(geom_data).getObject("Point"), "IFPoint")


def create_line_from_points(p1:'IFPoint', p2:'IFPoint') -> 'IFLine':
    """Helper function to create a line from two point objects.

    Args:
        p1 (IFPoint): Start point
        p2 (IFPoint): End point

    Returns:
        IFLine: Straight line connecting the two points
    """    
    # geometryData object contains all the settings to perform a geometry creation
    geom_data = lusas.geometryData().setAllDefaults()         
    # set the options for creating straight lines from points
    geom_data.setCreateMethod("straight").setLowerOrderGeometryType("points")        
    # Create an object set to contain the points and use this set to create the line
    obs = lusas.newObjectSet()                 
    obs.add(p1)
    obs.add(p2)
    # Create the line, get the line object array from the returned object set
    return win32.CastTo(obs.createLine(geom_data).getObject("Line"), "IFLine")



def create_line(p1:list, p2:list) -> 'IFLine':
    """Helper function to create a straight line from two point coordinates defined 

    Args:
        p1 (list): List of 3 floats x,y,z
        p2 (list): List of 3 floats x,y,z

    Returns:
        IFLine: Straight line between the two point coordinates
    """    
    assert len(p1) == len(p2) == 3, "Point coordinates must be a list of 3 values (x,y,z)"
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
    """Create geometric attributes representing individual bars in the LUSAS Databse

    Args:
        db (IFDatabase): Reference to the database
        diameters (list): List of diameters for which geometric attributes will be created

    Returns:
        list: Names of the created attributes in the form 'Bar <diameter>'
    """    
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



def create_circular_section(db:'IFDatabase', name:str, dia:float) -> 'IFGeometricLine':
    """Creates a geometric attribute based on a parametric circular definition

    Args:
        db (IFDatabase): Reference to the database
        name (str): Name of the attribute to be created
        dia (float): Diameter

    Returns:
        IFGeometricLine: Reference to the created geometric attribute
    """    
    util = db.createParametricSection(name).setType("Circular Solid").setDimensions(['D'], [dia])
    return db.createGeometricLine(name).setFromLibrary("Utilities", "", name, 0, 0, 0)
    



def create_rectangular_section(db:'IFDatabase', name:str, breadth:float, depth:float) -> 'IFGeometricLine':
    """Creates a geometric attribute based on a parametric rectandular definition

    Args:
        db (IFDatabase): Reference to the database
        name (str): Name of the attribute to be created
        breadth (float): Breadth of the section
        depth (float): Depth of the section

    Returns:
        IFGeometricLine: Reference to the created geometric attribute
    """    
    util = db.createParametricSection(name).setType("Rectangular Solid")
    util.setDimensions(['B', 'D'], [breadth, depth])

    return db.createGeometricLine(name).setFromLibrary("Utilities", "", name, 0, 0, 0)
    