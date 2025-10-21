#!/bin/sh

poetry install
poetry run hypercorn app:app "$@"
