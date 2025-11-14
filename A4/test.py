import ifcopenshell


# --- Open IFC model ---
model = ifcopenshell.open("IFC models/Group06_2025/25-06-D-MEP.ifc")  # Replace with your IFC file path

# --- Define the GlobalID to search for ---
target_global_id = "30ac8fta1DGRqfJGwTShxq"

# --- Get all duct segments in the model ---
duct_segments = model.by_type("IfcBuildingElementProxy")

print(f"Found {len(duct_segments)} duct segments:\n")

# --- Collect all GlobalIDs ---
global_ids = []
for duct in duct_segments:
    print(f"Covering: {duct.GlobalId}")
    global_ids.append(duct.GlobalId)

# --- Check if the target ID is in the list ---
if target_global_id in global_ids:
    print(f"\n✅ The GlobalID '{target_global_id}' is present in the duct segments.")
else:
    print(f"\n❌ The GlobalID '{target_global_id}' was NOT found among the duct segments.")
