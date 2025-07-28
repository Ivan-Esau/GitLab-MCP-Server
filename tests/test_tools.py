# tests/test_tools.py

import os
os.environ["GITLAB_TOKEN"] = "dummy-token"  # Muss vor allen Projektimports stehen!

import pytest
import pytest_asyncio

# Werkzeuge aus dem richtigen Subpackage importieren
from mcp_gitlab_server.tools.gitlab_tools import (
    list_projects   as tool_list_projects,
    create_issue    as tool_create_issue,
    list_branches   as tool_list_branches,
)
from mcp_gitlab_server.schemas import (
    Project, Issue, Branch,
    ListProjectsArgs, CreateIssueArgs, ListBranchesArgs,
)

class StubClient:
    def __init__(self, result):
        self._result = result
    async def list_projects(self, search, page, per_page):
        return self._result
    async def create_issue(self, project_id, title, description):
        return self._result
    async def list_branches(self, project_id):
        return self._result

@pytest_asyncio.fixture(autouse=True)
def patch_get_client(monkeypatch):
    """
    Monkeypatch get_gitlab_client in mcp_gitlab_server.tools.gitlab_tools,
    damit unsere Stub-Client-Instanz zurückgegeben wird.
    """
    def _factory(result):
        import mcp_gitlab_server.tools.gitlab_tools as gt_module
        # sicherstellen, dass Settings() nicht scheitert
        monkeypatch.setenv("GITLAB_TOKEN", "dummy-token")
        # hier auf das richtige Modul referenzieren!
        monkeypatch.setattr(
            gt_module,
            "get_gitlab_client",
            lambda: StubClient(result),
            raising=True
        )
    return _factory

@pytest.mark.asyncio
async def test_tool_list_projects(patch_get_client):
    dummy = [Project(id=1, name="X")]
    patch_get_client(dummy)
    args = ListProjectsArgs(search=None, page=1, per_page=10)
    res = await tool_list_projects(args)
    assert res == dummy

@pytest.mark.asyncio
async def test_tool_create_issue(patch_get_client):
    dummy = Issue(iid=2, title="T", description="D")
    patch_get_client(dummy)
    args = CreateIssueArgs(project_id=1, title="T", description="D")
    res = await tool_create_issue(args)
    assert res == dummy

@pytest.mark.asyncio
async def test_tool_list_branches(patch_get_client):
    dummy = [Branch(name="dev")]
    patch_get_client(dummy)
    args = ListBranchesArgs(project_id=1)
    res = await tool_list_branches(args)
    assert res == dummy
