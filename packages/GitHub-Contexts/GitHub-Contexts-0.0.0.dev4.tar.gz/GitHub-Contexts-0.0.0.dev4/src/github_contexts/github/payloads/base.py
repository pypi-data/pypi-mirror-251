"""Base class for all GitHub webhook payloads."""


from ruamel.yaml import YAML

from github_contexts.github.payloads.objects.user import UserObject
from github_contexts.github.payloads.objects.repository import RepositoryObject


class Payload:
    """
    The full webhook payload of the triggering event.

    References
    ----------
    - [GitHub Docs](https://docs.github.com/en/webhooks/webhook-events-and-payloads)
    """

    def __init__(self, payload: dict):
        self._payload = dict(sorted(payload.items()))
        return

    def __str__(self):
        return YAML(typ=["rt", "string"]).dumps(self._payload, add_final_eol=True)

    @property
    def enterprise(self) -> dict | None:
        """An enterprise on GitHub.

        This is only available when the webhook is configured on an enterprise account
        or an organization that's part of an enterprise account.
        """
        return self._payload.get("enterprise")

    @property
    def installation(self) -> dict | None:
        """The GitHub App installation.

        This is only available when the event is configured for and sent to a GitHub App.
        """
        return self._payload.get("installation")

    @property
    def organization(self) -> dict | None:
        """An organization on GitHub.

        This is only available when the event occurs from activity in a repository owned by an organization,
        or when the webhook is configured for an organization.
        """
        return self._payload.get("organization")

    @property
    def repository(self) -> RepositoryObject | None:
        """The repository on GitHub where the event occurred.

        This is only available when the event occurs from activity in the repository.
        """
        return RepositoryObject(self._payload["repository"]) if "repository" in self._payload else None

    @property
    def sender(self) -> UserObject:
        """The GitHub user that triggered the event."""
        return UserObject(self._payload["sender"])
