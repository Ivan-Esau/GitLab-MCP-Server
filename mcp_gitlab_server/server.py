# mcp_gitlab_server/server.py
from mcp_gitlab_server.config import Settings
from fastmcp import FastMCP          # neuer Import‑Pfad (empfohlen)

settings = Settings()
mcp = FastMCP(
    name=settings.server_name,
    host=settings.host,
    port=settings.port,
    debug=settings.debug,
)

# Ressourcen, Prompts, Tools wie gehabt importieren …
import mcp_gitlab_server.resources          # noqa: F401
import mcp_gitlab_server.prompts            # noqa: F401
import mcp_gitlab_server.tools.gitlab_tools # noqa: F401

# ↓ NEU: für Streamable HTTP einen ASGI‑App‑Wrapper erzeugen
# Fallback to `mcp.app` if `streamable_http_app` isn’t available (z.B. in Tests)
try:
    app = mcp.streamable_http_app()
except AttributeError:
    app = mcp.app  # Stubs like _DummyFastMCP setzen `app` in __init__
