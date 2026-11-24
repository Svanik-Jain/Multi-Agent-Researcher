
import json
from config import ask_gemini


def extract_claims(topic, research_data, analysis):

    print("\n[Fact Checker] Extracting claims...")

    prompt = f"""
You are a professional fact-checking researcher.

Extract important factual claims from the following
research and analysis reports.

TOPIC:
{topic}

RESEARCH:
{research_data}

ANALYSIS:
{analysis}

Identify claims involving:
- Statistics and numbers
- Company information
- Dates and historical events
- Market developments
- Financial information
- Important industry statements

Do not extract opinions, recommendations or predictions
as factual claims.

Prioritize claims that are important to the overall report.

Return ONLY valid JSON in this format:

{{
    "claims": [
        {{
            "claim_id": 1,
            "claim": "The factual statement",
            "importance": "high",
            "verification_query": "Search query to verify this claim"
        }}
    ]
}}

Extract at most 15 claims.
Do not invent additional claims.
"""

    response = ask_gemini(prompt)

    try:
        cleaned = response.strip()

        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1]
            cleaned = cleaned.rsplit("```", 1)[0]

        data = json.loads(cleaned)

        return data.get("claims", [])

    except json.JSONDecodeError:
        raise ValueError(
            "Gemini did not return valid JSON during claim extraction."
        )


def verify_claims(claims, search_web):

    print("\n[Fact Checker] Searching for supporting evidence...")

    verified_evidence = []

    for item in claims:

        claim_id = item.get("claim_id")
        claim = item.get("claim")
        query = item.get("verification_query", claim)

        print(f"\nChecking claim {claim_id}: {claim}")

        try:
            results = search_web(query, max_results=5)

            verified_evidence.append({
                "claim_id": claim_id,
                "claim": claim,
                "importance": item.get("importance"),
                "evidence": results
            })

        except Exception as e:

            print(f"Search failed: {e}")

            verified_evidence.append({
                "claim_id": claim_id,
                "claim": claim,
                "importance": item.get("importance"),
                "evidence": [],
                "error": str(e)
            })

    return verified_evidence


def evaluate_claims(topic, claims, evidence):

    print("\n[Fact Checker] Evaluating evidence...")

    prompt = f"""
You are the final verification stage of a professional
AI research system.

Your task is to evaluate factual claims using
independently collected web search evidence.

TOPIC:
{topic}

EXTRACTED CLAIMS:
{json.dumps(claims, indent=2)}

INDEPENDENT SEARCH EVIDENCE:
{json.dumps(evidence, indent=2)}

FOR EACH CLAIM:

1. Compare the original claim with the evidence.
2. Determine whether the evidence actually supports it.
3. Look for contradictory information.
4. Check whether the information may be outdated.
5. Identify whether the source is authoritative.
6. Explain your reasoning.
7. Include relevant source URLs.

ALLOWED VERDICTS:

- VERIFIED: Reliable evidence supports the claim.
- PARTIALLY VERIFIED: Some parts are supported,
  but the complete claim is not.
- UNVERIFIED: Available evidence is insufficient.
- CONTRADICTED: Reliable evidence conflicts with the claim.

IMPORTANT RULES:

- Search snippets alone are not definitive proof.
- Do not assume a claim is true because multiple
  websites repeat it.
- Give greater weight to primary sources,
  official reports and credible publications.
- Never invent URLs or sources.
- Do not convert predictions into established facts.
- If evidence is missing, use UNVERIFIED.
- Explain conflicting evidence.
- A claim must not be marked VERIFIED simply
  because the original research report included a source.

OUTPUT FORMAT:

# Fact-Checking Report

## 1. Executive Summary

## 2. Claim-by-Claim Verification

For each claim include:
- Claim ID
- Original claim
- Verdict
- Supporting evidence
- Contradictory evidence
- Source URLs
- Explanation

## 3. Incorrect or Misleading Claims

## 4. Unsupported Claims

## 5. Recommended Corrections

## 6. Final Verification Summary

Clearly distinguish between verified information
and information that still requires human review.
"""

    report = ask_gemini(prompt)

    return report


def fact_check(topic, research_data, analysis, search_web):

    print("\nFact-Checker Agent Started")

    # Stage 1: Extract claims
    claims = extract_claims(
        topic,
        research_data,
        analysis
    )

    print(f"\nExtracted {len(claims)} claims.")

    if not claims:
        return "No factual claims were extracted for verification."

    # Stage 2: Independently search for evidence
    evidence = verify_claims(
        claims,
        search_web
    )

    # Stage 3: Evaluate claims
    report = evaluate_claims(
        topic,
        claims,
        evidence
    )

    print("\nFact-Checker Agent Completed")

    return report
