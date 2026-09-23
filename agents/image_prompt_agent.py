from openai import OpenAI
from utils.config import Config
from utils.logger import activity_logger
from graph.state import AgentState
from prompts.image_prompt_prompts import IMAGE_PROMPT_SYSTEM_PROMPT, IMAGE_PROMPT_USER_PROMPT_TEMPLATE

client = OpenAI(api_key=Config.OPENAI_API_KEY)


def image_prompt_agent(state: AgentState) -> AgentState:
    activity_logger.log("Image Prompt Agent", "Writing DALL-E prompts for image assets...")
    brief = state["brief"]
    concept_map = {c["id"]: c["concept"] for c in state["visual_concepts"]}
    prompts = []

    for idea in state["content_ideas"]:
        if idea["type"] != "image":
            continue

        response = client.chat.completions.create(
            model=Config.TEXT_MODEL,
            temperature=Config.TEMPERATURE,
            messages=[
                {"role": "system", "content": IMAGE_PROMPT_SYSTEM_PROMPT},
                {"role": "user", "content": IMAGE_PROMPT_USER_PROMPT_TEMPLATE.format(
                    visual_concept=concept_map[idea["id"]],
                    brand=brief["brand"], product=brief["product"],
                )},
            ],
        )
        prompts.append({"id": idea["id"], "prompt": response.choices[0].message.content.strip()})

    state["image_prompts"] = prompts
    activity_logger.log("Image Prompt Agent", f"{len(prompts)} image prompts ready.")
    return state