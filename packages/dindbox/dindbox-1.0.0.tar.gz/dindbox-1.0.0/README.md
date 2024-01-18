dindbox
=======

Lightweight, docker-capable virtual testing environment.

DindBox creates virtual testing environments, each comprising two docker containers. These function like lightweight
virtual machines, allowing for the creation and operation of docker containers within them without affecting
the host system's main docker daemon. This "docker-in-docker" principle, used by CI platforms like GitLab CI or GitHub
Actions, enables docker capability within a containerized runner. DindBox offers this setup for local testing and
prototyping, and can also be used in a CI context with a dedicated runner.

Installation
-----------

Dindbox only runs on Linux-based systems. It requires a Python version >= 3.10, a running docker server, and an
installation of the Docker CLI.

Dindbox is mostly intended to be used as a command-line tool. For this use case, it is recommended to install it via
pipx in order to make it available globally but keep its dependencies within a separated environment:

```sh
python3 -m pip install --user pipx
python3 -m pipx ensurepath
pipx install dindbox
```

If you however do plan to use dindbox as a python library (see below), simply run `pip install dindbox` within the
virtual environment of your project.

Usage
----

All commands and options are documented in detail in the command-line help. Run `dindbox -h` for a list of available
commands, and `dindbox COMMAND -h` for help on each command.

The most basic use case is to directly start an interactive session:  
`dindbox my_box run`  
Where `my_box` is the name of your dindbox which you can re-use in further commands to interact with it. The `run`
command without further parameters will give you an Alpine Linux based environment, with a fully functional docker
client & daemon - encapsulated within docker containers themselves (docker-in-docker). The container containing the
docker daemon is referred to as *service container*. The container with which you're interacting, which contains the
docker client is referred to as *build container*.

If you are on an ubuntu-based system, `run` will also open a status screen in a separate console window. You may close
this status screen at any time, it is only for monitoring purposes. Also, you can reopen it at any time running 
`dindbox my_box status` from a separate shell window.

If you'd rather use an ubuntu image, do something like the following to change the default build container image:  
`dindbox my_box run -i ubuntu:focal`  
Note that in this case you will need to manually install the docker **client**, since it is not part of the ubuntu
image. The docker daemon however, will already be available, since it runs inside the service container.

Note that you may also replace the service container's image (using `-I`). Normally, it should always be a `dind`
tag of the official docker image, but you can use this to test with different versions of docker, for example.
Nevertheless, other use cases are possible, too, like running a SQL server is in the service image, and the client in
the build image.

When you're done, you should always clean up boxes which you do not need anymore. In order to remove all docker entities
associated with your dindbox, run:  
`dindbox my_box remove`  
Or, if you know it is a throw-away box, directly append `--rm` to the `run` command for automatic cleanup after exiting.

For further commands, check out the command-line help. Note that `run` is a shortcut for `create` + `start` + `attach`.
Only in special cases it makes sense to use these commands individually, for the most part you should be fine with
`run`.

Config file
----------

All command-line parameters can also be set through a config file, so you do not have to re-type them every time.  Note
that config file settings only affect CLI usage. They have **no** effect at all when using dindbox as a Python library.

### Config file locations

Dindbox will look for a config file in three locations:

* First, it will traverse the directory structure upwards, starting with the current directory and looking for a
  `pyproject.toml` file, as is usually present within a poetry environment. Any sections within that file of the format
  `[tool.dindbox.*]` will be considered (see below for exact format).
* Next, any file in the *current directory* of name `dindbox.conf` will be parsed.
* Lastly, a config file specified with the  `--config-file` or `-c` command-line argument will be parsed.

Config files will be parsed in the order specified above. Duplicate options provided in a later config file will
override values from previous config files. Additionally, a command-line parameter will always override a value set in
any of the config files.

### Config file format

Config files need to be in the TOML format. Arguments to each `dindbox` command are specified in a section named
`[dindbox.COMMAND]`, where `COMMAND` is the name of the command, e.g. `run`. The section name is case-sensitive.
Additionally, global arguments (the ones provided before a command and listed when running `dindbox --help`) can be 
specified in a section named `[dindbox.global]`.

Argument names must be provided in their long form, without the leading `--`. Here's an example:

```toml title="dindbox.conf"
[dindbox.global]
log-level = "DEBUG"

[dindbox.run]
no-status-screen = true
rm = true

[dindbox.remove]
force = true
```

