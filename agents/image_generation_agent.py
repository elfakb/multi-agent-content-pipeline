import os
from utils.logger import activity_logger
from graph.state import AgentState
from services.image_service import generate_image


def image_generation_agent(state: AgentState) -> AgentState:
    activity_logger.log("Image Generation Agent", "Generating images with DALL-E 3...")
    root = state["campaign_folder"]
    generated = []

    for item in state["image_prompts"]:
        save_path = os.path.join(root, "images", f"{item['id']}.png")
        try:
            path = generate_image(item["prompt"], save_path)
            generated.append({"id": item["id"], "file_path": path})
            activity_logger.log("Image Generation Agent", f"Generated {item['id']}.png")
        except Exception as e:
            activity_logger.log("Image Generation Agent", f"Failed for {item['id']}: {e}")

    state["generated_images"] = generated
    return state