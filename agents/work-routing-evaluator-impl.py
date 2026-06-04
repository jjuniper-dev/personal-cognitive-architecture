"""
PCA Work Routing Evaluator -- standalone CLI
Evaluates bot output against a work package's success criteria.

Usage:
    python work-routing-evaluator-impl.py <work_package.json> <bot_output.json>

Output:
    JSON eval result to stdout

Requires:
    ANTHROPIC_API_KEY env var
    anthropic >= 0.49.0  (pip install anthropic)
"""

import json
import os
import sys
from datetime import datetime, timezone
import anthropic

SYSTEM_PROMPT = """You are the PCA work routing evaluator. Assess whether a bot completed a work package successfully.

You receive:
1. The original work package (goal + success criteria)
2. The bot's reported output

Evaluate each success criterion as PASS, PARTIAL, or FAIL.
- PASS: criterion is clearly met with evidence
- PARTIAL: criterion is partially met or evidence is ambiguous
- FAIL: criterion is not met or evidence is absent

Make an overall decision:
- GO: all criteria PASS (or trivial PARTIALs with no blockers)
- NEEDS-REVISION: any PARTIAL, or exactly 1 recoverable FAIL
- NO-GO: 2+ FAILs, core goal not met, or bot output missing

Return ONLY valid JSON, no prose:
{
  "criteria_results": [
    {"id": "SC-1", "verdict": "PASS|PARTIAL|FAIL", "reason": "one sentence max"}
  ],
  "overall_decision": "GO|NEEDS-REVISION|NO-GO",
  "confidence": 0.85,
  "exec_summary": [
    "What was done (1 sentence)",
    "What passed / what failed (1 sentence)",
    "Recommended next action (1 sentence)"
  ],
  "blockers": ["blocker description if any"],
  "recommended_actions": ["specific action if NEEDS-REVISION or NO-GO"]
}"""


def evaluate(work_package: dict, bot_output: dict) -> dict:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": json.dumps({"work_package": work_package, "bot_output": bot_output}, indent=2)
        }]
    )
    result = json.loads(response.content[0].text)
    result["evaluated_at"] = datetime.now(timezone.utc).isoformat()
    result["work_package_id"] = work_package.get("work_package_id", "")
    result["work_package_title"] = work_package.get("title", "")
    result["assigned_bot"] = work_package.get("assigned_bot", "")
    result["sprint"] = work_package.get("sprint", "")
    return result


def main():
    if len(sys.argv) != 3:
        print("Usage: python work-routing-evaluator-impl.py <work_package.json> <bot_output.json>",
              file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1]) as f:
        work_package = json.load(f)
    with open(sys.argv[2]) as f:
        bot_output = json.load(f)
    result = evaluate(work_package, bot_output)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
