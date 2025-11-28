"""Legacy entry point kept for backwards compatibility.

The real application is now created via backend.app_factory.create_app.
Importing this module provides the same `app` object so existing scripts
do not break immediately, while allowing a cleaner OO architecture.

Note: Any duplicate copies of this file under `dist/` are build artifacts
from packaging the Electron app and can be ignored by linters/type checkers.
Use the virtual environment at `.venv/` for proper dependency resolution.
"""
from backend import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050)