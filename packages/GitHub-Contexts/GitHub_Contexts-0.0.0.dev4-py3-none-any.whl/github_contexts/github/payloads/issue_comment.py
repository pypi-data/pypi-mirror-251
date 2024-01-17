from github_contexts.github.payloads.base import Payload
from github_contexts.github.enums import ActionType
from github_contexts.github.payloads.objects.comment import CommentObject
from github_contexts.github.payloads.objects.issue import IssueObject
from github_contexts.github.payloads.objects.changes import IssueCommentEditedChangesObject


class IssueCommentPayload(Payload):
    def __init__(self, payload: dict):
        super().__init__(payload=payload)
        return

    @property
    def action(self) -> ActionType:
        """Action that triggered the event;
        either 'created', 'edited', or 'deleted'.
        """
        return ActionType(self._payload["action"])

    @property
    def comment(self) -> CommentObject:
        """Comment data."""
        return CommentObject(self._payload["comment"])

    @property
    def issue(self) -> IssueObject:
        """Issue data."""
        return IssueObject(self._payload["issue"])

    @property
    def is_on_pull(self) -> bool:
        """Whether the comment is on a pull request (True) or an issue (False)."""
        return bool(self.issue.pull_request)

    @property
    def changes(self) -> IssueCommentEditedChangesObject | None:
        """The changes to the comment if the action was 'edited'."""
        if self.action == ActionType.EDITED:
            return IssueCommentEditedChangesObject(self._payload["changes"])
        return
