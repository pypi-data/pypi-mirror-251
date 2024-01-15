""" An example of a custom repository for Kluster, that
    uses the Arkitekt project for configuration. """

from fakts import Fakts
from herre import Herre
from kluster.repository import Repository
from typing import Callable, Awaitable
from dask_gateway import GatewayCluster


async def dummy_loader() -> str:
    """This is a dummy loader for the token loader and refresher"""
    raise Exception("Not Implemented")


class ArkitektRepository(Repository):
    """A Repository for clusters

    This is a repostiroy for clusters, that
    encapsulates the logic for getting a gateway
    from a connected dask-gateway server.

    In this case, the repository uses the Fakts service
    to get the endpoint for the dask-gateway server, and
    the Herre service to get the token for the dask-gateway
    server.

    """

    fakts: Fakts
    herre: Herre
    fakts_key: str
    endpoint: str = "dummy"
    token_loader: Callable[[], Awaitable[str]] = dummy_loader
    token_refresher: Callable[[], Awaitable[str]] = dummy_loader

    _configured = False

    async def aconfigure(self) -> None:
        """Configure the repository"""
        self.endpoint = await self.fakts.aget(self.fakts_key)
        self.token_loader = self.herre.aget_token
        self.token_refresher = self.herre.arefresh_token
        self._configured = True

    async def aget_gatewayfor_cluster(self, *args, **kwargs) -> GatewayCluster:  # noqa
        """Get the dask gateway for a cluster"""
        if not self._configured:
            await self.aconfigure()
        return await super().aget_client_for_cluster(*args, **kwargs)

    async def aget_dashboard_url(self, dashboard_url: str) -> str:
        """Get the dask gateway for a cluster"""
        if not self._configured:
            await self.aconfigure()
        return await super().aget_dashboard_url(dashboard_url)
