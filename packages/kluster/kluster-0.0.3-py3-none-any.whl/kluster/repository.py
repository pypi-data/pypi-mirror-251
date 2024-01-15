""" The Repository for clusters packages"""
from koil.composition import KoiledModel
from dask_gateway import Gateway, GatewayCluster
from dask_gateway.auth import GatewayAuth
from typing import Callable, Awaitable, TypeVar, Optional, Tuple, Any, Dict
import contextvars

current_repository: contextvars.ContextVar[
    Optional["Repository"]
] = contextvars.ContextVar("current_repository", default=None)


class JWTAuth(GatewayAuth):
    """Attaches HTTP Bearer Authentication to the given Request object.
    while using the Gateway"""

    def __init__(self, token: str) -> None:
        """Initialize the auth object."""
        self.token = token

    def pre_request(self, req: Any) -> Tuple[Dict[str, str], Any]:  # noqa
        """Pre Request

        Parameters
        ----------
        resp : Request
            The response object

        Returns
        -------
        Tuple[Dict[str, str], Any]
            The headers and the body
        """
        headers = {"Authorization": "Bearer " + self.token}
        return headers, None


T = TypeVar("T", bound="Repository")


def get_current_repository() -> "Repository":
    """Get Current Repository

    Returns
    -------
    Repository
        The current repository
    """
    repo = current_repository.get()
    if repo is None:
        raise RuntimeError("No current repository")

    return repo


class Repository(KoiledModel):
    """A Repository for clusters

    This is a repostiroy for clusters, that
    encapsulates the logic for getting a gateway
    from a connected dask-gateway server.



    """

    endpoint: str
    token_loader: Callable[[], Awaitable[str]]
    token_refresher: Callable[[], Awaitable[str]]

    async def aget_gatewayfor_cluster(
        self, cluster_name: str, asynchronous: bool = False
    ) -> GatewayCluster:
        """Get the dask gateway for a cluster

        Parameters
        ----------
        cluster_name : str
            The name of the cluster
        asynchronous : bool, optional
            Whether to create the gateway asynchronously, by default False

        Returns
        -------
        cluster: GatewayCluster
                The dask gateway for the cluster.
        """

        token = await self.token_loader()

        gateway = Gateway(
            address=self.endpoint,
            auth=JWTAuth(token),
            asynchronous=asynchronous,
        )

        return gateway.connect(cluster_name)

    async def aget_dashboard_url(self, dashboard_url: str) -> str:
        """Get the absoltue dashboard url for a cluster

        This will return the absolute url for the dashboard
        of a cluster. This is an asynchronous method, as resolving
        the url may require a network request.

        Parameters
        ----------
        dashboard_url : str
            The name of the cluster

        Returns
        -------
        str
            The absolute url for the dashboard of the cluster.
        """

        return self.endpoint + dashboard_url

    async def __aenter__(self: T) -> T:
        """Set the current repository to this repository"""
        current_repository.set(self)
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore # noqa
        """Reset the current repository"""
        current_repository.set(None)
        return await super().__aexit__(exc_type, exc_val, exc_tb)

    class Config:
        """Config"""

        underscore_attrs_are_private = True
        arbitrary_types_allowed = True
