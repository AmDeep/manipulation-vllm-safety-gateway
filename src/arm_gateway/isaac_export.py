from __future__ import annotations

import json
from pathlib import Path

from .trajectory import JointWaypoint


def write_trajectory(path: Path, waypoints: list[JointWaypoint], frame_id: str = "world") -> None:
    """Write a simulator-neutral trajectory consumed by an Isaac Sim adapter."""
    payload = {"frame_id": frame_id, "waypoints": [{"time_s": point.time_s, "joints_rad": point.joints_rad} for point in waypoints]}
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
