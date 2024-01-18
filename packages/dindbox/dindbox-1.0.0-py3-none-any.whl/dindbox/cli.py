"""The command line interface for this package. Intended to be used through the shell script wrapper."""
# pylint: disable=fixme

from os import isatty
from pathlib import Path
import re
import sys
import logging
import subprocess
import configargparse

from .box import DindBox
from .status_screen import show_status_screen

logger = logging.getLogger("dindbox.cli")
logging.basicConfig()

# config file names to look for in the current folder and all parent folders
PARENT_DIR_CONFIG_FILES = ["pyproject.toml"]
# config files to look for in the current folder only
CURRENT_DIR_CONFIG_FILES = ["dindbox.conf"]


def main():
    """Entrypoint function, called by the poetry script of this package, and when executing this file as a module."""
    config_files = _find_default_config_files()
    # parse once, but only to retrieve log level and custom config file
    args = _parse_args(config_files)
    _set_log_level(args.log_level)
    config_files = _add_custom_config_file(args.config_file, config_files)
    # parse again, now with custom config files (-c) added to the default config file list, so they will also be
    # considered in the sub-parsers (ConfigArgParse lacks support for this, so we work around it)
    args = _parse_args(config_files)
    _log_debug_messages(args, config_files)
    # Call the appropriate function for the provided command
    #  vars(args) will transform the namespace object into a dict. The ** will expand it into keyword-arguments
    args.func(**vars(args))


def _find_default_config_files():
    config_files = []
    for filename in PARENT_DIR_CONFIG_FILES:
        cwd_with_parents = [Path.cwd()]
        cwd_with_parents.extend(Path.cwd().parents)
        for dir in cwd_with_parents:
            file = dir / filename
            if file.is_file():
                config_files.append(str(file))
                break
    for filename in CURRENT_DIR_CONFIG_FILES:
        if Path(filename).is_file():
            config_files.append(filename)
    return config_files


def _parse_args(config_files):
    """Parse the command line arguments and any provided config files.

    Returns a namespace of all arguments, containing the parsed argument values, and defaults for all other arguments.
    """
    parser = _create_parser(config_files)
    return parser.parse_args()


def _create_parser(config_files):
    parser = configargparse.ArgumentParser(
        description="Lightweight, docker-capable virtual testing environment.",
        default_config_files=config_files,
        config_file_parser_class=configargparse.TomlConfigParser(["dindbox.global", "tool.dindbox.global"]),
    )
    parser = _add_toplevel_arguments(parser)
    parser = _add_all_command_subparsers(parser, config_files)
    return parser


def _log_debug_messages(args, config_files):
    logger.debug("Command line arguments: %s", str(sys.argv))
    logger.debug("Using config files: %s", str(config_files))
    logger.debug("Parsed arguments: %s", str(args))


def _add_custom_config_file(custom_config_file, config_files):
    if custom_config_file:
        if not Path(custom_config_file).is_file():
            raise FileNotFoundError(f"Config file {custom_config_file} does not exist")
        config_files.append(custom_config_file)
    return config_files


def _add_toplevel_arguments(parser):
    parser.add_argument(
        "-c",
        "--config-file",
        is_config_file=False,  # we're not using ConfigArgParse's built-in support for config file arguments
        help="A config file from which to read command-line options, in addition to any existing default "
        + "config files.",
        default=None,
    )
    parser.add_argument(
        "-l",
        "--log-level",
        help="Log level. One of DEBUG, INFO, WARNING, or ERROR. Defaults to %(default)s.",
        default="INFO",
    )
    parser.add_argument(
        "-p",
        "--bind-volume-base-path",
        metavar="BIND_VOL_BASE_PATH",
        help="Directory where bind-mount volumes are created on the host. "
        + "If you are using bind volumes, and you plan to re-use a dindbox across reboots, change this to a location "
        + "outside the /tmp folder. When using a non-default path, it is enough to provide this "
        + "argument with COMMAND=create|run. Further COMMANDs should be able to identify the path automatically. "
        + "However, you can provide this argument with every COMMAND, and it will be considered. Default: "
        + DindBox.DEFAULT_BIND_VOLUME_BASE_PATH,
    )
    parser.add_argument(
        "name",
        nargs="?",
        default="dindbox",
        metavar="BOX_NAME",
        help="Name of the dindbox that should be created or modified. Defaults to '%(default)s', if omitted. For the "
        + "'get' and 'exec' commands, this is a mandatory argument.",
    )
    return parser


