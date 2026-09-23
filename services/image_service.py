import os
import requests
from openai import OpenAI
from utils.config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)


def generate_image(prompt: str, save_path: str) -> str:
    """Generates an image with DALL-E 3 and saves it to save_path. Returns the path."""
    response = client.images.generate(
        model=Config.IMAGE_MODEL,
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    image_data = requests.get(image_url, timeout=60).content

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(image_data)

    return save_path