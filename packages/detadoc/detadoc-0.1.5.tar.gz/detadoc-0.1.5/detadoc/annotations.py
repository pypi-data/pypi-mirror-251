from __future__ import annotations

import re
from typing import Annotated

from ormspace.keys import TableKey
from ormspace.metainfo import MetaInfo
from pydantic import BeforeValidator, Field


def string_to_list(string: str|list) -> list:
    if not string:
        return list()
    if isinstance(string, str):
        return re.split(r'[\n;]', string)
    return string


StringList = Annotated[list[str], BeforeValidator(string_to_list), Field(default_factory=list)]
ProfileKey = Annotated[TableKey, MetaInfo(tables=['Patient', 'Doctor', 'Employee'], item_name='profile'), Field('Doctor.admin')]
StaffKey = Annotated[TableKey, MetaInfo(tables=['Doctor', 'Employee'], item_name='staff'), Field('Doctor.admin')]


