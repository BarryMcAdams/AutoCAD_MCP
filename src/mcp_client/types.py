"""
Type definitions for MCP Client Library.
"""

from dataclasses import dataclass, field
from typing import Any

# Type aliases for better code clarity
Point3D = list[float]  # [x, y, z] coordinates
Vector3D = list[float]  # [x, y, z] vector components
EntityId = int  # AutoCAD entity ID
LayerName = str  # AutoCAD layer name


@dataclass
class EntityInfo:
    """Container for AutoCAD entity information."""

    id: int  # AutoCAD entity ID
    type: str  # Entity class name
    layer: str  # Layer name
    color: int  # Color index
    length: float | None = None  # Length (for lines)
    radius: float | None = None  # Radius (for circles)
    area: float | None = None  # Area (for closed entities)
    volume: float | None = None  # Volume (for solids)
    bounding_box: dict[str, Point3D] | None = None  # Min/max extents
    center_of_mass: Point3D | None = None  # Center point
    material: str | None = None  # Material assignment
    custom_properties: dict[str, Any] = field(default_factory=dict)

    @property
    def is_2d(self) -> bool:
        """Check if entity is 2D (no Z variation)."""
        if self.bounding_box:
            min_z = self.bounding_box["min_point"][2]
            max_z = self.bounding_box["max_point"][2]
            return abs(max_z - min_z) < 1e-6
        return True

    @property
    def is_solid(self) -> bool:
        """Check if entity is a 3D solid."""
        return self.type == "AcDb3dSolid"


@dataclass
class UnfoldResult:
    """Result container for surface unfolding operations."""

    pattern_id: int  # Entity ID of 2D pattern
    entity_type: str  # Type of created pattern entity
    deviation: float  # Area deviation percentage
    original_area: float  # Original 3D surface area
    unfolded_area: float  # Unfolded 2D pattern area
    fold_lines: list[int]  # Entity IDs of fold line markings
    cut_lines: list[int]  # Entity IDs of cut line markings
    method_used: str  # Actual algorithm method used
    success: bool  # Operation success flag
    warnings: list[str]  # Non-critical warnings
    execution_time: float  # Processing time in seconds

    @property
    def area_accuracy(self) -> float:
        """Calculate area accuracy percentage (100% - deviation)."""
        return 100.0 - self.deviation

    def is_manufacturing_ready(self, max_deviation: float = 0.1) -> bool:
        """Check if pattern meets manufacturing tolerances."""
        return self.deviation <= max_deviation and self.success


@dataclass
class LayoutResult:
    """Result container for layout creation operations."""

    layout_name: str  # Created layout name
    viewport_id: int  # Viewport entity ID
    dimensions_added: int  # Number of dimensions created
    dimension_ids: list[int]  # List of dimension entity IDs
    title_block_id: int | None  # Title block entity ID (if created)
    success: bool  # Operation success
    execution_time: float  # Processing time
