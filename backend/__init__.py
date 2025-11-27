"""Backend package for BackdoorCounter.
Exposes a factory for creating the Flask app.
"""
from .app_factory import create_app  # re-export for convenience
