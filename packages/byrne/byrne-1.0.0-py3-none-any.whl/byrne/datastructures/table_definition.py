from dataclasses import dataclass
from typing import Dict, List

from ..helpers import default
from .key_definition import KeyDefinition


@dataclass
class TableDefinition:
    name: str | None = None
    attributes: Dict[str, str] = default(dict)
    primary_key: KeyDefinition | None = None
    gsi: Dict[str, KeyDefinition] = default(dict)
    lsi: Dict[str, KeyDefinition] = default(dict)
    arn: str | None = None
    status: str | None = None

    @property
    def key_attributes(self) -> List[str]:
        if self.primary_key is not None:
            attrs = self.primary_key.attributes

            for key in self.secondary_keys:
                attrs += key.attributes

            return list(set(attrs))
        return list()

    @property
    def gsi_keys(self) -> List[KeyDefinition]:
        return list(self.gsi.values())

    @property
    def lsi_keys(self) -> List[KeyDefinition]:
        return list(self.lsi.values())

    @property
    def secondary_keys(self) -> List[KeyDefinition]:
        return self.gsi_keys + self.lsi_keys

    @property
    def is_valid(self) -> bool:
        if self.primary_key is not None:
            if not self.primary_key.is_valid(self.attributes):
                return False

            for key in self.secondary_keys:
                if not key.is_valid(self.attributes):
                    return False
            return True
        return False

    @property
    def keys(self) -> List[KeyDefinition]:
        return [self.primary_key, *self.secondary_keys]  # type: ignore

    def get_secondary_key(self, name):
        if name in self.lsi:
            return self.lsi[name]
        return self.gsi[name]

    def get_projected_attributes(self, index) -> List[str]:
        key = None

        if index in self.gsi:
            key = self.gsi[index]
        else:
            key = self.lsi[index]

        if key.projection != "ALL":
            base_keys = [self.primary_key.partition_key]  # type: ignore
            if key.projection == "KEYS_ONLY":
                return base_keys + key.attributes
            elif key.projection == "INCLUDE":
                return base_keys + key.attributes + key.include
        return list(self.attributes.keys())
