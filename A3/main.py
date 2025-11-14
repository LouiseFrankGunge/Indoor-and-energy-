"""
===============================================================================
 IFC MEP Component List Generator
===============================================================================

Group number: 18
Institution: DTU (Technical University of Denmark)
Course: Advanced BIM
Version: Final
"""

import ifcopenshell
import pandas as pd
from collections import defaultdict

# =============================================================================
# Helper Functions
# =============================================================================
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="pandas")

def get_level_name(element):
    """
    Identify which building level (storey) an element belongs to.

    The IFC model defines a hierarchy of elements inside building storeys
    using `IfcRelContainedInSpatialStructure`. This function extracts the
    `Name` of that storey and applies a **custom mapping** to normalize names.

    Custom mapping (specific for model 25-06_D_MEP.ifc):
        - "L7" → "Level 2"
        - "L1" → "Level 0"
        - "Level X" → keep original

    Parameters
    ----------
    element : ifcopenshell.entity_instance
        The IFC element whose level is to be determined.

    Returns
    -------
    str or None
        The unified level name or None if not found.
    """
    try:
        for rel in getattr(element, "ContainedInStructure", []):
            if rel.is_a("IfcRelContainedInSpatialStructure"):
                level = getattr(rel.RelatingStructure, "Name", None)
                if level:
                    lname = level.strip().lower()
                    # Apply mapping rules
                    if lname == "l7":
                        return "Level 2"
                    elif lname == "l1":
                        return "Level 0"
                    elif lname.startswith("level"):
                        return level  # already a proper level name
                    else:
                        return level  # unexpected label
    except Exception:
        pass
    return None


def extract_geom_dimensions(element):
    """
    Extract diameter and length from the geometry of ducts/pipes.

    This function reads the `IfcExtrudedAreaSolid` geometry representation of
    elements such as IfcDuctSegment or IfcPipeSegment and computes:
        - Diameter (for round or rectangular profiles)
        - Length (extrusion depth)

    Parameters
    ----------
    element : ifcopenshell.entity_instance
        The element to analyze.

    Returns
    -------
    (float, float)
        (diameter_mm, length_mm)
    """
    diameter = length = None
    try:
        rep = getattr(element, "Representation", None)
        if not rep:
            return None, None

        for r in getattr(rep, "Representations", []):
            for item in getattr(r, "Items", []):
                # Only consider extruded solids (typical for ducts/pipes)
                if not item.is_a("IfcExtrudedAreaSolid"):
                    continue

                profile = getattr(item, "SweptArea", None)
                if not profile:
                    continue

                # Round ducts/pipes
                if profile.is_a("IfcCircleProfileDef"):
                    diameter = 2 * float(profile.Radius)
                # Rectangular ducts: approximate equivalent diameter as min dimension
                elif profile.is_a("IfcRectangleProfileDef"):
                    diameter = float(min(profile.XDim, profile.YDim))

                # Extrusion depth corresponds to length
                if hasattr(item, "Depth"):
                    length = float(item.Depth)
    except Exception:
        pass

    return diameter, length


def extract_terminal_diameter(element):
    """
    Determine air terminal inlet/outlet diameter.

    The inlet size is either:
        - Explicitly modeled as geometry (IfcExtrudedAreaSolid)
        - Encoded in the ObjectType string (last three digits, e.g., "GRILLE-160")

    Parameters
    ----------
    element : ifcopenshell.entity_instance
        Air terminal element (IfcAirTerminal, IfcFlowTerminal)

    Returns
    -------
    float or None
        Diameter in millimeters if found, otherwise None.
    """
    d, _ = extract_geom_dimensions(element)
    if d:
        return d
    try:
        objtype = getattr(element, "ObjectType", "") or ""
        digits = "".join([c for c in objtype if c.isdigit()])
        if len(digits) >= 3:
            return float(digits[-3:])
    except Exception:
        pass
    return None


def classify_system(element):
    """
    Classify the element into one of the MEP system categories.

    The classification is determined using the IFC class and keywords found
    in the element's name or ObjectType. This ensures that even proxies or
    misclassified elements are grouped logically by their function.

    Categories:
        Ventilation
        Plumbing
        Heating
        Fire Protection
        Electrical
        Other (default)

    Parameters
    ----------
    element : ifcopenshell.entity_instance

    Returns
    -------
    str
        System name.
    """
    et = element.is_a()
    name = ((getattr(element, "Name", "") or "") + " " +
            (getattr(element, "ObjectType", "") or "")).lower()

    if et.startswith("IfcDuct") or et == "IfcAirTerminal" or "vent" in name or "ahu" in name:
        return "Ventilation"
    if et.startswith("IfcPipe"):
        if any(k in name for k in ["radiator", "heater", "coil", "heat"]):
            return "Heating"
        return "Plumbing"
    if any(k in name for k in ["fire", "sprinkler", "smoke", "damper", "nozzle"]):
        return "Fire Protection"
    if any(k in name for k in ["cable", "light", "switch", "electrical", "panel", "conduit"]):
        return "Electrical"
    return "Other"


