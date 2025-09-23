import ifcopenshell
import ifcopenshell.geom

# Load IFC

model = ifcopenshell.open("25-01-D-MEP.ifc")


# Collect duct segments
ducts = model.by_type("IfcFlowSegment")

for duct in ducts:
    # Some ducts are round, some rectangular → check the geometry
    if duct.Representation:
        for rep in duct.Representation.Representations:
            for item in rep.Items:
                # Round ducts usually use IfcCircleProfileDef
                if item.is_a("IfcExtrudedAreaSolid"):
                    profile = item.SweptArea
                    if profile.is_a("IfcCircleProfileDef"):
                        print("Round duct:", duct.GlobalId)
                        print("  Diameter:", 2 * profile.Radius)
                    elif profile.is_a("IfcRectangleProfileDef"):
                        # Rectangular ducts
                        print("Rectangular duct:", duct.GlobalId)
                        print("  Width:", profile.XDim)
                        print("  Height:", profile.YDim)
