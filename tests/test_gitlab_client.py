import pytest
from unittest.mock import patch
from mcp_gitlab_server.gitlab_client import GitLabClient
from mcp_gitlab_server.schemas import Project, Issue, Branch

class DummyResponse:
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code
    def raise_for_status(self):
        if not (200 <= self.status_code < 300):
            import httpx
            raise httpx.HTTPStatusError("Error", request=None, response=None)
    def json(self):
        return self._json

class DummyAsyncClient:
    def __init__(self, response):
        self._response = response
    async def get(self, url, params=None):
        return self._response
    async def post(self, url, json=None):
        return self._response
    async def aclose(self):
        pass

@pytest.fixture
def dummy_projects_response():
    return DummyResponse([{"id":1,"name":"A"},{"id":2,"name":"B"}])

@pytest.fixture
def dummy_issue_response():
    return DummyResponse({"iid":5,"title":"T","description":"D"})

@pytest.fixture
def dummy_branches_response():
    return DummyResponse([{"name":"main"},{"name":"dev"}])

@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("GITLAB_TOKEN", "dummy-token")
    c = GitLabClient()
    return c

@pytest.mark.asyncio
async def test_list_projects(monkeypatch, client, dummy_projects_response):
    monkeypatch.setattr(client, "client", DummyAsyncClient(dummy_projects_response))
    projects = await client.list_projects(search="X", page=1, per_page=2)
    assert isinstance(projects, list)
    assert all(isinstance(p, Project) for p in projects)
    assert [p.id for p in projects] == [1,2]
    await client.close()

@pytest.mark.asyncio
async def test_create_issue(monkeypatch, client, dummy_issue_response):
    monkeypatch.setattr(client, "client", DummyAsyncClient(dummy_issue_response))
    issue = await client.create_issue(project_id=10, title="Bug", description="Desc")
    assert isinstance(issue, Issue)
    assert issue.iid == 5
    assert issue.title == "T"
    await client.close()

@pytest.mark.asyncio
async def test_list_branches(monkeypatch, client, dummy_branches_response):
    monkeypatch.setattr(client, "client", DummyAsyncClient(dummy_branches_response))
    branches = await client.list_branches(project_id=7)
    assert isinstance(branches, list)
    assert all(isinstance(b, Branch) for b in branches)
    assert [b.name for b in branches] == ["main", "dev"]
    await client.close()
