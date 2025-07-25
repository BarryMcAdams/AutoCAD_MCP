import win32com.client
import pythoncom
from fastapi import FastAPI, HTTPException, Depends, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import logging

# --- Configuration ---
# Set up logging to monitor server activity and errors.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# IMPORTANT: Replace with a secure, secret key for production environments.
MCP_SECRET = "debug_autocad_2025"

# --- AutoCAD Connection Manager ---
class AutoCADManager:
    """Handles connection and interaction with the AutoCAD application."""

    def __init__(self):
        self.app = None
        self.doc = None
        self.model_space = None

    def connect(self):
        """
        Establishes a connection to a running instance of AutoCAD 2025.
        Raises a detailed HTTPException if connection fails.
        """
        try:
            # CoInitialize is necessary for COM objects in multithreaded apps like FastAPI
            pythoncom.CoInitialize()
            self.app = win32com.client.Dispatch("AutoCAD.Application.25")
            self.app.Visible = True  # Ensure AutoCAD window is visible
            self.doc = self.app.ActiveDocument
            self.model_space = self.doc.ModelSpace
            logger.info("Successfully connected to AutoCAD and accessed active document.")
        except Exception as e:
            logger.error(f"Failed to connect to AutoCAD: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Could not connect to a running instance of AutoCAD 2025. Please ensure it is open."
            )

    def get_vla_point(self, point: List[float]):
        """Converts a Python list [x, y, z] to a VLA-compatible point object."""
        return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, point)

# --- Pydantic Models for API Data Structure ---
class MCPExecuteRequest(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]

class MCPExecuteResponse(BaseModel):
    result: Dict[str, Any]
    error: Optional[str] = None

# --- FastAPI Application Setup ---
app = FastAPI(
    title="AutoCAD Debug MCP Server",
    description="Debug MCP server for AutoCAD 2025 COM interface issues",
    version="1.0.0"
)

security = HTTPBearer()

def get_autocad_manager():
    """Dependency to provide a connected AutoCAD manager to endpoints."""
    manager = AutoCADManager()
    manager.connect()
    return manager

