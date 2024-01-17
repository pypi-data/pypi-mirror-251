from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Optional
from typing import Union


@dataclass
class SdkConfig:
    amsdal_host: str
    amsdal_auth: Any
    client_extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class DictItem:
    key: 'TypeSchema'
    value: 'TypeSchema'


@dataclass
class TypeSchema:
    type: str
    items: Optional[Union[DictItem, 'TypeSchema']] = None  # noqa: UP007


@dataclass
class OptionSchema:
    key: str
    value: str


@dataclass
class PropertySchema:
    type: str
    default: Any
    title: str | None = None
    items: TypeSchema | DictItem | None = None
    options: list[OptionSchema] | None = None


@dataclass
class Schema:
    title: str
    type: str = 'object'
    properties: dict[str, PropertySchema] = field(default_factory=dict)
    required: list[str] = field(default_factory=list)
    indexed: list[str] = field(default_factory=list)
    unique: list[list[str]] = field(default_factory=list)
    custom_code: str = ''
