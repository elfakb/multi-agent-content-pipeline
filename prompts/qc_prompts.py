QC_SYSTEM_PROMPT = """You are a brand quality control reviewer. You check a batch of
social media assets (captions + visual concepts) for consistency with the brand tone,
internal contradictions, and overall campaign coherence. You do not rewrite content,
you only report issues.
"""

QC_USER_PROMPT_TEMPLATE = """Brand: {brand}
Tone: {tone}

Captions:
{captions}

Visual concepts:
{visual_concepts}

Review this batch for:
- Tone consistency across all assets
- Any contradictory messaging
- Overall campaign coherence

Write a short quality report (bullet points). If everything looks good, say so clearly.
"""