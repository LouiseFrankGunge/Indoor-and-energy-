import ifcopenshell
import math

# ---------------------------
# USER SETTINGS
# ---------------------------

air_density = 1.2      # kg/m³
air_viscosity = 1.8e-5 # Pa·s
flow_rate = 0.8        # m³/s (constant)
default_length = 5.0   # m (fallback if none found)

# ---------------------------
# LOAD IFC MODEL
# ---------------------------
model = ifcopenshell.open("IFC models/Group06_2025/25-06-D-MEP.ifc")

# ---------------------------
# SIMPLE HELPER FUNCTIONS
# ---------------------------
def get_length(duct):
    """Try to read duct length; if not found, use extrusion depth or fallback."""
    # Try BaseQuantities
    for rel in model.get_inverse(duct):
        if rel.is_a("IfcRelDefinesByProperties"):
            prop = rel.RelatingPropertyDefinition
            if prop.is_a("IfcElementQuantity"):
                for q in prop.Quantities:
                    if q.is_a("IfcQuantityLength") and "Length" in q.Name:
                        return float(q.LengthValue)
    # Try geometry extrusion
    if duct.Representation:
        for rep in duct.Representation.Representations:
            for item in rep.Items:
                if item.is_a("IfcExtrudedAreaSolid"):
                    return float(item.Depth)
    return default_length

def friction_factor(Re):
    """Simple Blasius correlation."""
    return 64 / Re if Re < 2300 else 0.3164 / (Re ** 0.25)

def pressure_loss(length, d, v):
    """Darcy–Weisbach pressure loss."""
    Re = air_density * v * d / air_viscosity
    f = friction_factor(Re)
    return f * (length / d) * 0.5 * air_density * v**2

# ---------------------------
# READ ROUND DUCTS
# ---------------------------
ducts = []

for duct in model.by_type("IfcFlowSegment"):
    if not duct.Representation:
        continue
    for rep in duct.Representation.Representations:
        for geom in rep.Items:
            if geom.is_a("IfcExtrudedAreaSolid") and geom.SweptArea.is_a("IfcCircleProfileDef"):
                d = 2 * geom.SweptArea.Radius
                length = get_length(duct)
                area = math.pi * (d / 2) ** 2
                velocity = flow_rate / area
                dp = pressure_loss(length, d, velocity)
                ducts.append((duct, length, d, dp))

# ---------------------------
# FIND CRITICAL PATH (MAX TOTAL ΔP)
# ---------------------------
if not ducts:
    print("⚠️ No round ducts found in IFC file.")
else:
    total_dp = sum(d[3] for d in ducts)
    max_dp = max(d[3] for d in ducts)
    max_duct = max(ducts, key=lambda x: x[3])[0]

    print("\n=== PRESSURE LOSS REPORT ===")
    print(f"Total ducts: {len(ducts)}")
    print(f"Total pressure drop (approx): {total_dp:.2f} Pa")
    print(f"Most critical single duct: {max_duct.GlobalId} with ΔP = {max_dp:.2f} Pa\n")

    print("Detailed results:")
    for duct, length, d, dp in ducts:
        print(f" - {duct.GlobalId}: L={length:.2f} m, D={d*1000:.0f} mm, ΔP={dp:.2f} Pa")

