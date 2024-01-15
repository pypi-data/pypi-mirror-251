""" Custom errors for kluster """


class KlusterError(Exception):
    """Base class for exceptions in this module."""

    pass


class NoKlusterRathInContextError(KlusterError):
    """Raised when there is no KlusterRath in the context"""

    pass
