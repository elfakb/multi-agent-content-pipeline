from utils.logger import activity_logger
from utils.file_manager import write_text_file, write_json_file
from graph.state import AgentState


def packaging_agent(state: AgentState) -> AgentState:
    activity_logger.log("Packaging Agent", "Writing final content package to disk...")
    root = state["campaign_folder"]

    write_text_file(root, "strategy/strategy.md", state["strategy"])
    write_json_file(root, "content_calendar/calendar.json", state["content_ideas"])

    captions_md = "\n\n".join(f"### {c['id']}\n{c['caption']}" for c in state["captions"])
    write_text_file(root, "captions/captions.md", captions_md)

    concepts_md = "\n\n".join(f"### {v['id']}\n{v['concept']}" for v in state["visual_concepts"])
    write_text_file(root, "visual_prompts/visual_concepts.md", concepts_md)

    if state["image_prompts"]:
        prompts_md = "\n\n".join(f"### {p['id']}\n{p['prompt']}" for p in state["image_prompts"])
        write_text_file(root, "visual_prompts/image_prompts.md", prompts_md)

    if state["video_scripts"]:
        for v in state["video_scripts"]:
            content = f"## Script\n{v['script']}\n\n## Sora 2 Prompt\n{v['sora_prompt']}"
            write_text_file(root, f"video_scripts/{v['id']}.md", content)

    write_text_file(root, "final_assets/qc_report.md", state["qc_report"])

    # manifest of what's ready to ship
    manifest = {
        "brand": state["brief"]["brand"],
        "campaign": state["brief"]["campaign"],
        "assets": state["content_ideas"],
        "images_generated": [g["id"] for g in state["generated_images"]],
        "videos_scripted": [v["id"] for v in state["video_scripts"]],
    }
    write_json_file(root, "final_assets/manifest.json", manifest)

    activity_logger.log("Packaging Agent", f"Campaign package ready at: {root}")
    return state