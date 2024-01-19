from __future__ import annotations

import logging
import re
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, Sequence, Type, TypeVar, cast

import aiomysql
from pydantic import BaseModel

from beni.bfunc import toAny
from beni.btype import Null


class BModel(BaseModel):

    _tableName: str = ''

    @classmethod
    @property
    def tableName(cls):
        if type(cls._tableName) is not str:
            className = cls.__name__
            result = [className[0].lower()]
            for char in className[1:]:
                if char.isupper():
                    result.extend(['_', char.lower()])
                else:
                    result.append(char)
            cls._tableName = ''.join(result)
        return cls._tableName


_BModel = TypeVar('_BModel', bound=BModel)
_T = TypeVar('_T')


_sqlFormatRe = re.compile(r'\s*\n\s*')


def _sqlFormat(sql: str):
    return _sqlFormatRe.sub(' ', sql).strip()


@dataclass
class MysqlDb:
    host: str
    port: int
    user: str
    password: str
    db: str = ''
    _pool: aiomysql.Pool = Null

    @asynccontextmanager
    async def getCursor(self):
        isEcho = logging.getLogger().level is logging.DEBUG
        if not self._pool:
            self._pool = await aiomysql.create_pool(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db or None, echo=isEcho)  # type: ignore
        async with self._pool.acquire() as conn:
            async with cast(aiomysql.Connection, conn).cursor() as cur:
                yield cast(aiomysql.Cursor, cur)

    async def getOne(self, modelClass: Type[_BModel], sql: str, *args: Any) -> _BModel | None:
        async with self.getCursor() as cur:
            await cur.execute(_sqlFormat(sql), args)
            result: Sequence[Any] = await cur.fetchone()
            if not result:
                return None
            columns = self._getColumns(cur)
            data = {v: result[i] for i, v in enumerate(columns)}
            if modelClass is Any:
                return cast(_BModel, data)
            else:
                return modelClass(**data)

    async def getList(self, modelClass: Type[_BModel], sql: str, *args: Any) -> list[_BModel]:
        async with self.getCursor() as cur:
            await cur.execute(_sqlFormat(sql), args)
            result: Sequence[Sequence[Any]] = await cur.fetchall()
            if not result:
                return []
            columns = self._getColumns(cur)
            datas = [{v: row[i] for i, v in enumerate(columns)} for row in result]
            if modelClass is Any:
                return cast(list[_BModel], datas)
            else:
                return [modelClass(**x) for x in datas]

    async def saveOne(self, model: BModel, *, tableName: str = ''):
        columns: list[str] = []
        values: list[Any] = []
        for k, v in model.model_dump(exclude_unset=True).items():
            columns.append(f'`{k}`')
            values.append(v)
        tableName = tableName or model.__class__.tableName
        updateSql = ','.join([f'{x} = VALUES( {x} )' for x in columns])
        sql = f'''INSERT INTO `{tableName}` ( {','.join(columns)} ) VALUES %s ON DUPLICATE KEY UPDATE {updateSql}'''
        async with self.getCursor() as cur:
            result = await cur.execute(sql, [values])
            if result:
                await cast(aiomysql.Connection, cur.connection).commit()
                return result

    async def saveList(self, modelList: Sequence[BModel], *, tableName: str = ''):
        assert modelList, 'modelList 必须至少有一个元素'
        columns: list[str] = []
        values: list[Sequence[Any]] = []
        for k in modelList[0].model_dump().keys():
            columns.append(f'`{k}`')
        for model in modelList:
            values.append(tuple(model.model_dump().values()))
        tableName = tableName or modelList[0].__class__.tableName
        updateSql = ','.join([f'{x} = VALUES( {x} )' for x in columns])
        sql = f'''INSERT INTO `{tableName}` ( {','.join(columns)} ) VALUES %s, %s ON DUPLICATE KEY UPDATE {updateSql}'''
        async with self.getCursor() as cur:
            result = await cur.execute(sql, values)
            if result:
                await cast(aiomysql.Connection, cur.connection).commit()
                return result

    async def execute(self, sql: str, *args: Any):
        async with self.getCursor() as cur:
            result = await cur.execute(sql, args)
            if result:
                await cast(aiomysql.Connection, cur.connection).commit()
                return result

    async def getValue(self, valueClass: Type[_T], sql: str, *args: Any) -> _T | None:
        async with self.getCursor() as cur:
            await cur.execute(sql, args)
            result: Sequence[Any] = await cur.fetchone()
            if not result:
                return None
            return result[0]

    async def getValueList(self, valueClass: Type[_T], sql: str, *args: Any) -> list[_T] | None:
        async with self.getCursor() as cur:
            await cur.execute(sql, args)
            result: Sequence[Sequence[Any]] = await cur.fetchall()
            if not result:
                return None
            return [x[0] for x in result]

    def makeByDb(self, db: str):
        return MysqlDb(self.host, self.port, self.user, self.password, db=db)

    def _getColumns(self, cur: aiomysql.Cursor) -> tuple[Any, ...]:
        return tuple(x[0] for x in toAny(cur.description))
