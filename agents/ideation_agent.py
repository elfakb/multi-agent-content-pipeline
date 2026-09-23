import json
from openai import OpenAI
from utils.config import Config
from utils.logger import activity_logger
from graph.state import AgentState
from prompts.ideation_prompts import IDEATION_SYSTEM_PROMPT, IDEATION_USER_PROMPT_TEMPLATE

client = OpenAI(api_key=Config.OPENAI_API_KEY)


def ideation_agent(state: AgentState) -> AgentState:
    activity_logger.log("Ideation Agent", "Generating content ideas...")
    brief = state["brief"]

    response = client.chat.completions.create(
        model=Config.TEXT_MODEL,
        temperature=Config.TEMPERATURE,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": IDEATION_SYSTEM_PROMPT},
            {"role": "user", "content": IDEATION_USER_PROMPT_TEMPLATE.format(
                strategy=state["strategy"], platforms=", ".join(brief["platforms"]),
                num_assets=brief["num_assets"],
            )},
        ],
    )

    parsed = json.loads(response.choices[0].message.content)
    ideas = parsed["ideas"]

    state["content_ideas"] = ideas
    activity_logger.log("Ideation Agent", f"{len(ideas)} content ideas generated.")
    return state