from openai import OpenAI
from utils.config import Config
from utils.logger import activity_logger
from graph.state import AgentState
from prompts.copy_prompts import COPY_SYSTEM_PROMPT, COPY_USER_PROMPT_TEMPLATE

client = OpenAI(api_key=Config.OPENAI_API_KEY)


def copy_agent(state: AgentState) -> AgentState:
    activity_logger.log("Copy Agent", "Writing captions for all assets...")
    brief = state["brief"]
    captions = []

    for idea in state["content_ideas"]:
        response = client.chat.completions.create(
            model=Config.TEXT_MODEL,
            temperature=Config.TEMPERATURE,
            messages=[
                {"role": "system", "content": COPY_SYSTEM_PROMPT},
                {"role": "user", "content": COPY_USER_PROMPT_TEMPLATE.format(
                    brand=brief["brand"], tone=brief["tone"],
                    platform=idea["platform"], idea=idea["idea"],
                )},
            ],
        )
        captions.append({"id": idea["id"], "caption": response.choices[0].message.content})

    state["captions"] = captions
    activity_logger.log("Copy Agent", f"{len(captions)} captions written.")
    return state