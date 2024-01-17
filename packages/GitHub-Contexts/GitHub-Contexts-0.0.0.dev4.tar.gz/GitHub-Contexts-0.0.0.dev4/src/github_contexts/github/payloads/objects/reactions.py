
class ReactionsObject:

    def __init__(self, reactions: dict):
        self._reactions = reactions
        return

    @property
    def plus_one(self) -> int:
        return self._reactions["+1"]

    @property
    def minus_one(self) -> int:
        return self._reactions["-1"]

    @property
    def confused(self) -> int:
        return self._reactions["confused"]

    @property
    def eyes(self) -> int:
        return self._reactions["eyes"]

    @property
    def heart(self) -> int:
        return self._reactions["heart"]

    @property
    def hooray(self) -> int:
        return self._reactions["hooray"]

    @property
    def laugh(self) -> int:
        return self._reactions["laugh"]

    @property
    def rocket(self) -> int:
        return self._reactions["rocket"]

    @property
    def total_count(self) -> int:
        return self._reactions["total_count"]

    @property
    def url(self) -> str:
        return self._reactions["url"]
