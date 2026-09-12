from __future__ import annotations

from typing import Any

from .limits import JointLimit


def validate_target(current: dict[str, float], target: dict[str, float], limits: dict[str, JointLimit]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if set(target) != set(limits):
        errors.append("target joints do not match configured robot joints")
        return False, errors
    for joint, limit in limits.items():
        value = target[joint]
        if not limit.minimum_rad <= value <= limit.maximum_rad:
            errors.append(f"{joint} exceeds absolute limit")
        if abs(value - current.get(joint, value)) > limit.max_step_rad:
            errors.append(f"{joint} exceeds single-cycle step limit")
    return not errors, errors


def validate_request(request: dict[str, Any]) -> tuple[bool, list[str]]:
    required = {"request_id", "current_joints_rad", "target_joints_rad", "execute"}
    missing = required - request.keys()
    if missing:
        return False, [f"missing fields: {sorted(missing)}"]
    return True, []
