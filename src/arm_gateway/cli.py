from __future__ import annotations

import argparse
import json
from pathlib import Path

from .limits import DEFAULT_LIMITS
from .planner import PlannerUnavailable, plan_from_vllm
from .safety import validate_request, validate_target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", type=Path)
    parser.add_argument("--plan", type=Path, help="use a plan captured from a real vLLM response")
    args = parser.parse_args()
    request = json.loads(args.request.read_text(encoding="utf-8"))
    valid, errors = validate_request(request)
    if not valid:
        print(json.dumps({"status": "rejected", "errors": errors}, sort_keys=True))
        return
    try:
        target = json.loads(args.plan.read_text(encoding="utf-8")) if args.plan else request.get("target_joints_rad")
        if target is None:
            target = plan_from_vllm(request["task"], request["current_joints_rad"])
    except PlannerUnavailable as error:
        print(json.dumps({"request_id": request["request_id"], "status": "planner_unavailable", "reason": str(error)}, sort_keys=True))
        return
    safe, errors = validate_target(request["current_joints_rad"], target, DEFAULT_LIMITS)
    status = "approved_dry_run" if safe and not request["execute"] else "rejected"
    print(json.dumps({"request_id": request["request_id"], "status": status, "errors": errors, "target_joints_rad": target}, sort_keys=True))


if __name__ == "__main__":
    main()
