"""GitHub Milestone Object"""


from github_contexts.github.payloads.objects.user import UserObject
from github_contexts.github.enums import State


class MilestoneObject:
    """GitHub Milestone Object"""

    def __init__(self, data: dict):
        """
        Parameters
        ----------
        data : dict
            The `milestone` dictionary contained in the payload.
        """
        self._milestone = data
        return

    @property
    def closed_at(self) -> str | None:
        return self._milestone["closed_at"]

    @property
    def closed_issues(self) -> int:
        return self._milestone["closed_issues"]

    @property
    def created_at(self) -> str:
        return self._milestone["created_at"]

    @property
    def creator(self) -> UserObject | None:
        return UserObject(self._milestone["creator"]) if self._milestone.get("creator") else None

    @property
    def description(self) -> str | None:
        return self._milestone["description"]

    @property
    def due_on(self) -> str | None:
        return self._milestone["due_on"]

    @property
    def html_url(self) -> str:
        return self._milestone["html_url"]

    @property
    def id(self) -> int:
        return self._milestone["id"]

    @property
    def labels_url(self) -> str:
        return self._milestone["labels_url"]

    @property
    def node_id(self) -> str:
        return self._milestone["node_id"]

    @property
    def number(self) -> int:
        return self._milestone["number"]

    @property
    def open_issues(self) -> int:
        return self._milestone["open_issues"]

    @property
    def state(self) -> State:
        return State(self._milestone["state"])

    @property
    def title(self) -> str:
        return self._milestone["title"]

    @property
    def updated_at(self) -> str:
        return self._milestone["updated_at"]

    @property
    def url(self) -> str:
        return self._milestone["url"]
