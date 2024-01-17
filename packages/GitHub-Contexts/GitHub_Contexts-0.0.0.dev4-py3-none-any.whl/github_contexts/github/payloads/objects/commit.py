from github_contexts.github.payloads.objects.commit_author import CommitAuthorObject


class CommitObject:

    def __init__(self, commit: dict):
        self._commit = commit
        return

    @property
    def added(self) -> list[str]:
        """Paths of added files."""
        return self._commit.get("added", [])

    @property
    def author(self) -> CommitAuthorObject:
        """Git author information."""
        return CommitAuthorObject(self._commit["author"])

    @property
    def committer(self) -> CommitAuthorObject:
        """Git committer information."""
        return CommitAuthorObject(self._commit["committer"])

    @property
    def distinct(self) -> bool:
        """Whether this commit is distinct from any that have been pushed before."""
        return self._commit["distinct"]

    @property
    def id(self) -> str:
        return self._commit["id"]

    @property
    def message(self) -> str:
        return self._commit["message"]

    @property
    def modified(self) -> list[str]:
        """Paths of modified files."""
        return self._commit.get("modified", [])

    @property
    def removed(self) -> list[str]:
        """Paths of removed files."""
        return self._commit.get("removed", [])

    @property
    def timestamp(self) -> str:
        """ISO 8601 (YYYY-MM-DDTHH:MM:SSZ) timestamp of the commit."""
        return self._commit["timestamp"]

    @property
    def tree_id(self) -> str:
        return self._commit["tree_id"]

    @property
    def url(self) -> str:
        """URL that points to the commit API resource."""
        return self._commit["url"]
