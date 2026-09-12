from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JointLimit:
    minimum_rad: float
    maximum_rad: float
    max_step_rad: float


DEFAULT_LIMITS = {
    "joint_1": JointLimit(-3.14, 3.14, 0.35),
    "joint_2": JointLimit(-1.57, 1.57, 0.35),
    "joint_3": JointLimit(-2.8, 2.8, 0.45),
    "joint_4": JointLimit(-3.14, 3.14, 0.55),
    "joint_5": JointLimit(-2.0, 2.0, 0.55),
    "joint_6": JointLimit(-6.28, 6.28, 0.8),
}
