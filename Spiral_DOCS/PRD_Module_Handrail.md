PRD_Module_Handrail.md
1. Functional Requirement: Continuous Handrail Generation

The system must generate a single, continuous 1.5" diameter 3D solid representing the handrail. The path of this handrail must be smooth (G2 continuity) through all transitions, including from the helical ascent to level mid-landings and the top landing.
2. Technical Specification: Path Generation

    Methodology: The handrail path will be generated as a Spline object in AutoCAD. Using a Helix object is insufficient due to its inability to handle level landings.

    Control Point Calculation:

        Define Handrail Centerline: The centerline of the handrail will be calculated at a fixed horizontal offset (default: 2.0 inches) inward from the outer edge of the treads.

        Generate Helical Points: For the main ascent sections, VBA will calculate a series of 3D points along the helical path. The density of these points should be sufficient to create a smooth curve (e.g., one point every 5-10 degrees of rotation).

        Generate Landing Points: For mid-landings and the top landing, VBA will calculate points along the 90-degree arc (for mid-landings) or straight run-out (for top landings). These points will share the same Z-coordinate.

        Assemble Master Array: All point arrays will be concatenated in the correct order to form a single master array for the AddSpline command.

3. Edge Case: Top Landing Termination

The PRD must define how the handrail terminates at the top landing. This is a critical safety and design detail.

    Option A (Default): Horizontal Run-out. The handrail will continue horizontally past the last riser for a specified distance (default: 12 inches) before terminating. This is the most common and safest configuration.

    Option B (Future): D-Loop Return. The handrail will loop back 180 degrees to connect to a post or wall. This is a more complex geometry but could be a future feature.

    Requirement: The script will implement Option A by default. The transition from the helical path to the horizontal run-out must be tangent and smooth.

4. Geometric Detail: Handrail Height

    Measurement Point: The handrail height (default: 36 inches) will be measured vertically from the tread nosing to the top of the 1.5" handrail profile, as per IBC code.

    Implementation: The Spline path represents the handrail's centerline. Therefore, the Z-coordinates of the control points will be calculated as: TreadNosing_Z + HandrailHeight - (HandrailDiameter / 2).