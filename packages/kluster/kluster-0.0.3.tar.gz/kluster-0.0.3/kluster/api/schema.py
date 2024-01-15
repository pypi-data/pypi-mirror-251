from pydantic import BaseModel, Field
from typing_extensions import Literal
from typing import List, Optional, Tuple
from rath.scalars import ID
from kluster.rath import KlusterRath
from kluster.traits import DaskClientBearer
from kluster.funcs import execute, aexecute
from enum import Enum


class DaskClusterState(str, Enum):
    """The state of a dask cluster"""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    FAILED = "FAILED"


class ClusterFilter(BaseModel):
    """Filter for Dask Clusters"""

    ids: Optional[Tuple[ID, ...]]
    search: Optional[str]

    class Config:
        """A config class"""

        frozen = True
        extra = "forbid"
        use_enum_values = True


class OffsetPaginationInput(BaseModel):
    offset: int
    limit: int

    class Config:
        """A config class"""

        frozen = True
        extra = "forbid"
        use_enum_values = True


class CreateClusterInput(BaseModel):
    """Create a dask cluster input"""

    name: str

    class Config:
        """A config class"""

        frozen = True
        extra = "forbid"
        use_enum_values = True


class DaskClusterFragmentSecurity(BaseModel):
    """A security object for a dask cluster"""

    typename: Optional[Literal["Security"]] = Field(alias="__typename", exclude=True)
    tls_cert: str = Field(alias="tlsCert")
    tls_key: str = Field(alias="tlsKey")

    class Config:
        """A config class"""

        frozen = True


class DaskClusterFragment(DaskClientBearer, BaseModel):
    typename: Optional[Literal["DaskCluster"]] = Field(alias="__typename", exclude=True)
    id: ID
    "The id of the dask cluster"
    name: str
    "The name of the dask cluster"
    dashboard_link: str = Field(alias="dashboardLink")
    "A link to the dashboard for the dask cluster. Relative to the proxy."
    status: DaskClusterState
    "The status of the dask cluster"
    scheduler_address: str = Field(alias="schedulerAddress")
    "A link to the scheduler for the dask cluster. Relative to the proxy."
    security: Optional[DaskClusterFragmentSecurity]
    "The user who created the dask cluster"

    class Config:
        """A config class"""

        frozen = True


class CreateDaskClusterMutation(BaseModel):
    create_dask_cluster: DaskClusterFragment = Field(alias="createDaskCluster")
    "Create a new dask cluster on a bridge server"

    class Arguments(BaseModel):
        name: str

    class Meta:
        document = "fragment DaskCluster on DaskCluster {\n  id\n  name\n  dashboardLink\n  status\n  schedulerAddress\n  security {\n    tlsCert\n    tlsKey\n  }\n}\n\nmutation CreateDaskCluster($name: String!) {\n  createDaskCluster(input: {name: $name}) {\n    ...DaskCluster\n  }\n}"


class ListDaskClustersQuery(BaseModel):
    dask_clusters: Tuple[DaskClusterFragment, ...] = Field(alias="daskClusters")
    "Return all dask clusters"

    class Arguments(BaseModel):
        pass

    class Meta:
        document = "fragment DaskCluster on DaskCluster {\n  id\n  name\n  dashboardLink\n  status\n  schedulerAddress\n  security {\n    tlsCert\n    tlsKey\n  }\n}\n\nquery ListDaskClusters {\n  daskClusters {\n    ...DaskCluster\n  }\n}"


class GetDaskClusterQuery(BaseModel):
    dask_cluster: DaskClusterFragment = Field(alias="daskCluster")
    "Return a dask cluster by id"

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment DaskCluster on DaskCluster {\n  id\n  name\n  dashboardLink\n  status\n  schedulerAddress\n  security {\n    tlsCert\n    tlsKey\n  }\n}\n\nquery GetDaskCluster($id: ID!) {\n  daskCluster(id: $id) {\n    ...DaskCluster\n  }\n}"


