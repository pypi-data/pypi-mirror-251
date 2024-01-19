# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : zhangzhanqi
# @FILE     : __init__.py
# @Time     : 2024/1/4 上午9:57
# @Desc     : $
from typing import Optional

from pydantic import BaseModel, Field
from fastapix.crud import SQLModel, Field as XField


class File(BaseModel):
    name: str = Field(None, title='文件名')
    key: str = Field(None, title='文件key')
    type: str = Field(None, title='文件类型')
    path: Optional[str] = Field(None, title='文件路径')


class ReportConfig(SQLModel, table=True):
    id: str = XField(..., title="ID", primary_key=True, nullable=False, update=False)
    name: str = XField(..., title='配置项名称', max_length=100, index=True)
    docs: Optional[str] = XField(None, title='配置项描述', query=False)
    cfile: Optional[File] = XField(None, title='配置项模板', query=False)

    files: list[File] = XField(None, title='')

print(ReportConfig(**{
    "id": "id",
    "name": "name",
    "cfile": {
        "name": "xxxx",
        "key": "xxxxxx",
        "type": ""
    },
    "files": [{
        "name": "xxxx",
        "key": "xxxxxx",
        "type": ""
    }]
}).files[0].key)
