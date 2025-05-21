import os
import hashlib
import urllib.request
from typing import Optional, Set, cast
from urllib.parse import urlparse, ParseResult
from urllib.error import URLError, HTTPError

import praw  # type: ignore


class RedditImageDownloader:
    CHUNK_SIZE: int = 8192
    IMAGE_DOMAINS: list[str] = ["i.imgur.com", "i.redd.it"]
    EXCLUDED_EXTENSIONS: list[str] = [".gif", ".gifv"]
    VALID_EXTENSIONS: list[str] = [".jpg", ".jpeg", ".png", ".bmp"]

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str,
        username: str,
        password: str,
        base_download_dir: str = "downloads",
    ) -> None:
        self.reddit: praw.Reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password,
        )
        self.base_download_dir: str = base_download_dir
        self.image_hashes: Set[str] = set()

    def _is_image_url(self, url: str) -> bool:
        """Check if a URL is an image (excluding GIFs)"""
        if not url:
            return False

        url = url.lower()
        if any(domain in url for domain in self.IMAGE_DOMAINS):
            return not any(url.endswith(ext) for ext in self.EXCLUDED_EXTENSIONS)
        return any(url.endswith(ext) for ext in self.VALID_EXTENSIONS)

    def _get_image_hash(self, url: str) -> Optional[str]:
        """Generate SHA256 hash of image from URL"""
        hasher = hashlib.sha256()
        try:
            with urllib.request.urlopen(url) as response:
                while True:
                    chunk = response.read(self.CHUNK_SIZE)
                    if not chunk:
                        break
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            print(f"Error hashing {url}: {e}")
            return None

    def _download_single_image(
        self, submission: praw.reddit.Submission, download_dir: str
    ) -> bool:
        """Download a single image from a submission"""
        img_hash = self._get_image_hash(submission.url)
        if not img_hash or img_hash in self.image_hashes:
            return False

        try:
            url_parts = cast(ParseResult, urlparse(submission.url))
            file_ext: str = os.path.splitext(url_parts.path)[1] or ".jpg"
            filename = f"{submission.id}{file_ext}"
            filepath = os.path.join(download_dir, filename)

            with urllib.request.urlopen(submission.url) as response, open(
                filepath, "wb"
            ) as out_file:
                while True:
                    chunk = response.read(self.CHUNK_SIZE)
                    if not chunk:
                        break
                    out_file.write(chunk)

            self.image_hashes.add(img_hash)
            print(f"Downloaded: {submission.title[:50]}... ({filename})")
            return True

        except (URLError, HTTPError) as e:
            print(f"Error downloading {submission.url}: {e}")
            return False

    def download_user_images(
        self,
        username: str,
        limit: Optional[int] = None,
        download_dir: Optional[str] = None,
    ) -> None:
        """Download all images from a user's posts (excluding GIFs)"""
        if download_dir is None:
            download_dir = os.path.join(self.base_download_dir, username)
        os.makedirs(download_dir, exist_ok=True)

        user = self.reddit.redditor(username)
        submissions = user.submissions.new(limit=limit)
        downloaded_count = 0

        for submission in submissions:
            if self._is_image_url(submission.url):
                if self._download_single_image(submission, download_dir):
                    downloaded_count += 1

        print(f"\nDownloaded {downloaded_count} images to '{download_dir}'")

    def download_subreddit_images(
        self,
        subreddit_name: str,
        limit: Optional[int] = 100,
        download_dir: Optional[str] = None,
    ) -> None:
        """Download all images from a subreddit (excluding GIFs)"""
        if download_dir is None:
            download_dir = os.path.join(self.base_download_dir, subreddit_name)
        os.makedirs(download_dir, exist_ok=True)

        subreddit = self.reddit.subreddit(subreddit_name)
        submissions = subreddit.new(limit=str(limit))
        downloaded_count = 0

        for submission in submissions:
            if self._is_image_url(submission.url):
                if self._download_single_image(submission, download_dir):
                    downloaded_count += 1

        print(f"\nDownloaded {downloaded_count} images to '{download_dir}'")
