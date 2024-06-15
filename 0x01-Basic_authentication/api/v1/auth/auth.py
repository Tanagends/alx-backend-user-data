#!/usr/bin/env python3
"""Manages API authentication"""
from flask import request
from typing import List, TypeVar


class Auth:
    """authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Auth required"""
        if path is None or not excluded_paths:
            return True
        if not path.endswith('/'):
            path += '/'
        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """Sets auth request header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Curr user"""
        return None
