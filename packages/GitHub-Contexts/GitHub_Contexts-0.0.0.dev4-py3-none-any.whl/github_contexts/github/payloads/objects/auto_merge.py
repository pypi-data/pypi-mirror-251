from github_contexts.github.payloads.objects.user import UserObject
from github_contexts.github.enums import MergeMethod


class AutoMergeObject:
    """The status of auto merging a pull request."""

    def __init__(self, auto_merge: dict):
        """
        Parameters
        ----------
        auto_merge : dict
            The `auto_merge` dictionary contained in the `pull_request` object of the payload.
        """
        self._auto_merge = auto_merge
        return

    @property
    def commit_message(self) -> str | None:
        """The commit message that will be used for the merge commit."""
        return self._auto_merge.get("commit_message")

    @property
    def commit_title(self) -> str | None:
        """The commit title that will be used for the merge commit."""
        return self._auto_merge.get("commit_title")

    @property
    def enabled_by(self) -> UserObject | None:
        """The user who enabled auto merging."""
        return UserObject(self._auto_merge["enabled_by"]) if self._auto_merge.get("enabled_by") else None

    @property
    def merge_method(self) -> MergeMethod:
        """The merge method that will be used to merge the pull request."""
        return MergeMethod(self._auto_merge["merge_method"])
