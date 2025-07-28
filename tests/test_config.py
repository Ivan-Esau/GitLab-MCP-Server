import os
import pytest
from mcp_gitlab_server.config import Settings

def test_settings_defaults_and_env(monkeypatch):
    # Set only the required token
    monkeypatch.delenv("GITLAB_TOKEN", raising=False)
    monkeypatch.setenv("GITLAB_TOKEN", "secret-token")

    s = Settings()
    assert s.server_name == "mcp-gitlab-server"
    assert s.host == "0.0.0.0"
    assert s.port == 8000
    assert s.debug is False
    assert s.gitlab_token == "secret-token"

    # Changing defaults via env
    monkeypatch.setenv("SERVER_NAME", "custom")
    monkeypatch.setenv("HOST", "127.0.0.1")
    monkeypatch.setenv("PORT", "1234")
    monkeypatch.setenv("DEBUG", "true")
    s2 = Settings()
    assert s2.server_name == "custom"
    assert s2.host == "127.0.0.1"
    assert s2.port == 1234
    assert s2.debug is True
