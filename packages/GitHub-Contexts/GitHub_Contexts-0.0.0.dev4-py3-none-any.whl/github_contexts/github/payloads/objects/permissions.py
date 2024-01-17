
class PermissionsObject:

    def __init__(self, permissions: dict):
        self._permissions = permissions
        return

    @property
    def admin(self) -> bool:
        return self._permissions["admin"]

    @property
    def maintain(self) -> bool | None:
        return self._permissions.get("maintain")

    @property
    def pull(self) -> bool:
        return self._permissions["pull"]

    @property
    def push(self) -> bool:
        return self._permissions["push"]

    @property
    def triage(self) -> bool | None:
        return self._permissions.get("triage")
