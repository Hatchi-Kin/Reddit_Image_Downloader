import os
import hashlib
import urllib.request
from urllib.parse import urlparse
from urllib.error import URLError, HTTPError

import praw


class RedditImageDownloader:
    def __init__(
        self,
        client_id,
        client_secret,
        user_agent,
        username,
        password,
        base_download_dir="downloads",
    ):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password,
        )
        self.base_download_dir = base_download_dir
        self.image_hashes = set()

    def is_image_url(self, url):
        """Check if a URL is an image (excluding GIFs)"""
        if not url:
            return False

        url = url.lower()
        image_domains = ["i.imgur.com", "i.redd.it"]

        if any(domain in url for domain in image_domains):
            return not any(url.endswith(ext) for ext in [".gif", ".gifv"])

        return any(url.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".bmp"])

    def _get_image_hash(self, url):
        hasher = hashlib.sha256()
        try:
            with urllib.request.urlopen(url) as response:
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            print(f"Error hashing {url}: {e}")
            return None

    def download_user_images(self, username, limit=None, download_dir=None):
        """Download all images from a user's posts (excluding GIFs)"""
        if download_dir is None:
            download_dir = os.path.join(self.base_download_dir, username)
        os.makedirs(download_dir, exist_ok=True)
        user = self.reddit.redditor(username)
        submissions = user.submissions.new(limit=limit)
        downloaded_count = 0

        for submission in submissions:
            if self.is_image_url(submission.url):
                img_hash = self._get_image_hash(submission.url)
                if not img_hash:
                    continue
                if img_hash in self.image_hashes:
                    continue
                try:
                    url_parts = urlparse(submission.url)
                    file_ext = os.path.splitext(url_parts.path)[1] or ".jpg"
                    filename = f"{submission.id}{file_ext}"
                    filepath = os.path.join(download_dir, filename)

                    # Download and save image
                    with urllib.request.urlopen(submission.url) as response, open(
                        filepath, "wb"
                    ) as out_file:
                        while True:
                            chunk = response.read(8192)
                            if not chunk:
                                break
                            out_file.write(chunk)

                    self.image_hashes.add(img_hash)
                    downloaded_count += 1
                    print(f"Downloaded: {submission.title[:50]}... ({filename})")

                except (URLError, HTTPError) as e:
                    print(f"Error downloading {submission.url}: {e}")

        print(f"\nDownloaded {downloaded_count} images to '{download_dir}'")

    def download_subreddit_images(self, subreddit_name, limit=None, download_dir=None):
        """Download all images from a subreddit (excluding GIFs)"""
        if download_dir is None:
            download_dir = os.path.join(self.base_download_dir, subreddit_name)
        os.makedirs(download_dir, exist_ok=True)
        subreddit = self.reddit.subreddit(subreddit_name)
        submissions = subreddit.new(limit=limit)
        downloaded_count = 0

        for submission in submissions:
            if self.is_image_url(submission.url):
                img_hash = self._get_image_hash(submission.url)
                if not img_hash:
                    continue
                if img_hash in self.image_hashes:
                    continue
                try:
                    url_parts = urlparse(submission.url)
                    file_ext = os.path.splitext(url_parts.path)[1] or ".jpg"
                    filename = f"{submission.id}{file_ext}"
                    filepath = os.path.join(download_dir, filename)

                    # Download and save image
                    with urllib.request.urlopen(submission.url) as response, open(
                        filepath, "wb"
                    ) as out_file:
                        while True:
                            chunk = response.read(8192)
                            if not chunk:
                                break
                            out_file.write(chunk)

                    self.image_hashes.add(img_hash)
                    downloaded_count += 1
                    print(f"Downloaded: {submission.title[:50]}... ({filename})")

                except (URLError, HTTPError) as e:
                    print(f"Error downloading {submission.url}: {e}")

        print(f"\nDownloaded {downloaded_count} images to '{download_dir}'")
