# mcp_gitlab_server/server.py
from mcp_gitlab_server.config import Settings
from mcp.server.fastmcp import FastMCP

settings = Settings()
mcp = FastMCP(
    name=settings.server_name,
    host=settings.host,
    port=settings.port,
    debug=settings.debug,
)

# 1) Ressourcen importieren, um @mcp.resource() auszuführen
import mcp_gitlab_server.resources  # noqa: F401

# 2) Prompts importieren, um @mcp.prompt() auszuführen
import mcp_gitlab_server.prompts    # noqa: F401

# 3) Tools importieren, um @mcp.tool() auszuführen
import mcp_gitlab_server.tools.gitlab_tools  # noqa: F401

app = mcp.app
