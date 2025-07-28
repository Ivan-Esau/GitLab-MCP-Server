from mcp_gitlab_server.server import mcp

@mcp.prompt(name="generate_merge_request_description", description="Generiert eine Merge-Request-Beschreibung.")
def generate_merge_request_description(title: str, summary: str) -> str:
    return f"### {title}\n\n{summary}\n"

@mcp.prompt(name="summarize_issue", description="Fasst ein Issue kurz zusammen.")
def summarize_issue(title: str, description: str) -> str:
    return f"Issue **{title}**: {description[:100]}..."

@mcp.prompt(name="generate_release_notes", description="Erstellt Release Notes aus MR-Titeln.")
def generate_release_notes(titles: list[str]) -> str:
    notes = "\n".join(f"- {t}" for t in titles)
    return f"## Release Notes\n{notes}"

@mcp.prompt(name="create_changelog_entry", description="Formatiert einen Changelog-Eintrag.")
def create_changelog_entry(version: str, notes: str) -> str:
    return f"## [{version}]\n{notes}"

@mcp.prompt(name="review_code_snippet", description="Erzeugt kurze Code-Review-Kommentare.")
def review_code_snippet(code: str) -> str:
    return "Sieht gut aus, achte auf PEP8-Konventionen."

@mcp.prompt(name="escalate_issue", description="Erzeugt eine Eskalationsnachricht für kritische Issues.")
def escalate_issue(issue_id: int, urgency: str) -> str:
    return f"Issue #{issue_id} muss dringend bearbeitet werden (Dringlichkeit: {urgency})."
