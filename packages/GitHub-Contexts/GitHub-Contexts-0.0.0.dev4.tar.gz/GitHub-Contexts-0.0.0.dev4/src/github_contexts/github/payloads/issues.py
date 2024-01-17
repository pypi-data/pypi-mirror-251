"""GitHub Webhook Issues Payload."""


from github_contexts.github.payloads.base import Payload
from github_contexts.github.enums import ActionType
from github_contexts.github.payloads.objects.issue import IssueObject
from github_contexts.github.payloads.objects.user import UserObject
from github_contexts.github.payloads.objects.milestone import MilestoneObject
from github_contexts.github.payloads.objects.label import LabelObject
from github_contexts.github.payloads.objects.changes import (
    IssueOpenedChangesObject, IssueEditedChangesObject, IssueTransferredChangesObject
)


class IssuesPayload(Payload):

    def __init__(self, payload: dict):
        super().__init__(payload=payload)
        return

    @property
    def action(self) -> ActionType:
        return ActionType(self._payload["action"])

    @property
    def issue(self) -> IssueObject:
        """The issue data.

        References
        ----------
        - [GitHub API Docs](https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28#get-an-issue)
        """
        return IssueObject(self._payload["issue"])

    @property
    def assignee(self) -> UserObject | None:
        """The user that was assigned or unassigned from the issue.

        This is only available for the 'assigned' and 'unassigned' events.
        """
        return UserObject(self._payload.get("assignee"))

    @property
    def changes(self) -> IssueOpenedChangesObject | IssueEditedChangesObject | IssueTransferredChangesObject | None:
        """The changes to the issue if the action was 'edited'."""
        if self.action == ActionType.EDITED:
            return IssueEditedChangesObject(self._payload["changes"])
        if self.action == ActionType.OPENED:
            return IssueOpenedChangesObject(self._payload["changes"])
        if self.action == ActionType.TRANSFERRED:
            return IssueTransferredChangesObject(self._payload["changes"])
        return

    @property
    def label(self) -> LabelObject | None:
        """The label that was added or removed from the issue.

        This is only available for the 'labeled' and 'unlabeled' events.
        """
        return LabelObject(self._payload["label"]) if self._payload.get("label") else None

    @property
    def milestone(self) -> MilestoneObject | None:
        """The milestone that was added to or removed from the issue.

        This is only available for the 'milestoned' and 'demilestoned' events.
        """
        return MilestoneObject(self._payload.get("milestone"))
