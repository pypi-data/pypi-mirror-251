import pytest
import pytest_check as check

import os


from hcraft.render.human import render_env_with_human
from hcraft.examples import EXAMPLE_ENVS, HCRAFT_GYM_ENVS
from hcraft.examples.minecraft import MineHcraftEnv
from hcraft.examples.minicraft import (
    MiniHCraftKeyCorridor,
    MiniHCraftBlockedUnlockPickup,
    MiniHCraftUnlockPickup,
)
from hcraft.env import HcraftEnv


@pytest.mark.slow
@pytest.mark.parametrize("env_class", EXAMPLE_ENVS)
def test_build_env(env_class):
    human_run = False
    env = env_class()
    if human_run:
        render_env_with_human(env)


KNOWN_TO_FAIL_ENHSP = [
    MineHcraftEnv,
    MiniHCraftBlockedUnlockPickup,
]


@pytest.mark.slow
@pytest.mark.parametrize("env_class", EXAMPLE_ENVS)
def test_pddl_solve(env_class):
    up = pytest.importorskip("unified_planning")
    write = False
    env: HcraftEnv = env_class(max_step=200)
    problem = env.planning_problem(timeout=5)

    if env_class in KNOWN_TO_FAIL_ENHSP:
        pytest.xfail("ENHSP planner is known to fail on this environment")

    if write:
        writer = up.io.PDDLWriter(problem.upf_problem)
        pddl_dir = os.path.join("planning", "pddl", env.name)
        os.makedirs(pddl_dir, exist_ok=True)
        writer.write_domain(os.path.join(pddl_dir, "domain.pddl"))
        writer.write_problem(os.path.join(pddl_dir, "problem.pddl"))

    done = False
    _observation = env.reset()
    while not done:
        action = problem.action_from_plan(env.state)
        _observation, _reward, done, _ = env.step(action)
    check.is_true(env.purpose.terminated, msg=f"Plan was :{problem.plans}")
    check.equal(env.current_step, problem.stats[0]["Plan-Length"])


KNOWN_TO_FAIL_HEBG = [
    MineHcraftEnv,
    MiniHCraftBlockedUnlockPickup,
    MiniHCraftUnlockPickup,
    MiniHCraftKeyCorridor,
]


@pytest.mark.slow
@pytest.mark.parametrize("env_class", EXAMPLE_ENVS)
def test_can_solve(env_class):
    env: HcraftEnv = env_class(max_step=50)
    if env_class in KNOWN_TO_FAIL_HEBG:
        pytest.xfail("Hebg is known to fail on this environment")
    done = False
    observation = env.reset()
    for task in env.purpose.best_terminal_group.tasks:
        solving_behavior = env.solving_behavior(task)
        task_done = task.terminated
        while not task_done and not done:
            action = solving_behavior(observation)
            if action == "Impossible":
                raise ValueError("Solving behavior could not find a solution.")
            observation, _reward, done, _ = env.step(action)
            task_done = task.terminated
    check.is_true(env.purpose.terminated)


@pytest.mark.slow
@pytest.mark.parametrize("env_gym_id", HCRAFT_GYM_ENVS)
def test_gym_make(env_gym_id):
    gym = pytest.importorskip("gym")
    gym.make(env_gym_id)


@pytest.mark.slow
@pytest.mark.parametrize("env_class", EXAMPLE_ENVS)
def test_requirements_graph(env_class):
    draw = True
    save = False
    env: HcraftEnv = env_class()
    requirements = env.world.requirements
    requirements.graph
    if draw:
        import matplotlib.pyplot as plt

        width = max(requirements.depth, 10)
        height = max(9 / 16 * width, requirements.width / requirements.depth * width)

        fig, ax = plt.subplots()
        plt.tight_layout()
        fig.set_size_inches(width, height)
        requirements.draw(ax)

        resolution = max(64 * requirements.depth, 900)

        if save:
            requirements_dir = os.path.join("docs", "images", "requirements_graphs")
            os.makedirs(requirements_dir, exist_ok=True)

            filename = os.path.join(requirements_dir, f"{env.name}.png")
            fig.savefig(filename, dpi=resolution / width, transparent=True)

        plt.close()
