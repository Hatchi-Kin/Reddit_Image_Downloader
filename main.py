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

### Download images from a user's profile
downloader.download_user_images(username="example_user", limit=300)

### Download images from a subreddit
# downloader.download_subreddit_images(subreddit_name="example_subreddit", limit=300)
