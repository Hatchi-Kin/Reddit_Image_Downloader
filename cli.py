import argparse

from dotenv import dotenv_values

from reddit_image_downloader.downloader import RedditImageDownloader


def main():
    parser = argparse.ArgumentParser(
        description="Download images from Reddit users or subreddits."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--user", help="Reddit username to download images from")
    group.add_argument("--subreddit", help="Subreddit name to download images from")
    parser.add_argument(
        "--limit", type=int, default=100, help="Number of posts to check"
    )
    parser.add_argument("--download-dir", help="Custom download directory")
    args = parser.parse_args()

    config = dotenv_values(".env.reddit")
    required_vars = ["CLIENT_ID", "CLIENT_SECRET", "USER_AGENT", "USERNAME", "PASSWORD"]
    missing_vars = [var for var in required_vars if not config.get(var)]
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        return

    downloader = RedditImageDownloader(
        client_id=str(config["CLIENT_ID"]),
        client_secret=str(config["CLIENT_SECRET"]),
        user_agent=str(config["USER_AGENT"]),
        username=str(config["USERNAME"]),
        password=str(config["PASSWORD"]),
    )

    if args.user:
        downloader.download_user_images(
            username=args.user, limit=args.limit, download_dir=args.download_dir
        )
    elif args.subreddit:
        downloader.download_subreddit_images(
            subreddit_name=args.subreddit,
            limit=args.limit,
            download_dir=args.download_dir,
        )


if __name__ == "__main__":
    main()
