import requests
from llm import call_llm

# ------------------------------------------------------------
# List of MCP servers that make up the AI's world
# Each server provides tools and/or resources
# ------------------------------------------------------------
MCP_SERVERS = [
    "http://localhost:8001",  # Memory MCP Server
    "http://localhost:8002"   # File MCP Server
]

# ------------------------------------------------------------
# Ask each MCP server what it can do
# This is how the AI discovers its universe
# ------------------------------------------------------------
def get_capabilities():
    all_caps = []
    for server in MCP_SERVERS:
        caps = requests.get(server + "/capabilities").json()
        all_caps.append(caps)
    return all_caps

# ------------------------------------------------------------
# Ask MCP servers for a resource (read-only data)
# The MCP Client does not know where it lives — it just tries
# ------------------------------------------------------------
def get_resource(resource_path):
    for server in MCP_SERVERS:
        try:
            r = requests.get(server + "/resources/" + resource_path)
            if r.text:
                return r.text
        except:
            pass
    return ""

# ------------------------------------------------------------
# Call a tool (action) on the correct MCP server
# The MCP Client looks for the server that owns the tool
# ------------------------------------------------------------
def call_tool(tool_name, args):
    for server in MCP_SERVERS:
        caps = requests.get(server + "/capabilities").json()
        if tool_name in caps["tools"]:
            return requests.post(
                server + "/tools/" + tool_name,
                json=args
            ).json()

# ------------------------------------------------------------
# Build the world snapshot (context) that the LLM will see
# ------------------------------------------------------------
def build_context(user_message):
    context = ""
    context += "You are an AI assistant.\n"
    context += f"User: {user_message}\n\n"

    # Inject available tools & resources
    context += "Available capabilities:\n"
    for cap in get_capabilities():
        context += str(cap) + "\n"

    return context

# ------------------------------------------------------------
# MCP Agent Loop
# This is where intelligence happens
# ------------------------------------------------------------
user_message = "Show me my tax file."

context = build_context(user_message)

while True:
    # Send the current world snapshot to the LLM
    reply = call_llm(context)

    print("LLM:", reply)

    # If the model is asking to read a file
    if "read_file" in reply:
        # Extract the filename (simple version)
        filename = "tax.txt"

        # Call the real MCP file server
        result = call_tool("read_file", {"path": filename})

        # Add the tool result back into the world
        context += "\nFILE CONTENT:\n" + str(result) + "\n"

    else:
        # The LLM gave a final answer
        break
