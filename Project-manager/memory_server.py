from fastapi import FastAPI
from typing import Dict

# ------------------------------------------------------------
# MCP Memory Server for Project Manager AI
# This server stores ALL persistent knowledge of the AI
# ------------------------------------------------------------

app = FastAPI()

# This is the AI's long-term memory store
# Structure:
# {
#   "user/profile": {...},
#   "projects/react-app": {...},
#   "tasks/react-app": [...]
# }
memory: Dict[str, any] = {}

# ------------------------------------------------------------
# MCP CAPABILITIES
# This tells the MCP Client what exists
# ------------------------------------------------------------
@app.get("/capabilities")
def capabilities():
    return {
        "resources": [
            "memory/user/*",
            "memory/projects/*",
            "memory/tasks/*",
            "memory/decisions/*"
        ],
        "tools": [
            "store",
            "retrieve",
            "update",
            "delete",
            "query"
        ]
    }

# ------------------------------------------------------------
# MCP RESOURCE ACCESS
# Allows the AI to READ memory
# Example:
#   GET /resources/memory/projects/react-app
# ------------------------------------------------------------
@app.get("/resources/{path:path}")
def get_resource(path: str):
    key = "memory/" + path
    return memory.get(key, "")

# ------------------------------------------------------------
# MCP TOOL: store
# Save new information into memory
# ------------------------------------------------------------
@app.post("/tools/store")
def store(data: dict):
    key = "memory/" + data["key"]
    memory[key] = data["value"]
    return {"status": "stored", "key": key}

# ------------------------------------------------------------
# MCP TOOL: update
# Modify existing memory
# ------------------------------------------------------------
@app.post("/tools/update")
def update(data: dict):
    key = "memory/" + data["key"]
    memory[key] = data["value"]
    return {"status": "updated", "key": key}

# ------------------------------------------------------------
# MCP TOOL: delete
# Remove memory
# ------------------------------------------------------------
@app.post("/tools/delete")
def delete(data: dict):
    key = "memory/" + data["key"]
    if key in memory:
        del memory[key]
        return {"status": "deleted"}
    return {"status": "not_found"}

# ------------------------------------------------------------
# MCP TOOL: retrieve
# Get one memory value by key
# ------------------------------------------------------------
@app.post("/tools/retrieve")
def retrieve(data: dict):
    key = "memory/" + data["key"]
    return memory.get(key, "")

# ------------------------------------------------------------
# MCP TOOL: query
# Allows the AI to search memory by prefix
# Example:
#   query(prefix="projects/")
# ------------------------------------------------------------
@app.post("/tools/query")
def query(data: dict):
    prefix = "memory/" + data["prefix"]
    results = {}

    for key, value in memory.items():
        if key.startswith(prefix):
            results[key] = value

    return results
