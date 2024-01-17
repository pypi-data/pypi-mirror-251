from __future__ import annotations
from typing import Union

from github_contexts.github.enums import TeamPrivacy


class TeamObject:

    def __init__(self, team: dict):
        self._team = team
        return

    @property
    def deleted(self) -> bool | None:
        return self._team.get("deleted")

    @property
    def description(self) -> str | None:
        return self._team.get("description")

    @property
    def html_url(self) -> str | None:
        return self._team.get("html_url")

    @property
    def id(self) -> int:
        return self._team["id"]

    @property
    def members_url(self) -> str | None:
        return self._team.get("members_url")

    @property
    def name(self) -> str:
        return self._team["name"]

    @property
    def node_id(self) -> str:
        return self._team["node_id"]

    @property
    def parent(self) -> Union["TeamObject", None]:
        return TeamObject(self._team["parent"]) if self._team.get("parent") else None

    @property
    def permission(self) -> str | None:
        return self._team.get("permission")

    @property
    def privacy(self) -> TeamPrivacy | None:
        return TeamPrivacy(self._team["privacy"]) if self._team.get("privacy") else None

    @property
    def repositories_url(self) -> str | None:
        return self._team.get("repositories_url")

    @property
    def slug(self) -> str | None:
        return self._team.get("slug")

    @property
    def url(self) -> str | None:
        return self._team.get("url")