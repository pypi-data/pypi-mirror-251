from github_contexts.github.payloads.objects.repository import RepositoryObject
from github_contexts.github.payloads.objects.user import UserObject


class HeadBaseObject:
    """Head or base branch info for a pull request."""

    def __init__(self, head_or_base: dict):
        """
        Parameters
        ----------
        head_or_base : dict
            The `head` or `base` object contained in the `pull_request` object of the payload.
        """
        self._branch = head_or_base
        return

    @property
    def label(self) -> str:
        """The label of the branch."""
        return self._branch["label"]

    @property
    def ref(self) -> str:
        """The reference name of the branch."""
        return self._branch["ref"]

    @property
    def repo(self) -> RepositoryObject:
        """The repository that contains the branch."""
        return RepositoryObject(self._branch["repo"])

    @property
    def sha(self) -> str:
        """The SHA hash of the branch."""
        return self._branch["sha"]

    @property
    def user(self) -> UserObject | None:
        return UserObject(self._branch["user"]) if self._branch.get("user") else None
