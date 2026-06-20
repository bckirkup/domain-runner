"""Batch runner tests."""

from __future__ import annotations

from pathlib import Path

from domain_runner.batch import run_batch


def test_run_batch_sequential(tmp_path: Path) -> None:
    results: list[tuple[str, dict]] = []

    def run_fn(name: str, cfg: dict, output_dir: Path, verbose: bool) -> dict:
        results.append((name, cfg))
        return {"status": "success", "layer": cfg.get("_layer", "domain_only")}

    batch = {
        "layer": "domain_only",
        "domain": {"steps": 10, "seed": 42},
        "runs": [
            {"name": "a", "config_overrides": {"seed": 1}},
            {"name": "b", "config_overrides": {"seed": 2}},
        ],
    }
    summary = run_batch(batch, run_fn, output_dir=tmp_path, default_config={"domain": {"steps": 5}})
    assert len(summary["runs"]) == 2
    assert summary["runs"]["a"]["status"] == "success"
    assert (tmp_path / "key.json").exists()
    assert results[0][1]["seed"] == 1
