"""Safe discovery and recommendation registry for security tools.

This module recommends tools only. It never launches scans or commands.
"""
import shutil
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class SecurityTool:
    name: str
    purpose: str
    categories: tuple[str, ...]
    requires_authorization: bool = True

    def to_dict(self):
        return asdict(self)


class SecurityToolRegistry:
    def __init__(self):
        self._tools = {
            "nmap": SecurityTool(
                "nmap",
                "Network host and service discovery",
                ("network", "ports", "services", "recon"),
            ),
            "whatweb": SecurityTool(
                "whatweb",
                "Identify web technologies",
                ("web", "technology", "fingerprinting"),
            ),
            "nikto": SecurityTool(
                "nikto",
                "Check web servers for common issues",
                ("web", "web-server", "vulnerability"),
            ),
            "nuclei": SecurityTool(
                "nuclei",
                "Template-based vulnerability checks",
                ("web", "network", "vulnerability"),
            ),
            "sqlmap": SecurityTool(
                "sqlmap",
                "Test for SQL injection",
                ("web", "sql-injection", "injection"),
            ),
            "gobuster": SecurityTool(
                "gobuster",
                "Discover web paths and DNS names",
                ("web", "directories", "dns", "enumeration"),
            ),
            "ffuf": SecurityTool(
                "ffuf",
                "Fuzz web endpoints and parameters",
                ("web", "fuzzing", "directories"),
            ),
        }

    def list_tools(self):
        """List registered tools and whether each executable is installed."""
        results = []
        for tool in self._tools.values():
            item = tool.to_dict()
            item["installed"] = shutil.which(tool.name) is not None
            results.append(item)
        return results

    def get_tool(self, name):
        """Return metadata for a registered tool, or None if unknown."""
        tool = self._tools.get(name.strip().lower())
        if tool is None:
            return None
        item = tool.to_dict()
        item["installed"] = shutil.which(tool.name) is not None
        return item

    def recommend(self, goal):
        """Recommend matching tools without executing them."""
        if not isinstance(goal, str) or not goal.strip():
            raise ValueError("Goal must be a non-empty string")
        if len(goal) > 2000:
            raise ValueError("Goal is too long")

        text = goal.lower()
        keywords = {
            "nmap": ("network", "port", "host", "service"),
            "whatweb": ("technology", "fingerprint", "identify web"),
            "nikto": ("web server", "web-server", "server checks"),
            "nuclei": ("vulnerability", "security check", "cve"),
            "sqlmap": ("sql injection", "sql-injection"),
            "gobuster": ("directory", "directories", "dns enumeration"),
            "ffuf": ("fuzz", "endpoint", "parameter"),
        }

        matches = []
        for name, terms in keywords.items():
            if any(term in text for term in terms):
                item = self.get_tool(name)
                item["reason"] = "Goal matched: " + ", ".join(
                    term for term in terms if term in text
                )
                item["execution"] = "not_started"
                matches.append(item)

        return {
            "goal": goal,
            "status": "recommendations_only",
            "tools": matches,
            "requires_authorization": True,
            "executed": False,
        }
