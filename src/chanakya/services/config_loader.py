import os
import json
from ..web.app_setup import app

MCP_CONFIG_FILENAME = "./mcp_config_file.json"


def load_mcp_config_internal(filename: str) -> dict:
    if not os.path.exists(filename):
        app.logger.error(f"Error: MCP config file '{filename}' not found.")
        return {}
    try:
        with open(filename, "r") as f:
            config_data = json.load(f)
        app.logger.info(f"Successfully loaded MCP config from '{filename}'.")
        return config_data.get("mcpServers", {})
    except Exception as e:
        app.logger.error(f"Error loading/parsing '{filename}': {e}")
        return {}