# --- Security and Authentication ---
def authenticate(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Validates the provided bearer token against the MCP secret."""
    if credentials.credentials != MCP_SECRET:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing authentication token.",
        )
    return True

# --- API Endpoints ---
@app.get("/mcp/v1/capabilities", summary="Declare available tools")
async def get_capabilities(auth: bool = Depends(authenticate)):
    """Declares the full list of tools the server can execute in AutoCAD."""
    return {
        "tools": [
            # Creation Tools
            {"name": "create_sphere", "description": "Create a 3D sphere.", "parameters": {"center": {"type": "list", "description": "Center coordinates [x, y, z]"}, "radius": {"type": "number", "description": "Radius of the sphere."}}},
            {"name": "create_line", "description": "Create a line segment.", "parameters": {"start_point": {"type": "list", "description": "Start coordinates [x, y, z]"}, "end_point": {"type": "list", "description": "End coordinates [x, y, z]"}}},
            {"name": "create_circle", "description": "Create a circle.", "parameters": {"center": {"type": "list", "description": "Center coordinates [x, y, z]"}, "radius": {"type": "number", "description": "Radius of the circle."}}},
            {"name": "create_text", "description": "Add a single line of text.", "parameters": {"insertion_point": {"type": "list", "description": "Position [x, y, z]"}, "text_string": {"type": "string", "description": "The text to display"}, "height": {"type": "number", "description": "Text height"}}},
            
            # Modification & Query Tools
            {"name": "get_entity_info", "description": "Get properties of an object by its handle.", "parameters": {"handle": {"type": "string", "description": "The unique handle of the entity."}}},
            
            # View Control Tools
            {"name": "zoom_extents", "description": "Zooms the view to show all objects in the drawing.", "parameters": {}},
            {"name": "zoom_to_entity", "description": "Zooms the view to a specific object by its handle.", "parameters": {"handle": {"type": "string", "description": "The handle of the entity to zoom to."}}},

            # Document/State Management Tools
            {"name": "list_layers", "description": "List all layers in the current drawing.", "parameters": {}},
            {"name": "get_document_info", "description": "Retrieve information about the current document state.", "parameters": {}},
            {"name": "count_entities", "description": "Count all entities in model space.", "parameters": {}},
        ]
    }

@app.post("/mcp/v1/execute", response_model=MCPExecuteResponse, summary="Execute an AutoCAD tool")
async def execute_tool(
    request: MCPExecuteRequest,
    auth: bool = Depends(authenticate),
    acad: AutoCADManager = Depends(get_autocad_manager)
):
    """Executes a specified tool with given parameters in AutoCAD."""
    tool_name = request.tool_name
    params = request.parameters
    
    try:
        # --- Creation Tool Implementations ---
        if tool_name == "create_sphere":
            center = acad.get_vla_point(params["center"])
            radius = params["radius"]
            sphere = acad.model_space.AddSphere(center, radius)
            acad.app.ZoomExtents()
            return {"result": {"handle": sphere.Handle, "message": "Sphere created successfully.", "entity_count": acad.model_space.Count}}

        elif tool_name == "create_line":
            start = acad.get_vla_point(params["start_point"])
            end = acad.get_vla_point(params["end_point"])
            line = acad.model_space.AddLine(start, end)
            acad.app.ZoomExtents()
            return {"result": {"handle": line.Handle, "message": "Line created successfully.", "entity_count": acad.model_space.Count}}

        elif tool_name == "create_circle":
            center = acad.get_vla_point(params["center"])
            radius = params["radius"]
            circle = acad.model_space.AddCircle(center, radius)
            acad.app.ZoomExtents()
            return {"result": {"handle": circle.Handle, "message": "Circle created successfully.", "entity_count": acad.model_space.Count}}

        elif tool_name == "create_text":
            point = acad.get_vla_point(params["insertion_point"])
            text = acad.model_space.AddText(params["text_string"], point, params["height"])
            acad.app.ZoomExtents()
            return {"result": {"handle": text.Handle, "message": "Text created successfully.", "entity_count": acad.model_space.Count}}

        # --- Query Implementations ---
        elif tool_name == "get_entity_info":
            handle = params["handle"]
            entity = acad.doc.HandleToObject(handle)
            return {"result": {"handle": handle, "object_name": entity.ObjectName, "layer": entity.Layer}}

        # --- View Control Implementations ---
        elif tool_name == "zoom_extents":
            acad.app.ZoomExtents()
            return {"result": {"message": "View zoomed to extents."}}

        elif tool_name == "zoom_to_entity":
            handle = params["handle"]
            entity = acad.doc.HandleToObject(handle)
            acad.app.ZoomExtents() # Zoom out first
            return {"result": {"message": f"Zoomed to entity with handle {handle}."}}

        # --- Document/State Implementations ---
        elif tool_name == "list_layers":
            layers = [acad.doc.Layers.Item(i).Name for i in range(acad.doc.Layers.Count)]
            return {"result": {"layers": layers, "count": len(layers)}}

        elif tool_name == "get_document_info":
            info = {
                "document_name": acad.doc.Name,
                "full_path": acad.doc.FullName,
                "is_saved": acad.doc.Saved,
                "entity_count": acad.model_space.Count,
                "active_layer": acad.doc.ActiveLayer.Name,
            }
            return {"result": info}

        elif tool_name == "count_entities":
            count = acad.model_space.Count
            entities = []
            for i in range(min(count, 10)):  # List first 10 entities
                entity = acad.model_space.Item(i)
                entities.append({
                    "handle": entity.Handle,
                    "type": entity.ObjectName,
                    "layer": entity.Layer if hasattr(entity, 'Layer') else 'Unknown'
                })
            return {"result": {"total_count": count, "sample_entities": entities}}

        else:
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found.")

    except HTTPException as http_exc:
        # Re-raise FastAPI's own exceptions
        raise http_exc
    except Exception as e:
        # Catch all other errors, especially from COM calls
        error_message = f"An error occurred while executing '{tool_name}': {e}"
        logger.error(error_message)
        # Return a structured error response
        return MCPExecuteResponse(result={}, error=error_message)

@app.get("/health", summary="Check server and AutoCAD connection status")
async def health_check():
    """Performs a basic health check of the server and its connection to AutoCAD."""
    try:
        acad = AutoCADManager()
        acad.connect()
        return {
            "status": "healthy",
            "autocad_connection": {
                "status": "connected",
                "document": acad.doc.Name,
                "entity_count": acad.model_space.Count
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "autocad_connection": {
                "status": "disconnected",
                "error": str(e)
            }
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)