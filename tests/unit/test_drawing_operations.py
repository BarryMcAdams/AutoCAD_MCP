"""
Unit tests for MCP drawing operations.

Tests the actual MCP protocol implementation rather than Flask REST endpoints.
Focuses on the MCP tool handlers and their integration with AutoCAD.
"""

import pytest
import json
from unittest.mock import Mock, patch, AsyncMock
import asyncio

# Import MCP server components
from src.server import _draw_line, _draw_circle, _list_entities, _get_entity_info, _server_status


@pytest.fixture
def mock_autocad():
    """Mock AutoCAD instance for MCP testing."""
    with patch('src.utils.get_autocad_instance') as mock_get_acad:
        # Mock the AutoCAD instance with all necessary properties
        mock_acad = Mock()
        mock_acad.model = Mock()
        mock_acad.ActiveDocument = Mock()
        mock_acad.ActiveDocument.Name = "Test Drawing"
        mock_acad.Visible = True
        
        # Mock modelspace iteration for entity listing
        mock_acad.model.modelspace = []
        
        mock_get_acad.return_value = mock_acad
        yield mock_acad


class TestDrawLine:
    """Test cases for MCP draw_line tool."""
    
    @pytest.mark.asyncio
    async def test_draw_line_success(self, mock_autocad):
        """Test successful line creation via MCP."""
        # Setup mock
        mock_line = Mock()
        mock_line.ObjectID = 12345
        mock_autocad.model.AddLine.return_value = mock_line
        
        # Test MCP tool call
        result_json = await _draw_line([0, 0, 0], [100, 100, 0])
        result = json.loads(result_json)
        
        assert result['success'] is True
        assert result['entity_id'] == 12345
        assert result['start_point'] == [0, 0, 0]
        assert result['end_point'] == [100, 100, 0]
        assert 'message' in result
        
        # Verify AutoCAD was called correctly
        mock_autocad.model.AddLine.assert_called_once_with([0, 0, 0], [100, 100, 0])
    
    @pytest.mark.asyncio
    async def test_draw_line_invalid_point(self):
        """Test line creation with invalid point format."""
        with patch('src.utils.validate_point3d') as mock_validate:
            mock_validate.side_effect = ValueError("Invalid point format")
            
            result_json = await _draw_line([0, 0], [100, 100, 0])  # Invalid 2D point
            result = json.loads(result_json)
            
            assert result['success'] is False
            assert 'error' in result
            assert 'Invalid point format' in result['error']
    
    @pytest.mark.asyncio
    async def test_draw_line_autocad_error(self):
        """Test line creation when AutoCAD connection fails."""
        with patch('src.utils.get_autocad_instance') as mock_get_acad:
            mock_get_acad.side_effect = ConnectionError("AutoCAD not running")
            
            result_json = await _draw_line([0, 0, 0], [100, 100, 0])
            result = json.loads(result_json)
            
            assert result['success'] is False
            assert 'AutoCAD not running' in result['error']


class TestDrawCircle:
    """Test cases for MCP draw_circle tool."""
    
    @pytest.mark.asyncio
    async def test_draw_circle_success(self, mock_autocad):
        """Test successful circle creation via MCP."""
        # Setup mock
        mock_circle = Mock()
        mock_circle.ObjectID = 12346
        mock_autocad.model.AddCircle.return_value = mock_circle
        
        # Test MCP tool call
        result_json = await _draw_circle([50, 50, 0], 25.0)
        result = json.loads(result_json)
        
        assert result['success'] is True
        assert result['entity_id'] == 12346
        assert result['center'] == [50, 50, 0]
        assert result['radius'] == 25.0
        assert 'message' in result
        
        # Verify AutoCAD was called correctly
        mock_autocad.model.AddCircle.assert_called_once_with([50, 50, 0], 25.0)
    
    @pytest.mark.asyncio
    async def test_draw_circle_negative_radius(self, mock_autocad):
        """Test circle creation with negative radius."""
        mock_autocad.model.AddCircle.side_effect = Exception("Invalid radius")
        
        result_json = await _draw_circle([0, 0, 0], -10.0)
        result = json.loads(result_json)
        
        assert result['success'] is False
        assert 'error' in result
    
    @pytest.mark.asyncio
    async def test_draw_circle_invalid_center(self):
        """Test circle creation with invalid center point."""
        with patch('src.utils.validate_point3d') as mock_validate:
            mock_validate.side_effect = ValueError("Invalid center point")
            
            result_json = await _draw_circle([0, 0], 10.0)  # Invalid 2D point
            result = json.loads(result_json)
            
            assert result['success'] is False
            assert 'Invalid center point' in result['error']


