"""Simulation layer protocol — pluggable orchestration above the domain adapter."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from domain_runner.types import RunContext


@runtime_checkable
class SimulationLayer(Protocol):
    """Orchestration layer above a domain adapter (Tots, future layers, or none)."""

    name: str

    def setup(self, adapter: Any, run: RunContext) -> dict[str, Any]:
        """Initialize layer state before the step loop."""

    def step(self, adapter: Any, step: int, layer_state: dict[str, Any]) -> dict[str, Any]:
        """Advance one time step; return per-step events for domain metrics hooks."""

    def finalize(
        self,
        adapter: Any,
        layer_state: dict[str, Any],
        run: RunContext,
    ) -> dict[str, Any]:
        """Return layer-specific summary metrics after the loop."""


class DomainOnlyLayer:
    """Default layer: advance the domain adapter with no agent ecology."""

    name = "domain_only"

    def setup(self, adapter: Any, run: RunContext) -> dict[str, Any]:
        return {}

    def step(self, adapter: Any, step: int, layer_state: dict[str, Any]) -> dict[str, Any]:
        adapter.step(step)
        return {
            "ground_truth_active": adapter.get_ground_truth(step),
            "active_locations": adapter.get_active_locations(step),
        }

    def finalize(
        self,
        adapter: Any,
        layer_state: dict[str, Any],
        run: RunContext,
    ) -> dict[str, Any]:
        return {}
