# Reddit Image Downloader

A simple Python tool to download images (excluding GIFs and videos) from a Reddit user's profile or a subreddit.

## Features

- Download images from a user's posts or a subreddit.
- Skips GIFs and videos.
- Saves images to a folder (`downloads/username` or `downloads/subreddit` by default).

## Setup

**Note:** Requires a Reddit account and API credentials. 
    
#### Some links: 
- [apps](https://www.reddit.com/prefs/apps)
    
- [old apps](https://old.reddit.com/prefs/apps)

- [Reddit API](https://www.reddit.com/dev/api/)

#
1. **Clone the repository** and install dependencies (with [uv](https://github.com/astral-sh/uv) or [Poetry](https://python-poetry.org/)):

    ```bash
    uv venv .venv
    source .venv/bin/activate
    uv pip install -r pyproject.toml
    ```

    Or with Poetry:

    ```bash
    poetry install
    ```

2. **Create a `.env.reddit` file** with your Reddit API credentials:

    ```
    CLIENT_ID="your_client_id"
    CLIENT_SECRET="your_client_secret"
    USER_AGENT="your_user_agent"
    USERNAME="your_username"
    PASSWORD="your_password"
    ```

## Usage

### As a CLI tool

You can use the CLI to download images from either a Reddit user or a subreddit.

#### Download images from a user's profile

```bash
python -m cli --user example_user --limit 100
```
or, if installed as a script:
```bash
reddit-image-downloader --user example_user --limit 100
```

#### Download images from a subreddit

```bash
python -m cli --subreddit example_subreddit --limit 50
```
or, if installed as a script:
```bash
reddit-image-downloader --subreddit example_subreddit --limit 50
```

You can also specify a custom download directory:

```bash
reddit-image-downloader --user example_user --download-dir /path/to/save/images
reddit-image-downloader --subreddit example_subreddit --download-dir /path/to/save/images
```

### As a Python module

Edit `main.py` to specify the user or subreddit and the number of images to download:

```python
from dotenv import dotenv_values
from reddit_image_downloader.downloader import RedditImageDownloader

config = dotenv_values(".env.reddit")
downloader = RedditImageDownloader(
    client_id=config['CLIENT_ID'],
    client_secret=config['CLIENT_SECRET'],
    user_agent=config['USER_AGENT'],
    username=config['USERNAME'],
    password=config['PASSWORD'],
)

downloader.download_user_images(username="example_user", limit=300)
downloader.download_subreddit_images(subreddit_name="example_subreddit", limit=300)
```

Images will be saved in the `downloads/` folder by default.