class TestListEntities:
    """Test cases for MCP list_entities tool."""
    
    @pytest.mark.asyncio
    async def test_list_entities_success(self, mock_autocad):
        """Test successful entity listing via MCP."""
        # Setup mock entities
        mock_entity1 = Mock()
        mock_entity1.ObjectID = 1001
        mock_entity1.ObjectName = "AcDbLine"
        mock_entity1.Layer = "0"
        mock_entity1.Length = 100.0
        
        mock_entity2 = Mock()
        mock_entity2.ObjectID = 1002
        mock_entity2.ObjectName = "AcDbCircle"
        mock_entity2.Layer = "CIRCLES"
        mock_entity2.Area = 78.54
        
        mock_autocad.model.modelspace = [mock_entity1, mock_entity2]
        
        # Test MCP tool call
        result_json = await _list_entities()
        result = json.loads(result_json)
        
        assert result['success'] is True
        assert result['count'] == 2
        assert len(result['entities']) == 2
        
        # Verify entity information
        entities = result['entities']
        assert entities[0]['id'] == 1001
        assert entities[0]['type'] == "AcDbLine"
        assert entities[0]['layer'] == "0"
        assert 'length' in entities[0]
        
        assert entities[1]['id'] == 1002
        assert entities[1]['type'] == "AcDbCircle"
        assert entities[1]['layer'] == "CIRCLES"
        assert 'area' in entities[1]
    
    @pytest.mark.asyncio
    async def test_list_entities_empty(self, mock_autocad):
        """Test entity listing with no entities."""
        mock_autocad.model.modelspace = []
        
        result_json = await _list_entities()
        result = json.loads(result_json)
        
        assert result['success'] is True
        assert result['count'] == 0
        assert result['entities'] == []
    
    @pytest.mark.asyncio
    async def test_list_entities_autocad_error(self):
        """Test entity listing when AutoCAD connection fails."""
        with patch('src.utils.get_autocad_instance') as mock_get_acad:
            mock_get_acad.side_effect = Exception("AutoCAD connection lost")
            
            result_json = await _list_entities()
            result = json.loads(result_json)
            
            assert result['success'] is False
            assert 'AutoCAD connection lost' in result['error']


class TestGetEntityInfo:
    """Test cases for MCP get_entity_info tool."""
    
    @pytest.mark.asyncio
    async def test_get_entity_info_success(self, mock_autocad):
        """Test successful entity info retrieval via MCP."""
        # Setup mock entity
        mock_entity = Mock()
        mock_entity.ObjectID = 12345
        mock_entity.ObjectName = "AcDbLine"
        mock_entity.Layer = "0"
        mock_entity.StartPoint = (0, 0, 0)
        mock_entity.EndPoint = (100, 100, 0)
        mock_entity.Length = 141.42
        
        mock_autocad.model.modelspace = [mock_entity]
        
        with patch('src.utils.extract_entity_properties') as mock_extract:
            mock_extract.return_value = {
                "id": 12345,
                "type": "AcDbLine", 
                "layer": "0",
                "start_point": [0, 0, 0],
                "end_point": [100, 100, 0],
                "length": 141.42
            }
            
            # Test MCP tool call
            result_json = await _get_entity_info(12345)
            result = json.loads(result_json)
            
            assert result['success'] is True
            assert result['entity']['id'] == 12345
            assert result['entity']['type'] == "AcDbLine"
            assert result['entity']['layer'] == "0"
    
    @pytest.mark.asyncio
    async def test_get_entity_info_not_found(self, mock_autocad):
        """Test entity info retrieval for non-existent entity."""
        mock_autocad.model.modelspace = []
        
        result_json = await _get_entity_info(99999)
        result = json.loads(result_json)
        
        assert result['success'] is False
        assert 'Entity not found' in result['error']
        assert result['message'] == "No entity found with ID 99999"