def _add_all_command_subparsers(parser, config_files):
    subparser_adder = parser.add_subparsers(
        dest="command",
        required=True,
        metavar="COMMAND",
        title="Available commands",
        description="Run %(prog)s COMMAND -h for help on each command.",
        parser_class=configargparse.ArgParser,
    )
    subparser_parents = _create_subparser_parents()

    def _add_command_subparser(command, help, parents=None):
        if parents is None:
            parents = []
        subparser = subparser_adder.add_parser(
            command,
            help=help,
            parents=parents,
            default_config_files=config_files,
            config_file_parser_class=configargparse.TomlConfigParser([f"dindbox.{command}", f"tool.dindbox.{command}"]),
            # TODO: Monitor this issue to check if a solution is provided by ConfigArgParse for using the global config
            #        file within subparsers: https://github.com/bw2/ConfigArgParse/issues/131
        )
        # the following sets the function from this file, whose name is identical to command (e.g. "run") as action for
        # this subcommand
        subparser.set_defaults(func=globals()[command])
        return subparser

    # Sub-parsers for the different commands
    subparsers = {}
    subparsers["run"] = _add_command_subparser(
        "run",
        help="Create and start a new DindBox",
        parents=[subparser_parents["run_create"], subparser_parents["run_start"]],
    )
    subparsers["create"] = _add_command_subparser(
        "create",
        help="Create a new DindBox, but do not start it yet",
        parents=[subparser_parents["run_create"]],
    )
    subparsers["start"] = _add_command_subparser(
        "start",
        help="Start a previously created DindBox",
        parents=[subparser_parents["run_start"]],
    )
    subparsers["stop"] = _add_command_subparser(
        "stop",
        help="Stop a running DindBox",
    )
    subparsers["remove"] = _add_command_subparser(
        "remove",
        help="Remove an existing DindBox (needs to be stopped first)",
        parents=[subparser_parents["remove"]],
    )
    subparsers["status"] = _add_command_subparser(
        "status",
        help="Show the status screen for an existing DindBox",
    )
    subparsers["attach"] = _add_command_subparser(
        "attach",
        help="Attach to a console session for an existing DindBox",
    )
    subparsers["exec"] = _add_command_subparser(
        "exec",
        help="Execute a single command within a running DindBox",
        parents=[subparser_parents["exec"]],
    )

    def property_string(arg):
        pattern = r"^([^.\s]*)\.([^.\s]*)$"
        match = re.match(pattern, arg)
        if not match:
            print("Property needs to be in the format entity.property")
            raise ValueError()
        entity = match.group(1)
        property = match.group(2)
        return (entity, property)

    subparsers["get"] = _add_command_subparser(
        "get",
        parents=[],
        help="Query various details about an existing DindBox",
    )
    subparsers["get"].add_argument(
        "property",
        type=property_string,
        metavar="ENTITY.PROPERTY",
        help="The property to be queried, e.g. 'network.name' for the name of the docker network associated with the "
        + "DindBox.",
    )
    return parser


