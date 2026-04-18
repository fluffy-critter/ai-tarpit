#!/bin/sh

poetry install
poetry run hypercorn --config config.toml app:app "$@"
