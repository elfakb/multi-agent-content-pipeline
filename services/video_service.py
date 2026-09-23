"""
Wrapper around OpenAI's Sora 2 video generation API.
Used ONLY by the manual "Video Studio" section of the app — never called
automatically by the main pipeline, since video generation is billed per
second and can be costly.

NOTE: Sora 2's API surface is new and may evolve. Verify endpoint/parameter
names against the current OpenAI API docs before relying on this in production.
"""

import time
import os
from openai import OpenAI
from utils.config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)


def generate_video(prompt: str, save_path: str, seconds: int = 8, poll_interval: int = 5, timeout: int = 300) -> str:
    """
    Submits a video generation job to Sora 2, polls until it's done,
    downloads the result to save_path, and returns the path.
    """
    job = client.videos.create(
        model=Config.VIDEO_MODEL,
        prompt=prompt,
        seconds=seconds,
    )

    elapsed = 0
    while job.status not in ("completed", "failed"):
        if elapsed >= timeout:
            raise TimeoutError(f"Video generation timed out after {timeout}s (job id: {job.id})")
        time.sleep(poll_interval)
        elapsed += poll_interval
        job = client.videos.retrieve(job.id)

    if job.status == "failed":
        raise RuntimeError(f"Video generation failed for job {job.id}")

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    content = client.videos.download_content(job.id)
    content.write_to_file(save_path)

    return save_path