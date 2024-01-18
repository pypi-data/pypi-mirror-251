"""Contains the dindbox class which contains the main functionality of this package, and some helper functions."""

# pylint: disable=fixme
# pylint: disable=too-many-lines

import ipaddress
import os
import logging
import shutil
import subprocess
import tarfile
import tempfile
from glob import glob
from os.path import abspath, basename, isdir, join, normpath
from time import sleep

import docker
import docker.errors

# pylint: disable=wildcard-import
from .errors import *

logger = logging.getLogger(__name__)


def is_running(container, wait_seconds=0):
    """Check if a docker container is in 'running' state.

    Args:
      container: A Container object as provided by the docker package.
      wait_seconds:  For how many seconds the should check be retried if the container is not running
        initially (optional, default = 0, only integer values allowed).

    Returns:
      True if the container is running, false otherwise.
    """
    container.reload()
    if container.status == "running":
        return True
    for _ in range(wait_seconds):
        sleep(1)
        container.reload()
        if container.status == "running":
            return True
    return False


def get_invalid_var_lib_docker_volume(container):
    """Find the name of a docker volume mounted to the container at '/var/lib/docke'

    This is a workaround for https://github.com/docker/docker-py/issues/2973

    Args:
      container: A Container object as provided by the docker package.

    Returns:
      The name of the invalidly mounted volume, None if there is no such volume.
    """
    for mnt in container.attrs["Mounts"]:
        if mnt["Destination"] == "/var/lib/docke":  # sic!
            return mnt["Name"]
    return None


def get_file(container, container_file, host_directory):
    """Retrieve a file from a docker container and place a copy in a directory on the docker host.

    This works even if the container is stopped/not yet started.

    Args:
      container: A Container object as provided by the docker package.
      container_file: In-container absolute path to the file as string.
      host_directory: Host directory (as string, without filename) where the file should be copied.

    Raises:
        DockerError: If reading the file from the container fails.
    """
    # TODO: document exceptions regarding opening the destination file for writing
    try:
        bits, _ = container.get_archive(container_file)
    except docker.errors.DockerException as exc:
        raise DockerError("Error reading file from container.") from exc
    filename = basename(container_file)
    host_file = abspath(join(host_directory, filename))
    host_tarfile = host_file + "_out.tar"
    with open(host_tarfile, "wb") as file:
        for chunk in bits:
            file.write(chunk)
    tar = tarfile.open(host_tarfile)
    tar.extractall(path=host_directory)
    tar.close()
    os.remove(host_tarfile)


def put_file(container, host_file, container_directory):
    """Copy a file from the docker host into a container.

    This works even if the container is stopped/not yet started.

    Args:
        container: A Container object as provided by the docker package.
        host_file: String containing the absolute path to the file on the host.
        container_directory: In-container directory (as string, without filename) where the file should be copied.

    Raises:
        DockerError: If copying the file to the container fails.
    """
    host_tarfile = host_file + "_in.tar"
    filename = basename(host_file)
    with tarfile.open(host_tarfile, "w") as tar:
        tar.add(host_file, arcname=filename)  # arcname=filename avoids storing the tmp-dir sub-path in the tar file
    with open(host_tarfile, "rb") as file:
        data = file.read()
    try:
        status = container.put_archive(container_directory, data)
        if status is not True:
            raise DockerError("Failed to write file to container.")
    except docker.errors.DockerException as exc:
        raise DockerError("Failed to write file to container.") from exc
    finally:
        os.remove(host_tarfile)


