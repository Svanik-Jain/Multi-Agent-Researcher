
import json
import streamlit as st

from main import run_research_pipeline
from visualizations.charts import display_visualizations


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Research Studio",
    page_icon="🔬",
    layout="wide"
)


# ==========================================
# SESSION STATE
# ==========================================

if "results" not in st.session_state:
    st.session_state.results = None

if "topic" not in st.session_state:
    st.session_state.topic = ""

if "running" not in st.session_state:
    st.session_state.running = False


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1300px;
}

.hero {
    padding: 30px;
    border-radius: 15px;
    background: linear-gradient(
        120deg,
        #172554,
        #312e81
    );
    margin-bottom: 30px;
}

.hero h1 {
    color: white;
    font-size: 40px;
    margin-bottom: 10px;
}

.hero p {
    color: #cbd5e1;
    font-size: 16px;
}

.agent-card {
    padding: 15px;
    border-radius: 10px;
    background-color: rgba(128,128,128,0.10);
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("🔬 Research Studio")

    st.caption("Multi-Agent AI Research System")

    st.divider()

    st.subheader("Your AI Team")

    agents = [
        ("🔎", "Researcher", "Collects information"),
        ("🧠", "Analyst", "Finds patterns and insights"),
        ("✔️", "Fact-Checker", "Verifies claims"),
        ("📊", "Visual Insights", "Creates data visualizations"),
        ("✍️", "Writer", "Produces the final report")
    ]

    for icon, name, description in agents:

        st.markdown(
            f"""
            <div class="agent-card">
                <strong>{icon} {name}</strong><br>
                <small>{description}</small>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.caption("Powered by Gemini and Tavily")


# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="hero">

<h1>AI Research Studio</h1>

<p>
Transform research questions into structured,
analysed, fact-checked and visualized reports.
</p>

</div>
""", unsafe_allow_html=True)


# ==========================================
# RESEARCH INPUT
# ==========================================

st.subheader("Start a new research project")

topic = st.text_area(
    "Research Topic",
    value=st.session_state.topic,
    placeholder=(
        "Example: How are AI agents changing SaaS businesses?"
    ),
    height=110
)


# ==========================================
# START BUTTON
# ==========================================

start_button = st.button(
    "🚀 Start Research",
    type="primary",
    use_container_width=True,
    disabled=st.session_state.running
)


if start_button:

    if not topic.strip():

        st.warning("Please enter a research topic.")

    else:

        st.session_state.results = None
        st.session_state.topic = topic.strip()
        st.session_state.running = True

        progress_bar = st.progress(0)

        status_text = st.empty()

        agent_text = st.empty()

        progress_values = {
            1: 10,
            2: 30,
            3: 50,
            4: 70,
            5: 90,
            6: 100
        }

        agent_names = {
            1: "Researcher Agent",
            2: "Analyst Agent",
            3: "Fact-Checker Agent",
            4: "Visual Insights Engine",
            5: "Writer Agent",
            6: "Completed"
        }

        # ----------------------------------
        # PROGRESS CALLBACK
        # ----------------------------------

        def update_progress(step, message):

            progress_bar.progress(
                progress_values.get(step, 0)
            )

            status_text.info(message)

            agent_text.markdown(
                f"**Current stage:** "
                f"{agent_names.get(step, 'Processing')}"
            )

        # ----------------------------------
        # RUN PIPELINE
        # ----------------------------------

        try:

            with st.spinner(
                "Your AI research team is working..."
            ):

                results = run_research_pipeline(
                    st.session_state.topic,
                    progress_callback=update_progress
                )

            st.session_state.results = results

            progress_bar.progress(100)

            status_text.success(
                "Research completed successfully!"
            )

            agent_text.markdown(
                "**All five stages completed.**"
            )

        except Exception as error:

            st.error(
                f"Research failed: {type(error).__name__}: {error}"
            )

            with st.expander("Technical error details"):

                st.exception(error)

        finally:

            st.session_state.running = False


# ==========================================
# DISPLAY RESULTS
# ==========================================

if st.session_state.results:

    results = st.session_state.results

    st.divider()

    st.header("Research Dashboard")

    st.markdown(
        f"**Research topic:** {st.session_state.topic}"
    )

    # --------------------------------------
    # RESULT TABS
    # --------------------------------------

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔎 Research",
        "🧠 Analysis",
        "✔️ Fact Check",
        "📊 Visual Insights",
        "📄 Final Report"
    ])

    # --------------------------------------
    # TAB 1: RESEARCH
    # --------------------------------------

    with tab1:

        st.subheader("Research Findings")

        st.markdown(
            results.get(
                "research",
                "No research data available."
            )
        )

        st.download_button(
            "⬇️ Download Research",
            data=results.get("research", ""),
            file_name="research.md",
            mime="text/markdown",
            key="download_research"
        )

    # --------------------------------------
    # TAB 2: ANALYSIS
    # --------------------------------------

    with tab2:

        st.subheader("Analyst Insights")

        st.markdown(
            results.get(
                "analysis",
                "No analysis available."
            )
        )

        st.download_button(
            "⬇️ Download Analysis",
            data=results.get("analysis", ""),
            file_name="analysis.md",
            mime="text/markdown",
            key="download_analysis"
        )

    # --------------------------------------
    # TAB 3: FACT CHECK
    # --------------------------------------

    with tab3:

        st.subheader("Fact-Checking Results")

        st.markdown(
            results.get(
                "fact_check",
                "No fact-checking data available."
            )
        )

        st.download_button(
            "⬇️ Download Fact Check",
            data=results.get("fact_check", ""),
            file_name="fact_check_output.md",
            mime="text/markdown",
            key="download_fact_check"
        )

    # --------------------------------------
    # TAB 4: VISUAL INSIGHTS
    # --------------------------------------

    with tab4:

        visual_data = results.get("visual_data", {})

        st.subheader("Visual Insights Dashboard")

        st.caption(
            "Charts and insights extracted from your research."
        )

        if visual_data:

            display_visualizations(visual_data)

            st.download_button(
                "⬇️ Download Visual Data",
                data=json.dumps(
                    visual_data,
                    indent=4,
                    ensure_ascii=False
                ),
                file_name="visual_data.json",
                mime="application/json",
                key="download_visual_data"
            )

        else:

            st.info(
                "No visual data was generated for this research."
            )

    # --------------------------------------
    # TAB 5: FINAL REPORT
    # --------------------------------------

    with tab5:

        st.subheader("Final Research Report")

        st.markdown(
            results.get(
                "final_report",
                "No final report available."
            )
        )

        st.download_button(
            "⬇️ Download Final Report",
            data=results.get("final_report", ""),
            file_name="final_report.md",
            mime="text/markdown",
            key="download_final_report"
        )


# ==========================================
# EMPTY STATE
# ==========================================

else:

    st.divider()

    st.info(
        "Enter a research topic and start the pipeline. "
        "Your reports and visual insights will appear here."
    )

    st.markdown("### What your research team will produce")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("🔎 **Research**")
        st.caption("Information and sources")

    with col2:
        st.markdown("🧠 **Analysis**")
        st.caption("Patterns and insights")

    with col3:
        st.markdown("✔️ **Verification**")
        st.caption("Evidence-backed claims")

    with col4:
        st.markdown("📊 **Visuals**")
        st.caption("Charts and comparisons")
