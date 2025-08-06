"""
AutoCAD MCP Client for NewSpiral Project
Simple REST API client for AutoCAD automation
"""

import requests
import json
from typing import List, Dict, Any, Optional


class AutoCADClient:
    """Client for AutoCAD MCP REST API."""
    
    def __init__(self, base_url: str = "http://localhost:5001"):
        """Initialize the AutoCAD client.
        
        Args:
            base_url: Base URL of the AutoCAD MCP server (default: http://localhost:5001)
        """
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the AutoCAD MCP server is running."""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.json()
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def autocad_status(self) -> Dict[str, Any]:
        """Check AutoCAD connection status."""
        try:
            response = self.session.get(f"{self.base_url}/acad-status")
            return response.json()
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def draw_line(self, start_point: List[float], end_point: List[float]) -> Dict[str, Any]:
        """Draw a line in AutoCAD.
        
        Args:
            start_point: Starting point [x, y, z]
            end_point: Ending point [x, y, z]
            
        Returns:
            Result dictionary with success status and entity ID
        """
        try:
            response = self.session.post(
                f"{self.base_url}/draw/line",
                json={
                    "start_point": start_point,
                    "end_point": end_point
                }
            )
            return response.json()
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def draw_circle(self, center: List[float], radius: float) -> Dict[str, Any]:
        """Draw a circle in AutoCAD.
        
        Args:
            center: Center point [x, y, z]
            radius: Circle radius
            
        Returns:
            Result dictionary with success status and entity ID
        """
        try:
            response = self.session.post(
                f"{self.base_url}/draw/circle",
                json={
                    "center": center,
                    "radius": radius
                }
            )
            return response.json()
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def extrude_profile(self, profile_points: List[List[float]], extrude_height: float) -> Dict[str, Any]:
        """Create a 3D solid by extruding a 2D profile.
        
        Args:
            profile_points: List of 2D points [[x1,y1], [x2,y2], ...]
            extrude_height: Height to extrude
            
        Returns:
            Result dictionary with success status and entity ID
        """
        try:
            response = self.session.post(
                f"{self.base_url}/draw/extrude",
                json={
                    "profile_points": profile_points,
                    "extrude_height": extrude_height
                }
            )
            return response.json()
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def unfold_surface(self, entity_id: int, algorithm: str = "lscm", tolerance: float = 0.001) -> Dict[str, Any]:
        """Unfold a 3D surface for manufacturing.
        
        Args:
            entity_id: AutoCAD entity ID/handle
            algorithm: Unfolding algorithm ("simple" or "lscm")
            tolerance: Maximum distortion tolerance
            
        Returns:
            Result dictionary with pattern data and fold lines
        """
        try:
            response = self.session.post(
                f"{self.base_url}/surface/unfold-advanced",
                json={
                    "entity_id": entity_id,
                    "algorithm": algorithm,
                    "tolerance": tolerance,
                    "generate_fold_lines": True
                }
            )
            return response.json()
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def optimize_patterns(self, patterns: List[Dict], material_sheets: List[Dict]) -> Dict[str, Any]:
        """Optimize material usage with pattern nesting.
        
        Args:
            patterns: List of pattern dictionaries
            material_sheets: List of material sheet specifications
            
        Returns:
            Result dictionary with optimized layout
        """
        try:
            response = self.session.post(
                f"{self.base_url}/pattern/optimize-nesting",
                json={
                    "patterns": patterns,
                    "material_sheets": material_sheets,
                    "algorithm": "best_fit_decreasing"
                }
            )
            return response.json()
        except Exception as e:
            return {"error": str(e), "success": False}


def main():
    """Test the AutoCAD client."""
    client = AutoCADClient()
    
    print("Testing AutoCAD MCP Client...")
    
    # Test server health
    health = client.health_check()
    print(f"Server Health: {health}")
    
    # Test AutoCAD status
    status = client.autocad_status()
    print(f"AutoCAD Status: {status}")
    
    # Test drawing a line (only if AutoCAD is connected)
    if status.get("success"):
        line_result = client.draw_line([0, 0, 0], [100, 100, 0])
        print(f"Line Drawing Result: {line_result}")
    else:
        print("AutoCAD not connected - skipping drawing tests")


if __name__ == "__main__":
    main()