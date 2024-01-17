from github_contexts.github.payloads.objects.issue import IssueObject
from github_contexts.github.payloads.objects.repository import RepositoryObject


class IssueOpenedChangesObject:

    def __init__(self, changes: dict):
        self._changes = changes
        return

    @property
    def old_issue(self) -> IssueObject | None:
        return IssueObject(self._changes["old_issue"]) if self._changes.get("old_issue") else None

    @property
    def old_repository(self) -> RepositoryObject:
        return RepositoryObject(self._changes["old_repository"])


class IssueTransferredChangesObject:

    def __init__(self, changes: dict):
        self._changes = changes
        return

    @property
    def new_issue(self) -> IssueObject:
        return IssueObject(self._changes["new_issue"])

    @property
    def new_repository(self) -> RepositoryObject:
        return RepositoryObject(self._changes["new_repository"])


class IssueEditedChangesObject:

    def __init__(self, changes: dict):
        self._changes = changes
        return

    @property
    def body(self) -> dict | None:
        return self._changes.get("body")

    @property
    def title(self) -> dict | None:
        return self._changes.get("title")


class PullRequestEditedChangesObject:

    def __init__(self, changes: dict):
        self._changes = changes
        return

    @property
    def base_ref(self) -> str | None:
        return self._changes.get("base", {}).get("ref", {}).get("from")

    @property
    def base_sha(self) -> str | None:
        return self._changes.get("base", {}).get("sha", {}).get("from")

    @property
    def body(self) -> str | None:
        """"The previous version of the body."""
        return self._changes.get("body", {}).get("from")

    @property
    def title(self) -> dict | None:
        """The previous version of the title."""
        return self._changes.get("title", {}).get("from")


class IssueCommentEditedChangesObject:

    def __init__(self, changes: dict):
        self._changes = changes
        return

    @property
    def body(self) -> str | None:
        """The previous version of the body."""
        return self._changes.get("body", {}).get("from")
