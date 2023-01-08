from appscript import app, mactypes
from typing import Optional
import requests
import datetime
import urllib
import click
import os


def save_latest_image(destination_folder: str) -> Optional[str]:
    SERVICE_URL = "https://api.nasa.gov/planetary/apod"
    API_KEY = os.environ.get(
        "NASA_API_KEY",
    )

    params = {"api_key": API_KEY}
    resp = requests.get(SERVICE_URL, params=params)

    if resp.status_code != 200:
        return

    # url to hd image of the day
    hdurl = resp.json().get("hdurl")

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
    saved_file = save_latest_image(destination_folder)
    if saved_file:
        print(f"Saved daily image: {saved_file}")
        app("Finder").desktop_picture.set(mactypes.File(saved_file))
        print("Wallpaper updated!")


if __name__ == "__main__":
    main()
