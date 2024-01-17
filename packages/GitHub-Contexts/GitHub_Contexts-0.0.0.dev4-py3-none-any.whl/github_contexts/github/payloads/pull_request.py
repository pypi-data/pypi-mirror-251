
from github_contexts.github.payloads.base import Payload
from github_contexts.github.enums import ActionType
from github_contexts.github.payloads.objects.pull_request import PullRequestObject
from github_contexts.github.payloads.objects.user import UserObject
from github_contexts.github.payloads.objects.team import TeamObject
from github_contexts.github.payloads.objects.milestone import MilestoneObject
from github_contexts.github.payloads.objects.label import LabelObject
from github_contexts.github.payloads.objects.changes import (
    PullRequestEditedChangesObject
)


class PullRequestPayload(Payload):

    def __init__(self, payload: dict):
        super().__init__(payload=payload)
        self._pull_request = payload["pull_request"]
        return

    @property
    def action(self) -> ActionType:
        return ActionType(self._payload["action"])

    @property
    def number(self) -> int:
        """Pull request number"""
        return self._payload["number"]

    @property
    def pull_request(self) -> PullRequestObject:
        return PullRequestObject(self._pull_request)

    @property
    def internal(self) -> bool:
        """Whether the pull request is internal, i.e., within the same repository."""
        return self.pull_request.head.repo.full_name == self.repository.full_name

    @property
    def after(self) -> str | None:
        """
        The SHA hash of the most recent commit on the head branch after the synchronization event.

        This is only available for the 'synchronize' action.
        """
        return self._payload.get("after")

    @property
    def assignee(self) -> UserObject | None:
        """The user that was assigned or unassigned from the pull request.

        This is only available for the 'assigned' and 'unassigned' events.
        """
        return UserObject(self._payload.get("assignee"))

    @property
    def before(self) -> str | None:
        """
        The SHA hash of the most recent commit on the head branch before the synchronization event.

        This is only available for the 'synchronize' action.
        """
        return self._payload.get("before")

    @property
    def changes(self) -> PullRequestEditedChangesObject | None:
        """The changes to the pull request if the action was 'edited'."""
        if self.action == ActionType.EDITED:
            return PullRequestEditedChangesObject(self._payload["changes"])
        return

    @property
    def label(self) -> LabelObject | None:
        """The label that was added or removed from the pull request.

        This is only available for the 'labeled' and 'unlabeled' events.
        """
        return LabelObject(self._payload["label"]) if self._payload.get("label") else None

    @property
    def milestone(self) -> MilestoneObject | None:
        """The milestone that was added to or removed from the pull request.

        This is only available for the 'milestoned' and 'demilestoned' events.
        """
        return MilestoneObject(self._payload.get("milestone"))

    @property
    def reason(self) -> str | None:
        """This is only available for the
        'auto_merge_disabled', 'auto_merge_disabled', 'dequeued' events.
        """
        return self._payload.get("reason")

    @property
    def requested_reviewer(self) -> UserObject | None:
        """The user that was requested for review.

        This is only available for the 'review_request_removed', 'review_requested' events.
        """
        return UserObject(self._payload["requested_reviewer"]) if self._payload.get("requested_reviewer") else None

    @property
    def requested_team(self) -> TeamObject | None:
        """The team that was requested for review.

        This is only available for the 'review_request_removed', 'review_requested' events.
        """
        return TeamObject(self._payload["requested_team"]) if self._payload.get("requested_team") else None
