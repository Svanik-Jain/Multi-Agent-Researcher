
from config import ask_gemini


def write_report(topic, research_data, analysis, verified_data):
    print("\nWriter Agent Started")

    prompt = f"""
You are the Writer Agent in a multi-agent AI research system.

Your responsibility is to produce a comprehensive,
well-structured research report using the outputs of
three previous agents.

RESEARCH TOPIC:
{topic}


RESEARCHER REPORT:
{research_data}


ANALYST REPORT:
{analysis}


FACT-CHECKER REPORT:
{verified_data}


YOUR OBJECTIVE:

Create a high-quality research report that combines
the collected information, analytical insights and
fact-checking results.

WRITING INSTRUCTIONS:

1. EXECUTIVE SUMMARY
- Explain the topic in a few paragraphs.
- Highlight the most important findings.
- Give the reader a clear understanding of the subject.

2. BACKGROUND AND CONTEXT
- Explain the fundamentals.
- Introduce relevant companies, technologies or industries.
- Provide context necessary to understand the topic.

3. KEY RESEARCH FINDINGS
- Present the most important facts and developments.
- Include relevant statistics and real-world examples.
- Preserve source IDs such as [S1], [S2].

4. ANALYSIS AND INSIGHTS
- Incorporate the Analyst Agent's strongest insights.
- Explain patterns, business implications and relationships.
- Distinguish evidence from interpretation.

5. OPPORTUNITIES AND CHALLENGES
- Explain potential opportunities.
- Discuss risks, limitations and competitive threats.

6. FUTURE OUTLOOK
- Present possible future developments.
- Clearly distinguish evidence-based predictions
  from speculation.

7. FACT-CHECKING AND RELIABILITY
- Respect the Fact-Checker Agent's verdicts.
- VERIFIED claims may be presented as supported.
- PARTIALLY VERIFIED claims must include qualifications.
- UNVERIFIED claims must be labelled as unverified
  or excluded if they are not essential.
- CONTRADICTED claims must not be presented as facts.
- Explain important disagreements or unresolved claims.

8. CONCLUSION
- Summarize the most important findings.
- Explain what the research ultimately tells us.

9. SOURCES
- Include the source references and URLs supplied
  in the Researcher and Fact-Checker reports.
- Preserve source IDs wherever possible.
- Do not invent URLs or citations.

IMPORTANT RULES:

- Never invent facts, statistics, dates or quotations.
- Never fabricate sources or URLs.
- Do not treat an Analyst interpretation as a verified fact.
- Do not hide contradictions between sources.
- Do not turn speculation into certainty.
- Avoid repetitive information.
- Use clear, professional and engaging language.
- Explain technical concepts in simple language.
- Do not mention the internal agent workflow in the report.
- If evidence is insufficient, explicitly acknowledge it.

OUTPUT FORMAT:

# [Research Topic]

## 1. Executive Summary
## 2. Background and Context
## 3. Key Research Findings
## 4. Analysis and Insights
## 5. Business Implications
## 6. Opportunities and Challenges
## 7. Future Outlook
## 8. Fact-Checking and Reliability
## 9. Conclusion
## 10. Sources

The final report should be detailed enough to serve as
a standalone research document.

Return the report in Markdown format only.
"""

    report = ask_gemini(prompt)

    print("\nWriter Agent Completed")

    return report
