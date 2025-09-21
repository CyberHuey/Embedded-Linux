.PHONY: venv deps smoke all format lint


venv:
python3 -m venv .venv
. .venv/bin/activate && pip install -U pip wheel


deps:
. .venv/bin/activate && pip install -r requirements.txt


smoke:
. .venv/bin/activate && pytest -q tests/smoke -n auto --maxfail=1 --junitxml=artifacts/junit-smoke.xml


all:
. .venv/bin/activate && pytest -q -n auto --junitxml=artifacts/junit-all.xml
