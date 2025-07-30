# tests/conftest.py  (Ergänzungen)

import types, sys, os

# Dummy-Token für Settings
os.environ.setdefault("GITLAB_TOKEN", "dummy_token")

# 1) Fake fastmcp -> stellt FastMCP-Basisklasse bereit
fake_fastmcp = types.ModuleType("fastmcp")
class _DummyFastMCP:
    def __init__(self, *a, **kw):
        self.app = object()          # damit server.py `app = ...` setzen kann
    # No‑ops für Dekoratoren
    def prompt(self, *a, **kw):   return lambda fn: fn
    def resource(self, *a, **kw): return lambda fn: fn
    def tool(self, *a, **kw):     return lambda fn: fn
fake_fastmcp.FastMCP = _DummyFastMCP
sys.modules["fastmcp"] = fake_fastmcp     # ← entscheidend

# 2) (Optional) alte Aliase beibehalten:
pkg = types.ModuleType("mcp.server")
pkg.fastmcp = fake_fastmcp
sys.modules["mcp.server"] = pkg
sys.modules["mcp.server.fastmcp"] = fake_fastmcp
