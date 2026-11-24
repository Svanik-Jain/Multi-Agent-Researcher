
import json
import re

from config import ask_gemini


def extract_visual_data(topic, research_data, analysis, fact_check):

    prompt = f"""
You are a research data extraction specialist.

Your task is to extract numerical data and insights
from the research reports below for visualization.

TOPIC:
{topic}

RESEARCH:
{research_data}

ANALYSIS:
{analysis}

FACT CHECK:
{fact_check}

Return ONLY valid JSON. Do not use Markdown code fences.

Use this exact structure:

{{
    "key_metrics": [
        {{
            "name": "Metric name",
            "value": 100,
            "unit": "million",
            "context": "What this number represents",
            "source_url": "Exact source URL",
            "source_id": "Source ID if available"
        }}
    ],

    "time_series": [
        {{
            "metric": "Metric name",
            "unit": "Percentage",
            "points": [
                {{
                    "period": "2022",
                    "value": 20,
                    "source_url": "Exact source URL",
                    "source_id": "Source ID"
                }}
            ]
        }}
    ],

    "comparisons": [
        {{
            "metric": "Metric being compared",
            "unit": "Revenue in USD millions",
            "items": [
                {{
                    "name": "Company A",
                    "value": 100,
                    "source_url": "Exact source URL",
                    "source_id": "Source ID"
                }}
            ]
        }}
    ],

    "opportunities": [
        {{
            "title": "Opportunity",
            "description": "Explanation"
        }}
    ],

    "risks": [
        {{
            "title": "Risk",
            "description": "Explanation"
        }}
    ]
}}

IMPORTANT RULES:

1. Extract only information explicitly supported by the reports.
2. Never invent numbers, dates, statistics or comparisons.
3. Every numerical data point must have a traceable source URL
   or source ID from the provided reports.
4. Do not mix different units in the same chart.
5. Do not assume missing values.
6. Only include time-series data when actual dated values exist.
7. Only include comparisons when the compared values are
   genuinely comparable.
8. Exclude contradicted claims.
9. Treat unverified claims as unsuitable for numerical charts.
10. Partially verified claims must be clearly qualified.
11. If no suitable data exists, return an empty array.
12. Return valid JSON only.
"""

    response = ask_gemini(prompt)

    # Remove accidental Markdown code fences
    cleaned_response = re.sub(
        r"^```(?:json)?\s*|\s*```$",
        "",
        response.strip(),
        flags=re.IGNORECASE
    )

    try:
        data = json.loads(cleaned_response)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Visual data extraction returned invalid JSON: {error}"
        )

    return data
