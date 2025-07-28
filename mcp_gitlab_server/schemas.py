# mcp_gitlab_server/schemas.py

from pydantic import BaseModel
from typing import List, Optional, Dict

# ——————————————————————————————
# Grundlegende Ressourcen-Modelle
# ——————————————————————————————
class Project(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    web_url: Optional[str] = None

class Issue(BaseModel):
    id: Optional[int] = None             # hier Optional
    iid: int
    title: str
    description: Optional[str] = None
    state: Optional[str] = None
    web_url: Optional[str] = None

class Branch(BaseModel):
    name: str
    commit: Optional[Dict] = None
    protected: Optional[bool] = None

# ——————————————————————————————
# Argument-Modelle für Tools
# ——————————————————————————————
class ListProjectsArgs(BaseModel):
    search: Optional[str] = None
    page: Optional[int] = 1
    per_page: Optional[int] = 20

class CreateIssueArgs(BaseModel):
    project_id: int
    title: str
    description: Optional[str] = None

class ListBranchesArgs(BaseModel):
    project_id: int

# Bereits definiert in deinem bisherigen Schema:
class ListMergeRequestsArgs(BaseModel):
    project_id: int
    state: Optional[str] = "all"
    page: Optional[int] = 1
    per_page: Optional[int] = 20

class CreateMergeRequestArgs(BaseModel):
    project_id: int
    source_branch: str
    target_branch: str
    title: str
    description: Optional[str] = None

class MergeMergeRequestArgs(BaseModel):
    project_id: int
    merge_request_iid: int

class ListPipelinesArgs(BaseModel):
    project_id: int
    ref: Optional[str] = None

class TriggerPipelineArgs(BaseModel):
    project_id: int
    ref: str
    variables: Optional[Dict[str, str]] = None

class ListCommitsArgs(BaseModel):
    project_id: int
    ref_name: Optional[str] = None
    since: Optional[str] = None
    until: Optional[str] = None

class CreateNoteArgs(BaseModel):
    project_id: int
    noteable_type: str      # "issues" oder "merge_requests"
    noteable_iid: int
    body: str

class MergeRequest(BaseModel):
    id: int
    iid: int
    project_id: int
    title: str
    description: Optional[str] = None
    state: str
    web_url: Optional[str] = None

class Pipeline(BaseModel):
    id: int
    status: str
    ref: str
    sha: Optional[str] = None
    web_url: Optional[str] = None

class Commit(BaseModel):
    id: str
    short_id: str
    title: str
    author_name: str
    created_at: str