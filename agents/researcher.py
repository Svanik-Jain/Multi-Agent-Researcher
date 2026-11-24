
import json
from config import ask_gemini


def generate_search_queries(topic):

    prompt = f"""
    You are an expert research strategist.

    Research topic: {topic}

    Generate 5 different web search queries that
    will help thoroughly investigate this topic.

    Cover:
    1. Background and fundamentals
    2. Latest developments
    3. Companies, people or real-world examples
    4. Statistics and supporting evidence
    5. Challenges, opportunities and future trends

    Return ONLY a numbered list of search queries.
    Do not include explanations.
    """

    response = ask_gemini(prompt)

    queries = []

    for line in response.splitlines():
        line = line.strip()

        if line:
            query = line.lstrip("0123456789.-) ").strip()

            if query:
                queries.append(query)

    return queries[:5]


def collect_search_results(queries, search_web):

    all_results = []
    seen_urls = set()

    for query in queries:

        print(f"Searching: {query}")

        try:
            results = search_web(query, max_results=6)

            for result in results:

                url = result.get("url")

                if not url or url in seen_urls:
                    continue

                seen_urls.add(url)

                result["search_query"] = query

                all_results.append(result)

        except Exception as e:
            print(f"Search failed for '{query}': {e}")

    return all_results


def organize_research(topic, search_results):

    if not search_results:
        return "Research failed: No search results were collected."

    sources = []

    for index, result in enumerate(search_results, start=1):

        sources.append({
            "source_id": f"S{index}",
            "title": result.get("title"),
            "url": result.get("url"),
            "description": result.get("body"),
            "search_query": result.get("search_query")
        })

    prompt = f"""
    You are an expert research analyst working as
    the Researcher Agent in a multi-agent AI system.

    Your task is to collect and organize information.
    Do not write a final article or give personal opinions.

    RESEARCH TOPIC:
    {topic}

    SEARCH RESULTS:
    {json.dumps(sources, indent=2)}

    INSTRUCTIONS:

    1. Organize the information into relevant sections.
    2. Identify important facts, statistics and developments.
    3. Include company names, examples and case studies
       where relevant.
    4. Identify different perspectives and viewpoints.
    5. Include relevant opportunities and challenges.
    6. Attach source IDs such as [S1], [S2] to claims
       supported by the supplied search results.
    7. Never invent statistics, quotations or sources.
    8. If information is insufficient, explicitly say so.
    9. Distinguish factual information from interpretations.
    10. Preserve conflicting findings instead of hiding them.

    OUTPUT FORMAT:

    # Research Topic

    ## 1. Background
    ## 2. Key Findings
    ## 3. Important Statistics
    ## 4. Companies and Real-World Examples
    ## 5. Recent Developments
    ## 6. Opportunities
    ## 7. Challenges
    ## 8. Unanswered Questions
    ## 9. Source References

    Remember: You are only the Researcher Agent.
    Your output will be passed to another AI agent
    for deeper analysis and fact-checking.
    """

    research = ask_gemini(prompt)

    source_list = "\n\n## Collected Sources\n"

    for source in sources:
        source_list += (
            f"\n[{source['source_id']}] "
            f"{source['title']}\n"
            f"URL: {source['url']}\n"
        )

    return research + source_list


def research(topic, search_web):

    print("\nResearcher Agent Started")

    # Step 1: Generate search queries
    queries = generate_search_queries(topic)

    print("\nGenerated Search Queries:")
    for query in queries:
        print("-", query)

    # Step 2: Search the web
    search_results = collect_search_results(
        queries,
        search_web
    )

    print(f"\nCollected {len(search_results)} unique sources.")

    # Step 3: Organize research
    research_data = organize_research(
        topic,
        search_results
    )

    print("\nResearcher Agent Completed")

    return research_data
