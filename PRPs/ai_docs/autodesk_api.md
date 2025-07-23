## PRPs/ai_docs/autodesk_api.md

### Autodesk AutoCAD API Reference

- **Overview**: COM-based API for automating AutoCAD operations.
- **Key Objects**:
  - Application: Root object for AutoCAD instance.
  - ModelSpace: For adding entities in model space.
  - PaperSpace: For layout viewports and dimensions.
- **3D Operations**: Add3DMesh, Union, Subtract.
- **Best Practices**: Release objects after use to avoid memory leaks.
- **Gotchas**: API calls are synchronous; handle timeouts for complex operations.