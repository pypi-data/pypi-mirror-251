from __future__ import annotations

import os
from pathlib import Path

from pydantic import BaseModel, Field
from yaml import safe_load


class ClusterInfo(BaseModel):
    certificate_authority: Path | None = Field(default=None, alias="certificate-authority")
    certificate_authority_data: str | None = Field(default=None, alias="certificate-authority-data")
    server: str


class Cluster(BaseModel):
    name: str
    cluster: ClusterInfo


class UserInfo(BaseModel):
    client_certificate: str | None = Field(default=None, alias="client-certificate")
    client_certificate_data: str | None = Field(default=None, alias="client-certificate-data")
    client_key: str | None = Field(default=None, alias="client-key")
    client_key_data: str | None = Field(default=None, alias="client-key-data")


class User(BaseModel):
    name: str
    user: UserInfo


class Konfig(BaseModel):
    apiVersion: str
    clusters: list[Cluster]
    users: list[User]

    @classmethod
    def build(cls) -> Konfig:
        path = Path(os.getenv("KUBECONFIG", str(Path.home() / ".kube" / "config")))

        y = safe_load(path.read_text())

        return cls.model_validate(y)