# =============================================================================
# Main  Function
# =============================================================================

def build_list(model_path, out_xlsx):
    """
    Process the IFC model and create the Excel component workbook.

    Steps:
    ------
    1. Open the IFC file.
    2. Collect all physical MEP elements (skip ports and virtuals).
    3. Extract relevant data (geometry, type, level, etc.).
    4. Classify each element into a system category.
    5. Export to Excel with:
        - One sheet per system
        - Component list and grouped summary
        - A global summary sheet
    6. Print system totals to the terminal.

    Parameters
    ----------
    model_path : str
        Full path to the IFC file.

    out_xlsx : str
        Path to the output Excel workbook.
    """
    print(f"Opening IFC: {model_path}")
    model = ifcopenshell.open(model_path)

    # -------------------------------------------------------------------------
    # Step 1: Collect all valid elements
    # -------------------------------------------------------------------------
    elements = [
        e for e in model.by_type("IfcElement")
        if not e.is_a("IfcDistributionPort") and not e.is_a("IfcVirtualElement")
    ]
    print(f"Total elements collected: {len(elements)}")

    rows_by_system = defaultdict(list)

    # -------------------------------------------------------------------------
    # Step 2: Process each element
    # -------------------------------------------------------------------------
    for e in elements:
        et = e.is_a()
        gid = getattr(e, "GlobalId", "")
        objtype = getattr(e, "ObjectType", "")
        name = getattr(e, "Name", "")
        level = get_level_name(e)
        sys = classify_system(e)

        diameter = None
        length = None

        # Ducts/pipes: read geometry for diameter + length
        if et in ("IfcDuctSegment", "IfcPipeSegment", "IfcFlowSegment"):
            diameter, length = extract_geom_dimensions(e)

        # Air terminals: diameter from geometry or ObjectType digits
        elif et in ("IfcAirTerminal", "IfcFlowTerminal"):
            diameter = extract_terminal_diameter(e)

        # Other: skip geometry data
        else:
            diameter, length = None, None

        # Store the result row
        row = {
            "GlobalId": gid,
            "EntityType": et,
            "ObjectType": objtype,
            "Name": name,
            "Level": level,
            "Diameter_mm": round(diameter, 1) if diameter else None,
            "Length_mm": round(length, 1) if length else None,
        }
        rows_by_system[sys].append(row)

    # -------------------------------------------------------------------------
    # Step 3: Export all system data to Excel
    # -------------------------------------------------------------------------

    writer = pd.ExcelWriter(out_xlsx, engine="openpyxl")
    summary = []

    print("\n=== Component Summary ===")
    for sys_name, rows in rows_by_system.items():
        df = pd.DataFrame(rows).drop_duplicates(subset=["GlobalId"])
        df["Length_m"] = df["Length_mm"].astype(float) / 1000  # convert to meters


        total_length = df["Length_m"].sum()
        total_components = len(df)

        print(f"{sys_name:<15}: {total_components} components")

        # Group by ObjectType + Diameter for detailed overview
        group = (
            df.groupby(["ObjectType", "Diameter_mm"], dropna=False)
              .agg(Count=("GlobalId", "count"),
                   TotalLength_m=("Length_m", "sum"))
              .reset_index()
              .sort_values(by=["ObjectType", "Diameter_mm"])
        )

        # Write detailed component list and grouped summary
        df.to_excel(writer, sheet_name=sys_name[:31], index=False)
        group.to_excel(writer, sheet_name=sys_name[:31], startrow=len(df) + 3, index=False)

        # Add to global summary
        summary.append({
            "System": sys_name,
            "Components": total_components,
            "Unique ObjectTypes": df["ObjectType"].nunique(),
            "Total length (m)": total_length,
        })

    # -------------------------------------------------------------------------
    # Step 4: Write global summary sheet
    # -------------------------------------------------------------------------
    pd.DataFrame(summary).to_excel(writer, sheet_name="SUMMARY", index=False)
    writer.close()

    print(f"\n✅ Excel workbook written to: {out_xlsx}")


# =============================================================================
# Run Script
# =============================================================================

if __name__ == "__main__":
    # Define IFC input file and output Excel path
    from pathlib import Path

    model_path = Path(r"C:\Users\louis\OneDrive - Danmarks Tekniske Universitet\DTU\Kandidat\7. Semester\41934 Advanced BIM\Modeller\25-06-D-MEP.ifc")
    if not model_path.is_file():
        raise FileNotFoundError(f"No file found at {model_path}!")
    
    out_xlsx = r"C:\Users\louis\OneDrive - Danmarks Tekniske Universitet\DTU\Kandidat\7. Semester\41934 Advanced BIM\Indoor-and-energy-\A3\MEP_component_list.xlsx"

    # Run the tool
    build_list(model_path, out_xlsx)
