#!/bin/sh
export $(cat .env | xargs)
poetry install
poetry run wallpaper_bot $1
