import ifcopenshell

# Load IFC

model = ifcopenshell.open(r"Indoor-and-energy-\25-01-D-MEP.ifc")


# Storage for categorized ducts
round_ducts = []
rectangular_ducts = []

# Iterate over all ducts
for duct in model.by_type("IfcFlowSegment"):
    if duct.Representation:
        for rep in duct.Representation.Representations:
            for item in rep.Items:
                if item.is_a("IfcExtrudedAreaSolid"):
                    profile = item.SweptArea
                    
                    # Round ducts
                    if profile.is_a("IfcCircleProfileDef"):
                        diameter = 2 * profile.Radius
                        round_ducts.append((duct, diameter))
                    
                    # Rectangular ducts
                    elif profile.is_a("IfcRectangleProfileDef"):
                        width = profile.XDim
                        height = profile.YDim
                        rectangular_ducts.append((duct, width, height))

# Check round ducts against limit
limit = 0.355  # mm

within_limit = []
exceeding = []

for d, dia in round_ducts:
    if dia <= limit:
        within_limit.append(d)
    else:
        exceeding.append((d, dia))


# Print summary
print("\nSummary:")
print(f"  Total round ducts: {len(round_ducts)}")
print(f"  Round ducts ≤ {limit} mm: {len(within_limit)}")
print(f"  Round ducts > {limit} mm: {len(exceeding)}")

# Optionally, list the ones exceeding
if exceeding:
    print("\n Ducts exceeding limit:")
    for duct, dia in exceeding:
        dia_mm = dia * 1000  # convert meters → mm
        print(f"  - {duct.GlobalId} : {dia_mm:.2f} mm")