def _create_subparser_parents():
    # subparser_parents contains parsers with shared options of multiple sub-parsers. They are not intended to be
    # used directly, just as parents= argument to the actual subparsers further below.
    subparser_parents = dict()
    subparser_parents["run_create"] = configargparse.ArgumentParser(add_help=False)
    subparser_parents["run_create"].add_argument(
        "-i",
        "--build-image",
        metavar="BUILD_IMAGE",
        default="docker:latest",
        help="Docker image to use for the build container. Default: %(default)s",
    )
    subparser_parents["run_create"].add_argument(
        "-I",
        "--service-image",
        metavar="SERVICE_IMAGE",
        default="docker:dind",
        help="Docker image to use for the service container. Default: %(default)s",
    )
    subparser_parents["run_create"].add_argument(
        "-v",
        "--volumes",
        nargs="+",
        metavar="VOLUME",
        default=["/var/lib/docker", "/etc/buddyboxx"],
        help="Mount a docker volume to the the in-container directory VOLUME_PATH of both build and service "
        + "container. The volume will be shared across both containers. Defaults: %(default)s",
    )
    subparser_parents["run_create"].add_argument(
        "-b",
        "--bind-volumes",
        nargs="+",
        metavar="BIND_VOLUME",
        default=["/srv"],
        help="Bind-mount a temporary host directory to the in-container directory BIND_VOLUME of both build and "
        + "service container. Similar to -v, but uses a plain host directory instead of a docker volume. Uses shared "
        + "propagation in order to allow mounting a FUSE filesystems inside. Default: %(default)s",
    )
    subparser_parents["run_create"].add_argument(
        "-o",
        "--host-network-name",
        metavar="HOSTOSNAME",
        default="docker.buddyboxx",
        help="Hostname under which to reach the host operating system. Default: %(default)s",
    )
    subparser_parents["run_create"].add_argument(
        "--docker-network",
        "--net",
        metavar="DOCKER_NETWORK",
        default=None,
        help="Connect to an already existing docker network instead of creating a dedicated new network.",
    )
    subparser_parents["run_create"].add_argument(
        "--subnet",
        metavar="SUBNET",
        default=None,
        help="IPv4 subnet to use for the docker network, in CIDR notation. Will be randomly selected by the docker deaemon, if not provided.",
    )
    subparser_parents["run_create"].add_argument(
        "-e",
        "--env-vars",
        nargs="+",
        metavar="VAR[=VALUE]",
        default=["DEBUG"],
        help="Specify environment variables which will be set inside the build container. If VALUE is not "
        + "provided, the variable will be inherited from the current shell, but only if it is actually defined there."
        + " Default: %(default)s",
    )
    subparser_parents["run_create"].add_argument(
        "-c",
        "--cmd",
        metavar="CMD",
        default=None,
        help='Run CMD within the build container. Enclose in "..." and use && and/or ; to concatenate multiple '
        + "commands. Most containers (debian, alpine, ...) will return the last command's exit code and DindBox "
        + 'will forward that exit code as well. Note that using this option makes the DindBox "single use": it will '
        + "exit after CMD has completed. If started again, CMD will be executed again. If you want to run multiple "
        + "shell commands inside a detached DindBox, you should use the 'exec' command instead."
        + "If this option is not provided, the normal entrypoint of the build container will run, which is usually an "
        + "interactive shell.",
    )
    subparser_parents["run_create"].add_argument(
        "-a",
        "--always-pull",
        action="store_true",
        help="Always pull images, even if they are already available locally. Can be used to make sure to always "
        + "use the latest version of images, but will slow down startup of the dindbox.",
    )
    subparser_parents["run_create"].add_argument(
        "-S",
        "--shell",
        metavar="SHELL",
        default=None,
        help='Set the shell in which to run COMMAND. Defaults to "bash" for debian/ubuntu, and "sh" otherwise.',
    )
    subparser_parents["run_create"].add_argument(
        "--no-fancy-prompt",
        action="store_false",
        dest="fancy_prompt",
        help="Do not modify the shell prompt within the build container.",
    )
    subparser_parents["run_create"].add_argument(
        "--no-status-screen",
        action="store_false",
        dest="show_status_screen",
        help="Do not automatically open a separate shell window with the status screen.",
    )
    subparser_parents["run_start"] = configargparse.ArgumentParser(add_help=False)
    run_start_mutually_exclusive = subparser_parents["run_start"].add_mutually_exclusive_group()
    run_start_mutually_exclusive.add_argument(
        "-d",
        "--detach",
        action="store_true",
        help="Do not attach to the container, but start it in the background. You may later attach to it with the "
        + "'attach' command.",
    )
    run_start_mutually_exclusive.add_argument(
        "--rm",
        action="store_true",
        dest="remove",
        help="Remove the DindBox immediately after the build container has been stopped (e.g. by exiting from its "
        + "shell), even if the service container is still running. Note that this will not work if you detach and "
        + "re-attach to the container.",
    )
    subparser_parents["remove"] = configargparse.ArgumentParser(add_help=False)
    subparser_parents["remove"].add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Remove even if the containers are still running.",
    )
    subparser_parents["exec"] = configargparse.ArgumentParser(add_help=False)
    subparser_parents["exec"].add_argument(
        "command",
        metavar="COMMAND",
        help='The command to be run. Enclose in quotes (") if it contains spaces. The exit code of the command will be '
        + "returned.",
    )
    subparser_parents["exec"].add_argument(
        "-d",
        "--detach",
        action="store_true",
        help="Do not attach to the container, run COMMAND in the background.",
    )
    return subparser_parents


