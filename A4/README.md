# BIMmanager group 18

**Focus area**
Indoor (and energy)

**Role**

Our role is a BIM manager and the manager level is level 2

**Teach**

The tool used for our A4 teach is different from our A3 tool as we were told that it should focus on something we learned during the course, and not necessarily on the specific tool we chose.

A different tool was therefore implemented instead of using the tool from A3, which also had to be edited, as it was not possible to implement due to the way the IFC model was structured. We chose to explain the different IFC types that MEP elements can be assigned. We also demonstrate how to determine what these elements are called in the specific IFC model you are working with. The topic was chosen because, during the creation of A1, we discovered that in IFC files the names of MEP objects are not always consistent. 

**Summary**

Title: Identifying IFC types in MEP models
Category: Indoor & Energy / Acoustic / Daylight
Description: Explains common IFC type names used in MEP models and shows how to determine which names appear in a given IFC file, addressing inconsistencies where identical components may be assigned different classifications across models.

**Identification of different MEP elements**

The purpose of this assignment is to understand the terminology and object naming conventions used for mechanical components such as pipes, radiators,
and air handling units (AHUs) in Blender, and to compare these with the corresponding terms and structures used in OpenShell.

As mentioned, this is because the components are not always consistently named in the IFC file, as the naming can vary depending on how the model has been structured.
In some cases, elements such as pipes, radiators, or AHUs may be defined as generic or non-specific objects.
As a result, they cannot be easily identified or accessed through Python scripting,
which can complicate the process of linking or manipulating these elements within the MEP model.

**IFC types**

In the table below, is the different names for MEP Categories in IfcOpenShell

| Category | IFC type |
|:------------|:-------------:|
| Duct        | IfcFlowSegement <br> IfcDuctSegement | 
| Pipe        | IfcFlowSegement <br> IfcPipeSegement |
| Radiators/convecters        | IfcBuildingElementProxy <br> IfcSpaceHeater |
| AHU       | IfcBuildingElementProxy <br> IfcUnitaryEquipment |
| Diffuser        | IfcAirTherminal  |
| Duct fitting       | IfcFlowFitting <br> IfcDuctFitting |
| Pipe fitting       | IfcFlowFitting <br> IfcPipeFitting |
| Fan       | IfcFan |
| Coil      | IfcCoil |
| Valve      | IfcValve |
| Pump       | IfcPump |
| Tank       | IfcTank |
| Light fixture       | IfcLightFixture |


As mentioned, the definitions of different components vary between models depending on how each model is structured. The table above shows some of the different names they can have.

For example, you can use IfcFlowSegment to find both ducts and pipes, but if your Python script simply looks for IfcFlowSegments, it won’t distinguish between the two. To make that distinction, you need to use a more specific name, such as IfcDuctSegment.

On the other hand, if you want to find all AHUs (air handling units), that’s not possible directly because they are often defined as IfcBuildingElementProxy objects. This means that if you search for all IfcBuildingElementProxy, you’ll find everything defined under that category and not just the AHUs. There’s no property you can use to differentiate between these components unless you either inspect the model directly or use a report where you can locate the specific GlobalIDs.

**Script for testing**

The script below can be used to identify the various element types present in the model and to generate a list of all GlobalIDs corresponding to each detected type

```python
import ifcopenshell

# Open IFC model
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
        for i in elements:
            print(f" - Type: {i.is_a()} | GlobalID: {i.GlobalId}")
        print()  


```

In our A4.ipynb Jupyter Notebook, there are more scripts demonstrating different ways to check which IFC types are present in the models

*AI Acknowledgment*

Generative AI was used to support the programming skills of the group.












