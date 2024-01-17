from typing import Any

from amsdal_integrations.clients.amsdal_client import AmsdalClient
from amsdal_integrations.clients.amsdal_client import AsyncAmsdalClient
from amsdal_integrations.clients.base import AsyncBaseClient
from amsdal_integrations.clients.base import BaseClient
from amsdal_integrations.data_classes import Schema
from amsdal_integrations.data_classes import SdkConfig


class AmsdalSdk:
    def __init__(
        self,
        config: SdkConfig,
        client_class: type[BaseClient] | None = None,
    ) -> None:
        client_class = client_class or AmsdalClient
        self.client = client_class(
            host=config.amsdal_host,
            auth=config.amsdal_auth,
            **config.client_extra,
        )

    def register_schema(
        self,
        schema: Schema,
        operation_id: str | None = None,
        *,
        skip_data_migrations: bool = False,
    ) -> None:
        self.client.register_schema(schema, operation_id=operation_id, skip_data_migrations=skip_data_migrations)

    def unregister_schema(self, class_name: str, operation_id: str | None = None) -> None:
        self.client.unregister_schema(class_name, operation_id=operation_id)

    def create(self, class_name: str, data: dict[str, Any], operation_id: str | None = None) -> None:
        self.client.create(class_name, data, operation_id=operation_id)

    def update(self, class_name: str, object_id: str, data: dict[str, Any], operation_id: str | None = None) -> None:
        self.client.update(class_name, object_id, data, operation_id=operation_id)

    def delete(self, class_name: str, object_id: str, operation_id: str | None = None) -> None:
        self.client.delete(class_name, object_id, operation_id=operation_id)


class AsyncAmsdalSdk:
    def __init__(
        self,
        config: SdkConfig,
        client_class: type[AsyncBaseClient] | None = None,
    ) -> None:
        client_class = client_class or AsyncAmsdalClient
        self.client = client_class(
            host=config.amsdal_host,
            auth=config.amsdal_auth,
            **config.client_extra,
        )

    async def register_schema(self, schema: Schema, operation_id: str | None = None) -> None:
        await self.client.register_schema(schema, operation_id=operation_id)

    async def unregister_schema(self, class_name: str, operation_id: str | None = None) -> None:
        await self.client.unregister_schema(class_name, operation_id=operation_id)

    async def create(self, class_name: str, data: dict[str, Any], operation_id: str | None = None) -> None:
        await self.client.create(class_name, data, operation_id=operation_id)

    async def update(
        self,
        class_name: str,
        object_id: str,
        data: dict[str, Any],
        operation_id: str | None = None,
    ) -> None:
        await self.client.update(class_name, object_id=object_id, data=data, operation_id=operation_id)

    async def delete(self, class_name: str, object_id: str, operation_id: str | None = None) -> None:
        await self.client.delete(class_name, object_id, operation_id=operation_id)
