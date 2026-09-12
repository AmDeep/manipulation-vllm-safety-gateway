from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JointWaypoint:
    time_s: float
    joints_rad: dict[str, float]


def linear_trajectory(start: dict[str, float], target: dict[str, float], duration_s: float, steps: int = 20) -> list[JointWaypoint]:
    if duration_s <= 0 or steps < 2 or set(start) != set(target):
        raise ValueError("trajectory requires matching joints, positive duration, and at least two steps")
    waypoints: list[JointWaypoint] = []
    for index in range(steps):
        ratio = index / (steps - 1)
        waypoints.append(JointWaypoint(duration_s * ratio, {joint: start[joint] + (target[joint] - start[joint]) * ratio for joint in start}))
    return waypoints
