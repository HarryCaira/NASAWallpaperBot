## NASA Wallpaper Bot (For Mac)

Updates desktop wallpaper with image from the [NASA APOD API](https://api.nasa.gov/). Saves image locally to a given destination folder.

### Requirements
1. Python 3.10
2. Poetry
3. .env with NASA_API_KEY={my_nasa_api_key} set

### Manual Usage
1. `export $(cat .env | xargs)`
2. `poetry install`
3. `poetry run wallpaper_bot {path_to_destination_folder}`

### Running as a cronjob
1. `sudo crontab -e`
2. set PATH at the top level, pointing to bin and your poetry installation e.g. `PATH=/opt/homebrew/bin:/bin:/usr/bin:`
3. add crontab line:
    e.g. `0 12 * * * cd {local_path_to_this_dir} && sh wallpaper_bot.sh {path_to_destination_folder}` Runs everyday at 12pm. [Crontab guru](https://crontab.guru/) for reference.

**Note:** You will have to give the shell program that is running your jobs accessibility access in the security and privacy settings.   


