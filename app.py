import os
import streamlit as st

from utils.config import Config
from utils.logger import activity_logger
from graph.workflow import run_pipeline
from services.video_service import generate_video

st.set_page_config(page_title="AI Content Production Pipeline", layout="wide")
st.title("🎬 AI Content Production Pipeline")

try:
    Config.validate()
except EnvironmentError as e:
    st.error(str(e))
    st.stop()

tab_pipeline, tab_video_studio = st.tabs(["Content Pipeline", "Video Studio"])

# ---------------------------------------------------------------------------
# TAB 1 — Main pipeline
# ---------------------------------------------------------------------------
with tab_pipeline:
    st.caption("Client Brief → Contets")

    with st.form("brief_form"):
        col1, col2 = st.columns(2)
        brand = col1.text_input("Brand")
        product = col2.text_input("Product")
        audience = st.text_input("Target audience")
        campaign = st.text_input("Campaign name")
        platforms = st.multiselect(
            "Platforms",
            ["Instagram", "TikTok", "Facebook", "LinkedIn", "X (Twitter)", "YouTube Shorts"],
            default=["Instagram", "TikTok"],
        )
        tone = st.text_input("Tone", placeholder="e.g. playful, premium, bold")
        num_assets = st.slider("Number of assets", 2, 20, 6)

        submitted = st.form_submit_button("Run Pipeline", type="primary")

    if submitted:
        if not all([brand, product, audience, campaign, platforms, tone]):
            st.warning("Please fill in all fields.")
        else:
            brief = {
                "brand": brand, "product": product, "audience": audience,
                "campaign": campaign, "platforms": platforms, "tone": tone,
                "num_assets": num_assets,
            }

            log_placeholder = st.empty()
            with st.spinner("Agents are producing your campaign..."):
                final_state = run_pipeline(brief)

            with log_placeholder.container():
                st.subheader("🔄 Agent Activity Log")
                for entry in activity_logger.get_entries():
                    st.markdown(f"`{entry['timestamp']}` **[{entry['agent']}]** {entry['message']}")

            st.session_state["final_state"] = final_state

    if "final_state" in st.session_state:
        state = st.session_state["final_state"]
        st.divider()
        st.success(f"Campaign package ready at: `{state['campaign_folder']}`")

        with st.expander("📈 Strategy"):
            st.markdown(state["strategy"])

        with st.expander("🗓️ Content Ideas / Calendar"):
            st.json(state["content_ideas"])

        with st.expander("✍️ Captions"):
            for c in state["captions"]:
                st.markdown(f"**{c['id']}**: {c['caption']}")

        with st.expander("🎨 Visual Concepts"):
            for v in state["visual_concepts"]:
                st.markdown(f"**{v['id']}**: {v['concept']}")

        with st.expander("🖼️ Generated Images"):
            for img in state["generated_images"]:
                st.image(img["file_path"], caption=img["id"], width=300)

        with st.expander("🎬 Video Scripts + Sora 2 Prompts"):
            for v in state["video_scripts"]:
                st.markdown(f"**{v['id']} — Script**")
                st.text(v["script"])
                st.markdown(f"**{v['id']} — Sora 2 Prompt**")
                st.code(v["sora_prompt"])

        with st.expander("✅ QC Report"):
            st.markdown(state["qc_report"])

# ---------------------------------------------------------------------------
# TAB 2 — Manual video generation (Sora 2), separate from the automatic pipeline
# ---------------------------------------------------------------------------
with tab_video_studio:
    st.caption("Pick a video prompt produced by the pipeline and generate the actual clip "
               "with Sora 2. This step is manual and billed per second — it never runs automatically.")

    if "final_state" not in st.session_state or not st.session_state["final_state"]["video_scripts"]:
        st.info("Run the pipeline first with at least one video asset to unlock this step.")
    else:
        state = st.session_state["final_state"]
        options = {v["id"]: v for v in state["video_scripts"]}
        selected_id = st.selectbox("Select a video asset", list(options.keys()))
        selected = options[selected_id]

        st.text_area("Sora 2 prompt (editable)", value=selected["sora_prompt"], key="sora_prompt_edit", height=120)
        seconds = st.slider("Clip length (seconds)", 4, 20, 8)

        st.warning(f"Estimated cost: ~${seconds * 0.10:.2f} (standard 720p, sora-2 model)")

        if st.button("🎬 Generate Video", type="primary"):
            save_path = os.path.join(state["campaign_folder"], "final_assets", "videos", f"{selected_id}.mp4")
            with st.spinner("Generating video with Sora 2... this can take a minute."):
                try:
                    path = generate_video(
                        prompt=st.session_state["sora_prompt_edit"],
                        save_path=save_path,
                        seconds=seconds,
                    )
                    st.success(f"Video saved to: {path}")
                    st.video(path)
                except Exception as e:
                    st.error(f"Video generation failed: {e}")