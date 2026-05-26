# Log Processing Exercise

Read a log file line by line and print `"LINE_NUMBER : NEW_DATA"` according to 5
prioritized rules.

## Prerequisites
- Python ≥ 3.11
- [uv](https://docs.astral.sh/uv/)

## Quickstart

```bash
make install   # uv sync --group dev
make run       # run process_log.py on data.log
make test      # pytest
make check     # lint + typecheck + tests
make help      # list all targets
```

## Structure
```
.
├── process_log.py            # script
├── data.log                  # input
├── tests/test_process_log.py # parametrized tests + end-to-end
├── pyproject.toml            # ruff + mypy strict + pytest + uv deps
├── Makefile                  # install / run / test / check
└── .gitlab-ci.yml            # CI: lint + typecheck + test
```
