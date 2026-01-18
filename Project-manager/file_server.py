from fastapi import FastAPI
from typing import Dict, List

# ------------------------------------------------------------
# Create the FastAPI application
# This is one MCP server in your Project Manager system.
# Its job is to manage project files for the AI.
# ------------------------------------------------------------
app = FastAPI()

# ------------------------------------------------------------
# In-memory "file system"
# In a real application this would be:
#   - your local disk
#   - a cloud bucket (S3, Google Drive, etc.)
#   - or a real database
#
# We structure files by folders:
#   projects/
#   notes/
#   reports/
# ------------------------------------------------------------
files: Dict[str, str] = {
    "projects/react-roadmap.md": "# React Learning Roadmap\n1. Basics\n2. Hooks\n3. Routing",
    "notes/react-notes.md": "Use Vite + React, learn useEffect deeply.",
    "reports/react-progress.md": "Started project setup."
}

# ------------------------------------------------------------
# MCP CAPABILITIES ENDPOINT
# Tells the MCP Client:
#   - What resources exist
#   - What tools the AI can call
# ------------------------------------------------------------
@app.get("/capabilities")
def capabilities():
    return {
        "resources": [
            "files/projects/*",
            "files/notes/*",
            "files/reports/*"
        ],
        "tools": [
            "read_file",
            "write_file",
            "append_file",
            "list_files"
        ]
    }

# ------------------------------------------------------------
# MCP RESOURCE ENDPOINT
# Allows READ-ONLY access to files.
#
# Example:
#   GET /resources/files/projects/react-roadmap.md
# ------------------------------------------------------------
@app.get("/resources/{path:path}")
def get_resource(path: str):
    key = "files/" + path
    return files.get(key, "")

# ------------------------------------------------------------
# TOOL: read_file
# The AI can explicitly request a file.
# ------------------------------------------------------------
@app.post("/tools/read_file")
def read_file(data: dict):
    path = "files/" + data["path"]
    return files.get(path, "")

# ------------------------------------------------------------
# TOOL: write_file
# Creates or overwrites a file.
#
# Example request from MCP Client:
# {
#   "path": "projects/new-plan.md",
#   "content": "My new project plan"
# }
# ------------------------------------------------------------
@app.post("/tools/write_file")
def write_file(data: dict):
    path = "files/" + data["path"]
    files[path] = data["content"]
    return {"status": "saved", "path": path}

# ------------------------------------------------------------
# TOOL: append_file
# Adds new content to an existing file instead of replacing it.
# ------------------------------------------------------------
@app.post("/tools/append_file")
def append_file(data: dict):
    path = "files/" + data["path"]

    if path not in files:
        files[path] = ""

    files[path] += "\n" + data["content"]
    return {"status": "appended", "path": path}

# ------------------------------------------------------------
# TOOL: list_files
# Allows the AI to explore the workspace.
# You can filter by folder (projects, notes, reports).
# ------------------------------------------------------------
@app.post("/tools/list_files")
def list_files(data: dict = None):
    if data and "folder" in data:
        folder = "files/" + data["folder"]
        return [p for p in files.keys() if p.startswith(folder)]

    # If no folder provided, return everything
    return list(files.keys())
