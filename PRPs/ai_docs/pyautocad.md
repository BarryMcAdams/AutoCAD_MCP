## PRPs/ai_docs/pyautocad.md

### pyautocad Library Documentation

- **Overview**: pyautocad is a Python library that simplifies interaction with AutoCAD's COM API, allowing programmatic control over drawings, entities, and sessions.
- **Key Methods**:
  - Autocad(create_if_not_exists=True): Initializes or connects to AutoCAD instance.
  - model.AddExtrudedSolid(profile, height, taper): Creates 3D extruded solid.
  - doc.Layouts.Add(name): Adds a new layout tab.
  - model.AddDimAligned(p1, p2, text_pos): Adds linear dimension.
- **Best Practices**: Use within try-except blocks for COM errors; ensure AutoCAD is running.
- **Gotchas**: Limited to Windows; requires administrative privileges for COM registration.