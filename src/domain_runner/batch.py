"""Batch simulation runner — domain-local batch execution."""

from __future__ import annotations

import datetime
import json
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from domain_runner.config import deep_merge, load_json


RunFn = Callable[[str, dict[str, Any], Path, bool], dict[str, Any]]


def resolve_worker_count(requested: int | None, n_jobs: int) -> int:
    if requested is not None and requested > 0:
        return min(requested, n_jobs)
    try:
        import os

        return min(os.cpu_count() or 1, n_jobs)
    except Exception:
        return 1


def run_batch(
    batch_config: dict[str, Any],
    run_fn: RunFn,
    *,
    output_dir: Path,
    default_config: dict[str, Any] | None = None,
    parallel: bool = False,
    workers: int | None = None,
    verbose: bool = False,
) -> dict[str, Any]:
    """Execute batch runs with per-run config overrides."""
    output_dir.mkdir(parents=True, exist_ok=True)
    runs: list[dict[str, Any]] = batch_config.get("runs", [])
    if not runs:
        raise ValueError("Batch config must contain a non-empty 'runs' list")

    defaults = default_config or {}
    domain_base = deep_merge(
        dict(defaults.get("domain", {})),
        dict(batch_config.get("domain", {})),
    )
    simulation_base = deep_merge(
        dict(defaults.get("simulation", {})),
        dict(batch_config.get("simulation", {})),
    )
    default_layer = batch_config.get("layer", defaults.get("layer", "domain_only"))

    results: dict[str, Any] = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "output_directory": str(output_dir),
        "layer": default_layer,
        "runs": {},
    }

    submit_args: list[tuple[str, dict[str, Any], Path, bool]] = []
    for run in runs:
        name = run["name"]
        domain_cfg = deep_merge(domain_base, run.get("config_overrides", {}))
        simulation_cfg = deep_merge(simulation_base, run.get("simulation_overrides", {}))
        payload = {
            **domain_cfg,
            "simulation": simulation_cfg,
            "_layer": run.get("layer", default_layer),
        }
        submit_args.append((name, payload, output_dir, verbose))

    worker_count = resolve_worker_count(workers, len(submit_args))

    if parallel and len(submit_args) > 1:

        def _execute(args: tuple[str, dict[str, Any], Path, bool]) -> tuple[str, dict[str, Any]]:
            name, cfg, out, verb = args
            return name, run_fn(name, cfg, out, verb)

        with ProcessPoolExecutor(max_workers=worker_count) as pool:
            futures = [pool.submit(_execute, args) for args in submit_args]
            for future in as_completed(futures):
                name, res = future.result()
                results["runs"][name] = res
    else:
        for name, cfg, out, verb in submit_args:
            results["runs"][name] = run_fn(name, cfg, out, verb)

    key_path = output_dir / "key.json"
    with open(key_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    return results


def load_batch_config(path: Path | str) -> dict[str, Any]:
    return load_json(path)
