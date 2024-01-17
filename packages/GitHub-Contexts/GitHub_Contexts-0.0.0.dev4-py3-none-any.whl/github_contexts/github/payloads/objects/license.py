
class LicenseObject:

    def __init__(self, license_data: dict):
        self._license = license_data
        return

    @property
    def key(self) -> str:
        return self._license["key"]

    @property
    def name(self) -> str:
        return self._license["name"]

    @property
    def node_id(self) -> str:
        return self._license["node_id"]

    @property
    def spdx_id(self) -> str:
        return self._license["spdx_id"]

    @property
    def url(self) -> str:
        return self._license["url"]
