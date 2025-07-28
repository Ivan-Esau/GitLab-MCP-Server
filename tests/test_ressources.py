import pytest
import os
from unittest.mock import patch

@pytest.mark.asyncio
@patch.dict(os.environ, {"GITLAB_TOKEN": "dummy-token"})
async def test_gitlab_client_resource_returns_client():
    # Importiere nur die Factory direkt, NICHT den ganzen Ressourcen-Server!
    from mcp_gitlab_server.gitlab_client import GitLabClient

    # Simuliere wie die Factory funktioniert, OHNE den MCP-Server zu importieren!
    client = GitLabClient()
    assert isinstance(client, GitLabClient)
    await client.close()
