import json

from agents.researcher import research
from agents.analyst import analyse
from agents.fact_checker import fact_check
from agents.writer import write_report

from tools.web_search import search_web
from visualizations.data_extractor import extract_visual_data


def run_research_pipeline(topic, progress_callback=None):

    results = {}

    def update_progress(step, message):

        print(f"\n[{step}/5] {message}")

        if progress_callback:
            progress_callback(step, message)

    print("\n" + "=" * 60)
    print("          MULTI-AGENT AI RESEARCH SYSTEM")
    print("=" * 60)

    # ==========================================
    # AGENT 1: RESEARCHER
    # ==========================================

    update_progress(
        1,
        "Researcher Agent is collecting information..."
    )

    research_data = research(topic, search_web)

    results["research"] = research_data

    with open("research.md", "w", encoding="utf-8") as file:
        file.write(research_data)

    print("Research saved: research.md")

    # ==========================================
    # AGENT 2: ANALYST
    # ==========================================

    update_progress(
        2,
        "Analyst Agent is identifying patterns and insights..."
    )

    analysis = analyse(topic, research_data)

    results["analysis"] = analysis

    with open("analysis.md", "w", encoding="utf-8") as file:
        file.write(analysis)

    print("Analysis saved: analysis.md")

    # ==========================================
    # AGENT 3: FACT CHECKER
    # ==========================================

    update_progress(
        3,
        "Fact-Checker Agent is verifying claims..."
    )

    verified_data = fact_check(
        topic,
        research_data,
        analysis,
        search_web
    )

    results["fact_check"] = verified_data

    with open(
        "fact_check_output.md",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(verified_data)

    print("Fact check saved: fact_check_output.md")

    # ==========================================
    # AGENT 4: VISUAL INSIGHTS ENGINE
    # ==========================================

    update_progress(
        4,
        "Visual Insights Engine is extracting structured data..."
    )

    visual_data = extract_visual_data(
        topic,
        research_data,
        analysis,
        verified_data
    )

    results["visual_data"] = visual_data

    with open(
        "visual_data.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            visual_data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("Visual data saved: visual_data.json")

    # ==========================================
    # AGENT 5: WRITER
    # ==========================================

    update_progress(
        5,
        "Writer Agent is preparing the final report..."
    )

    final_report = write_report(
        topic,
        research_data,
        analysis,
        verified_data
    )

    results["final_report"] = final_report

    with open(
        "final_report.md",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(final_report)

    print("Final report saved: final_report.md")

    # ==========================================
    # COMPLETION
    # ==========================================

    print("\n" + "=" * 60)
    print("          RESEARCH PIPELINE COMPLETED")
    print("=" * 60)

    if progress_callback:
        progress_callback(
            6,
            "All research stages completed successfully!"
        )

    print("\nGenerated files:")
    print("1. research.md")
    print("2. analysis.md")
    print("3. fact_check_output.md")
    print("4. visual_data.json")
    print("5. final_report.md")

    return results


# ==========================================
# COMMAND LINE EXECUTION
# ==========================================

if __name__ == "__main__":

    topic = input("\nEnter your research topic: ").strip()

    if not topic:

        print("Please enter a valid research topic.")

    else:

        try:

            run_research_pipeline(topic)

        except Exception as error:

            print("\nPipeline failed!")
            print(
                f"Error: {type(error).__name__}: {error}"
            )
