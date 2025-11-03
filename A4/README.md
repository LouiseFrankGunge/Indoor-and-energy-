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

Duct - IfcDuctSegement, IfcFlowSegement
Pipe - IfcFlowSegement, IfcPipeSegement
AHU - IfcBuildingElementProxy
Radiators/convecters - IfcBuildingElementProxy, IfcSpaceHeater
Diffuser - IfcAirTherminal

When the pipe or duct is not straight it is called a IfcPipeFitting or IfcDuctFitting or IfcFlowFitting



