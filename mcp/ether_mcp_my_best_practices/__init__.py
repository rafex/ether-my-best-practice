"""ether-mcp-my-best-practices — MCP server for Ether Best Practices."""
__version__ = "0.4.0"
try:
    from ether_mcp_my_best_practices._build import BUILD  # type: ignore
except ImportError:
    BUILD = "dev"
