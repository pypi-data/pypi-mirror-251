"""Exception class definitions for all exceptions raised within the dindbox package"""


class DindBoxException(Exception):
    """A base class for all exceptions raised by Dindbox methods.

    If you want to catch all errors that a Dindbox instance may be raising, it is enough to catch this base exception.
    """


class DockerError(DindBoxException):
    """This exception is raised for any error the occurs from interacting with the docker daemon.

    Any Exception raised by the docker-py library, or any call to the docker-cli with exit code > 0, will be
    transformed into an instance of this exception, such that users of this package do not have to deal with the
    various Exception types raised by these calls.
    """


class DockerInDockerError(DockerError):
    """Raised when a call to the docker-in-docker client fails.

    Note that this class inherits from DockerError, so catching DockerError exceptions will cover instances of this
    class, too.
    """


class DindBoxExists(DindBoxException):
    "Raised when trying to create a DindBox under a name that already exists."


class DindBoxRunning(DindBoxException):
    "Raised when trying to remove a DindBox which is running."


class DindBoxCreationFailed(DindBoxException):
    "Raised when an error occurs during creation of a new DindBox"


class AutoRemoveNotPossible(DindBoxException):
    "Raised when trying to set auto-remove for a detached DindBox"


class ContainerAlreadyRunning(DindBoxException):
    """Raised when trying to start a DindBox that is already running."""


class ContainerNotRunning(DindBoxException):
    """Raised when trying to access a stopped container."""


class ContainerNotFound(DindBoxException):
    """Raised when trying to access a container which does not exist."""


class ContainerRestartFailed(DindBoxException):
    """Raised when restarting a container fails without any Excepction from the docker client library"""


class InvalidContainerType(DindBoxException):
    """Raised when requesting an invalid container type."""


class VolumeAlreadyExists(DindBoxException):
    """Raised when trying to create a docker volume under an already existing name."""


class UndefinedBindVolumeBasePath(DindBoxException):
    """Raised when the base path of bind mounts of an existing DindBox cannot be determined."""


class InvalidBindMountName(DindBoxException):
    """Raised when trying to bind-mount a directory, whose name begins with the DindBox name.

    Such a directory name could confuse the auto-identification heuristics for the different mount types and is
    therefore not permitted.
    """


class DockerNetworkAlreadyExists(DindBoxException):
    """Raised when trying to create a docker network under an already existing name."""
