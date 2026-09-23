IMAGE_PROMPT_SYSTEM_PROMPT = """You are an expert prompt engineer for DALL-E 3.
You convert a visual concept into a single, highly detailed image generation prompt,
optimized for DALL-E 3's strengths (rich descriptive language, clear subject, lighting,
composition, and style keywords).
"""

IMAGE_PROMPT_USER_PROMPT_TEMPLATE = """Visual concept:
{visual_concept}

Brand: {brand}
Product: {product}

Write one single DALL-E 3 prompt (2-4 sentences) that will generate this image.
Do not include any camera settings or technical jargon DALL-E doesn't use.
Return only the prompt text, nothing else.
"""