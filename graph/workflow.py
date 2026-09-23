from langgraph.graph import StateGraph, END

from graph.state import AgentState, CampaignBrief
from agents.strategy_agent import strategy_agent
from agents.ideation_agent import ideation_agent
from agents.copy_agent import copy_agent
from agents.visual_concept_agent import visual_concept_agent
from agents.image_prompt_agent import image_prompt_agent
from agents.video_script_agent import video_script_agent
from agents.image_generation_agent import image_generation_agent
from agents.qc_agent import qc_agent
from agents.packaging_agent import packaging_agent

from utils.logger import activity_logger
from utils.file_manager import create_campaign_folder


def build_workflow():
    graph = StateGraph(AgentState)

    graph.add_node("strategy", strategy_agent)
    graph.add_node("ideation", ideation_agent)
    graph.add_node("copy", copy_agent)
    graph.add_node("visual_concepts", visual_concept_agent)
    graph.add_node("image_prompts", image_prompt_agent)
    graph.add_node("video_scripts", video_script_agent)
    graph.add_node("image_generation", image_generation_agent)
    graph.add_node("qc", qc_agent)
    graph.add_node("packaging", packaging_agent)

    graph.set_entry_point("strategy")
    graph.add_edge("strategy", "ideation")
    graph.add_edge("ideation", "copy")
    graph.add_edge("copy", "visual_concepts")
    graph.add_edge("visual_concepts", "image_prompts")
    graph.add_edge("image_prompts", "video_scripts")
    graph.add_edge("video_scripts", "image_generation")
    graph.add_edge("image_generation", "qc")
    graph.add_edge("qc", "packaging")
    graph.add_edge("packaging", END)

    return graph.compile()


def run_pipeline(brief: CampaignBrief) -> AgentState:
    activity_logger.clear()

    campaign_folder = create_campaign_folder(brief["brand"], brief["campaign"])

    initial_state: AgentState = {
        "brief": brief,
        "strategy": "",
        "content_ideas": [],
        "captions": [],
        "visual_concepts": [],
        "image_prompts": [],
        "video_scripts": [],
        "generated_images": [],
        "qc_report": "",
        "campaign_folder": campaign_folder,
    }

    workflow = build_workflow()
    final_state = workflow.invoke(initial_state)
    return final_state