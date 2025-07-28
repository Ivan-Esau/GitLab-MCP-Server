# tests/test_prompts.py

import pytest
import os
from mcp_gitlab_server.prompts import (
    generate_merge_request_description,
    summarize_issue,
    generate_release_notes,
    create_changelog_entry,
    review_code_snippet,
    escalate_issue,
)

@pytest.fixture(autouse=True)
def dummy_gitlab_token(monkeypatch):
    """
    Setzt automatisch eine Dummy-Umgebungsvariable GITLAB_TOKEN,
    damit Settings() in server.py beim Import keine ValidationError wirft.
    """
    monkeypatch.setenv('GITLAB_TOKEN', 'dummy_token')

@pytest.mark.parametrize(
    "title, summary, expected",
    [
        ("Feature X implementiert", "Beschreibung des Features.", "### Feature X implementiert\n\nBeschreibung des Features.\n"),
        ("", "", "### \n\n\n"),
    ],
)
def test_generate_merge_request_description(title, summary, expected):
    """
    Prüft, dass die Merge-Request-Beschreibung korrekt formatiert wird,
    auch für leere Titel und Summary.
    """
    result = generate_merge_request_description(title, summary)
    assert result == expected, f"Unerwartetes Ergebnis: {result!r}"

@pytest.mark.parametrize(
    "title, description, expected_prefix, expect_truncation",
    [
        ("Bugfix", "Ein kurzer Beschreibungstext.", "Issue **Bugfix**: Ein kurzer Beschreibungstext.", False),
        ("LongTitle", "A" * 150, None, True),  # >100 Zeichen → Trunkierung erwartet
    ],
)
def test_summarize_issue(title, description, expected_prefix, expect_truncation):
    """
    Summarize_issue sollte bei kurzen Beschreibungen den vollen Text mit '...'
    zurückgeben und bei langen Texten auf 100 Zeichen plus '...' truncieren.
    """
    result = summarize_issue(title, description)
    assert result.endswith("..."), "Erwartet immer '...' am Ende"
    if expect_truncation:
        # Gesamtlänge von Präfix + 100 Zeichen + "..."
        expected_len = len(f"Issue **{title}**: ") + 100 + 3
        assert len(result) == expected_len, f"Erwartete Länge {expected_len}, got {len(result)}"
    else:
        assert result == expected_prefix + "...", f"Unerwarteter zusammengefügter Text: {result!r}"

def test_generate_release_notes():
    """
    Prüft, dass generate_release_notes eine Liste von Titeln in eine
    Release-Notes-Section umwandelt.
    """
    titles = ["Initial Commit", "Feature A", "Bugfix B"]
    expected = "## Release Notes\n- Initial Commit\n- Feature A\n- Bugfix B"
    assert generate_release_notes(titles) == expected

def test_create_changelog_entry():
    """
    Prüft, dass create_changelog_entry Version und Notes korrekt formatiert.
    """
    version = "v1.2.3"
    notes = "- Added X\n- Fixed Y"
    expected = "## [v1.2.3]\n- Added X\n- Fixed Y"
    assert create_changelog_entry(version, notes) == expected

def test_review_code_snippet_returns_static_comment():
    """
    review_code_snippet liefert einen festen Hinweistext für beliebigen Code.
    """
    snippet = "def foo(): pass"
    expected = "Sieht gut aus, achte auf PEP8-Konventionen."
    assert review_code_snippet(snippet) == expected

@pytest.mark.parametrize(
    "issue_id, urgency, expected",
    [
        (42, "hoch", "Issue #42 muss dringend bearbeitet werden (Dringlichkeit: hoch)."),
        (0, "niedrig", "Issue #0 muss dringend bearbeitet werden (Dringlichkeit: niedrig)."),
    ],
)
def test_escalate_issue(issue_id, urgency, expected):
    """
    Prüft, dass escalate_issue die Issue-ID und Dringlichkeit korrekt einsetzt.
    """
    result = escalate_issue(issue_id, urgency)
    assert result == expected, f"Unerwartetes Ergebnis für escalate_issue({issue_id}, {urgency!r}): {result!r}"
