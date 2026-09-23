import os
import json
import re
from utils.config import Config


def _slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def create_campaign_folder(brand: str, campaign: str) -> str:
    """Creates the campaign/ folder tree and returns its root path."""
    folder_name = f"{_slugify(brand)}_{_slugify(campaign)}"
    root = os.path.join(Config.OUTPUT_ROOT, folder_name)

    subfolders = [
        "strategy",
        "content_calendar",
        "captions",
        "visual_prompts",
        "images",
        "video_scripts",
        "final_assets",
        "final_assets/videos",
    ]

    for sub in subfolders:
        os.makedirs(os.path.join(root, sub), exist_ok=True)

    return root


def write_text_file(root: str, relative_path: str, content: str):
    full_path = os.path.join(root, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    return full_path


def write_json_file(root: str, relative_path: str, data):
    full_path = os.path.join(root, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return full_path