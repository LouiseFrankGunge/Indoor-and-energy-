***A3 – MEP Component List Generating Tool***
**About the Tool**
Problem Statement

The tool was developed to address a problem identified during the process of completing this assignment.
Initially, the goal was to create a tool that could analyze the critical path and pressure losses in a ventilation system. However, as development progressed, it became clear that too many assumptions and estimations regarding airflow and system properties were required to achieve reliable results.

Additionally, the available MEP IFC models did not include defined connection relationships (IfcRelConnectsPortToElement or IfcRelNests) between system components. This limitation made it impossible to trace how components were connected.

This realization highlighted another issue — none of the Advanced Building Design reports contained a complete component list for any of the MEP systems.

This led to the development of the MEP Component List Generating Tool, which enables system designers to model their systems in BIM software and then export a complete list of all required components (ducts, fittings, terminals, etc.) directly from the IFC file.

The tool allows for quick quantity extraction and supports early design coordination by identifying all elements within each MEP system.

**Description of the Tool**

This script reads an IFC model exported from Revit (or any similar BIM authoring software) and extracts information about MEP components — including ventilation, plumbing, heating, and fire protection systems.

It generates a multi-sheet Excel workbook that includes:

- All individual components (one sheet per system)
- Count and total length per type and size
- A system-wide summary overview

The script only uses explicit geometry (IfcExtrudedAreaSolid) to calculate dimensions such as diameter and length.
This ensures that results are accurate for components modeled as true extrusion solids (e.g., ducts, pipes).

*Limitations*

The accuracy of the tool depends on the property sets and geometry information available in the IFC file.
Connection diameters for fittings are often not included in standard IFC exports, since they are not defined by IfcExtrudedAreaSolid.
Using a bounding box to estimate connected duct or pipe diameters would introduce too much uncertainty, as unrelated elements might fall within the same geometric distance.

Further development would be possible with IFC files that contain more complete MEP connection data.
In that case, the tool could evolve into a foundation for more advanced analytical tools (e.g., flow or pressure calculations).

**Requirements**

Before running the script, make sure you have Python installed and the following packages:

pip install ifcopenshell pandas openpyxl

**How to Use**

1. Open the main script file (main.py or similar).
2. Update the file paths at the bottom of the script:
3. Run the script
4. The resulting Excel file will be saved to the location specified in out_xlsx.


**Output**

Excel Workbook:
MEP_component_list.xlsx

Sheets:
- Ventilation
- Plumbing
- Heating
- Fire Protection
- Electrical (if applicable)
- Other
- SUMMARY

Each system sheet includes the following data columns:
GlobalId | EntityType | ObjectType | Name | Level | Diameter_mm | Length_mm | Length_m

The SUMMARY sheet contains aggregated statistics:

- Total number of components per system
- Total length of ducts and pipes
- Count of unique component types



**Advanced Building Design Context**

Stage of Use:
This tool is most useful in Stage C (Design Development) and Stage D (Detailed Design), where accurate quantity outputs and coordination between disciplines are required.

Relevant Subjects:
The tool would be beneficial for students or professionals within:
- Building Services Engineering
- HVAC Design
- Plumbing Design
- Energy Engineering
- BIM Coordination and Management

Model Requirements:
- IFC elements must contain IfcExtrudedAreaSolid geometry.
- Elements should be classified under correct IFC entities (e.g., IfcDuctSegment, IfcPipeSegment, IfcAirTerminal, etc.).
- Storey names should be properly defined (Level -1, Level 0, Level 1, Level 2, etc.) for accurate level assignment.


*AI Acknowledgment*
Generative AI was used to support the prommaming skills of the group.