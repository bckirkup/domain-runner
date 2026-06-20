# domain-runner

Layer-agnostic **single** and **batch** simulation runners shared by domain repositories (fire ecology, grain guard, reef watch, etc.).

Domains implement **hooks** (adapter factory, metrics, config). An optional **layer** sits above the adapter:

- `domain_only` — advance the domain simulation only (no Tots, no other orchestration)
- `tattletots` — provided by the [TattleTots](https://github.com/bckirkup/TattleTots) integration package

Future layers (new agent ecologies, human-in-the-loop stacks, etc.) implement the same `SimulationLayer` protocol without changing domain physics code.

## Install

```bash
git clone https://github.com/bckirkup/domain-runner.git
pip install -e domain-runner[dev]
```

Or as a git dependency from another repo:

```toml
dependencies = [
    "domain-runner @ git+https://github.com/bckirkup/domain-runner.git",
]
```

## Usage (in a domain repo)

```python
from domain_runner.layer import DomainOnlyLayer
from domain_runner.single import run_simulation
from domain_runner.types import RunContext
from my_domain.runner import MyDomainHooks

run = RunContext(steps=200, seed=42, domain_config={"grid_rows": 20})
result = run_simulation(MyDomainHooks(), DomainOnlyLayer(), run)
```

Batch runs use a JSON config with a `runs` list; see each domain’s `configs/batch_example.json`.

## Repository role

```
domain-runner     ← this repo (no TattleTots dependency)
       ↑
domain repos      ← fire / grain / coral (+ optional layers)
```

## Development

```bash
pytest
ruff check src tests
```

## License

Apache License 2.0 — see [LICENSE](LICENSE) or [LICENSE.md](LICENSE.md).
