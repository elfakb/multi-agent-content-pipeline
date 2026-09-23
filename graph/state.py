from typing import TypedDict, List, Dict, Any


class CampaignBrief(TypedDict):
    brand: str
    product: str
    audience: str
    campaign: str
    platforms: List[str]
    tone: str
    num_assets: int


class AgentState(TypedDict):
    brief: CampaignBrief

    strategy: str                     # output of strategy agent
    content_ideas: List[Dict[str, Any]]   # id, platform, type(image/video), idea
    captions: List[Dict[str, Any]]        # id, caption
    visual_concepts: List[Dict[str, Any]] # id, concept
    image_prompts: List[Dict[str, Any]]   # id, prompt   (only image-type assets)
    video_scripts: List[Dict[str, Any]]   # id, script, sora_prompt (only video-type assets)
    generated_images: List[Dict[str, Any]] # id, file_path

    qc_report: str
    campaign_folder: str