#!/bin/sh
export $(cat .env | xargs)
poetry install
poetry run apod_wallpaper $1