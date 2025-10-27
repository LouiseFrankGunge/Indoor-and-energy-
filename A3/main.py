import ifcopenshell
import math

# Load IFC
model = ifcopenshell.open("IFC models/Group06_2025/25-06-D-MEP.ifc")


# Categorized ducts
round_ducts = []
rectangular_ducts = []


# Loop over all duct segments
for duct in model.by_type("IfcDuctSegment"):
    
    # Check for geometry representation
    if not duct.Representation:
        continue
    
    # Loop over representations of the duct
    for representation in duct.Representation.Representations:
        
        # Loop over representation items
        for geometry_item in representation.Items:
            
            # Extruded solids
            if not geometry_item.is_a("IfcExtrudedAreaSolid"):
                continue
            
            # 2D profile
            profile = geometry_item.SweptArea
                   
            # Round ducts
            if profile.is_a("IfcCircleProfileDef"):
                diameter = 2 * profile.Radius
                round_ducts.append((duct, diameter))
            # Rectangular ducts
            elif profile.is_a("IfcRectangleProfileDef"):
                width = profile.XDim
                height = profile.YDim
                rectangular_ducts.append((duct, width, height))

    print(f"  - {duct.GlobalId} : {diameter:.2f} mm")