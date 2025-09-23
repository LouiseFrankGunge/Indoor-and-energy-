import ifcopenshell

# Load IFC
model = ifcopenshell.open(r"Indoor-and-energy-\25-01-D-MEP.ifc")


# Categorized ducts
round_ducts = []
rectangular_ducts = []

limit = 0.355#m


# Loop over all duct segments
for duct in model.by_type("IfcFlowSegment"):
    
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




within_limit = []
exceeding = []

for duct, diameter in round_ducts:
    if diameter <= limit:
        within_limit.append(duct)
    else:
        exceeding.append((duct, diameter))

print("\nSummary:")
print(f"  Total round ducts: {len(round_ducts)}")
print(f"  Round ducts ≤ {limit} mm: {len(within_limit)}")
print(f"  Round ducts > {limit} mm: {len(exceeding)}")

if exceeding:
    print("\n Ducts exceeding limit:")
    for duct, diameter in exceeding:
        diameter_mm = diameter * 1000
        print(f"  - {duct.GlobalId} : {diameter_mm:.2f} mm")

