"""Models utilized in session management."""

from pydantic import BaseModel


class SessionMapping(BaseModel):
    """Session mapping model."""

    name: str
    mapping: str
