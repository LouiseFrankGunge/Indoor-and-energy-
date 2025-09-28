# BIMmanager group 18

Focus area:
Indoor (and Energy)

Claim: The HVAC system does not contain any round ducts exceeding a diameter of 355 mm.

Report: D_Report_Team01_SubMEP
Page: 5


Description of script:
The Group 18 script ("A1.py") loops over all ducts in the MEP model and classifies them as either round or rectangular. It then checks whether any round ducts exceed the maximum diameter of 355 mm, and counts how many are within the limit (“correct”) and how many exceed it (“wrong”) It does this by checking the geometry. Ducts can be descriped as an extruded circle or rectangle where the radius, height and width is the descriptive dimensions. Finally, it lists the Global IDs and diameters of all ducts that do not comply with the claim.

Summary of analysts scripts:

Group 13:
Link: https://github.com/s223928/Group-13.git


Group 15:
Link: https://github.com/Kolde16/Group-15.git


Group ApocalypseBIM (Group 12): Link: https://github.com/teiturteitur/ApocalypseBIM.git

Group 12 Checks if the ceiling height is at least 2.6 m; if not, it’s flagged in the overview and a new IFC is generated.



