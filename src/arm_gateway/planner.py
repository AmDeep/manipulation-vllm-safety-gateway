from __future__ import annotations

import json
import os
import urllib.request


class PlannerUnavailable(RuntimeError):
    pass


def plan_from_vllm(task: str, current_joints_rad: dict[str, float]) -> dict[str, float]:
    model = os.environ.get("VLLM_MODEL")
    if not model:
        raise PlannerUnavailable("VLLM_MODEL is not configured")
    prompt = "Return JSON only with six target joint values in radians named joint_1 through joint_6. Task: " + task + " Current: " + json.dumps(current_joints_rad)
    payload = json.dumps({"model": model, "temperature": 0, "messages": [{"role": "user", "content": prompt}]}).encode()
    request = urllib.request.Request(os.environ.get("VLLM_BASE_URL", "http://localhost:8000/v1").rstrip("/") + "/chat/completions", data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            content = json.loads(response.read().decode())["choices"][0]["message"]["content"]
        value = json.loads(content)
        return {joint: float(value[joint]) for joint in ("joint_1", "joint_2", "joint_3", "joint_4", "joint_5", "joint_6")}
    except (OSError, KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError) as error:
        raise PlannerUnavailable(str(error)) from error
