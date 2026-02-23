# from .main import main  # noqa: F401
"""
Reusable persistence layer.

This package provides:
- BaseModel: base class for domain entities (Django-like model behavior)
- JSONStorage: file-backed JSON storage
- Repository: generic CRUD repository
"""

from .model import BaseModel
from .repository import Repository
from .storage_json import JSONStorage

__all__ = ["BaseModel", "Repository", "JSONStorage"]
