# BIMmanager group 18

**Group information**

Coding level: 2 - neutral 

Focus area: Indoor (and Energy)

We are managers of the group

**Researched Claim**

Model: 25-06-D-MEP

Claim: Critical path analysis of the pressure loss (page 25)

Description: We are testing if the claim about the critical presurre loss for the different AHU. By calling the differnet ducts and other components that together form the most critical path.

**Use Case and tool idea**

The tool aims to automate the analysis of pressure losses in a buildings ventilation system using IFC based BIM data. By using Ifcopenshell in Python, the tool extracts ducts, fittings and terminal elements from the IFC model and constructs a network representation of the ventilation system. It then calculates the pressure loss along each path, identifies the critical path with the highest total resistance, and reports the results. This makes performance checking without manual calculations possible. It thereby supports HVAC engingeers by reducing calculation time and they can instead focus on optimizing the system design and efficiency. It can also be used as a tool in the procees of documenting compliance with regulations according to BR18.


The BPMN diagram demonstrates the process of checking the claim, outlining the phases necessary to carry out the analysis.

![alt text](<A2_Pressure loss.svg>)



**Information Requirements**

To perform the pressure loss analysis the follow information is needed.
- The structure of the ventilation system and the conncetions between each element.
- Geometry and dimensions of each component.
- Property sets with flow and performance data.
 