**Note:** When setting options in poetry's `pyproject.toml`, the section name needs to be prefixed with `tool.`:

```toml
[tool.dindbox.run]
rm = true
```

Usage as a Python Library
------------------------

Althogh `dindbox` is primarily intended to be used as a command-line tool, it can also be used as a Python library and
you can create your own custom scripts and applications based on it. The main entry point is the `DindBox` class. Here's
a minimal example of how to use it:

```python
from dindbox import DindBox

box = DindBox("my_box", build_image="ubuntu:focal")
box.run()
```

For further usage details, rely on the docstrings and type annotations of the `DindBox` class and its methods.

Use Cases
--------

Although there are probably more, DindBox was created with a particular set of use cases in mind. Most of these are
aimed at local testing on your development machine, but there are some rare cases, where it may even make sense to run
DindBox on your CI server. (In that case however, you're gonna need a dedicated runner, since DindBox itself should not
be run within a container.)

* **Test installation and execution of dockerized apps in a safe environment and on different Linux distributions**  
  You've created an application which is nicely bundled into microservices. Maybe there's also a nice little install
  script to set it all up on a machine. But how do you test it? Hopefully not by running an untested script with root
  permissions directly on your development machine. You'll either need a VM, or a tedious manually cobbled-together
  docker setup - or you just type `dindbox run` and give it a go! And by switching out the image for the build container,
  you can even easily test if your script runs fine on different Linux distros (and different releases of these).

* **Test a dockerized application against different versions of docker**  
  Switching the docker version locally means uninstalling and re-installing for each version switch. With DindBox, you
  can just swap out the images and re-run your application (or re-build your images) based on a different release of
  docker.

* **Reproduce and debug errors which occur in continuous integration (CI) jobs**  
  CI pipelines can be difficult to debug. And sometimes, the problem is not in the pipeline code alone, but also has to
  do with the fact that the job is executed within a containerized runner. This can be particularly tricky, when
  running docker commands as part of the pipeline, e.g. to test a self-built image. DindBox allows to easily reproduce
  the containerized setup locally, with one simple command-line.

* **Build docker images locally within a well-defined environment**  
  In CI, your docker images are built in a containerized environment with a fixed docker version etc. DindBox makes it
  easy to reproduce the exact same conditions locally.

* **Anything else you would otherwise use a virtual machine for**, because you need it to be isolated, and it requires
  docker.

Note: the service running in the second container does not *have* to be dockerd. Since the image is freely configurable,
you could also switch it our for a database image like MySQL, and test your DB-dependent, non-dockerized application
in a DindBox. That's totally possible, but it is not what I had in mind when I created it.

How is it different from docker-compose?
---------------------------------------

Good question. For many use cases, docker-compose may be a good solution. But specifically for the testing use cases
listed above, DindBox offers some advantages, and also some specific features, which are not easily reproduced with
docker-compose:

* Ease of use: no need to create a config file, just type a short command-line with a few options, and you're up and
  running. DindBox allows for some helpful configuration options, but the defaults will work fine, usually.
* Easy management of multiple boxes: each box has a specific name. By referencing that name you can easily manage,
  re-use, and clean up your various test environments. All docker entities (containers, networks, volumes) that make
  up a single box, will be set up or removed automatically, with a one-line command.
* Nice status screen: allows you to monitor what is going on inside a box, even if you're not interacting with it
  directly.
* Bind volumes: In addition to attaching docker volumes to your containers, or bind-mounting existing host directories,
  DindBox also offers to configure so-called "bind volumes". These are basically host directories which behave like
  docker volumes: they are created on-demand in a temporary folder, mounted to both DindBox containers, and cleaned up
  on removal of the DindBox. They can be used for specific cases, which are not supported by standard docker volumes.
  One example for this is running a user-space file system within on of your docker-ind-docker containers, and have it
  access the volume.

Development
----------

DindBox uses [poetry](https://python-poetry.org) for dependency management, isolation and packaging.

* If you do not have it already, install poetry on your machine as described in
  [its documentation](https://python-poetry.org/docs/#installation). Make sure to install in an isolated environment
  (the official installer does that), do not simply `pip install` it.
* Optional: enable poetry bash completion, as described in the docs
* Clone this repository and enter the directory
* Run `poetry install`
