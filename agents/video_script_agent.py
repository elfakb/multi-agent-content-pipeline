import json
from openai import OpenAI
from utils.config import Config
from utils.logger import activity_logger
from graph.state import AgentState
from prompts.video_script_prompts import VIDEO_SCRIPT_SYSTEM_PROMPT, VIDEO_SCRIPT_USER_PROMPT_TEMPLATE

client = OpenAI(api_key=Config.OPENAI_API_KEY)


def video_script_agent(state: AgentState) -> AgentState:
    activity_logger.log("Video Script Agent", "Writing scripts + Sora 2 prompts for video assets...")
    brief = state["brief"]
    concept_map = {c["id"]: c["concept"] for c in state["visual_concepts"]}
    idea_map = {i["id"]: i for i in state["content_ideas"]}
    scripts = []

    for idea in state["content_ideas"]:
        if idea["type"] != "video":
            continue

        response = client.chat.completions.create(
            model=Config.TEXT_MODEL,
            temperature=Config.TEMPERATURE,
            messages=[
                {"role": "system", "content": VIDEO_SCRIPT_SYSTEM_PROMPT},
                {"role": "user", "content": VIDEO_SCRIPT_USER_PROMPT_TEMPLATE.format(
                    visual_concept=concept_map[idea["id"]],
                    brand=brief["brand"], product=brief["product"],
                    platform=idea["platform"], tone=brief["tone"],
                )},
            ],
        )

        raw = response.choices[0].message.content.strip()
        raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        parsed = json.loads(raw)

        scripts.append({
            "id": idea["id"],
            "script": parsed["script"],
            "sora_prompt": parsed["sora_prompt"],
        })

    state["video_scripts"] = scripts
    activity_logger.log("Video Script Agent", f"{len(scripts)} video scripts ready.")
    return state