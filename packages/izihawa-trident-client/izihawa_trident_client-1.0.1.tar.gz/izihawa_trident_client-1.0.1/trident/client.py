import typing
from typing import AsyncGenerator

from aiobaseclient import BaseClient
from aiobaseclient.exceptions import ExternalServiceError


class TridentClient(BaseClient):
    async def response_processor(self, response):
        if response.status == 404:
            return None
        elif response.status != 200:
            data = await response.read()
            if hasattr(response, "request"):
                raise ExternalServiceError(response.request.url, response.status, data)
            else:
                raise ExternalServiceError(None, response.status, data)
        return response

    async def sinks_ls(self) -> dict:
        response = await self.get(f"/sinks/")
        return await response.json()

    async def sinks_create(self, sink_name: str, sink_config: dict) -> dict:
        response = await self.post(f"/sinks/{sink_name}/", json=sink_config)
        return await response.read()

    async def tables_ls(self) -> dict:
        response = await self.get(f"/tables/")
        return await response.json()

    async def tables_create(self, table_name: str, storage_name: str | None = None) -> bytes:
        url = f"/tables/{table_name}/"
        response = await self.post(url, params={'storage_name': storage_name})
        return await response.read()

    async def tables_import(self, table_name: str, table_ticket: str, storage_name: str | None = None) -> bytes:
        url = f"/tables/{table_name}/import/"
        response = await self.post(url, params={'table_ticket': table_ticket, 'storage_name': storage_name})
        return await response.read()

    async def tables_drop(self, table_name: str) -> bytes:
        url = f"/tables/{table_name}/"
        response = await self.delete(url)
        return await response.read()

    async def table_insert(self, table_name: str, key: str, value: bytes) -> bytes:
        url = f"/tables/{table_name}/{key}/"
        response = await self.put(url, data=value)
        return await response.read()

    async def table_share(self, table_name: str) -> dict:
        url = f"/tables/{table_name}/share/"
        response = await self.get(url)
        return await response.json()

    async def table_delete(self, table_name: str, key: str) -> dict:
        url = f"/tables/{table_name}/{key}/"
        response = await self.delete(url)
        return await response.json()

    async def table_foreign_insert(self, from_table_name: str, from_key: str, to_table_name: str, to_key: str) -> bytes:
        url = f"/tables/foreign_insert/"
        response = await self.post(url, params={
            'from_table_name': from_table_name,
            'from_key': from_key,
            'to_table_name': to_table_name,
            'to_key': to_key,
        })
        return await response.read()

    async def table_get(self, table_name: str, key: str, timeout: float = None) -> bytes:
        url = f"/tables/{table_name}/{key}/"
        response = await self.get(url, timeout=timeout)
        return await response.read()

    async def table_get_chunks(self, table_name: str, key: str, timeout: float = None) -> AsyncGenerator[bytes, None]:
        url = f"/tables/{table_name}/{key}/"
        response = await self.get(url, timeout=timeout)
        async for data, _ in response.content.iter_chunks():
            yield data

    async def table_ls(self, table_name) -> typing.AsyncGenerator[str, None]:
        response = await self.get(f"/tables/{table_name}/")
        async for data, _ in response.content.iter_chunks():
            for line in data.split('\n'):
                yield line

    async def table_exists(self, table_name: str, key: str) -> bool:
        url = f"/tables/{table_name}/{key}/exists/"
        response = await self.get(url)
        if response is None:
            return False
        response = await response.json()
        return response["exists"]
