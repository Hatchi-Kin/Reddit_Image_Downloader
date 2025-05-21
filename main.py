from dotenv import dotenv_values
from typing import Dict

from reddit_image_downloader.downloader import RedditImageDownloader


def get_config() -> Dict[str, str]:
    config = dotenv_values(".env.reddit")
    required_vars = ["CLIENT_ID", "CLIENT_SECRET", "USER_AGENT", "USERNAME", "PASSWORD"]
    missing_vars = [var for var in required_vars if not config.get(var)]

    if missing_vars:
        raise ValueError
    return {key: str(value) for key, value in config.items() if value is not None}


config = get_config()

downloader = RedditImageDownloader(
    client_id=config["CLIENT_ID"],
    client_secret=config["CLIENT_SECRET"],
    user_agent=config["USER_AGENT"],
    username=config["USERNAME"],
    password=config["PASSWORD"],
)


### Download images from a user's profile
downloader.download_user_images(username="example_user", limit=300)

### Download images from a subreddit
# downloader.download_subreddit_images(subreddit_name="example_subreddit", limit=300)
