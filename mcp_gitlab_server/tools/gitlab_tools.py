# mcp_gitlab_server/tools/gitlab_tools.py

from mcp_gitlab_server.server import mcp
from mcp_gitlab_server.schemas import (
    ListProjectsArgs, CreateIssueArgs, ListBranchesArgs,
    ListMergeRequestsArgs, CreateMergeRequestArgs, MergeMergeRequestArgs,
    ListPipelinesArgs, TriggerPipelineArgs, ListCommitsArgs, CreateNoteArgs,
    Project, Issue, Branch, MergeRequest, Pipeline, Commit
)
from mcp_gitlab_server.gitlab_client import GitLabClient

def get_gitlab_client() -> GitLabClient:
    """Ermöglicht Tests, einen Dummy-Client via Monkeypatch einzuspeisen."""
    return GitLabClient()

# ——————————————————————————————
# Basis-Tools
# ——————————————————————————————
@mcp.tool(name="gitlab_list_projects", description="Listet GitLab-Projekte")
async def list_projects(args: ListProjectsArgs) -> list[Project]:
    client = get_gitlab_client()
    return await client.list_projects(search=args.search, page=args.page, per_page=args.per_page)

@mcp.tool(name="gitlab_create_issue", description="Erstellt ein GitLab-Issue")
async def create_issue(args: CreateIssueArgs) -> Issue:
    client = get_gitlab_client()
    return await client.create_issue(project_id=args.project_id, title=args.title, description=args.description)

@mcp.tool(name="gitlab_list_branches", description="Listet Branches eines GitLab-Projekts")
async def list_branches(args: ListBranchesArgs) -> list[Branch]:
    client = get_gitlab_client()
    return await client.list_branches(project_id=args.project_id)

# ——————————————————————————————
# Merge-Request-Tools
# ——————————————————————————————
@mcp.tool(name="gitlab_list_merge_requests", description="Listet Merge Requests eines Projekts")
async def list_merge_requests(args: ListMergeRequestsArgs) -> list[MergeRequest]:
    client = get_gitlab_client()
    return await client.list_merge_requests(
        project_id=args.project_id, state=args.state, page=args.page, per_page=args.per_page
    )

@mcp.tool(name="gitlab_create_merge_request", description="Erstellt ein Merge Request")
async def create_merge_request(args: CreateMergeRequestArgs) -> MergeRequest:
    client = get_gitlab_client()
    return await client.create_merge_request(
        project_id=args.project_id,
        source_branch=args.source_branch,
        target_branch=args.target_branch,
        title=args.title,
        description=args.description
    )

@mcp.tool(name="gitlab_merge_merge_request", description="Merget ein offenes Merge Request")
async def merge_merge_request(args: MergeMergeRequestArgs) -> MergeRequest:
    client = get_gitlab_client()
    return await client.merge_merge_request(
        project_id=args.project_id,
        merge_request_iid=args.merge_request_iid
    )

# ——————————————————————————————
# Pipeline-Tools
# ——————————————————————————————
@mcp.tool(name="gitlab_list_pipelines", description="Listet Pipelines eines Projekts")
async def list_pipelines(args: ListPipelinesArgs) -> list[Pipeline]:
    client = get_gitlab_client()
    return await client.list_pipelines(project_id=args.project_id, ref=args.ref)

@mcp.tool(name="gitlab_trigger_pipeline", description="Triggert eine neue Pipeline")
async def trigger_pipeline(args: TriggerPipelineArgs) -> Pipeline:
    client = get_gitlab_client()
    return await client.trigger_pipeline(project_id=args.project_id, ref=args.ref, variables=args.variables)

# ——————————————————————————————
# Commit- und Note-Tools
# ——————————————————————————————
@mcp.tool(name="gitlab_list_commits", description="Listet Commits in einem Projekt-Ref")
async def list_commits(args: ListCommitsArgs) -> list[Commit]:
    client = get_gitlab_client()
    return await client.list_commits(
        project_id=args.project_id,
        ref_name=args.ref_name,
        since=args.since,
        until=args.until
    )

@mcp.tool(name="gitlab_create_note", description="Erstellt einen Kommentar zu Issue oder MR")
async def create_note(args: CreateNoteArgs) -> dict:
    client = get_gitlab_client()
    return await client.create_note(
        project_id=args.project_id,
        noteable_type=args.noteable_type,
        noteable_iid=args.noteable_iid,
        body=args.body
    )
