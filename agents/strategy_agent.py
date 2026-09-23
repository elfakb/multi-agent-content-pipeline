from openai import OpenAI
from utils.config import Config
from utils.logger import activity_logger
from graph.state import AgentState
from prompts.strategy_prompts import STRATEGY_SYSTEM_PROMPT, STRATEGY_USER_PROMPT_TEMPLATE

client = OpenAI(api_key=Config.OPENAI_API_KEY)


def strategy_agent(state: AgentState) -> AgentState:
    activity_logger.log("Strategy Agent", "Building content strategy from brief...")
    brief = state["brief"]

    response = client.chat.completions.create(
        model=Config.TEXT_MODEL,
        temperature=Config.TEMPERATURE,
        messages=[
            {"role": "system", "content": STRATEGY_SYSTEM_PROMPT},
            {"role": "user", "content": STRATEGY_USER_PROMPT_TEMPLATE.format(
                brand=brief["brand"], product=brief["product"], audience=brief["audience"],
                campaign=brief["campaign"], platforms=", ".join(brief["platforms"]),
                tone=brief["tone"], num_assets=brief["num_assets"],
            )},
        ],
    )

    state["strategy"] = response.choices[0].message.content
    activity_logger.log("Strategy Agent", "Strategy complete.")
    return state