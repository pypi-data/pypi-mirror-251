""" The Kluster (Client) Composition packages"""
from koil.composition import Composition
from .rath import KlusterRath
from .repository import Repository


class Kluster(Composition):
    """The KLuseter (Client) Composition

    This composition is the main entry point for the kluster client.
    and is used to build a client for a kluster instance, that can be
    used to execute graphql operations and retrieve the dask client
    from a connected dask gateway trough the repository.

    """

    rath: KlusterRath
    repo: Repository