class SearchDaskClusterQueryOptions(DaskClientBearer, BaseModel):
    """A dask cluster"""

    typename: Optional[Literal["DaskCluster"]] = Field(alias="__typename", exclude=True)
    value: ID
    "The id of the dask cluster"
    label: str
    "The name of the dask cluster"

    class Config:
        """A config class"""

        frozen = True


class SearchDaskClusterQuery(BaseModel):
    options: Tuple[SearchDaskClusterQueryOptions, ...]
    "Return all dask clusters"

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchDaskCluster($search: String, $values: [ID!]) {\n  options: daskClusters(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: name\n  }\n}"


async def acreate_dask_cluster(
    name: str, rath: Optional[KlusterRath] = None
) -> DaskClusterFragment:
    """CreateDaskCluster


     createDaskCluster:  A dask cluster


    Arguments:
        name (str): name
        rath (kluster.rath.KlusterRath, optional): The omero_ark rath client

    Returns:
        DaskClusterFragment"""
    return (
        await aexecute(CreateDaskClusterMutation, {"name": name}, rath=rath)
    ).create_dask_cluster


def create_dask_cluster(
    name: str, rath: Optional[KlusterRath] = None
) -> DaskClusterFragment:
    """CreateDaskCluster


     createDaskCluster:  A dask cluster


    Arguments:
        name (str): name
        rath (kluster.rath.KlusterRath, optional): The omero_ark rath client

    Returns:
        DaskClusterFragment"""
    return execute(
        CreateDaskClusterMutation, {"name": name}, rath=rath
    ).create_dask_cluster


async def alist_dask_clusters(
    rath: Optional[KlusterRath] = None,
) -> List[DaskClusterFragment]:
    """ListDaskClusters


     daskClusters:  A dask cluster


    Arguments:
        rath (kluster.rath.KlusterRath, optional): The omero_ark rath client

    Returns:
        List[DaskClusterFragment]"""
    return (await aexecute(ListDaskClustersQuery, {}, rath=rath)).dask_clusters


def list_dask_clusters(rath: Optional[KlusterRath] = None) -> List[DaskClusterFragment]:
    """ListDaskClusters


     daskClusters:  A dask cluster


    Arguments:
        rath (kluster.rath.KlusterRath, optional): The omero_ark rath client

    Returns:
        List[DaskClusterFragment]"""
    return execute(ListDaskClustersQuery, {}, rath=rath).dask_clusters


async def aget_dask_cluster(
    id: ID, rath: Optional[KlusterRath] = None
) -> DaskClusterFragment:
    """GetDaskCluster


     daskCluster:  A dask cluster


    Arguments:
        id (ID): id
        rath (kluster.rath.KlusterRath, optional): The omero_ark rath client

    Returns:
        DaskClusterFragment"""
    return (await aexecute(GetDaskClusterQuery, {"id": id}, rath=rath)).dask_cluster


def get_dask_cluster(id: ID, rath: Optional[KlusterRath] = None) -> DaskClusterFragment:
    """GetDaskCluster


     daskCluster:  A dask cluster


    Arguments:
        id (ID): id
        rath (kluster.rath.KlusterRath, optional): The omero_ark rath client

    Returns:
        DaskClusterFragment"""
    return execute(GetDaskClusterQuery, {"id": id}, rath=rath).dask_cluster


async def asearch_dask_cluster(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KlusterRath] = None,
) -> List[SearchDaskClusterQueryOptions]:
    """SearchDaskCluster


     options:  A dask cluster


    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kluster.rath.KlusterRath, optional): The omero_ark rath client

    Returns:
        List[SearchDaskClusterQueryDaskclusters]"""
    return (
        await aexecute(
            SearchDaskClusterQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_dask_cluster(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KlusterRath] = None,
) -> List[SearchDaskClusterQueryOptions]:
    """SearchDaskCluster


     options:  A dask cluster


    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kluster.rath.KlusterRath, optional): The omero_ark rath client

    Returns:
        List[SearchDaskClusterQueryDaskclusters]"""
    return execute(
        SearchDaskClusterQuery, {"search": search, "values": values}, rath=rath
    ).options
