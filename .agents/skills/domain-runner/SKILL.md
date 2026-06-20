---
name: domain-runner-development
description: Layer-agnostic single and batch simulation runners shared by domain repos.
---

# domain-runner Development Skill

## Purpose

Provides **single-run** and **batch-run** orchestration for domain simulations without requiring TattleTots. Domains implement `DomainHooks`; optional **layers** (e.g. TattleTots) plug in above the adapter.

## Setup

```bash
git clone https://github.com/bckirkup/domain-runner.git
cd domain-runner
pip install -e ".[dev]"
```

## Validation

```bash
ruff check src/ tests/
ruff format --check src/ tests/
pytest
```

Tests: `tests/test_runner.py` (single run), `tests/test_batch.py` (batch JSON).

## Core Concepts

| Concept | Module | Role |
|---------|--------|------|
| `RunContext` | `types.py` | Steps, seed, domain config, layer name |
| `DomainHooks` | `hooks.py` | Protocol: build adapter, metrics, I/O |
| `SimulationLayer` | `layer.py` | Protocol: setup / step / finalize |
| `DomainOnlyLayer` | `layer.py` | Default — `adapter.step()` only |
| `run_simulation` | `single.py` | Main loop |
| `run_batch` | `batch.py` | JSON batch config → many runs |

## Batch Config Shape

```json
{
  "layer": "domain_only",
  "domain": { "steps": 200, "seed": 42 },
  "simulation": { "initial_population": 20 },
  "runs": [
    { "name": "baseline", "config_overrides": {} },
    { "name": "hot", "config_overrides": { "seed": 7 } }
  ]
}
```

## Adding a New Layer

Implement `SimulationLayer` in your layer package (e.g. TattleTots registers `TattleTotsLayer`). Domains call `resolve_layer(name)` from their `{domain}/runner.py`.

Do **not** add TattleTots imports to this repo.

## Domain Repo Integration

Each domain provides `{package}/runner.py` with a `*DomainHooks` class and:

```bash
{domain-cli} sim --layer domain_only
{domain-cli} sim --layer tattletots
{domain-cli} batch --config configs/batch_example.json
```
