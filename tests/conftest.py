# tests/conftest.py

import os
import sys
from types import ModuleType

# 1) Projekt-Root in den Suchpfad einfügen
#    __file__ ist tests/conftest.py → zwei Ebenen nach oben ins Projekt-Root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 2) Dummy-GitLab-Token setzen, bevor server.py geladen wird
os.environ.setdefault('GITLAB_TOKEN', 'dummy_token')

# 3) FastMCP-Stub (wie zuvor) injizieren, damit `mcp.app` existiert
fake_fastmcp = ModuleType('mcp.server.fastmcp')
class DummyFastMCP:
    def __init__(self, *args, **kwargs):
        self.app = object()
    def prompt(self, *args, **kwargs):
        return lambda fn: fn
    def resource(self, *args, **kwargs):
        return lambda fn: fn
    def tool(self, *args, **kwargs):
        return lambda fn: fn
fake_fastmcp.FastMCP = DummyFastMCP

import sys as _sys
# Parent-Package stubben, falls noch nicht importiert
_pkg = ModuleType('mcp.server')
_pkg.fastmcp = fake_fastmcp
_sys.modules['mcp.server.fastmcp'] = fake_fastmcp
_sys.modules['mcp.server'] = _pkg
