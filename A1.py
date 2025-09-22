import ifcopenshell
import ifcopenshell.util.element

model = ifcopenshell.open('IFC models/25-01-D-MEP.ifc')

# Extract all elements of type DuctSegement from the model.
All_ducts = model.by_type("IfcDuctSegment")
print(len(All_ducts))
# Get specific obejct type
Target_obejct = "Round Duct:Default"
filter_duct = [d for d in All_ducts if d.ObjectType == Target_obejct]
print(len(filter_duct))

# Set the threshold
max_diameter = 0.355
all_ok = True

count_duct_without_d = 0

#Loop
for duct in filter_duct:
    count = +1
    psets = ifcopenshell.util.element.get_psets(duct)


#    for definition in duct.IsDefinedBy:
#        if definition.RelatingPropertyDefinition.is_a("IfcPropertySet"):
#            pset = definition.RelatingPropertyDefinition
#            print("Pset:", pset.Name)
#            for prop in pset.HasProperties:
#                if prop.is_a("IfcPropertySingleValue"):
#                    try:
#                        val = prop.NominalValue.wrappedValue
#                    except:
#                        val = None
#                    print(f" {prop.Name}: {val}")

    if duct.Representation:
        for rep in duct.Representation.Representations:
            for item in rep.Items:
                if item.is_a("IfcSweptArealSolid"):
                    profile = item.SweptArea
                    if profile.is_a("IfcCircleProfileDef"):
                        diameter = 2*profile.Radius
                        print("Diamter (from profile)", diameter)
                    
#    #Check diameter
#    diameter = None
#    width = None
#    height = None
#
#    for pset_name, props in psets.items():
#        for key, value in props.items():
#            key_lower = key.lower()
#            if 'NorminalDiameter' in key_lower:
#                diameter = value
#            #elif 'width' in key_lower:
#            #    width = value
#            #elif 'height' in key_lower:
#            #    height = value
#
#    if diameter is None:
#        count_duct_without_d +=1
#        print(f"Duct {duct.GlobalId}({duct.ObjectType}) has NO diamter property")
#    else:
#        if float(diameter) < max_diameter:
#            print(f"Duct {duct.GlobalId} ({duct.ObjectType}) diameter {diameter} < {max_diameter}")
#        else:
#            print(f"Duct {duct.GlobalId} ({duct.ObjectType}) diameter {diameter} >= {max_diameter}")
#            all_ok = False
print(count_duct_without_d)

if all_ok:
    print("\n All ducts have a diameter under 355 mm")
else:
    print("\n Some docts are missing diameter info or exceed 355 mm")
print(len(filter_duct))


