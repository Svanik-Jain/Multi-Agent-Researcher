
import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")

if not api_key:
    raise ValueError("TAVILY_API_KEY missing from .env")

client = TavilyClient(api_key=api_key)


def search_web(query, max_results=8):

    print(f"\n[Tavily] Searching: {query}")

    try:
        response = client.search(
            query=query,
            search_depth="basic",
            max_results=max_results,
            include_answer=False
        )

        formatted_results = []

        for result in response.get("results", []):

            formatted_results.append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "body": result.get("content", ""),
                "score": result.get("score", 0)
            })

        print(
            f"[Tavily] Found {len(formatted_results)} results"
        )

        return formatted_results

    except Exception as e:

        print(f"[Tavily ERROR] {type(e).__name__}: {e}")

        return []
