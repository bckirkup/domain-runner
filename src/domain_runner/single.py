"""Single simulation run orchestration."""

from __future__ import annotations

import json
import time
from typing import Any

from domain_runner.hooks import DomainHooks
from domain_runner.layer import SimulationLayer
from domain_runner.types import RunContext, SimulationResult


def run_simulation(
    hooks: DomainHooks,
    layer: SimulationLayer,
    run: RunContext,
) -> SimulationResult:
    """Execute one simulation with the given domain hooks and orchestration layer."""
    adapter = hooks.build_adapter(run.domain_config)
    layer_state = layer.setup(adapter, run)
    hooks.print_header(adapter, run)

    steps_completed = 0
    for step in range(run.steps):
        layer_events = layer.step(adapter, step, layer_state)
        hooks.on_step(adapter, step, layer_events)
        hooks.print_step(adapter, step, layer_events, verbose=run.verbose)
        steps_completed = step + 1
        if hooks.should_stop(adapter, step, layer_events):
            break

    layer_metrics = layer.finalize(adapter, layer_state, run)
    domain_metrics = hooks.summarize(adapter, layer_metrics)

    result = SimulationResult(
        domain=hooks.domain_name,
        layer=layer.name,
        steps_completed=steps_completed,
        seed=run.seed,
        wall_time_seconds=0.0,
        domain_config=run.domain_config,
        domain_metrics=domain_metrics,
        layer_metrics=layer_metrics,
        output_path=run.output_path,
    )
    return result


def run_simulation_timed(
    hooks: DomainHooks,
    layer: SimulationLayer,
    run: RunContext,
) -> SimulationResult:
    """Run simulation and record wall time; optionally write JSON output."""
    start = time.time()
    result = run_simulation(hooks, layer, run)
    result.wall_time_seconds = time.time() - start
    if run.output_path is not None:
        hooks.write_output(result, str(run.output_path))
    return result


def print_result_summary(result: SimulationResult) -> None:
    print()
    print("=== Simulation Complete ===")
    print(f"  Domain:  {result.domain}")
    print(f"  Layer:   {result.layer}")
    print(f"  Steps:   {result.steps_completed}")
    print(f"  Wall:    {result.wall_time_seconds:.1f}s")
    for key, value in result.domain_metrics.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: {value}")


def dump_result_json(result: SimulationResult, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result.to_dict(), f, indent=2)
