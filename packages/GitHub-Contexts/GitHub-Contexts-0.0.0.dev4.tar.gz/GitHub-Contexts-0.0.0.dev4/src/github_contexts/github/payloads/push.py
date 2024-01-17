from github_contexts.github.payloads.base import Payload
from github_contexts.github.payloads.objects.commit import CommitObject
from github_contexts.github.payloads.objects.commit_author import CommitAuthorObject
from github_contexts.github.enums import ActionType


class PushPayload(Payload):

    def __init__(self, payload: dict):
        super().__init__(payload=payload)
        return

    @property
    def action(self) -> ActionType:
        """Push action type; either 'created', 'deleted', or 'edited'."""
        if self.created:
            return ActionType.CREATED
        if self.deleted:
            return ActionType.DELETED
        return ActionType.EDITED

    @property
    def after(self) -> str:
        """The SHA hash of the most recent commit on the branch after the event."""
        return self._payload["after"]

    @property
    def base_ref(self) -> str | None:
        return self._payload.get("base_ref")

    @property
    def before(self) -> str:
        """The SHA hash of the most recent commit on the branch before the event."""
        return self._payload["before"]

    @property
    def commits(self) -> list[CommitObject]:
        """List of pushed commits."""
        return [CommitObject(commit) for commit in self._payload["commits"]]

    @property
    def compare(self) -> str:
        """URL comparing the before and after commits."""
        return self._payload["compare"]

    @property
    def created(self) -> bool:
        """Whether the push created the reference."""
        return self._payload["created"]

    @property
    def deleted(self) -> bool:
        """Whether the push deleted the reference."""
        return self._payload["deleted"]

    @property
    def forced(self) -> bool:
        """Whether the push was forced."""
        return self._payload["forced"]

    @property
    def head_commit(self) -> CommitObject | None:
        """The most recent commit on the branch after the event."""
        return CommitObject(self._payload["head_commit"]) if self._payload.get("head_commit") else None

    @property
    def pusher(self) -> CommitAuthorObject:
        """The user that pushed the commits."""
        return CommitAuthorObject(self._payload["pusher"])

    @property
    def ref(self) -> str:
        """The full reference name that was pushed to, e.g.: 'refs/heads/main', 'refs/tags/v1.0.0'."""
        return self._payload["ref"]
