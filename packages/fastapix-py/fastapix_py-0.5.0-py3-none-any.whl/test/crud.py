# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : zhangzhanqi
# @FILE     : crud.py
# @Time     : 2024/1/3 下午3:57
# @Desc     : $
import json
from contextlib import asynccontextmanager
from typing import Optional
from uuid import UUID, uuid4

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

import fastapix
from fastapix import offline, handlers
from fastapix.common.serializer import pydantic_json_serializer
from fastapix.crud import SQLModel, Field, SQLAlchemyCrud, EngineDatabase


@asynccontextmanager
async def lifespan(app: FastAPI):
    """"""
    await database.async_run_sync(SQLModel.metadata.create_all, is_session=False)
    yield


app = FastAPI(lifespan=lifespan)

offline.register_offline_openapi(app)
handlers.register_exception_handlers(app)


class File(SQLModel):
    name: str = Field(None, title='文件名')
    key: str = Field(None, title='文件key')
    type: str = Field(None, title='文件类型')
    path: Optional[str] = Field(None, title='文件路径')


class Category(SQLModel, table=True):
    id: str = Field(..., title="ID", primary_key=True, nullable=False, update=False)
    name: str = Field(..., title='配置项名称', max_length=100, index=True)
    docs: Optional[str] = Field(None, title='配置项描述', query=False)
    cfile: Optional[File] = Field(None, title='配置项模板', query=False)

    files: list[File] = Field(None, title='')


database_url = 'sqlite+aiosqlite:///test.db'

engine: AsyncEngine = create_async_engine(database_url, json_serializer=pydantic_json_serializer)

database = EngineDatabase(engine)

cate_router = SQLAlchemyCrud(Category, database).router_manager()

# 挂载中间件
app.add_middleware(database.asgi_middleware)
# 挂载路由
app.include_router(cate_router.create_object_router())
app.include_router(cate_router.read_object_router())
app.include_router(cate_router.update_object_router())
app.include_router(cate_router.delete_object_router())

if __name__ == '__main__':
    fastapix.run(app)