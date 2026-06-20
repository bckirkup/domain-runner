"""Domain-specific hook protocol."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from domain_runner.types import RunContext


@runtime_checkable
class DomainHooks(Protocol):
    """Domain repo implements adapter construction and metrics recording."""

    domain_name: str
    default_config_path: str | None

    def load_run_context(
        self,
        *,
        config_path: str | None = None,
        cli_overrides: dict[str, Any] | None = None,
    ) -> RunContext:
        """Build a RunContext from a config file and/or CLI overrides."""

    def build_adapter(self, domain_config: dict[str, Any]) -> Any:
        """Construct the domain adapter from resolved domain config."""

    def print_header(self, adapter: Any, run: RunContext) -> None:
        """Print run banner."""

    def on_step(self, adapter: Any, step: int, layer_events: dict[str, Any]) -> None:
        """Record domain metrics for one step."""

    def should_stop(self, adapter: Any, step: int, layer_events: dict[str, Any]) -> bool:
        """Return True to end the run early."""

    def print_step(
        self,
        adapter: Any,
        step: int,
        layer_events: dict[str, Any],
        *,
        verbose: bool,
    ) -> None:
        """Optional per-step console output."""

    def summarize(self, adapter: Any, layer_metrics: dict[str, Any]) -> dict[str, Any]:
        """Return final domain metrics dict."""

    def write_output(self, result: Any, path: str) -> None:
        """Serialize results to disk (domain-specific JSON schema)."""
