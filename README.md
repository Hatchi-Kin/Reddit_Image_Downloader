# Reddit Image Downloader

A simple Python tool to download images (excluding GIFs and videos) from a Reddit user's profile or a subreddit.

## Features

- Download images from a user's posts or a subreddit.
- Skips GIFs and videos.
- Saves images to a folder (`downloads/username` or `downloads/subreddit` by default).

## Setup
---
**Note:** Requires a Reddit account and API credentials.

1. **Clone the repository** and install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. **Create a `.env.reddit` file** with your Reddit API credentials:
    ```
    CLIENT_ID="your_client_id"
    CLIENT_SECRET="your_client_secret"
    USER_AGENT="your_user_agent"
    USERNAME="your_username"
    PASSWORD="your_password"
    ```

3. **Run the script**:
    ```bash
    python main.py
    ```

## Usage

Edit `main.py` to specify the user or subreddit and the number of images to download.

```python
downloader.download_user_images(username="example_user", limit=300)
downloader.download_subreddit_images(subreddit_name="example_subreddit", limit=300)
```

Images will be saved in the `downloads/` folder by default.

