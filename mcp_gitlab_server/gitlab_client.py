# mcp_gitlab_server/gitlab_client.py

import os
import httpx
from typing import List, Optional, Dict
from .schemas import (
    Project, Issue, Branch,
    MergeRequest, Pipeline, Commit
)

class GitLabClient:
    """
    Asynchronous HTTP wrapper for GitLab REST API.
    """

    def __init__(self, token: Optional[str] = None, base_url: Optional[str] = None):
        if token is None:
            token = os.getenv("GITLAB_TOKEN")
        if not token:
            raise ValueError("GitLab token must be provided via parameter or GITLAB_TOKEN environment variable")

        if base_url is None:
            base_url = os.getenv("GITLAB_URL", "https://gitlab.com/api/v4")

        self.client = httpx.AsyncClient(
            base_url=base_url,
            headers={"Authorization": f"Bearer {token}"}
        )

    async def list_projects(self, search: Optional[str] = None, page: int = 1, per_page: int = 20) -> List[Project]:
        params = {"search": search, "page": page, "per_page": per_page}
        response = await self.client.get("/projects/", params={k: v for k, v in params.items() if v is not None})
        response.raise_for_status()
        return [Project.parse_obj(item) for item in response.json()]

    async def create_issue(self, project_id: int, title: str, description: Optional[str] = None) -> Issue:
        payload = {"title": title, **({"description": description} if description else {})}
        url = f"/projects/{project_id}/issues"
        response = await self.client.post(url, json=payload)
        response.raise_for_status()
        return Issue.parse_obj(response.json())

    async def list_branches(self, project_id: int) -> List[Branch]:
        url = f"/projects/{project_id}/repository/branches"
        response = await self.client.get(url)
        response.raise_for_status()
        return [Branch.parse_obj(item) for item in response.json()]

    # ——————————————————————————————
    # Neue Methoden für MR, Pipelines, Commits, Notes
    # ——————————————————————————————
    async def list_merge_requests(self, project_id: int, state: str = "all", page: int = 1, per_page: int = 20) -> List[MergeRequest]:
        params = {"state": state, "page": page, "per_page": per_page}
        url = f"/projects/{project_id}/merge_requests"
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return [MergeRequest.parse_obj(item) for item in response.json()]

    async def create_merge_request(self, project_id: int, source_branch: str, target_branch: str, title: str, description: Optional[str] = None) -> MergeRequest:
        payload = {
            "source_branch": source_branch,
            "target_branch": target_branch,
            "title": title,
            **({"description": description} if description else {})
        }
        url = f"/projects/{project_id}/merge_requests"
        response = await self.client.post(url, json=payload)
        response.raise_for_status()
        return MergeRequest.parse_obj(response.json())

    async def merge_merge_request(self, project_id: int, merge_request_iid: int) -> MergeRequest:
        url = f"/projects/{project_id}/merge_requests/{merge_request_iid}/merge"
        response = await self.client.put(url)
        response.raise_for_status()
        return MergeRequest.parse_obj(response.json())

    async def list_pipelines(self, project_id: int, ref: Optional[str] = None) -> List[Pipeline]:
        params = {"ref": ref} if ref else {}
        url = f"/projects/{project_id}/pipelines"
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return [Pipeline.parse_obj(item) for item in response.json()]

    async def trigger_pipeline(self, project_id: int, ref: str, variables: Optional[Dict[str, str]] = None) -> Pipeline:
        payload = {"ref": ref}
        if variables:
            # GitLab erwartet eine Liste von {key,value}-Objekten
            payload["variables"] = [{"key": k, "value": v} for k, v in variables.items()]
        url = f"/projects/{project_id}/pipeline"
        response = await self.client.post(url, json=payload)
        response.raise_for_status()
        return Pipeline.parse_obj(response.json())

    async def list_commits(self, project_id: int, ref_name: Optional[str] = None, since: Optional[str] = None, until: Optional[str] = None) -> List[Commit]:
        params = {k: v for k, v in {"ref_name": ref_name, "since": since, "until": until}.items() if v}
        url = f"/projects/{project_id}/repository/commits"
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return [Commit.parse_obj(item) for item in response.json()]

    async def create_note(self, project_id: int, noteable_type: str, noteable_iid: int, body: str) -> Dict:
        url = f"/projects/{project_id}/{noteable_type}/{noteable_iid}/notes"
        response = await self.client.post(url, json={"body": body})
        response.raise_for_status()
        return response.json()

    async def close(self) -> None:
        await self.client.aclose()
