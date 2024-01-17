
class CommitAuthorObject:

    def __init__(self, author: dict):
        self._author = author
        return

    @property
    def date(self) -> str | None:
        return self._author.get("date")

    @property
    def email(self) -> str | None:
        return self._author.get("email")

    @property
    def name(self) -> str | None:
        """The Git author's name."""
        return self._author.get("name")

    @property
    def username(self) -> str | None:
        return self._author.get("username")