class TestServerStatus:
    """Test cases for MCP server_status tool."""
    
    @pytest.mark.asyncio
    async def test_server_status_success(self, mock_autocad):
        """Test successful server status retrieval via MCP."""
        mock_autocad.ActiveDocument.Name = "Test Drawing.dwg"
        
        result_json = await _server_status()
        result = json.loads(result_json)
        
        assert result['success'] is True
        assert result['mcp_server'] == "running"
        assert result['autocad_connected'] is True
        assert result['active_document'] == "Test Drawing.dwg"
        assert result['tools_available'] == 8
        assert result['tools_advanced'] == 1
        assert 'LSCM Surface Unfolding' in result['advanced_algorithms']
        assert result['transport'] == "stdio"
    
    @pytest.mark.asyncio
    async def test_server_status_autocad_disconnected(self):
        """Test server status when AutoCAD is disconnected."""
        with patch('src.utils.get_autocad_instance') as mock_get_acad:
            mock_get_acad.side_effect = Exception("AutoCAD not available")
            
            result_json = await _server_status()
            result = json.loads(result_json)
            
            assert result['success'] is False
            assert result['mcp_server'] == "running"
            assert result['autocad_connected'] is False
            assert 'AutoCAD not available' in result['error']
            assert "AutoCAD connection failed" in result['message']


class TestMCPToolsIntegration:
    """Integration tests for MCP tools working together."""
    
    @pytest.mark.asyncio
    async def test_draw_and_list_workflow(self, mock_autocad):
        """Test drawing entities and then listing them via MCP."""
        # Setup mock entities
        mock_line = Mock()
        mock_line.ObjectID = 1001
        mock_line.ObjectName = "AcDbLine"
        mock_line.Layer = "0"
        mock_line.Length = 100.0
        
        mock_circle = Mock()
        mock_circle.ObjectID = 1002
        mock_circle.ObjectName = "AcDbCircle"
        mock_circle.Layer = "0"
        mock_circle.Area = 78.54
        
        # Mock drawing operations
        mock_autocad.model.AddLine.return_value = mock_line
        mock_autocad.model.AddCircle.return_value = mock_circle
        mock_autocad.model.modelspace = [mock_line, mock_circle]
        
        # Draw line
        line_result = await _draw_line([0, 0, 0], [100, 0, 0])
        line_data = json.loads(line_result)
        assert line_data['success'] is True
        
        # Draw circle
        circle_result = await _draw_circle([50, 50, 0], 25.0)
        circle_data = json.loads(circle_result)
        assert circle_data['success'] is True
        
        # List entities
        list_result = await _list_entities()
        list_data = json.loads(list_result)
        assert list_data['success'] is True
        assert list_data['count'] == 2
        assert list_data['entities'][0]['type'] == "AcDbLine"
        assert list_data['entities'][1]['type'] == "AcDbCircle"
    
    @pytest.mark.asyncio
    async def test_get_entity_after_draw(self, mock_autocad):
        """Test drawing an entity and then retrieving its info via MCP."""
        # Setup mock
        mock_line = Mock()
        mock_line.ObjectID = 12345
        mock_line.ObjectName = "AcDbLine"
        mock_line.Layer = "0"
        
        mock_autocad.model.AddLine.return_value = mock_line
        mock_autocad.model.modelspace = [mock_line]
        
        with patch('src.utils.extract_entity_properties') as mock_extract:
            mock_extract.return_value = {
                "id": 12345,
                "type": "AcDbLine",
                "layer": "0"
            }
            
            # Draw line
            line_result = await _draw_line([0, 0, 0], [100, 0, 0])
            line_data = json.loads(line_result)
            assert line_data['success'] is True
            entity_id = line_data['entity_id']
            
            # Get entity info
            info_result = await _get_entity_info(entity_id)
            info_data = json.loads(info_result)
            assert info_data['success'] is True
            assert info_data['entity']['id'] == entity_id
            assert info_data['entity']['type'] == "AcDbLine"
    
    @pytest.mark.integration
    @pytest.mark.skip(reason="Requires AutoCAD 2025 running")
    async def test_real_autocad_integration(self):
        """Integration test with actual AutoCAD instance."""
        # This would test with real AutoCAD - skipped for unit tests
        pass