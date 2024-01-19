# Poetry Dockerize Plugin

![PyPI](https://img.shields.io/pypi/v/poetry-dockerize-plugin?color=green&label=pypi%20package)
![PyPI](https://img.shields.io/pypi/pyversions/poetry-dockerize-plugin?color=gree)

Key features:

* Automatically generate a docker image from your Poetry application.
* Highly configurable. You can configure the image by adding a section in the `pyproject.toml` configuration file.

## Installation

In order to install the plugin you need to have installed a poetry version `>=1.2.0` and type:

```bash
poetry self add poetry-dockerize-plugin
```

## Quickstart

No configuration needed! Just type:
```bash
poetry dockerize
>Building image: poetry-sample-app:latest
>Successfully built image: poetry-sample-app:latest
docker run --rm -it poetry-sample-app:latest
>hello world!
```

## Configuration
To customize some options, you can add a `[tool.dockerize]` section in your `pyproject.toml` file. For example to change the image name:

```toml
[tool.dockerize]
name = "myself/myproject-app"
```

## Configuration API Reference

This examples shows a complete configuration of the docker image:

```toml
[tool.docker]
name = "alternative-image-name"
tags = ["latest-dev"]
entrypoint = ["python", "-m", "whatever"]
python = "3.8"
ports = [5000]
env = {"MY_APP_ENV" = "dev"}
labels = {"MY_APP_LABEL" = "dev"}
```

* `name` customizes the docker image name.
* `tags` declares a list of tags for the image.
* `entrypoint` customizes the entrypoint of the image. If not provided, the default entrypoint is retrieved from the `packages` configuration.
* `python` python version to use. Default is `3.11`
* `ports` exposes ports
* `env` declares environment variables inside the docker image.
* `labels` append labels to the docker image. Default labels are added following the opencontainers specification.


## Command-Line options

All command line options provided by the `poetry-dockerize-plugin` may be accessed by typing:

```bash
poetry dockerize --help
```

## License

This project is licensed under the terms of the MIT license.
