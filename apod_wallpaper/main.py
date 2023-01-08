from __future__ import annotations
from appscript import app, mactypes
from dataclasses import dataclass
from requests import Response
from typing import Optional
import requests
import datetime
import urllib
import click
import os


class APIError(Exception):
    ...


@dataclass
class APODWallpaper:
    api_key: str
    service_url: str

    def _make_request(self) -> Response:
        params = {"api_key": self.api_key}
        response = requests.get(self.service_url, params=params)
        if response.status_code != 200:
            raise APIError(
                f"Error with request: {self.service_url}\n{str(response.status_code)}: {response.content}"
            )
        return response

    def saved_wallpaper(self, destination_folder: str) -> str:
        response = self._make_request()
        hdurl = response.json().get("hdurl")

        current_time = datetime.datetime.now().strftime("%d-%m-%Y")
        destination_path = os.path.join(
            destination_folder,
            f"{hdurl.split('/')[-1].replace('.', f'_{current_time}.')}",
        )
        urllib.request.urlretrieve(hdurl, destination_path)
        return destination_path


@click.command()
@click.argument(
    "destination-folder",
    required=True,
    type=click.Path(file_okay=False, exists=True),
)
def main(destination_folder: str) -> Optional[str]:
    service_url = "https://api.nasa.gov/planetary/apod"
    api_key = os.environ.get(
        "NASA_API_KEY",
    )
    wallpaper = APODWallpaper(api_key, service_url)

    try:
        saved_wallpaper = wallpaper.saved_wallpaper(destination_folder)
    except APIError as exception:
        print(str(exception))
        return

    app("Finder").desktop_picture.set(mactypes.File(saved_wallpaper))
    print("Wallpaper updated!")


if __name__ == "__main__":
    main()
