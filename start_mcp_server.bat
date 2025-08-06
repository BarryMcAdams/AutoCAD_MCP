@echo off
echo Starting AutoCAD MCP Server...
echo.

cd /d "C:\Users\barrya\source\repos\AutoCAD_MCP"

echo Checking server dependencies...
poetry check
if errorlevel 1 (
    echo ERROR: Poetry configuration has issues
    pause
    exit /b 1
)

echo.
echo Starting MCP server on localhost:5001...
echo Press Ctrl+C to stop the server
echo.

poetry run python src/server.py

pause