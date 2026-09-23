VISUAL_CONCEPT_SYSTEM_PROMPT = """You are an art director. You translate content ideas
into a clear visual concept: composition, mood, color palette, setting, and style
direction, consistent with the brand tone.
"""

VISUAL_CONCEPT_USER_PROMPT_TEMPLATE = """Brand: {brand}
Product: {product}
Tone: {tone}
Platform: {platform}
Asset type: {type}
Content idea: {idea}

Describe the visual concept for this asset in 3-5 sentences: composition, mood,
color palette, setting/background, and style (e.g. photography, illustration, 3D render).
"""