"""Tests for domain-runner package."""

from __future__ import annotations

from domain_runner.config import deep_merge
from domain_runner.layer import DomainOnlyLayer
from domain_runner.single import run_simulation
from domain_runner.types import RunContext


class _StubAdapter:
    def __init__(self) -> None:
        self.steps: list[int] = []

    def step(self, step: int) -> None:
        self.steps.append(step)

    def get_ground_truth(self, step: int) -> bool:
        return step > 5

    def get_active_locations(self, step: int) -> list[tuple[int, int]]:
        return [(step, 0)] if step > 5 else []


class _StubHooks:
    domain_name = "stub"
    default_config_path = None

    def load_run_context(self, *, config_path=None, cli_overrides=None) -> RunContext:
        return RunContext(steps=3, seed=1, domain_config={})

    def build_adapter(self, domain_config):
        return _StubAdapter()

    def print_header(self, adapter, run) -> None:
        pass

    def on_step(self, adapter, step, layer_events) -> None:
        pass

    def should_stop(self, adapter, step, layer_events) -> bool:
        return False

    def print_step(self, adapter, step, layer_events, *, verbose) -> None:
        pass

    def summarize(self, adapter, layer_metrics):
        return {"steps_run": len(adapter.steps)}

    def write_output(self, result, path) -> None:
        pass


def test_domain_only_layer_runs_adapter_steps() -> None:
    result = run_simulation(
        _StubHooks(), DomainOnlyLayer(), RunContext(steps=3, seed=1, domain_config={})
    )
    assert result.steps_completed == 3
    assert result.domain_metrics["steps_run"] == 3


def test_deep_merge_nested() -> None:
    base = {"domain": {"seed": 42, "grid_rows": 20}}
    merged = deep_merge(base, {"domain": {"seed": 7}})
    assert merged["domain"]["seed"] == 7
    assert merged["domain"]["grid_rows"] == 20
