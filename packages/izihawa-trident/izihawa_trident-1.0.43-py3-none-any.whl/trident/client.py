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

    async def store(self, key: str, data: bytes, timeout: float = None) -> dict:
        url = f"/kv/{key}/"
        response = await self.put(url, data=data, timeout=timeout)
        return await response.json()

    async def add_to_document(self, doc_name: str, kv_key: str, doc_key: str) -> dict:
        url = f"/documents/{doc_name}/"
        response = await self.put(url, params={'kv_key': kv_key, 'doc_key': doc_key})
        return await response.json()

    async def document_share(self, doc_name: str) -> dict:
        url = f"/documents/{doc_name}/"
        response = await self.get(url)
        return await response.json()

    async def delete_key(self, key: str) -> dict:
        url = f"/kv/{key}/"
        response = await self.delete(url)
        return await response.json()

    async def read(self, key: str, timeout: float = None) -> bytes:
        url = f"/kv/{key}/"
        response = await self.get(url, timeout=timeout)
        return await response.read()

    async def ls(self, mask: str = '*') -> list[str]:
        response = await self.get("/kv/", params={'mask': mask})
        response = await response.json()
        return response['keys']

    async def read_chunks(self, key: str, timeout: float = None) -> AsyncGenerator[bytes, None]:
        url = f"/kv/{key}/"
        response = await self.get(url, timeout=timeout)
        async for data, _ in response.content.iter_chunks():
            yield data

    async def exists(self, key: str) -> bool:
        url = f"/kv/{key}/exists/"
        response = await self.get(url)
        if response is None:
            return False
        response = await response.json()
        return response["exists"]