# TODO: Command-line output at log_level=WARNING is maybe too quiet. Probably we should add some kind of confirmation
#       messages (print instead of log?) to signal succesful completion of commands.
class DindBox:
    """A virtual docker-capable testing environment based on docker-in-docker (dind).

    Every DindBox uses two containers:
      * the build container is the one with which the user (or parent program) interacts
      * the service container is running the docker daemon.

    All docker-related objects used and returned by the methods of this class are from classes, by the Python
    package "docker". This applies to container, volumes, networks, and the client, unless noted otherwise.
    """

    SERVICE_CONTAINER_SUFFIX = "_docker"
    BUILD_CONTAINER_SUFFIX = "_build"
    NETWORK_SUFFIX = "_net"
    DEFAULT_BIND_VOLUME_BASE_PATH = "/tmp/dindbox/mounts"
    PROMPT_STRING = "\\[\\033[1;34m\\][dindbox]\\[\\033[0m\\]\\[\\033[1;32m\\] \\u@$DINDBOX\\[\\033[0m\\]:\\w\\$ "

    def __init__(
        self,
        name,
        _recover=False,
        build_image="debian:bullseye",
        service_image="docker:dind",
        volumes=None,
        bind_volumes=None,
        bind_volume_base_path=None,
        host_network_name="registry.local",
        docker_network=None,
        subnet=None,
        env_vars=None,
        shell=None,
        cmd=None,
        fancy_prompt=True,
        always_pull=False,
        **kwargs,
    ):
        """Constructor. Create an object for an entirely new DindBox.

        Note that you will need to call create() or run() subsequently, to actually create the associated docker
        entities and directories.

        In order to retroactively create a new object for a pre-existing DindBox (i.e. for which the docker entities
        already exist and which already may be running), call recover() instead of this constructor.

        Args:
            name (str): _description_
            build_image (str, optional): Docker image for the build container. Defaults to 'debian:bullseye'.
            service_image (str, optional): Docker image for the service container. Defaults to 'docker:dind'.
            volumes (list of str, optional): In-container paths for which docker volumes will be created and mounted
              to both containers. Defaults to None.
            bind_volumes (list of str, optional): In-container paths for which temporary host directories will be
              created and mounted to both containers. Defaults to None.
            bind_volume_base_path (str, optional): Directory where bind-mount volumes are created on the host. For
              the default, see the DindBox.DEFAULT_BIND_VOLUME_BASE_PATH constant.
            host_network_name (str, optional): Hostname under which to reach the host operating system. Defaults to
              'host.local'.
            docker_network (str, optiona): Name of a docker network to connect to. If not provided, a new network will
              be created.
            env_vars (list of str, optional): List of environment variables which will be set inside the build
              container. Each entry needs to be either in the form VARNMAE or VARNAME=VALUE. If =VALUE is not
              provided, the variable will be inherited from the current shell, but only if it is actually defined
              there. Defaults to None.
            shell (str, optional): Set the shell in which to run cmd (see below). Defaults to "bash" for debian/
              ubuntu, and "sh" otherwise.
            cmd (str, optional): Command to run in the build container. Defaults to None, which means the normale
              entrypoint will run, usually providing an interactive shell.
            fancy_prompt (bool, optional): Modify the prompt within the build container to show that it is a DindBox
              and include its name. Defaults to True.
            always_pull (bool, optional): Always pull images, even if they are already available locally. Can be used
              to make sure to always use the latest version of images, but will slow down startup of the dindbox.
              defaults to False.

        Raises:
            DindBoxExists: If  DindBox of the same name already exists.
        """
        self.client = docker.from_env()
        self._name = name
        self._bind_volume_base_path = bind_volume_base_path
        self.__assumed_bind_volume_base_path = None
        if _recover:
            self._service_image = None
            self._build_image = None
            # __create_data containes information needed for create() only, will not be initialized when recovering
            self.__create_data = None  # pylint: disable=unused-private-member
        else:
            if self.__get_container("service") is not None:
                raise DindBoxExists(
                    "A DindBox of name '"
                    + name
                    + "' seems to already exist. Choose a different "
                    + "name Alternatively, to create an object for the existing DindBox, call "
                    + "DindBox.recover(name)"
                )

            self._service_image = service_image
            self._build_image = build_image

            # This dict will hold information that is needed only during create(). It will not be initialized during
            # recover mode.
            self.__create_data = {}
            self.__create_data["host_network_name"] = host_network_name
            self.__create_data["docker_network"] = docker_network
            self.__create_data["subnet"] = subnet
            if volumes is None:
                self.__create_data["volumes"] = ["/var/lib/docker"]
            else:
                self.__create_data["volumes"] = volumes
            if bind_volumes is None:
                self.__create_data["bind_volumes"] = []
            else:
                self.__create_data["bind_volumes"] = bind_volumes
            self.__create_data["env_vars"] = []
            if env_vars:
                for var in env_vars:
                    if "=" in var:
                        self.__create_data["env_vars"].append(var)
                    else:
                        # variable name has been provided without value, need to retrieve it from current env
                        value = os.getenv(var)
                        if value:
                            self.__create_data["env_vars"].append(var + "=" + value)
                        else:
                            logger.info(
                                "Environment variable %s does not exist in current shell and will not be passed into containers.",
                                var,
                            )
            if shell is None:
                if "ubuntu" in self._build_image.lower() or "debian" in self._build_image.lower():
                    self.__create_data["shell"] = "bash"
                else:
                    self.__create_data["shell"] = "sh"
            else:
                self.__create_data["shell"] = shell
            self.__create_data["cmd"] = cmd
            self.__create_data["fancy_prompt"] = fancy_prompt
            self.__create_data["always_pull"] = always_pull

        # The remaining attributes will be populated during create() or recover():
        # The following four are references to objects from the docker package
        self._network = None
        self._service_container = None
        self._build_container = None
        self._volumes = []
        # _bind_volumes is a list of Str, in the format SOURCE_DIR:TARGET_DIR, containing all bind-volumes
        # (mounted temporary host directories that are auto-created and auto-removed with the dindbox)
        self._bind_volumes = []
        # _bind_mounts has the same format, but contains pre-existing host dirs that will be mounted and NOT
        # auto-removed at the end. This list currently only contains the mount of the CWD to /mnt and cannot be
        # configured by the user
        self._bind_mounts = []
        # _mounts will be a list of docker.type.Mount objects, which contains *all* mounts of the two containers
        # (docker volumes, bind volumes, /mnt). This list can directly be used as the
        # mounts= argument of docker.container.create()
        # It is populated by the _create_volumes and _create_bind_volumes methods and their _recover_* counterparts
        self._mounts = []
        # _invalid_var_lib_docker_volumes will store references to invalid volumes created due to a bug in
        # docker-py, so we can remove them at the end
        self._invalid_var_lib_docker_volumes = []

    @classmethod
    def recover(cls, name, partial=False, **kwargs):
        """Create a new object for a pre-existing DindBox (i.e. for which the docker entities already exist).

        Use this if you have no access to the DindBox object that was instantiated at initial creation of the
        DindBox. It does not matter if the DindBox is already running or not. This method will identify all
        associated docker entities and directories based on the naming conventions.

        Args:
            name (str): Name of the existing DindBox for which to re-create an object.
            partial (bool, optional):  Create the object even if the DindBox exists only partially, and parts of it
              are missing. This is useful to recover a DindBox that has been only partially created or removed due to
              an error, and clean it up. Defaults to False.

        Additional Args:
        Any other keyword arguments passed to this method will be forwarded to the constructor (__init__). However,
        most of them will be of no effect, since they represent properties which cannot be modified for an already
        existing DindBox. One which has an effect is

            bind_volume_base_path (str, optional): Directory where bind-mount volumes are created on the host. The tool should be able to identify this path automatically. If it does not work for you, use this parameter to specify the path explicitly.

        Returns: a new DindBox object associated with the pre-existing DindBox.

        Raises:
            DockerError: If any error occurs while interacting with docker.
            docker.errors.NotFound: If partial=False and parts of the DinDox do not exist, or if partial=True and no
              parts exist at all
        """
        # Additional arguments:
        # * bind_volume_base_path (used inside __init__)
        box = cls(name, _recover=True, **kwargs)
        logger.info("Recovering DindBox by name '%s'...", name)
        box._recover_containers(partial)
        box._recover_mounts()
        box._find_invalid_var_lib_docker_volumes()
        box._recover_network(partial)
        if not (
            box._service_container
            or box._build_container
            or box._network
            or box._volumes
            or box._bind_volumes
            or box._bind_mounts
        ):
            raise docker.errors.NotFound(f"No parts of DindBox '{name}' could be recovered.")
        return box

    def create(self):
        """Create all docker entities and directories for the DindBox, but do not start the containers yet.

        Raises:
            DindBoxCreationFailed: If any error occurs during the creation of the DindBox.
        """
        # TODO: Investigate if we can add labels to docker objects in order to safely recover/remove them later. This
        #       would also allow to implement something like 'dindbox purge' or 'dindbox list'
        try:
            self._pull_images()
            self._create_or_find_network()
            self._create_volumes()
            self._create_bind_volumes()
            self._create_bind_mounts()
            self._create_service_container()
            self._create_build_container()
            self._find_invalid_var_lib_docker_volumes()
        except Exception as exc:
            logger.error("Error while creating DindBox. Cleaning up...")
            self.remove()
            raise DindBoxCreationFailed("Error while creating DindBox.") from exc

    def reload(self):
        """Update the state and attributes of all docker-related objects.

        Unless called before, any queries to docker-related attributes may be out of date.

        Raises:
            DockerError: If any error occurs while interacting with docker.
        """
        try:
            if self._network:
                self._network.reload()
            for vol in self._volumes:
                vol.reload()
            if self._service_container:
                self._service_container.reload()
            if self._build_container:
                self._build_container.reload()
        except docker.errors.DockerException as exc:
            raise DockerError(
                "Error reloading DindBox objects. This may happen if parts of the box have been removed."
            ) from exc

    def status(self):
        """Return a dict with datailed status information about the DindBox.

        This is used by the status screen module, but may also be used as an API to query DindBox status from your
        own programs. Note that you need not call reload() before calling this method, it will do this by itself.

        Raises:
            DockerError: If any error occurs while interacting with docker.
        """
        self.reload()
        try:
            status = {}
            status["box"] = {"Name": self._name, "Bind volume base path": self._bind_volume_base_path}
            if self._build_container:
                status["build_container"] = {
                    "Name": self._build_container.name,
                    "Image": self._build_container.image.tags[0],
                    "Short ID": self._build_container.short_id,
                    "Status": self._build_container.status,
                    "IP": self.__get_container_ip("build"),
                }
                status["build_container"]["Running Processes"] = []
                status["build_container"]["Environment"] = []
                if self._build_container.status == "running":
                    processes = self._build_container.top()["Processes"]
                    for proc in processes:
                        # append a string in the form 'PID UID CMD'
                        status["build_container"]["Running Processes"].append(" ".join([proc[1], proc[0], proc[-1]]))
                    status["build_container"]["Environment"] = self._build_container.attrs["Config"]["Env"]
            else:
                status["build_container"] = None
            if self._service_container:
                status["service_container"] = {
                    "Name": self._service_container.name,
                    "Image": self._service_container.image.tags[0],
                    "Short ID": self._service_container.short_id,
                    "Status": self._service_container.status,
                    "IP": self.__get_container_ip("service"),
                }
                if self._service_container.status == "running":
                    # get running dind containers
                    dind_containers_statuses = (
                        self._service_container.exec_run('docker ps -a --format "{{.Names}} {{.Status}}"')
                        .output.decode("utf-8")
                        .splitlines()
                    )
                    # the following yields a list of lists in the form
                    # [['nginx', 'Up 2 days'], ['nextcloud', 'Up 2 days'], ...]
                    status["service_container"]["DinD Containers"] = [
                        *(s.split(" ", 1) for s in dind_containers_statuses)
                    ]
                    status["service_container"]["Environment"] = self._service_container.attrs["Config"]["Env"]
                else:
                    status["service_container"]["DinD Containers"] = []
                    status["service_container"]["Environment"] = []
            else:
                status["service_container"] = None
            if self._network:
                status["network"] = {
                    "Name": self._network.name,
                    "Short ID": self._network.short_id,
                    "Subnet": self._network.attrs["IPAM"]["Config"][0]["Subnet"],
                    "Gateway": self._network.attrs["IPAM"]["Config"][0]["Gateway"],
                }
            else:
                status["network"] = None
            status["mounts"] = []
            for mnt in self._mounts:
                mnt_status = {"Source": mnt["Source"], "Target": mnt["Target"]}
                if mnt["Type"] == "volume":
                    mnt_status["Type"] = "Docker volume"
                    mnt_status["Auto-remove"] = "yes"
                elif mnt["Type"] == "bind":
                    if mnt["Source"] + ":" + mnt["Target"] in self._bind_volumes:
                        mnt_status["Type"] = "Bind volume"
                        mnt_status["Auto-remove"] = "yes"
                    elif mnt["Source"] + ":" + mnt["Target"] in self._bind_mounts:
                        mnt_status["Type"] = "Bind mount"
                        mnt_status["Auto-remove"] = "no"
                    else:
                        raise Exception("Found untracked bind mount, this should not happen!")
                else:
                    raise Exception("Unhandled mount type, this should not happen!")
                status["mounts"].append(mnt_status)
        except docker.errors.DockerException as exc:
            raise DockerError("Error querying status from docker.") from exc
        return status

    def start(self, detach=True, remove=False):
        """Start the container of a DindBox that has previously been created or stopped.

        Args:
            detach (bool, optional): Start the DindBox and return immediately. Defaults to True. Set to False to
              obtain an interactive session. The CLI makes use of this, but you may also use it from iPython.
            remove (bool, optional): Automatically remove the DindBox once the interactive session ends. Only works
              with detach=False. Defaults to False.

        Returns:
            The exit code of the container (int), which is usually the exit code of the last executed command.
            None if detach=True.

        Raises:
            AutoRemoveNotPossible: When setting remove=True and detach=True simultaneously.
            DockerError: If any error occurs while interacting with docker.
            ContainerAlreadyRunning: If the build container of the DindBox is already running.
        """
        # Note that detach=False will give an interactive session. The CLI always uses this mode. It may be also
        # used from iPython, but when using programatically, it makes no sense, therfore the default is True.
        # Auto-remove only works when attached, otherwise we will not be running anymore when the container exits.
        if detach and remove:
            raise AutoRemoveNotPossible("Auto-remove is not possible with a detached session.")
        self._start_service_container()
        docker_exitcode = self._start_build_container(detach=detach, strict=True)
        if remove:
            # if the user just detached from the build container, we will not auto-remove it
            if is_running(self._build_container):
                logger.info("Build container is still running, will not auto-remove the DindBox.")
            else:
                logger.info("Build container exited. Auto-removing the DindBox...")
                self.remove(force=True)
        return docker_exitcode

    def stop(self):
        """Stop both the build and the service container.

        Raises:
            DockerError: If any error occurs while interacting with docker.
        """
        if self._build_container:
            self._stop_build_container()
        if self._service_container:
            self._stop_service_container()

    def remove(self, force=False):
        """Remove all entities associated to the DindBox (but not the object itself).

        This method aims to be tolerant towards an only partially-existing box and will remove all sub-parts
        individually, as far as possible. If both containers are missing, though, removal of networks and volumes
        can only be done based on name-matching, which might lead to unintended removal, if names match by accident.
        Therefore, removal for a box with no containers at all requires the force parameter to be set to True.

        Also, the method is not tolerant towards errors when interacting with the docker API - the first error occuring
        here will lead to a DockerError Exception being raised.

        Args:
            force (bool, optional): Remove even if one of the containers is still running, or, try to remove network
              and volumes even if both docker containers are missing. Defaults to False.

        Raises:
            DindBoxRunning: If trying to remove a running DindBox with force=False.
            ContainerNotFound: If both containers of the DindBox are missing and force=False.
            DockerError: If any error occurs while interacting with docker.
            UndefinedBindVolumeBasePath: If the base path for bind volumes cannot be automatically determined.
        """
        # Note on Exception handling: DockerErrors from methods like _stop_build_container() and
        # _remove_build_container() are not handled, since generally, the order of things here should
        # work, and if any of these calls fails, we can assume that something is generally wrong in our
        # interaction with docker - and as such ist makes no sense to continue.
        if not (self._build_container or self._service_container) and not force:
            raise ContainerNotFound(
                "Both containers of the DindBox are missing. You may use 'remove --force' to "
                + "remove volumes and network based on simple name matching, but be aware that this"
                + f" is dangerous, as it will simply remove everything starting with '{self._name }_'."
            )

        if self._build_container and is_running(self._build_container):
            if force:
                self._stop_build_container()
            else:
                raise DindBoxRunning("DindBox is still running. Stop it before removing or use --force.")
        if self._service_container and is_running(self._service_container):
            if not force:
                raise DindBoxRunning("DindBox is still running. Stop it before removing or use --force.")
            # will not stop  service container with --force, since we would restart it anyway in the next step
        self._remove_build_container()  # will fail if the build container is still running
        if self._service_container:
            try:
                self._restart_service_container_for_cleanup()  # will tolerate either running or stopped container
                self._remove_dind_containers()
                self._clean_bind_volumes()
            except DindBoxException as exc:
                logger.error("Error during clean-up within service container: %s", exc)
            finally:
                self._stop_service_container()
            self._remove_service_container()
        self._remove_invalid_var_lib_docker_volumes()
        self._remove_volumes()
        self._remove_network()
        # bind volumes go last, since they may raise a non-docker-related Exception
        self._remove_bind_volumes()

    def run(self, detach=True, remove=False):
        """Create and start a new DindBox in one step.

        Args:
            detach (bool, optional): Start the DindBox and return immediately. Defaults to True. Set to False to
              obtain an interactive session. The CLI makes use of this, but you may also use it from iPython.
            remove (bool, optional): Automatically remove the DindBox once the interactive session ends. Only works
              with detach=False. Defaults to False.

        Returns:
            The exit code of the container (int), which is usually the exit code of the last executed command.
            None if detach=True.

        Raises:
            AutoRemoveNotPossible: When setting remove=True and detach=True simultaneously.
            DindBoxCreationFailed: If any error occurs during the creation of the DindBox.
            DockerError: If any error occurs while interacting with docker.
        """
        # Note that detach=False will give an interactive session. The CLI always uses this mode. It may be also
        # used from iPython, but when using programatically, it makes no sense, therfore the default is False.
        # Auto-remove only works when attached, otherwise we will not be running anymore when the container exits.
        if detach and remove:
            raise AutoRemoveNotPossible("Auto-remove is not possible with a detached session.")
        self.create()
        docker_exitcode = self.start(detach=detach, remove=remove)
        return docker_exitcode

    def attach(self):
        """Attach to an interactive session with the build container of an existing DindBox.

        Raises:
            ContainerNotRunning: If any of the DindBox's containers is not running.
            DockerError: If any error occurs while interacting with docker.
        """
        if not is_running(self._service_container) or not is_running(self._build_container):
            raise ContainerNotRunning("Cannot attach to a stopped DindBox, start it first.")
        self._print("\nPress Ctrl+p>Ctrl+q to detach from the container and keep it running. Presss Ctrl+d to stop it.")
        self._print("\n+++ BEGIN BUILD CONTAINER OUTPUT (ATTACH) +++\n", color="BOLD_GREEN")
        try:
            subprocess.run("docker attach " + self._build_container.id, shell=True, check=True)
        except subprocess.CalledProcessError as exc:
            docker_exitcode = exc.returncode
            self._print(
                f"\n+++ END BUILD CONTAINER OUTPUT. EXIT CODE: {docker_exitcode} +++\n",
                color="BOLD_RED",
            )
        except Exception as exc:
            # re-raise all other kinds of exceptions as Docker error
            raise DockerError("Error while attaching to build container through docker CLI.") from exc
        else:
            docker_exitcode = 0
            self._print("\n+++ END BUILD CONTAINER OUTPUT +++\n", color="BOLD_GREEN")
        return docker_exitcode

    def exec(self, command, detach=True):
        """Run a command inside the build container

        Args:
            command (str): The command-line to execute
            detach (bool, optional): Detach from the container terminal. Defaults to True.
              Note that detach=False will give an interactive session. This is intended mainly for the CLI and usage
              in CI, so we get nice real-time command-line output. It may be also used from iPython, but when using
              programatically from other Python code, it makes no sense.

        Returns:
            The exit code of the command, or None if detach=True

        Raises:
            ContainerNotRunning: If one of the containers is not running.
            DockerError: If a docker-specific error occurs when trying to run the command.
        """
        if not (is_running(self._build_container) and is_running(self._build_container)):
            raise ContainerNotRunning(
                "At least one of the containers is not running. Start the DindBox before trying to execute a command."
            )
        logger.info("Running command '%s' within build container", command)
        if detach:
            try:
                self._build_container.exec_run(command, detach=True)
            except docker.errors.DockerException as exc:
                raise DockerError("Could not run command in build container") from exc
            # logger.info("Command '%s' returned exit code %d", command, result.exit_code)
            # logger.debug("+++ Command output: +++\n%s+++ End command output +++", result.output.decode("utf-8"))
            return None
        # attached mode
        self._print("\nPress Ctrl+p>Ctrl+q to detach from the container and keep the current command running.")
        self._print("\n+++ BEGIN BUILD CONTAINER OUTPUT +++\n", color="BOLD_GREEN")
        try:
            subprocess.run("docker exec -it " + self._build_container.id + " " + command, shell=True, check=True)
        except subprocess.CalledProcessError as exc:
            docker_exitcode = exc.returncode
            self._print(
                f"\n+++ END BUILD CONTAINER OUTPUT. COMMAND EXIT CODE: {docker_exitcode} +++\n",
                color="BOLD_RED",
            )
        except Exception as exc:
            # re-raise all other kinds of exceptions as Docker error
            raise DockerError("Error while executing command in attached mode through docker CLI.") from exc
        else:
            docker_exitcode = 0
            self._print("\n+++ END BUILD CONTAINER OUTPUT +++\n", color="BOLD_GREEN")
        return docker_exitcode

    def __get_container(self, container_type, error_if_not_found=False):
        """Return the container object for either service or build container.

        The container is identified via the naming convention, based on the name stored in the current object.

        Args:
            container_type (str): Either 'build' or 'service'
            error_if_not_found (bool, optional): Raise an error if the container cannot be found. Defaults to False.

        Raises:
            InvalidContainerType: If container_type is not a valid option.
            docker.errors.NotFound: If error_if_not_found=True and the container does not exist.
            DockerError: If any other error occurs while interacting with docker.

        Returns:
            container: The requested Container object.
        """
        if container_type == "build":
            container_name = self._name + self.BUILD_CONTAINER_SUFFIX
        elif container_type == "service":
            container_name = self._name + self.SERVICE_CONTAINER_SUFFIX
        else:
            raise InvalidContainerType("Valid types are 'build' and 'service'.")
        try:
            container = self.client.containers.get(container_name)
        except docker.errors.NotFound:
            if error_if_not_found:
                raise
            container = None
        except docker.errors.DockerException as exc:
            # All other docker exceptions will be transformed do DockerError.
            # DockerException is the super-class of docker.errors.NotFound, so order matters here.
            raise DockerError("message") from exc
        return container

    def __get_container_ip(self, container_type, error_if_not_found=False):
        """Return the container IP of either service or build container.

        Args:
            container_type (str): Either 'build' or 'service'
            error_if_not_found (bool, optional): Raise an execpetion if the container does not exist. Defaults to
              False.

        Raises:
            InvalidContainerType: If container_type is not a valid option.
            DockerError: If the container is not attached to the docker network or generally if any error occurs
              while interacting with docker.

        Returns:
            ip (str): The requested container IP, or None, if the container is not running or does not exist.
        """
        if container_type == "build":
            container = self._build_container
        elif container_type == "service":
            container = self._service_container
        else:
            raise InvalidContainerType("Valid types are 'build' and 'service'.")
        try:
            container.reload()
            self._network.reload()
            if container.status != "running":
                # if the container is not running, it is also not attached to the network and has no defined IP
                return None
        except docker.errors.DockerException as exc:
            raise DockerError("Error reloading container and network status.") from exc
        try:
            ip = self._network.attrs["Containers"][container.id]["IPv4Address"]
            return ip.split("/")[0]  # remove /16 subnet suffix
        except docker.errors.DockerException as exc:
            if error_if_not_found:
                raise DockerError("Container seems not to be attached to network") from exc
            return None

    def _create_or_find_network(self):
        """Create docker network for the DindBox containers ot identify an already existing one.

        If the docker_network parameter has been provided to the constructor, this method will look for a network
        under this name and connect to it. If it does not exist, it will be created. If docker_network has
        not been provided, the network name will be derived from the DindBox name. In this case however, the function
        will raise an Exception if a network under the default name already exists.

        Raises:
            DockerNetworkAlreadyExists: If a docker network under the same name already exists.
            DockerError: If any error occurs while interacting with docker.
        """
        if self.__create_data["docker_network"] is None:
            network_name = self._name + self.NETWORK_SUFFIX
        else:
            network_name = self.__create_data["docker_network"]
        matching_network = self._get_network_by_name(network_name, partial=True)
        if matching_network:
            if self.__create_data["docker_network"] is None:
                raise DockerNetworkAlreadyExists(
                    f"Network name {network_name} already exists. To connect to an existing network, you need to provide its name as docker_network parameter."
                )
            if self.__create_data["subnet"]:
                raise DockerNetworkAlreadyExists(
                    f"Network name {network_name} already exists. Providing an IP subnet specification is not possible when connecting to an existing network."
                )
            self._network = matching_network
            return
        # network does not exist yet
        logger.info("Creating docker network: %s", network_name)
        try:
            self._network = self.client.networks.create(network_name, driver="bridge", ipam=self._ipam_config())
        except docker.errors.DockerException as exc:
            raise DockerError("Error while creating docker network.") from exc

    def _ipam_config(self):
        if not self.__create_data["subnet"]:
            return None
        if not "/" in self.__create_data["subnet"]:  # netmask is missing, assume /24
            self.__create_data["subnet"] = self.__create_data["subnet"] + "/24"
        # check validity of subnet parameter, will throw paddress.AddressValueError or ValueError, if not
        ipnetwork = ipaddress.IPv4Network(self.__create_data["subnet"], strict=False)
        gateway = str(ipnetwork.network_address).rsplit(".", 1)[0] + ".1"
        ipam_pool = docker.types.IPAMPool(
            subnet=str(ipnetwork),
            gateway=gateway,
        )
        return docker.types.IPAMConfig(pool_configs=[ipam_pool])

    def _get_network_by_name(self, network_name, partial=False):
        """Get the docker network object from a network name

        Args:
            network_name (string): The name of the docker network to look for
            partial (bool,optional): Do not raise an error, but just return None if thedocker network does not exist.
                Defaults to False.

        Returns:
            docker.Network: The object associated with the respective docker network, or None if there is no network
                under the name network_name (and partial=True).

        Raises:
            docker.errors.NotFound: It the network does not exist and partial is False.
            DockerError: If any error occurs while interacting with docker.
        """
        try:
            matching_networks = self.client.networks.list(names=network_name)
        except docker.errors.DockerException as exc:
            raise DockerError("Error while listing docker networks.") from exc
        for net in matching_networks:
            if net.name == network_name:
                logger.info("Found network: %s", net.name)
                return net
        logger.info("Could not find network: %s", network_name)
        if not partial:
            raise docker.errors.NotFound(f"Could not find docker network {network_name}")
        return None

    def _recover_network(self, partial=False):
        """Recover the docker network object.

        This function will try to identify the docker network through the docker container. If they do not exist, it
        will fall back to identifying the networt from the DindBox name.

        Args:
            partial (bool,optional): Tolerate quietly if no docker network exists and thus allow recovery of a DinBox
              that has been only partially deleted or created. Defaults to False.

        Raises:
            docker.errors.NotFound: It the network does not exist and partial is False.
            DockerError: If any error occurs while interacting with docker.
        """
        if self._build_container:
            network_name = self._build_container.attrs["HostConfig"]["NetworkMode"]
        elif self._service_container:
            network_name = self._service_container.attrs["HostConfig"]["NetworkMode"]
        else:
            logger.warning("Both docker containers are missing. Looking for docker network by name pattern.")
            network_name = self._name + self.NETWORK_SUFFIX
        self._network = self._get_network_by_name(network_name, partial)

    def _remove_network(self):
        """Remove the private docker network of the two DindBox containers, if it exists.

        Will return without error, if no network object is referenced with the DindBox object.

        Raises:
            DockerError: If any error occurs while interacting with docker.
        """
        if self._network:
            try:
                logger.info("Removing docker network: %s", self._network.name)
                self._network.remove()
            except docker.errors.DockerException as exc:
                raise DockerError("Error while removing docker network.") from exc
            self._network = None

    def _is_a_bind_volume(self, mount):
        """Perform some safety and plausibility checks on a mount to make sure it really is a bind volume.

        Returns True if the mount is a bind volume.

        Args:
            mount: Either a string in the form SOURCE:TARGET or a Mount object. Alternatively, it may also be just
              the SOURCE path, with or without trailing ':'. In that case, checks are less thorough.

        Raises:
            UndefinedBindVolumeBasePath: If the base path for bind volumes cannot be automatically determined.
        """
        # First, check if the potential bind volume follows the expected naming convention
        if isinstance(mount, docker.types.Mount):
            source = mount["Source"]
            target = mount["Target"]
        elif mount.count(":") > 0:
            # if we have a SOURCE:TARGET string, we can determine the same information
            # (unless target is an empty string, which will be handled like the case below)
            [source, target] = mount.split(":")
        else:
            # if we only have the source path, we cannot know the target mount-point
            source = mount
            target = None

        volume_name = basename(normpath(source))

        if target:
            if volume_name != self._name + "_" + target[1:].replace("/", "-"):
                return False
        else:
            # If we do not know the target mount point, we can only check part of the naming convention.
            if not volume_name.startswith(self._name + "_"):
                return False
        # Then check if it is located in the expected host-side location.
        base_path = abspath(join(source, ".."))  # parent dir of host-side bind vol location
        if self._bind_volume_base_path:
            return bool(base_path == self._bind_volume_base_path)
        else:
            # If the bind-volume base path has not been explicitely set by the user, we have to guess it
            # We will guess from the first volume, but bail out if there are contradicting patterns
            if self.__assumed_bind_volume_base_path:
                if base_path == self.__assumed_bind_volume_base_path:
                    return True
                raise UndefinedBindVolumeBasePath(
                    "Bind volume base path is not configured and there are apparent "
                    + "bind-volumes with differing base paths. Explicitely provide a base path to resolve the situation."
                )
            else:
                # This is the first bind-volume we encounter and the base path is not set - derive the (assumed) base
                # path from this volume.
                self.__assumed_bind_volume_base_path = base_path
                # if the derived base path is identical to the default path, we can be confident that we guessed right
                # and take it over into the more trusted _bind_volume_base_path variable. The idea behind having two
                # variables is that we can act differently when deleting the bind-volumes, depending on how sure we
                # are that we identified them correctly. (Note though, that currently we always delete them.)
                if self.__assumed_bind_volume_base_path == self.DEFAULT_BIND_VOLUME_BASE_PATH:
                    # note that even this assumption can still be identified later, since
                    # __assumed_bind_volume_base_path is not None
                    self._bind_volume_base_path = self.DEFAULT_BIND_VOLUME_BASE_PATH
                    default_str = "(default)"
                else:
                    default_str = ""
                logger.info(
                    "Automatically detected bind volume base path is %s %s",
                    self.__assumed_bind_volume_base_path,
                    default_str,
                )
                return True

    def _recover_mounts(self):
        """Recover object information on all docker mounts for an already existing DindBox.

        This method recovers all three types of mounts: docker volumes, bind volumes, and bind mounts. It will try to
        find mounts through the two docker containers. If these do not exist, it will try to identify docker volumes
        and bind-volumes by name pattern.

        Raises:
            DockerError: If any error occurs while interacting with docker.
        """
        if self._service_container:
            mounts = self._service_container.attrs["Mounts"]
        elif self._build_container:
            mounts = self._build_container.attrs["Mounts"]
        else:
            mounts = None
            logger.warning("Both docker containers are missing. Looking for volumes and bind-volumes by name pattern.")
            self._recover_volumes_by_name()
            self._recover_bind_volumes_by_name()
            # bind-mounts need no recovering in that case, they are not defined if there is no container

        if mounts:
            for mnt in mounts:
                if mnt["Type"] == "volume":
                    logger.info("Found docker volume %s:%s", mnt["Name"], mnt["Destination"])
                    mount = docker.types.Mount(target=mnt["Destination"], source=mnt["Name"], type="volume")
                    self._mounts.append(mount)
                    # additionally, store docker object in _volumes array
                    self._volumes.append(self.client.volumes.get(mnt["Name"]))

                elif mnt["Type"] == "bind":
                    mount = docker.types.Mount(
                        target=mnt["Destination"],
                        source=mnt["Source"],
                        type="bind",
                        propagation=mnt["Propagation"],
                    )
                    self._mounts.append(mount)
                    # decide if this is a bind-volume or a bind-mount:
                    # - bind-volumes are auto-created and will be removed during teardown of the dindbox.
                    #   They reside in _bind_volume_base_path and follow a naming pattern just like docker volumes
                    # - bind-mounts are user-provided host directories that are mounted to the containers in the
                    #   same way, but they must NOT be removed at the end. Very important to not confuse the two!
                    try:
                        is_a_bind_volume = self._is_a_bind_volume(mount)
                    except UndefinedBindVolumeBasePath:
                        logger.error(
                            "For mount %s:%s it could not clearly be identified if it is a bind volume and it is therefore skipped. "
                            + "Explicitely specify the bind volume base path as an argument and try again.",
                            mnt["Source"],
                            mnt["Destination"],
                        )
                    if is_a_bind_volume:
                        logger.info(
                            "Found bind-volume (will auto-remove): %s:%s",
                            mnt["Source"],
                            mnt["Destination"],
                        )
                        # store host-side path in _bind_volumes array, which is used during removal
                        self._bind_volumes.append(mnt["Source"] + ":" + mnt["Destination"])
                    else:
                        logger.info("Found bind-mount %s:%s", mnt["Source"], mnt["Destination"])
                        # store host-side path in _bind_volumes array, which is used during removal
                        self._bind_mounts.append(mnt["Source"] + ":" + mnt["Destination"])

    def _create_volumes(self):
        """Create the docker volumes (but not bind mounts and bind volumes) for a new DindBox.

        Raises:
            VolumeAlreadyExists: If a volume of the same name already exists.
            DockerError: If any error occurs while interacting with docker.
        """
        for volpath in self.__create_data["volumes"]:
            logger.info("Creating docker volume for path: %s", volpath)
            # construct volume name. Ex.: for /var/log this gives "test-rig_var-log"
            volume_name = self.name + "_" + volpath[1:].replace("/", "-")
            # check if a volume of this name already exists (the create method will fail silently if so)
            try:
                matching_volumes = self.client.volumes.list(filters={"name": volume_name})
            except docker.errors.DockerException as exc:
                raise DockerError("Error listing docker volumes.") from exc
            for vol in matching_volumes:
                if vol.name == volume_name:
                    raise VolumeAlreadyExists("Volume " + volume_name + " already exists")
            try:
                self._volumes.append(self.client.volumes.create(volume_name))
            except docker.errors.DockerException as exc:
                raise DockerError("Error while creating volume.") from exc
            # add the volume to the mounts list, so it will be passed to containers on creation
            self._mounts.append(docker.types.Mount(target=volpath, source=volume_name, type="volume"))

    def _remove_volumes(self):
        """Remove the docker volumes (but not bind mounts and bind volumes) of the DindBox.

        Raises:
            DockerError: If any error occurs while interacting with docker.
        """
        for vol in self._volumes:
            logger.info("Removing docker volume: %s", vol.name)
            try:
                vol.remove()
            except docker.errors.DockerException as exc:
                raise DockerError("Error removing docker volume " + vol.name) from exc
        self._volumes = []

    def _recover_volumes_by_name(self):
        """Recover the docker volume objects of an existing DindBox, based on the naming scheme.

        Raises:
            DockerError: If any error occurs while interacting with docker.
        """
        try:
            self._volumes = self.client.volumes.list(filters={"name": self.name + "_"})
        except docker.errors.DockerException as exc:
            raise DockerError("Error while listing docker volumes.") from exc
        for vol in self._volumes:
            logger.info("Found docker volume: %s", vol.name)

    def _create_bind_volumes(self):
        """Create the bind volumes for a new DindBox."""
        # TODO: Transform or document Exceptions related to filesystem operations.
        # use default base path if not set by the user
        if self._bind_volume_base_path is None:
            self._bind_volume_base_path = self.DEFAULT_BIND_VOLUME_BASE_PATH
        # If necessary, create the base path where we store all bin-volumes
        if not os.path.exists(self._bind_volume_base_path):
            logger.info(
                "Creating global source directory for bind volumes: %s",
                self._bind_volume_base_path,
            )

            os.makedirs(self._bind_volume_base_path)
        # Add all bind-volumes to the mounts list. The propagation='rshared' arg will ensure that we can mount
        # filesystems within these bin-mounts, and they will propagate to and from containers
        for target in self.__create_data["bind_volumes"]:
            volume_name = self.name + "_" + target[1:].replace("/", "-")
            source = os.path.join(self._bind_volume_base_path, volume_name)
            logger.info("Creating bind volume host directory: %s", volume_name)
            os.makedirs(source)
            # _mounts is a list of Mount objects and only needed for container creation
            self._mounts.append(docker.types.Mount(target=target, source=source, type="bind", propagation="rshared"))
            # _bind_volumes is an array of the host-side source directories, needed during removal of the dindbox
            self._bind_volumes.append(source + ":" + target)

    def _clean_bind_volumes(self):
        """Clean the contents of all bind volumes, so they can later be removed without root privileges.

        Raises:
            ContainerNotFound: If the service container does not exist.
            ContainerNotRunning: If the service container is not running.
            DockerError: If cleaning the bind volumes from within the service container fails.
        """
        if not self._bind_volumes:
            logger.info("No bind-volumes present, nothing to clean up.")
            return
        if not self._service_container:
            raise ContainerNotFound("Service container not found, cannot clean bind volumes.")
        if not is_running(self._service_container):
            raise ContainerNotRunning("Service container is not running.")

        logger.info("Cleaning contents of bind-volumes from within service container:")
        for vol in self._bind_volumes:
            [source, target] = vol.split(":")
            # get the corresponding Mount object
            mount = next((mnt for mnt in self._mounts if mnt["Source"] == source), None)
            # make sure to not clean and regular bind-mounts (like /mnt which is by default mounting the user's
            # working directory). This is already made sure when constructing _bind_volumes, but we do check again
            # here, since the possible damage when doing it wrong is really grave
            if not self._is_a_bind_volume(mount):
                logger.warning(
                    "_bind_volumes entry %s failed to qualify as a bind-volume during clean-up. "
                    + "THIS IS A BUG AND SHOULD NOT BE HAPPENING!",
                    vol,
                )

            logger.info("  %s:%s", source, target)
            cmd = 'sh -c "rm -Rf ' + target + '/*"'
            try:
                result = self._service_container.exec_run(cmd)
            except docker.errors.DockerException as exc:
                raise DockerError("Could not clean bind-volume " + source) from exc
            if result.exit_code != 0:
                raise DockerError("Could not clean bind-volume " + source + result.output.decode("utf-8"))

    def _remove_bind_volumes(self):
        """Remove all bind volumes.

        Raises:
            UndefinedBindVolumeBasePath: If the base path for bind volumes cannot be automatically determined.
        """

        def error_handler(_, path, excinfo):
            print("Error while recursively deleting", path + ":")
            print("  ", excinfo)

        for vol in self._bind_volumes:
            if vol.count(":"):
                [source, _] = vol.split(":")
            else:
                source = vol
            if self._is_a_bind_volume(vol):
                logger.info("Removing bind-volume: %s", vol)
                shutil.rmtree(source, onerror=error_handler)
            else:
                logger.warning(
                    "_bind_volumes entry %s failed to qualify as a bind-volume during removal. "
                    + "THIS IS A BUG AND SHOULD NOT BE HAPPENING!",
                    vol,
                )

    def _recover_bind_volumes_by_name(self):
        """Recover the bind volumes of an existing DindBox, based on the naming scheme."""
        # use default base path if not set by the user
        if self._bind_volume_base_path is None:
            self._bind_volume_base_path = self.DEFAULT_BIND_VOLUME_BASE_PATH
        # find all subdirectories that match the dindbox name. Note that if a non-default base path was used
        # during creation of the dindbox, it needs to again be passed as arg to recover() for this to work.
        self._bind_volumes = glob(join(self._bind_volume_base_path, self.name + "_*"))
        # glob() returns a list of absolute paths as strings. Check if each of them is a directory and not a file
        for vol in self._bind_volumes:
            if not isdir(vol):
                self._bind_volumes.remove(vol)
            else:
                logger.info("Found bind-volume: %s", vol)

    def _create_bind_mounts(self):
        """Create the bind mounts for a new DindBox.

        Raises:
            InvalidBindMountName: When trying to bind-mount a directory, whose name begins with the DindBox name.
        """
        # Just like the bind-volumes above, this is a rshared bind mount - but different in that we're not mounting a
        # temporary dir created for that purpose, but the current working dir of the user
        if not self._bind_mounts:
            self._bind_mounts = [os.getcwd() + ":/mnt"]
        # Currently ,the current working dir will always be mounted to /mnt - there is no way for the user to change
        # it. However, the implementation here foresees a more flexible functionality already.
        # TODO: user-provided bind-mounts instead of just mounting CWD
        for mnt in self._bind_mounts:
            [source, target] = mnt.split(":")
            if source.startswith(self._name + "_"):
                raise InvalidBindMountName(
                    "You are trying to bind-mount a directory that starts with "
                    + self._name
                    + "_  This is identical to the naming convention for bind-volumes (which "
                    + "are automatically created and removed) and is not permitted."
                )
            self._mounts.append(docker.types.Mount(source=source, target=target, type="bind", propagation="rshared"))

    def _find_invalid_var_lib_docker_volumes(self):
        """Find docker volumes that are mounted to /var/lib/docke [sic!], so they can later be cleaned up.

        This is a workaround for https://github.com/docker/docker-py/issues/2973
        """
        if self._service_container:
            for mnt in self._service_container.attrs["Mounts"]:
                if mnt["Destination"] == "/var/lib/docke":  # sic!
                    self._invalid_var_lib_docker_volumes.append(self.client.volumes.get(mnt["Name"]))
        if self._build_container:
            for mnt in self._build_container.attrs["Mounts"]:
                if mnt["Destination"] == "/var/lib/docke":  # sic!
                    self._invalid_var_lib_docker_volumes.append(self.client.volumes.get(mnt["Name"]))
        for vol in self._invalid_var_lib_docker_volumes:
            logger.info("Found invalid /var/lib/docke [sic!] docker volume: %s", vol.name)

    def _remove_invalid_var_lib_docker_volumes(self):
        """Remove the docker volumes that were previously mounted to /var/lib/docke [sic!].

        This is a workaround for https://github.com/docker/docker-py/issues/2973
        """
        if len(self._invalid_var_lib_docker_volumes) > 0:
            for volume in self._invalid_var_lib_docker_volumes:
                logger.info(
                    "Removing invalid /var/lib/docke [sic!] docker volume: %s",
                    volume.name,
                )
                volume.remove()
            self._invalid_var_lib_docker_volumes = []

    def _pull_images(self):
        """Pull the docker images for build and service container.

        Raises:
            DockerError: If any error occurs while interacting with docker.
        """
        try:
            if self.__create_data["always_pull"] or not self.client.images.list(self._service_image):
                logger.info("Pulling service image: %s", self._service_image)
                self.client.images.pull(self._service_image)
            if self.__create_data["always_pull"] or not self.client.images.list(self._build_image):
                logger.info("Pulling build image: %s", self._build_image)
                self.client.images.pull(self._build_image)
        except docker.errors.DockerException as exc:
            raise DockerError("Error pulling docker image.") from exc

    def _create_service_container(self):
        """Create the service container, which will run the docker daemon of the DindBox.

        Raises:
            DockerError: If any error occurs while interacting with docker.
        """
        # TODO: actively configure IP address. (--ip=$SERVICE_IP) The way to do this seems to be to not require a
        #  network here, and instead use the Network.connect() method after container creation.
        service_container_name = self._name + self.SERVICE_CONTAINER_SUFFIX
        environment = self.__create_data["env_vars"] + [
            "DINDBOX=" + self._name,
            "DOCKER_TLS_CERTDIR=",
        ]

        logger.info("Creating service container: %s", service_container_name)
        try:
            self._service_container = self.client.containers.create(
                name=service_container_name,
                image=self._service_image,
                privileged=True,
                detach=True,
                environment=environment,
                network=self._network.name,
                mounts=self._mounts,
                # Map the gateway IP to an accessible name. This allows to reach the host OS, e.g. a local registry
                extra_hosts={
                    self.__create_data["host_network_name"]: self._network.attrs["IPAM"]["Config"][0]["Gateway"]
                },
                # The image entrypoint makes sure that the following will be passed to dockerd as options
                command="--storage-driver overlay2 --insecure-registry "
                + self.__create_data["host_network_name"]
                + ":5000",
            )
        except docker.errors.DockerException as exc:
            raise DockerError("Error creating service container.") from exc

    def _remove_service_container(self):
        """Remove the service container.

        Raises:
            DockerError: If any error occurs while interacting with docker.
        """
        if self._service_container:
            # Before we remove the service container, we need to clean out the contents of the bind volumes from
            # within it. Otherwise there may remain root-owned files in the bind-volumes, which we will not be abl
            # to remove at the end.
            logger.info("Removing service container: %s", self._service_container.name)
            try:
                self._service_container.remove()
            except docker.errors.DockerException as exc:
                raise DockerError("Error removing service container.") from exc
            self._service_container = None

    def _restart_service_container_for_cleanup(self):
        """Restart a stopped service container to allow clean-up of bind-volumes and dind containers.

        Will return without error if the container is already running.

        Raises:
            ContainerRestartFailed: If the service container cannot be restarted.
            DockerError: If any error occurs while interacting with docker.
        """
        if not is_running(self._service_container):
            logger.info("Restarting service container for clean-up...")
            try:
                self._service_container.start()
            except docker.errors.DockerException as exc:
                raise DockerError("Error while restarting service container.") from exc
            if not is_running(self._service_container, wait_seconds=5):
                raise ContainerRestartFailed("Failed to restart service container.")
        logger.info("Service container is up.")

    def _remove_dind_containers(self):
        """Stop and remove all docker-in-docker containers *inside* the DindBox.

        If these containers are not removed, they may block us from deleting the contents of the bind mounts or
          populate them again immediately after deletion.

        Raises:
            ContainerNotFound: If the service container does not exist.
            DockerInDockerError: If stopping and removing the dind containers fails.
            DockerError: If any error occurs while interacting with docker.
        """
        if not self._service_container:
            raise ContainerNotFound("Service container not found, no DIND containers to clean.")
        try:  # globally catch DockerExceptions from the following calls to Container.exec_run
            # Run docker ps inside the service container to find dind containers
            result = self._service_container.exec_run("docker ps -aq")
            if result.exit_code != 0:
                raise DockerInDockerError(
                    "Could not run docker ps within the service container: " + result.output.decode("utf-8")
                )
            container_list = result.output.decode("utf-8").splitlines()
            container_list_arg = result.output.decode("utf-8").replace("\n", " ")
            if not container_list:
                logger.info("No docker-in-docker containers running inside service container.")
                return
            logger.info(
                "Found %d docker-in-docker containers inside service container: %s",
                len(container_list),
                result.output.decode("utf-8"),
            )

            # stop the containers
            logger.info("Stopping all docker-in-docker containers inside service container...")
            result = self._service_container.exec_run("docker stop " + container_list_arg)
            if result.exit_code != 0:
                raise DockerInDockerError("Could not stop all containers: " + result.output.decode("utf-8"))

            # remove the containers
            logger.info("Removing all docker-in-docker containers inside service container...")
            result = self._service_container.exec_run("docker stop " + container_list_arg)
            if result.exit_code != 0:
                raise DockerInDockerError("Could not remove containers: " + result.output.decode("utf-8"))
        except docker.errors.DockerException as exc:
            raise DockerError("Error while removing docker-in-docker containers.") from exc

    def _start_service_container(self, strict=False):
        """Start the service container.

        Args:
            strict (bool, optional): Raise an error if the container is already running. Defaults to False.

        Raises:
            ContainerAlreadyRunning: If the service container is already running.
            DockerError: If any error occurs while interacting with docker.
        """
        if is_running(self._service_container) and strict:
            raise ContainerAlreadyRunning("Service container is already running.")
        logger.info("Starting service container: %s", self._service_container.name)
        try:
            self._service_container.start()
        except docker.errors.DockerException as exc:
            raise DockerError("Error starting service container.") from exc

    def _stop_service_container(self):
        """Stop the service container.

        Raises:
            DockerError: If any error occurs while interacting with docker.
        """
        logger.info("Stopping service container: %s", self._service_container.name)
        try:
            self._service_container.stop()
        except docker.errors.DockerException as exc:
            raise DockerError("Error stopping service container.") from exc

    def _create_build_container(self):
        """Create the build container, in which the user will run their program or interactive shell.

        Raises:
            DockerError: If any error occurs while interacting with docker.
        """
        # TODO: actively configure IP address (see above)
        # TODO: check if this container can be unprivileged?
        build_container_name = self._name + self.BUILD_CONTAINER_SUFFIX
        logger.info("Creating build container: %s", build_container_name)
        environment = self.__create_data["env_vars"] + [
            "DINDBOX=" + self._name,
            "SERVICE_CONTAINER=" + self._service_container.name,
            "DOCKER_HOST=tcp://" + self._service_container.name + ":2375",
        ]
        if self.__create_data["fancy_prompt"]:
            environment += ["PS1=" + self.PROMPT_STRING]  # this will only have an effect for non-bash shell images
        if self.__create_data["cmd"]:
            command = self.__create_data["shell"] + ' -c "' + self.__create_data["cmd"] + '"'
            # Having No tty is required for execution within gitlab-CI. It also seems to work well locally when
            # running a command with -c. At least, interactive prompts seems to work. If this creates problems in
            # some specific case, we might need to differentiate between CI execution and local exectution with -c
            # parameter.
            tty = False
        else:
            command = None
            tty = True
        # The detach parameter of Container.create() or run() is not equivalent to attaching/detaching in the CLI:
        #  First of all, detach=False will only work with run(), although the docs say differently.
        #  And, it will have the effect that the call to run() is blocking, and will return the shell output instead
        #  of the container object, but only after the CMD has finished. In contrary to the CLI, it is not meant to
        #  provide an interactively session attached to a container. Therefore, we always pass detach=True, and
        #  - if requested - attach to the container through the docker CLI in subprocess calls (see attach(), start(),
        #  and run() methods of this class).
        detach = True
        try:
            self._build_container = self.client.containers.create(
                name=build_container_name,
                image=self._build_image,
                privileged=True,
                detach=detach,
                tty=tty,
                stdin_open=True,  # equivalent to -i in docker CLI
                environment=environment,
                network=self._network.name,
                mounts=self._mounts,
                # Map the gateway IP to an accessible name. This allows to reach the host OS, e.g. a local registry
                extra_hosts={
                    self.__create_data["host_network_name"]: self._network.attrs["IPAM"]["Config"][0]["Gateway"]
                },
                working_dir="/mnt",  #  start in /mnt where the outside cwd is mounted
                command=command,
            )
        except docker.errors.DockerException as exc:
            raise DockerError("Error creating build container.") from exc
        # debian/ubuntu-based images usually use bash as interactive shell, alpine-based images use sh.
        # For bash, we cannot modify the prompt by simply setting the PS1 env variable, it will be overwritten by the
        # contents of ~/.bashrc or /etc/profile. In order to still modify the prompt, we need to amend .bashrc
        # This can be done even before the container is started the fist time.
        if self.__create_data["fancy_prompt"] and "bash" in self.__create_data["shell"]:
            self._patch_bashrc()

    def _remove_build_container(self):
        """Remove the build container.

        Raises:
            DockerError: If any error occurs while interacting with docker.
        """
        if self._build_container:
            logger.info("Removing build container: %s", self._build_container.name)
            try:
                self._build_container.remove()
            except docker.errors.DockerException as exc:
                raise DockerError("Error removing build container.") from exc
            self._build_container = None

    def _start_build_container(self, detach=True, strict=False):
        """Start the build container.

        Args:
            detach (bool, optional): Detach from the container terminal. Defaults to True.
              Note that detach=False will give an interactive session. This is intended mainly for the CLI and usage
              in CI, so we get nice real-time command-line output. It may be also used from iPython, but when using
              programatically from other Python code, it makes no sense.
            strict (bool, optional): Raise an error if the container is already running. Defaults to False.

        Returns:
            The exit code of the container (int), which is usually the exit code of the last executed command.
            None if detach=True.

        Raises:
            ContainerAlreadyRunning: If the build container is already running.
            ContainerNotRunning: If the corresponding service container is not running.
            DockerError: If any error occurs while interacting with docker.
        """
        if is_running(self._build_container) and strict:
            raise ContainerAlreadyRunning("Cannot start build container, it is already running.")
        if not is_running(self._service_container):
            raise ContainerNotRunning("Cannot start build container without running service container.")
        logger.info("Starting build container: %s", self._build_container.name)

        if detach:
            try:
                self._build_container.start()
            except docker.errors.DockerException as exc:
                raise DockerError("Error while starting build container in detached mode.") from exc
            return None

        # attached mode
        self._print("\nPress Ctrl+p>Ctrl+q to detach from the container and keep it running. Presss Ctrl+d to stop it.")
        self._print("\n+++ BEGIN BUILD CONTAINER OUTPUT +++\n", color="BOLD_GREEN")
        try:
            subprocess.run("docker start -ai " + self._build_container.id, shell=True, check=True)
        except subprocess.CalledProcessError as exc:
            docker_exitcode = exc.returncode
            self._print(
                f"\n+++ END BUILD CONTAINER OUTPUT. EXIT CODE: {docker_exitcode} +++\n",
                color="BOLD_RED",
            )
        except Exception as exc:
            # re-raise all other kinds of exceptions as Docker error
            raise DockerError("Error while starting build container in attached mode through docker CLI.") from exc
        else:
            docker_exitcode = 0
            self._print("\n+++ END BUILD CONTAINER OUTPUT +++\n", color="BOLD_GREEN")
        return docker_exitcode

    def _stop_build_container(self):
        """Stop the build container.

        Raises:
            DockerError: If any error occurs while interacting with docker.
        """
        logger.info("Stopping build container: %s", self._build_container.name)
        try:
            self._build_container.stop()
        except docker.errors.DockerException as exc:
            raise DockerError("Error while stopping build container.") from exc

    def _recover_containers(self, partial=False):
        """Recover the container objects for already existing service and build containers.

        Args:
            partial (bool, optional): Tolerate quietly if one or both containers do not exist and thus allow recovery
              of a DinBox that has been only partially deleted or created. Defaults to False.

        Raises:
            docker.errors.NotFound: If partial=False and at least one of the containers does not exist.
            DockerError: If any error occurs while interacting with docker.
        """
        self._service_container = self.__get_container("service", error_if_not_found=not partial)
        if self._service_container:
            logger.info("Found service container: %s", self._service_container.name)
            self._service_image = self._service_container.image.tags[0]
        self._build_container = self.__get_container("build", error_if_not_found=not partial)
        if self._build_container:
            logger.info("Found build container: %s", self._build_container.name)
            self._build_image = self._build_container.image.tags[0]

    def _patch_bashrc(self):
        """Patch the global .bashrc file of the build container to set a nice prompt.

        Raises:
            DockerError: If any error occurs while interacting with docker.
        """
        # TODO: document (or catch?) exceptions caused by filesystem access (missing right etc.)
        logger.info("Patching .bashrc to set dindbox prompt...")
        tmp_dir = tempfile.mkdtemp()
        logger.info("Using temporary directory: %s", tmp_dir)
        filename = ".bashrc"
        tmp_file = join(tmp_dir, filename)
        container = self._build_container
        get_file(container, "/root/.bashrc", tmp_dir)
        with open(
            tmp_file,
            "a",
            encoding="utf-8",
        ) as file:  # append mode
            file.write('PS1="' + self.PROMPT_STRING + '"')
        put_file(container, tmp_file, "/root/")
        os.remove(tmp_file)
        os.rmdir(tmp_dir)

    def _print(self, *args, color=None):
        """Print command line output.

        This is currently a stub. In a later version, it is supposed to support different debug levels, more colors,
        and maybe logging to a file.

        Args:
            *args: An arbitrary number of arguments that will be passed on to Python's print function.
            color (str, optional): Print text in a non-default color. If using this argument, you must not include
                the 'end' argument as part of *args. Currently supported values for color are:
                BOLD_GREEN, BOLD_RED
        """
        colors = {}
        colors["NORMAL"] = "\033[0m"
        colors["BOLD_GREEN"] = "\033[32m"
        colors["BOLD_RED"] = "\033[31m"

        if color is None:
            print(*args)
        else:
            print(colors[color.upper()], end="")
            print(*args, end="")
            print(colors["NORMAL"])

    # getter methods for properties which should be accessible, but read-only
    @property
    def name(self):
        """The name of the DindBox, acts as a unique identifies and as namespace for all related entities."""
        return self._name

    @property
    def network(self):
        """The docker network object used to connect build and service container."""
        return self._network

    @property
    def volumes(self):
        """A list of the docker volumes which are mounted to both build and service container."""
        return self._volumes

    @property
    def bind_volumes(self):
        """List of volume-like host directories which are are mounted to both containers. These directories are
        created specifically for one DindBox and will be removed once the DindBox is removed.
        """
        return self._bind_volumes

    @property
    def bind_mounts(self):
        """List of pre-existing host directories which are mounted to both containers. In contrary to bind_volumes,
        these will not be removed together with the DindBox."""
        return self._bind_mounts

    @property
    def build_container(self):
        """The build container object."""
        return self._build_container

    @property
    def service_container(self):
        """The service container object."""
        return self._service_container

    @property
    def build_image(self):
        """The docker image used by the build container."""
        return self._build_image

    @property
    def service_image(self):
        """The docker image used by the service container."""
        return self._service_image
