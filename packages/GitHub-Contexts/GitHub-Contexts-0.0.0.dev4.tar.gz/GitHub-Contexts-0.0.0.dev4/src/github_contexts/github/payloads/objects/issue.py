from github_contexts.github.enums import ActiveLockReason, AuthorAssociation, State
from github_contexts.github.payloads.objects.label import LabelObject
from github_contexts.github.payloads.objects.user import UserObject
from github_contexts.github.payloads.objects.milestone import MilestoneObject
from github_contexts.github.payloads.objects.performed_via_github_app import PerformedViaGitHubAppObject
from github_contexts.github.payloads.objects.pull_request import PullRequestObject
from github_contexts.github.payloads.objects.reactions import ReactionsObject


class IssueObject:
    """
    The `issue` object contained in the payload of the `issues` and `issue_comment` events.
    """

    def __init__(self, issue: dict):
        """
        Parameters
        ----------
        issue : dict
            The `issue` dictionary contained in the payload.
        """
        self._issue = issue
        return

    @property
    def active_lock_reason(self) -> ActiveLockReason:
        return ActiveLockReason(self._issue["active_lock_reason"])

    @property
    def assignee(self) -> UserObject | None:
        return UserObject(self._issue["assignee"]) if "assignee" in self._issue else None

    @property
    def assignees(self) -> list[UserObject]:
        assignees_list = self._issue.get("assignees", [])
        return [UserObject(assignee) for assignee in assignees_list if assignee]

    @property
    def author_association(self) -> AuthorAssociation:
        return AuthorAssociation(self._issue["author_association"])

    @property
    def body(self) -> str | None:
        """Contents of the issue."""
        return self._issue["body"]

    @property
    def closed_at(self) -> str | None:
        return self._issue["closed_at"]

    @property
    def comments(self) -> int:
        return self._issue["comments"]

    @property
    def comments_url(self) -> str:
        return self._issue["comments_url"]

    @property
    def created_at(self) -> str:
        return self._issue["created_at"]

    @property
    def draft(self) -> bool | None:
        return self._issue.get("draft")

    @property
    def events_url(self) -> str:
        return self._issue["events_url"]

    @property
    def html_url(self) -> str:
        return self._issue["html_url"]

    @property
    def id(self) -> int:
        return self._issue["id"]

    @property
    def labels(self) -> list[LabelObject]:
        return [LabelObject(label) for label in self._issue.get("labels", [])]

    @property
    def labels_url(self) -> str:
        return self._issue["labels_url"]

    @property
    def locked(self) -> bool | None:
        return self._issue.get("locked")

    @property
    def milestone(self) -> MilestoneObject | None:
        return MilestoneObject(self._issue["milestone"]) if self._issue.get("milestone") else None

    @property
    def node_id(self) -> str:
        return self._issue["node_id"]

    @property
    def number(self) -> int:
        return self._issue["number"]

    @property
    def performed_via_github_app(self) -> PerformedViaGitHubAppObject | None:
        return PerformedViaGitHubAppObject(self._issue["performed_via_github_app"]) if self._issue.get("performed_via_github_app") else None

    @property
    def pull_request(self) -> PullRequestObject | None:
        return PullRequestObject(self._issue["pull_request"]) if self._issue.get("pull_request") else None

    @property
    def reactions(self) -> ReactionsObject:
        return ReactionsObject(self._issue["reactions"])

    @property
    def repository_url(self) -> str:
        return self._issue["repository_url"]

    @property
    def state(self) -> State | None:
        return State(self._issue["state"]) if self._issue.get("state") else None

    @property
    def state_reason(self) -> str | None:
        return self._issue.get("state_reason")

    @property
    def timeline_url(self) -> str | None:
        return self._issue.get("timeline_url")

    @property
    def title(self) -> str:
        """Title of the issue."""
        return self._issue["title"]

    @property
    def updated_at(self) -> str:
        return self._issue["updated_at"]

    @property
    def url(self) -> str:
        return self._issue["url"]

    @property
    def user(self) -> UserObject | None:
        return UserObject(self._issue["user"]) if self._issue.get("user") else None

    @property
    def label_names(self) -> list[str]:
        return [label.name for label in self.labels]
