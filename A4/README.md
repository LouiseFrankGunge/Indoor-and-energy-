# BIMmanager group 18

**Focus area**
Indoor (and energy)

**Role**

Our role is a BIM manager and the manager level is level 2

**Identification of different MEP elements**

The purpose of this assignment is to understand the terminology and object naming conventions used for mechanical components such as pipes, radiators,
and air handling units (AHUs) in Blender, and to compare these with the corresponding terms and structures used in OpenShell.

This is because the components are not always consistently named in Blender,as the naming can vary depending on how the model has been structured.
In some cases, elements such as pipes, radiators, or AHUs may be defined as generic or non-specific objects.
As a result, they cannot be easily identified or accessed through Python scripting,
which can complicate the process of linking or manipulating these elements within the MEP model.

**IfcOpenShell names**

In the table below, is the different names for MEP componets in IfcOpenShell

| Componet | IfcOpenShell |
|:------------|:-------------:|
| Duct        | IfcFlowSegement <br> IfcDuctSegement | 
| Pipe        | IfcFlowSegement <br> IfcPipeSegement |
| Radiators/convecters        | IfcBuildingElementProxy <br> IfcSpaceHeater |
| AHU       | IfcBuildingElementProxy |
| Diffuser        | IfcAirTherminal |
| Curved duct        | IfcFlowFitting <br> IfcDuctFitting |
| Curved pipe        | IfcFlowFitting <br> IfcPipeFitting |

As mentioned, the definitions of different components vary between models depending on how each model is structured. The table above shows some of the different names they can have.

For example, you can use IfcFlowSegment to find both ducts and pipes, but if your Python script simply looks for IfcFlowSegments, it won’t distinguish between the two. To make that distinction, you need to use a more specific name, such as IfcDuctSegment.

On the other hand, if you want to find all AHUs (Air Handling Units), that’s not possible directly because they are often defined as IfcBuildingElementProxy objects. This means that if you search for all IfcBuildingElementProxy, you’ll find everything defined under that category — not just the AHUs. There’s no property you can use to differentiate between these components unless you either inspect the model directly or use a report where you can locate the specific GlobalIDs.

**Script for testing**

The script below can be used to identify the various element types present in the model and to generate a list of all GlobalIDs corresponding to each detected type

```python
import ifcopenshell

# Open IFC model and replace the path below with your actual IFC file path
model = ifcopenshell.open("")

# Define the IFC types you want to search for
ifc_types = [
    "IfcDuctSegment",
    "IfcPipeSegment"
]

# Search for each type
for ifc_type in ifc_types:
    elements = model.by_type(ifc_type)

    if not elements:
        print(f" {ifc_type} not found in file.\n")
    else:
        print(f" Found {len(elements)} elements of type {ifc_type}:")
        for e in elements:
            print(f" - Type: {e.is_a()} | GlobalID: {e.GlobalId}")
        print()  # Blank line for readability




