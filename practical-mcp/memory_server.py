from fastapi import FastAPI

# ------------------------------------------------------------
# Create a FastAPI application
# This app represents ONE MCP server in the MCP ecosystem.
# It will expose memory to the MCP Client.
# ------------------------------------------------------------
app = FastAPI()

# ------------------------------------------------------------
# This dictionary acts as the AI's long-term memory.
# In real systems this could be a database, Redis, or vector DB.
# For learning purposes, we use a simple Python dictionary.
# ------------------------------------------------------------
memory = {}

# ------------------------------------------------------------
# MCP Capability Endpoint
# The MCP Client calls this to discover:
#   - What resources this server provides
#   - What tools this server provides
# ------------------------------------------------------------
@app.get("/capabilities")
def caps():
    return {
        # This server provides memory resources
        # MCP Client will expose them to the LLM as memory/*
        "resources": ["memory/*"],

        # These are the actions (tools) that the LLM can request
        # via the MCP Client
        "tools": ["store", "retrieve"]
    }

# ------------------------------------------------------------
# MCP Resource Endpoint
# This allows the MCP Client to read stored memory.
# The LLM accesses this as a RESOURCE (read-only).
#
# Example:
#   GET /resources/username
#   → returns memory["username"]
# ------------------------------------------------------------
@app.get("/resources/{key}")
def get_resource(key):
    # Look up the key in memory
    # If it does not exist, return empty string
    return memory.get(key, "")

# ------------------------------------------------------------
# MCP Tool: store
# This allows the LLM (via MCP Client) to write to memory.
#
# Example LLM request:
#   store(key="name", value="Sohaib")
#
# The MCP Client will convert this into:
#   POST /tools/store
#   { "key": "name", "value": "Sohaib" }
# ------------------------------------------------------------
@app.post("/tools/store")
def store(data: dict):
    # Save the key-value pair into memory
    memory[data["key"]] = data["value"]

    # Inform the MCP Client that the operation succeeded
    return {"status": "ok"}

# ------------------------------------------------------------
# MCP Tool: retrieve
# This allows the LLM to ask for a memory value by key.
#
# Example:
#   retrieve(key="name")
# ------------------------------------------------------------
@app.post("/tools/retrieve")
def retrieve(data: dict):
    # Return the stored value (or empty string if missing)
    return memory.get(data["key"], "")
