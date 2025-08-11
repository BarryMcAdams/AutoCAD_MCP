1. Functional Requirement: Code-Compliant Picket System

The system must generate a complete set of vertical (0.75" square) and horizontal (0.84" round) pickets such that no opening allows a 4-inch sphere to pass through.
2. Technical Specification: Vertical Picket Placement

    Primary Placement: One vertical picket will be placed on each tread.

    Centerline: The picket's centerline will align vertically with the handrail's centerline (2" offset from the tread edge).

    Connection Model:

        Top: The picket solid will be extruded to intersect the bottom surface of the handrail solid. (No complex cope cut will be modeled in v1.0).

        Bottom: The picket solid will be extruded to sit directly on the top surface of the tread solid. (No base plate will be modeled in v1.0).

3. Technical Specification: Horizontal Picket Logic (VBA-Python Interaction)

This is the most complex module and requires a strict protocol.

    3.1. Bay Definition (VBA)

        A "bay" is the 3D space bounded by two adjacent vertical pickets, the tread edge(s) between them, and the underside of the handrail.

        For each bay, VBA will construct a JSON object containing the precise geometric boundaries. These are not just points, but surfaces.

        JSON Schema:
        {
  "bay_id": 1,
  "boundaries": {
    "picket_1_plane": [A, B, C, D], // Plane equation for the inner face of the first picket
    "picket_2_plane": [A, B, C, D], // Plane equation for the inner face of the second picket
    "tread_surface_eq": "params",   // Parameters defining the helical top surface of the tread
    "handrail_underside_eq": "params" // Parameters for the handrail's helical underside
  },
  "parameters": {
    "sphere_diameter": 4.0,
    "horizontal_picket_diameter": 0.84
  }
}

    3.2. Gap Analysis (Python)

        Algorithm: The Python script will use an optimization algorithm (e.g., from the SciPy.optimize library) to solve the problem: "Find the point (x,y,z) within the boundaries that maximizes the minimum distance to any boundary." This is more robust than a brute-force grid search.

        Iterative Process:

            Analyze the initial bay. Find the center of the largest inscribed sphere.

            If the sphere's radius is >= 2.0 inches, a picket is required. The Z-coordinate of the sphere's center becomes the target BaseZ for the new picket.

            This new picket now becomes a new boundary, splitting the bay into two smaller sub-bays (upper and lower).

            The algorithm re-runs recursively on both sub-bays until no gap in any bay can contain a 4-inch sphere.

        Output: The script returns a simple JSON object of the required BaseZ heights for all new horizontal pickets. {"bay_1_heights": [12.5, 25.0], "bay_2_heights": [13.1, 26.2]}.

    3.3. Helical Picket Generation (VBA)

        For each BaseZ height returned by Python, VBA will generate a helical sweep path using the exact same PicketRadius, TurnHeight, and TotalRotation parameters as the handrail.

        For stairs with landings: The path must be a composite Spline (Helix-Arc-Helix) as we detailed previously, ensuring it remains parallel to the main handrail.

        The 0.84" circular profile will be swept along this path to create the final picket solid.

4. Unresolved Question / Edge Case: The First Bay

    Problem: The very first "bay" is the space between the floor and the first horizontal picket. This space is often the largest.

    Requirement: The analysis for the lowest bay must use the floor plane (Z=0) as its bottom boundary instead of a tread surface. The Python script must be able to handle a planar boundary as well as a helical one. This must be explicitly defined in the JSON handoff.