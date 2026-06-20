# AGENTS.md — AI Agent Guidelines for domain-runner

## Repository Purpose

Layer-agnostic **single** and **batch** simulation orchestration for domain repos.
No TattleTots dependency — optional layers (e.g. `TattleTotsLayer`) plug in via protocol.

## Setup

```bash
pip install -e ".[dev]"
```

## Validation Commands

```bash
ruff check src/ tests/
ruff format --check src/ tests/
pytest
```

## Architecture Rules

- **Never import TattleTots** — layers live in other repos
- **Domains implement `DomainHooks`** — adapter factory, metrics, config I/O
- **Layers implement `SimulationLayer`** — setup / step / finalize
- **`DomainOnlyLayer` is the default** — adapter physics only
- **Never modify tests to make them pass** — fix the implementation

## Key Files

| File | Purpose |
|------|---------|
| `src/domain_runner/hooks.py` | `DomainHooks` protocol |
| `src/domain_runner/layer.py` | `SimulationLayer`, `DomainOnlyLayer` |
| `src/domain_runner/single.py` | `run_simulation()` main loop |
| `src/domain_runner/batch.py` | `run_batch()` JSON batch runner |
| `src/domain_runner/types.py` | `RunContext`, `RunResult` |

## PR Requirements

- All ruff checks pass
- All tests pass
- New features include tests
- Update README if changing batch config shape or public API
