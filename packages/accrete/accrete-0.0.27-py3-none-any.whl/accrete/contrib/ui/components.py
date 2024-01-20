from dataclasses import dataclass, field
from enum import Enum


class TableFieldAlignment(Enum):

    LEFT = 'left'
    CENTER = 'center'
    RIGHT = 'right'


class TableFieldType(Enum):

    NONE = ''
    STRING = '_string'
    MONETARY = '_monetary'
    FLOAT = '_float'


@dataclass
class TableField:

    label: str
    name: str
    alignment: TableFieldAlignment | Enum = TableFieldAlignment.LEFT
    header_alignment: TableFieldAlignment | Enum = None
    header_info: str = None
    field_type: TableFieldType | Enum = TableFieldType.NONE
    prefix: str = ''
    suffix: str = ''
    truncate_after: int = 0
    template: str = None


@dataclass
class BreadCrumb:

    name: str
    url: str


@dataclass
class ClientAction:

    name: str
    url: str = ''
    query_params: str = ''
    attrs: list[tuple[str, str]] = field(default_factory=list)
    submit: bool = False
    form_id: str = 'form'
    class_list: list[str] = field(default_factory=list)
