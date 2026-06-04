#!/usr/bin/env python3
"""
Work Routing Evaluator Implementation

CLI and HTTP client for the PCA work routing evaluation loop.
Submits {work_package, bot_output} to WF-Eval and prints the result.
Can also run as a FastAPI service for programmatic use.

Usage (CLI):
    python work-routing-evaluator-impl.py --eval eval-payload.json
    python work-routing-evaluator-impl.py --work-package wp.json --bot-output out.json
    cat eval-payload.json | python work-routing-evaluator-impl.py --stdin

See templates/work-package.json for the expected payload format.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from typing import Any

DEFAULT_EVAL_URL = os.getenv("PCA_EVAL_URL", "http://localhost:5678/webhook/pca/eval")
REQUEST_TIMEOUT = int(os.getenv("PCA_EVAL_TIMEOUT", "60"))


def post_eval(payload: dict, url: str) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {error_body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Connection failed: {e.reason}") from e


def format_result(result: dict) -> str:
    lines = [
        f"Decision:   {result.get('overall_decision', 'unknown')}",
        f"Confidence: {result.get('confidence', 0.0):.2f}",
        f"WP:         {result.get('work_package_id', '')} — {result.get('work_package_title', '')}",
        "",
        "Executive Summary:",
    ]
    for bullet in result.get("exec_summary", []):
        lines.append(f"  - {bullet}")

    criteria = result.get("criteria_results", [])
    if criteria:
        lines.append("")
        lines.append("Criteria:")
        for c in criteria:
            lines.append(f"  [{c.get('verdict', '?'):7s}] {c.get('id', '')}: {c.get('reason', '')}")

    blockers = result.get("blockers", [])
    if blockers:
        lines.append("")
        lines.append("Blockers:")
        for b in blockers:
            lines.append(f"  - {b}")

    actions = result.get("recommended_actions", [])
    if actions:
        lines.append("")
        lines.append("Recommended Actions:")
        for a in actions:
            lines.append(f"  - {a}")

    return "\n".join(lines)


def load_json_file(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Submit a PCA work package evaluation to WF-Eval."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--eval",
        metavar="FILE",
        help="JSON file with full {work_package, bot_output} payload",
    )
    group.add_argument(
        "--stdin",
        action="store_true",
        help="Read full {work_package, bot_output} payload from stdin",
    )
    parser.add_argument(
        "--work-package",
        metavar="FILE",
        help="JSON file with work_package object (use with --bot-output)",
    )
    parser.add_argument(
        "--bot-output",
        metavar="FILE",
        help="JSON file with bot_output object (use with --work-package)",
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_EVAL_URL,
        help=f"WF-Eval webhook URL (default: {DEFAULT_EVAL_URL})",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_out",
        help="Print raw JSON result instead of formatted output",
    )
    args = parser.parse_args()

    if args.work_package and args.bot_output:
        payload = {
            "work_package": load_json_file(args.work_package),
            "bot_output": load_json_file(args.bot_output),
        }
    elif args.eval:
        payload = load_json_file(args.eval)
    elif args.stdin:
        payload = json.load(sys.stdin)
    else:
        parser.print_help()
        return 2

    if "work_package" not in payload or "bot_output" not in payload:
        print("ERROR: payload must have 'work_package' and 'bot_output' keys", file=sys.stderr)
        return 2

    try:
        result = post_eval(payload, args.url)
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    if args.json_out:
        print(json.dumps(result, indent=2))
    else:
        print(format_result(result))

    decision = result.get("overall_decision", "")
    return 0 if decision == "GO" else 1


# FastAPI service (optional — run with: uvicorn work-routing-evaluator-impl:app)
try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    from typing import List

    app = FastAPI(title="PCA Work Routing Evaluator", version="1.0.0")

    class SuccessCriterion(BaseModel):
        id: str
        description: str
        verifiable_by: str = "human-review"

    class WorkPackage(BaseModel):
        work_package_id: str
        title: str
        goal: str
        success_criteria: List[SuccessCriterion]
        assigned_bot: str
        sprint: str

    class BotOutput(BaseModel):
        summary: str
        deliverables: List[str] = []
        tests_passed: bool = False
        verification_notes: str = ""

    class EvalRequest(BaseModel):
        work_package: WorkPackage
        bot_output: BotOutput

    class EvalResponse(BaseModel):
        overall_decision: str
        confidence: float
        criteria_results: list
        exec_summary: List[str]
        blockers: List[str] = []
        recommended_actions: List[str] = []
        evaluated_at: str
        work_package_id: str
        work_package_title: str
        assigned_bot: str
        sprint: str

    @app.post("/eval", response_model=EvalResponse)
    async def evaluate(request: EvalRequest) -> EvalResponse:
        eval_url = os.getenv("PCA_EVAL_URL", "http://localhost:5678/webhook/pca/eval")
        try:
            result = post_eval(request.dict(), eval_url)
        except RuntimeError as e:
            raise HTTPException(status_code=502, detail=str(e))
        return EvalResponse(**result)

    @app.get("/health")
    async def health():
        return {
            "status": "healthy",
            "agent": "work-routing-evaluator",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

except ImportError:
    pass


if __name__ == "__main__":
    sys.exit(main())
