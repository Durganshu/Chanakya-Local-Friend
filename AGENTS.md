# AGENTS.md - Chanakya-Local-Friend Development Guide

This guide provides essential information for agentic coding agents working on the Chanakya-Local-Friend project.

## Build and Development Commands

### Application Start
```bash
# Main entry point (HTTP)
python chanakya.py

# With HTTPS (requires certs/cert.pem and certs/key.pem)
# Generate certificates first if needed:
python -m src.chanakya.services.generate_cert

# Docker build and run
docker build -t chanakya-assistant .
docker run --restart=always -d --network="host" --env-file .env --name chanakya chanakya-assistant
```

### Dependency Management
```bash
# Install dependencies from requirements.txt
pip install -r requirements.txt

# Install development dependencies (if available)
pip install -r requirements-dev.txt  # Check if exists

# Check Python version compatibility (requires 3.11+)
python --version
```

### Testing
**Note**: The project currently has no formal test suite. When adding new features:

1. Manually test the feature through the web interface (`http://localhost:5001`)
2. Test API endpoints (`/chat`, `/record`, `/play_response`, `/memory`, etc.)
3. Verify tool integration with MCP (Model Context Protocol)
4. Check Flask route functionality

### Code Quality Tools
```bash
# Run ruff linter
ruff check .

# Format code with ruff
ruff format .

# Type checking (if mypy is installed)
mypy src/
```

## Code Style Guidelines

### Imports
- **Order**: Standard library → third-party → local modules
- **Format**: One import per line, grouped with blank lines between groups
- **Example** from `routes.py:7-30`:
  ```python
  import asyncio
  import base64
  import datetime
  import os
  import tempfile
  import time
  from flask import jsonify, render_template, request, redirect, url_for
  from .app_setup import app
  ```

### Formatting
- **Indentation**: 4 spaces (no tabs)
- **Line length**: ~100 characters (based on existing code)
- **String quotes**: Single quotes (`'`) for strings, double quotes (`"`) for docstrings
- **Trailing commas**: Use in multi-line collections
- **Use ruff for formatting**: Consistent with `.ruff_cache` presence

### Naming Conventions
- **Variables/Local**: `snake_case` (e.g., `user_message`, `temp_audio_file_path`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `APP_SECRET_KEY`, `WAKE_WORD`)
- **Functions/Methods**: `snake_case` (e.g., `update_client_activity`, `get_plain_text_content`)
- **Classes**: `PascalCase` (e.g., likely in external libraries, less common in current codebase)
- **Modules/Files**: `snake_case` (e.g., `config.py`, `memory_management.py`)

### Error Handling Pattern
Follow existing patterns from `routes.py`:

1. **Try/Except with specific exceptions**:
   ```python
   try:
       # operation
   except RuntimeError as e:
       if "Event loop is closed" in str(e):
           # Handle specific case
           app.logger.error(f"EVENT LOOP CLOSED ERROR: {e}", exc_info=True)
           return jsonify({"response": "Internal server error"}), 500
       else:
           app.logger.error(f"Runtime error: {e}", exc_info=True)
           return jsonify({"response": f"Sorry, a runtime error occurred: {e}"}), 500
   except Exception as e:
       app.logger.error(f"Error in endpoint: {e}", exc_info=True)
       return jsonify({"response": "Sorry, I encountered an error"}), 500
   ```

2. **Logging**: Use `app.logger.info/warning/error` with descriptive messages
3. **User-facing errors**: Return JSON responses with appropriate HTTP codes
4. **Resource cleanup**: Use `finally` blocks for file/network cleanup

### Type Hints
- **Use typing imports** when available (not consistently used in current codebase)
- **Add type hints** for new functions and public APIs
- **Example from `utils.py:6`**:
  ```python
  def get_plain_text_content(response_object):
      # Would benefit from type hints
  ```

### Project Structure
```
src/chanakya/
├── config.py              # Configuration and environment variables
├── core/                  # Core logic (agents, memory, chat history)
├── services/              # External service integrations (STT, TTS, tools)
├── utils/                 # Utility functions
├── web/                   # Flask web application (routes, app setup)
└── prompts/               # Prompt templates
```

### Flask-Specific Guidelines
1. **Route decorators**: Use `@app.route("/path")` with appropriate methods
2. **Async routes**: Use `async def` and `asyncio` for long-running operations
3. **Template rendering**: Use `render_template()` with `template_folder` configured in `app_setup.py:8`
4. **Static files**: Store in `src/frontend/static/`
5. **Templates**: Store in `src/frontend/templates/`

### Environment Configuration
- **`.env` file**: Required for runtime configuration (copy from `.env.example`)
- **`mcp_config_file.json`**: Tool configuration (copy from `mcp_config_file.json.example`)
- **Config loading**: Use `config.py` helper functions (`get_env_clean()`)

### Tool Integration (MCP)
- **Tool naming**: Use `snake_case` for tool names in MCP configuration
- **Tool instructions**: See `tool_specific_instructions.txt` for Home Assistant specifics
- **Tool loading**: Async loading via `load_all_mcp_tools_async()` in `tool_loader.py`

### Documentation
- **Function docstrings**: Use triple quotes with brief description
- **Complex logic**: Add inline comments explaining non-obvious code
- **README updates**: Update relevant sections when adding major features
- **API endpoints**: Document new routes in appropriate doc files

### Security Considerations
1. **Never commit secrets**: `.env`, `mcp_config_file.json` with secrets, certificate files
2. **Input validation**: Validate user input in routes before processing
3. **Error messages**: Avoid exposing stack traces or sensitive info in production
4. **Dependencies**: Keep requirements.txt updated with version pins

## Development Workflow

1. **Start development server**: `python chanakya.py`
2. **Access web interface**: `http://localhost:5001`
3. **Test changes**: Use the web interface to test functionality
4. **Check logs**: Monitor Flask logs for errors and info messages
5. **Run linter**: `ruff check .` before committing
6. **Update documentation**: Add to relevant docs/ files if adding features

## Common Issues
- **TemplateNotFound**: Ensure templates are in `src/frontend/templates/`
- **Async errors**: Use `nest_asyncio.apply()` at entry point
- **MCP tool failures**: Check `mcp_config_file.json` configuration
- **SSL/HTTPS**: Generate certs with `generate_cert.py` for microphone access

## Notes for Agentic Coding
- This project uses Flask with async/await patterns
- MCP (Model Context Protocol) integration is key for tool functionality
- Memory management uses SQLite database (`DATABASE_PATH` config)
- Voice features require STT/TTS services to be running
- Focus on privacy: all processing should be local when possible