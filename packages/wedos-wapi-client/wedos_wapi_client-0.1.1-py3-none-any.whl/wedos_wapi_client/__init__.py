import hashlib
import os
from datetime import datetime
from json import dumps
from logging import getLogger
from zoneinfo import ZoneInfo

import requests

logger = getLogger(__name__)


def _hash(value: str) -> str:
    return hashlib.sha1(value.encode()).hexdigest()


class WapiError(Exception):
    pass


class WapiResponse:
    code: int
    result: str
    timestamp: int
    svTRID: str
    command: str
    data: dict | None
    raw: dict

    def __init__(self, response_data: dict) -> None:
        self.code = response_data["code"]
        self.result = response_data["result"]
        self.timestamp = response_data["timestamp"]
        self.svTRID = response_data["svTRID"]
        self.command = response_data["command"]
        self.data = response_data.get("data")
        self.raw = response_data

    def __str__(self) -> str:
        return f"<{self.__module__}.{self.__class__.__name__} {self.raw}>"


class WapiClient:
    def __init__(
        self,
        user: str | None = None,
        password: str | None = None,
        url: str | None = None,
        test=False,
    ) -> None:
        if user is None:
            user = os.environ["WAPI_USER"]
        if password is None:
            password = os.environ["WAPI_PASSWORD"]
        if url is None:
            url = os.environ.get("WAPI_URL", "https://api.wedos.com/wapi/json")
        self.user = user
        self.hashed_password = _hash(password)
        self.url = url
        self.test = test

    @property
    def _auth(self):
        hour = datetime.now(tz=ZoneInfo("Europe/Prague")).hour
        return _hash(f"{self.user}{self.hashed_password}{hour:02}")

    def request(self, command, **data) -> WapiResponse:
        request = {
            "request": {
                "user": self.user,
                "auth": self._auth,
                "command": command,
                "data": data,
                "test": int(self.test),
            }
        }
        logger.debug("Sending WAPI request", request)
        response = requests.post(self.url, data={"request": dumps(request)})
        response_data = response.json()["response"]
        logger.debug("Got WAPI response", response)
        if response_data["result"] != "OK":
            raise WapiError(response_data)
        return WapiResponse(response_data)

    # Shortcuts for some commands

    def ping(self):
        return self.request("ping")

    def domains_list(self):
        return self.request("domains-list")

    def dns_rows_list(self, domain: str):
        return self.request("dns-rows-list", domain=domain)

    def dns_row_add(
        self,
        domain: str,
        name: str,
        type: str,
        rdata: str,
        ttl: int = 300,
        auth_comment: str = "",
    ):
        return self.request(
            "dns-row-add",
            domain=domain,
            name=name,
            ttl=ttl,
            type=type,
            rdata=rdata,
            auth_comment=auth_comment,
        )

    def dns_row_delete(self, domain: str, row_id: int):
        return self.request("dns-row-delete", domain=domain, row_id=row_id)

    def dns_row_update(
        self,
        domain: str,
        row_id: int,
        rdata: str,
        ttl: int = 300,
    ):
        return self.request(
            "dns-row-update",
            domain=domain,
            row_id=row_id,
            rdata=rdata,
            ttl=ttl,
        )

    def dns_domain_commit(self, name: str):
        return self.request("dns-domain-commit", name=name)
