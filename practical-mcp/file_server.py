from fastapi import FastAPI

# ------------------------------------------------------------
# Create a FastAPI application
# This MCP server gives the AI access to files.
# ------------------------------------------------------------
app = FastAPI()

# ------------------------------------------------------------
# This dictionary represents the AI's file system.
# In real life this would be:
#   - disk
#   - cloud storage
#   - S3
#   - project folder
#
# We keep it simple for learning.
# ------------------------------------------------------------
files = {
    "tax.txt": "Your 2024 tax document: Income = $100,000",
    "todo.txt": "1. Pay taxes\n2. Book flight"
}

# ------------------------------------------------------------
# MCP Capability Endpoint
# Tells the MCP Client what this server provides
# ------------------------------------------------------------
@app.get("/capabilities")
def caps():
    return {
        # AI can see any file under files/*
        "resources": ["files/*"],

        # AI can perform these actions on files
        "tools": ["read_file", "write_file", "list_files"]
    }

# ------------------------------------------------------------
# MCP Resource Endpoint
# Allows the AI (via MCP Client) to read file contents.
#
# Example:
#   GET /resources/tax.txt
# ------------------------------------------------------------
@app.get("/resources/{path}")
def get_file(path):
    # Return the file contents if it exists
    return files.get(path, "")

# ------------------------------------------------------------
# MCP Tool: read_file
# This allows the AI to request a file by name.
#
# Example:
#   read_file(path="tax.txt")
# ------------------------------------------------------------
@app.post("/tools/read_file")
def read_file(data: dict):
    # Look up the file contents
    return files.get(data["path"], "")

# ------------------------------------------------------------
# MCP Tool: write_file
# Allows the AI to create or overwrite files.
#
# Example:
#   write_file(path="notes.txt", content="Hello world")
# ------------------------------------------------------------
@app.post("/tools/write_file")
def write_file(data: dict):
    # Store or update the file
    files[data["path"]] = data["content"]
    return {"status": "saved"}

# ------------------------------------------------------------
# MCP Tool: list_files
# Allows the AI to see which files exist.
# ------------------------------------------------------------
@app.post("/tools/list_files")
def list_files():
    # Return all filenames
    return list(files.keys())
