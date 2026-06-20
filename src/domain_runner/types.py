"""Shared run result types."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class RunContext:
    """Parameters for a single simulation run."""

    steps: int
    seed: int
    domain_config: dict[str, Any]
    layer: str = "domain_only"
    simulation_config: dict[str, Any] = field(default_factory=dict)
    verbose: bool = False
    output_path: Path | None = None


@dataclass
class SimulationResult:
    """Outcome of a completed simulation run."""

    domain: str
    layer: str
    steps_completed: int
    seed: int
    wall_time_seconds: float
    domain_config: dict[str, Any]
    domain_metrics: dict[str, Any]
    layer_metrics: dict[str, Any] = field(default_factory=dict)
    output_path: Path | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "domain": self.domain,
            "layer": self.layer,
            "steps_completed": self.steps_completed,
            "seed": self.seed,
            "wall_time_seconds": self.wall_time_seconds,
            "domain_config": self.domain_config,
            "domain_metrics": self.domain_metrics,
            "layer_metrics": self.layer_metrics,
            "output_path": str(self.output_path) if self.output_path else None,
        }
