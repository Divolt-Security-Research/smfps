"""SMFPS conformance test runner.

Usage:
    python -m conformance.runner --target https://staging.vendor.example \
        --credentials example-creds.yaml --profile minimum

Each test corresponds to one SMFPS requirement (R1..R8). The runner invokes
tests in order, collects results, and prints a per-requirement pass/fail
summary that the provider can use to self-assess conformance.

The suite is intentionally minimal: it is reproducible, carries no network
dependencies beyond the provider under test, and is suitable for CI use by
the provider.
"""
from __future__ import annotations

import importlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import typer
import yaml
from rich.console import Console
from rich.table import Table

app = typer.Typer(add_completion=False, help="SMFPS conformance test runner")
console = Console()

MINIMUM_PROFILE = {"R1", "R2", "R3", "R4"}
FULL_PROFILE    = {"R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8"}


@dataclass(slots=True)
class Result:
    requirement: str
    ok: bool
    detail: str


def _load_tests() -> dict[str, callable]:
    """Discover test functions from `conformance.tests.r1` through `.r8`."""
    tests: dict[str, callable] = {}
    for i in range(1, 9):
        mod_name = f"conformance.tests.r{i}"
        try:
            mod = importlib.import_module(mod_name)
            tests[f"R{i}"] = mod.run
        except ModuleNotFoundError:
            tests[f"R{i}"] = None
    return tests


@app.command()
def main(
    target: str = typer.Option(..., "--target", help="Base URL of the staging provider API"),
    credentials: Path = typer.Option(..., "--credentials", help="Path to credentials YAML"),
    profile: str = typer.Option("minimum", "--profile", help="minimum | full"),
    verbose: bool = typer.Option(False, "-v", "--verbose"),
) -> None:
    if profile not in {"minimum", "full"}:
        console.print(f"[red]Unknown profile {profile!r}; expected 'minimum' or 'full'[/red]")
        sys.exit(2)
    scope = MINIMUM_PROFILE if profile == "minimum" else FULL_PROFILE

    creds = yaml.safe_load(credentials.read_text())
    tests = _load_tests()

    results: list[Result] = []
    for req_id in sorted(scope):
        fn = tests.get(req_id)
        if fn is None:
            results.append(Result(req_id, False, "test module not implemented"))
            continue
        try:
            ok, detail = fn(target=target, credentials=creds, verbose=verbose)
            results.append(Result(req_id, bool(ok), str(detail)))
        except Exception as e:  # noqa: BLE001
            results.append(Result(req_id, False, f"test error: {e}"))

    table = Table(title=f"SMFPS conformance against {target} ({profile})")
    table.add_column("Req", justify="center")
    table.add_column("Status", justify="center")
    table.add_column("Detail")
    for r in results:
        status = "[green]PASS[/green]" if r.ok else "[red]FAIL[/red]"
        table.add_row(r.requirement, status, r.detail[:120])
    console.print(table)

    all_pass = all(r.ok for r in results)
    console.print(
        f"\n[bold]{'PASS' if all_pass else 'FAIL'}[/bold] — "
        f"{sum(r.ok for r in results)}/{len(results)} requirements in profile "
        f"[cyan]{profile}[/cyan]"
    )
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":  # pragma: no cover
    app()
