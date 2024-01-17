

class LabelObject:

    def __init__(self, label: dict):
        self._label = label
        return

    @property
    def color(self) -> str:
        return self._label["color"]

    @property
    def default(self) -> bool:
        return self._label["default"]

    @property
    def description(self) -> str | None:
        return self._label["description"]

    @property
    def id(self) -> int:
        return self._label["id"]

    @property
    def name(self) -> str:
        return self._label["name"]

    @property
    def node_id(self) -> str:
        return self._label["node_id"]

    @property
    def url(self) -> str:
        return self._label["url"]