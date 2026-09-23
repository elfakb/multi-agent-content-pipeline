STRATEGY_SYSTEM_PROMPT = """You are a senior social media strategist. You turn a client
brief into a clear content strategy: positioning, key messages, and content pillars.
Be concrete and campaign-specific, not generic.
"""

STRATEGY_USER_PROMPT_TEMPLATE = """Client brief:
Brand: {brand}
Product: {product}
Target audience: {audience}
Campaign: {campaign}
Platforms: {platforms}
Tone: {tone}
Number of assets requested: {num_assets}

Write a content strategy with these sections:
1. Positioning statement (1-2 sentences)
2. Key messages (3-4 bullet points)
3. Content pillars (2-3 themes the assets should rotate around)
4. Platform-specific notes (how tone/format should adapt per platform)
"""