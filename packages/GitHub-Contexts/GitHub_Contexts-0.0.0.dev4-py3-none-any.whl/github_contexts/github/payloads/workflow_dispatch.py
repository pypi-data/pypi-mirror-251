from github_contexts.github.payloads.base import Payload


class WorkflowDispatchPayload(Payload):

    def __init__(self, payload: dict):
        super().__init__(payload=payload)
        return

    @property
    def inputs(self) -> dict | None:
        """Input arguments of the dispatch evenet."""
        return self._payload["inputs"]

    @property
    def ref(self) -> str:
        """The target reference of the dispatch event."""
        return self._payload["ref"]

    @property
    def workflow(self) -> str:
        """The workflow file name of the dispatch event."""
        return self._payload["workflow"]
