from openai import OpenAI
from utils.config import Config
from utils.logger import activity_logger
from graph.state import AgentState
from prompts.visual_concept_prompts import VISUAL_CONCEPT_SYSTEM_PROMPT, VISUAL_CONCEPT_USER_PROMPT_TEMPLATE

client = OpenAI(api_key=Config.OPENAI_API_KEY)


def visual_concept_agent(state: AgentState) -> AgentState:
    activity_logger.log("Visual Concept Agent", "Designing visual concepts...")
    brief = state["brief"]
    concepts = []

    for idea in state["content_ideas"]:
        response = client.chat.completions.create(
            model=Config.TEXT_MODEL,
            temperature=Config.TEMPERATURE,
            messages=[
                {"role": "system", "content": VISUAL_CONCEPT_SYSTEM_PROMPT},
                {"role": "user", "content": VISUAL_CONCEPT_USER_PROMPT_TEMPLATE.format(
                    brand=brief["brand"], product=brief["product"], tone=brief["tone"],
                    platform=idea["platform"], type=idea["type"], idea=idea["idea"],
                )},
            ],
        )
        concepts.append({"id": idea["id"], "concept": response.choices[0].message.content})

    state["visual_concepts"] = concepts
    activity_logger.log("Visual Concept Agent", f"{len(concepts)} visual concepts created.")
    return state