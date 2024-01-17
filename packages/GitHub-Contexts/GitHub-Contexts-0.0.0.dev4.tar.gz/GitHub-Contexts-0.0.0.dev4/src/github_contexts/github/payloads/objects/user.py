from github_contexts.github.enums import UserType


class UserObject:

    def __init__(self, user: dict):
        self._user = user
        return

    @property
    def avatar_url(self) -> str | None:
        return self._user.get("avatar_url")

    @property
    def deleted(self) -> bool | None:
        return self._user.get("deleted")

    @property
    def email(self) -> str | None:
        return self._user.get("email")

    @property
    def events_url(self) -> str | None:
        return self._user.get("events_url")

    @property
    def followers_url(self) -> str | None:
        return self._user.get("followers_url")

    @property
    def following_url(self) -> str | None:
        return self._user.get("following_url")

    @property
    def gists_url(self) -> str | None:
        return self._user.get("gists_url")

    @property
    def gravatar_id(self) -> str | None:
        return self._user.get("gravatar_id")

    @property
    def html_url(self) -> str | None:
        return self._user.get("html_url")

    @property
    def id(self) -> int:
        return self._user["id"]

    @property
    def login(self) -> str:
        """GitHub username."""
        return self._user["login"]

    @property
    def name(self) -> str | None:
        return self._user.get("name")

    @property
    def node_id(self) -> str | None:
        return self._user.get("node_id")

    @property
    def organizations_url(self) -> str | None:
        return self._user.get("organizations_url")

    @property
    def received_events_url(self) -> str | None:
        return self._user.get("received_events_url")

    @property
    def repos_url(self) -> str | None:
        return self._user.get("repos_url")

    @property
    def site_admin(self) -> bool | None:
        return self._user.get("site_admin")

    @property
    def starred_url(self) -> str | None:
        return self._user.get("starred_url")

    @property
    def subscriptions_url(self) -> str | None:
        return self._user.get("subscriptions_url")

    @property
    def type(self) -> UserType | None:
        return UserType(self._user["type"]) if "type" in self._user else None

    @property
    def url(self) -> str | None:
        return self._user.get("url")

    @property
    def github_email(self) -> str:
        return f"{self.id}+{self.login}@users.noreply.github.com"
