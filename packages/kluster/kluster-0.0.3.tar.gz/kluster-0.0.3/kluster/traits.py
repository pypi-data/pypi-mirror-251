"""
Traits for omero_ark


Traits are mixins that are added to every graphql type that exists on the mikro schema.
We use them to add functionality to the graphql types that extend from the base type.

Every GraphQL Model on Mikro gets a identifier and shrinking methods to ensure the compatibliity
with arkitekt. This is done by adding the identifier and the shrinking methods to the graphql type.
If you want to add your own traits to the graphql type, you can do so by adding them in the graphql
.config.yaml file.

"""

from pydantic import BaseModel
from typing import TYPE_CHECKING
from rath.turms.utils import get_attributes_or_error
from dask_gateway import GatewayCluster
from .repository import get_current_repository
from koil import unkoil
import webbrowser

if TYPE_CHECKING:
    pass


class DaskClientBearer(BaseModel):
    """Client Bearer Trait

    Implements both identifier and shrinking methods.
    Also Implements the data attribute


    """

    async def aget_gateway(self, asynchronous: bool = False) -> GatewayCluster:
        """Get the dask client for the representation.

        This is a synchronous version of the aget_gateway method.

        Usage:
            >>> gateway = cluster.get_gateway()
            >>> gateway.get_client()

        Parameters
        ----------
        asynchronous : bool, optional
            Whether to create the gateway asynchronously, by default False


        Returns
        -------
        cluster: GatewayCluster
                The dask gateway for the representation.
        """

        id = get_attributes_or_error(self, "id")

        return await get_current_repository().aget_gatewayfor_cluster(
            id, asynchronous=asynchronous
        )

    async def aget_dashboard_url(self) -> str:
        """Get the dask client for the representation.

        Returns:
            Client: The dask client for the representation.
        """
        dashboard_link = get_attributes_or_error(self, "dashboard_link")

        return await get_current_repository().aget_dashboard_url(dashboard_link)

    def get_gateway(self) -> GatewayCluster:
        """Get the dask client for the representation.

        This is a synchronous version of the aget_gateway method.

        Usage:
            >>> gateway = cluster.get_gateway()
            >>> gateway.get_client()


        Returns
        -------
        cluster: GatewayCluster
                The dask gateway for the representation.
        """

        return unkoil(self.aget_gateway)

    def open_dashboard(self) -> str:
        """Get the dask client for the representation."""
        absolute_url = unkoil(self.aget_dashboard_url)
        webbrowser.open(absolute_url)
        return absolute_url
