from openai import OpenAI
from utils.config import Config
from utils.logger import activity_logger
from graph.state import AgentState
from prompts.qc_prompts import QC_SYSTEM_PROMPT, QC_USER_PROMPT_TEMPLATE

client = OpenAI(api_key=Config.OPENAI_API_KEY)


def qc_agent(state: AgentState) -> AgentState:
    activity_logger.log("QC Agent", "Reviewing campaign for consistency...")
    brief = state["brief"]

    captions_text = "\n".join(f"- [{c['id']}] {c['caption']}" for c in state["captions"])
    concepts_text = "\n".join(f"- [{v['id']}] {v['concept']}" for v in state["visual_concepts"])

    response = client.chat.completions.create(
        model=Config.TEXT_MODEL,
        temperature=0.3,
        messages=[
            {"role": "system", "content": QC_SYSTEM_PROMPT},
            {"role": "user", "content": QC_USER_PROMPT_TEMPLATE.format(
                brand=brief["brand"], tone=brief["tone"],
                captions=captions_text, visual_concepts=concepts_text,
            )},
        ],
    )

    state["qc_report"] = response.choices[0].message.content
    activity_logger.log("QC Agent", "Quality review complete.")
    return state