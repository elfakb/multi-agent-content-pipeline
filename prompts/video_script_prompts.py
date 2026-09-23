VIDEO_SCRIPT_SYSTEM_PROMPT = """You are a short-form video director for social media
(Reels, TikTok, Shorts). You write scene-by-scene scripts and a matching Sora 2
generation prompt.

Respond ONLY with valid JSON in this format:
{
  "script": "scene-by-scene breakdown with timestamps, on-screen text, and audio/music notes",
  "sora_prompt": "a single, detailed, cinematic text-to-video prompt ready to paste into Sora 2"
}
"""

VIDEO_SCRIPT_USER_PROMPT_TEMPLATE = """Visual concept:
{visual_concept}

Brand: {brand}
Product: {product}
Platform: {platform}
Tone: {tone}
Target length: 8-15 seconds

Write:
1. A scene-by-scene script (timestamps, visuals, on-screen text, music/audio direction)
2. A single Sora 2 prompt describing the whole clip cinematically (subject, action,
   setting, camera movement, lighting, mood) so it can be generated directly.

Respond with the JSON object only.
"""