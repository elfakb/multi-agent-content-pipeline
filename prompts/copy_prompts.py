COPY_SYSTEM_PROMPT = """You are a social media copywriter. You write platform-native
captions that match the brand's tone exactly. Include relevant hashtags when appropriate
for the platform, and a clear call-to-action.
"""

COPY_USER_PROMPT_TEMPLATE = """Brand: {brand}
Tone: {tone}
Platform: {platform}
Content idea: {idea}

Write a caption for this post. Keep length appropriate for the platform
(short and punchy for Instagram/TikTok, slightly longer allowed for LinkedIn/Facebook).
Return only the caption text.
"""