def _set_log_level(log_level):
    """Set the logging level according to ehe log_level argument"""
    numeric_log_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_log_level, int):
        raise ValueError("Invalid log level: %s" % log_level)
    package_logger = logging.getLogger(__package__)
    package_logger.setLevel(numeric_log_level)
    logger.debug("Set log level to: %s", log_level.upper())


def show_status_screen_if_interactive(box):
    """Open separate x-terminal window, displaying the status screen for the dindbox, if running in interactive shell.

    Will only work on debian-based systems.
    """
    if isatty(sys.stdout.fileno()) and Path("/etc/alternatives/x-terminal-emulator").is_file():
        logger.info("Launching status screen")
        subprocess.Popen(["x-terminal-emulator", "-e", "dindbox", box.name, "status"])


# One of the following handler functions is called from main(), based on what is set in .set_defaults(func=...)


def run(**kwargs):
    """CLI handler for the run command."""
    box = DindBox(**kwargs)
    if kwargs["show_status_screen"]:
        show_status_screen_if_interactive(box)
    exitcode = box.run(detach=kwargs["detach"], remove=kwargs["remove"])
    sys.exit(exitcode)


def create(**kwargs):
    """CLI handler for the create command."""
    box = DindBox(**kwargs)
    box.create()
    if kwargs["show_status_screen"]:
        show_status_screen_if_interactive(box)


def start(**kwargs):
    """CLI handler for the start command."""
    box = DindBox.recover(kwargs["name"])
    exitcode = box.start(detach=kwargs["detach"], remove=kwargs["remove"])
    sys.exit(exitcode)


def stop(**kwargs):
    """CLI handler for the stop command."""
    box = DindBox.recover(kwargs["name"], partial=True)
    box.stop()


def remove(**kwargs):
    """CLI handler for the remove command."""
    box = DindBox.recover(kwargs["name"], partial=True)
    box.remove(force=kwargs["force"])


def status(**kwargs):
    """CLI handler for the status command."""
    box = DindBox.recover(kwargs["name"], partial=True)
    show_status_screen(box)


def attach(**kwargs):
    """CLI handler for the attach command."""
    box = DindBox.recover(kwargs["name"])
    box.attach()


def exec(**kwargs):
    """CLI handler for the exec command."""
    box = DindBox.recover(kwargs["name"])
    exitcode = box.exec(command=kwargs["command"], detach=kwargs["detach"])
    sys.exit(exitcode)


def get(**kwargs):
    """CLI handler for the get command."""
    entity = kwargs["property"][0]
    property = kwargs["property"][1]
    box = DindBox.recover(kwargs["name"], partial=True)
    logger.debug("Querying {}.{}.{}".format(kwargs["name"], entity, property))
    box_status = box.status()

    if not entity in box_status.keys():
        raise ValueError(f"Invalid entity. Supported entities are {list(box_status.keys())}")

    # to find the right entry in the status dicts, we need to match keys unsensitive and also match underscore to space
    # e.g. an arg of build_container.short_id should retrieve status["build_container"]["Short ID"]
    def find_property_key(prop, status_dict):
        for k in status_dict.keys():
            if k.lower().replace(" ", "_") == prop.lower():
                return k
        return None

    property_key = find_property_key(property, box_status[entity])
    if not property_key:
        normalized_properties = [k.lower().replace(" ", "_") for k in box_status[entity].keys()]
        raise ValueError(f"Invalid property for entity {entity}. Supported properties are {normalized_properties}")

    print(box_status[entity][property_key])


if __name__ == "__main__":
    main()
