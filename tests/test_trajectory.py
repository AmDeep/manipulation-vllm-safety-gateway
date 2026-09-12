from arm_gateway.trajectory import linear_trajectory


def test_trajectory_has_monotonic_time_and_endpoints() -> None:
    waypoints = linear_trajectory({"joint_1": 0.0}, {"joint_1": 1.0}, 2.0, steps=3)
    assert [point.time_s for point in waypoints] == [0.0, 1.0, 2.0]
    assert waypoints[-1].joints_rad["joint_1"] == 1.0
