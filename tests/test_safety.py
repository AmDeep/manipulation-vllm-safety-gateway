from arm_gateway.limits import DEFAULT_LIMITS
from arm_gateway.safety import validate_target


def test_safe_target_is_approved() -> None:
    current = {joint: 0.0 for joint in DEFAULT_LIMITS}
    target = {joint: 0.1 for joint in DEFAULT_LIMITS}
    assert validate_target(current, target, DEFAULT_LIMITS)[0]


def test_large_step_is_rejected() -> None:
    current = {joint: 0.0 for joint in DEFAULT_LIMITS}
    target = {joint: 0.1 for joint in DEFAULT_LIMITS}
    target["joint_1"] = 1.0
    accepted, errors = validate_target(current, target, DEFAULT_LIMITS)
    assert not accepted
    assert "single-cycle" in " ".join(errors)
