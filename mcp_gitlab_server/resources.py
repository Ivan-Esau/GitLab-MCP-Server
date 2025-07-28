# mcp_gitlab_server/resources.py
from mcp_gitlab_server.server import mcp
from .config import Settings
from .gitlab_client import GitLabClient

settings = Settings()

@mcp.resource("resource://gitlab-client")
async def gitlab_client() -> GitLabClient:
    """
    Stellt eine Singleton-Instanz des GitLabClient bereit,
    konfiguriert durch die Settings (Single Source of Truth).
    """
    return GitLabClient(
        token=settings.gitlab_token,
        base_url=settings.gitlab_url
    )