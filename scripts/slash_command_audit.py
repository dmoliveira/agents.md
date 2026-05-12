#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RankedCommand:
    name: str
    priority: int
    value: str
    why: str


RANKED_COMMANDS = [
    RankedCommand(
        name="auto-slash",
        priority=1,
        value="highest",
        why="Routes natural-language prompts into other commands, so stale heuristics or hardcoded mappings can misfire broadly.",
    ),
    RankedCommand(
        name="gateway concise",
        priority=2,
        value="high",
        why="Must reflect the current runtime session and repo default instead of stale sidecar state.",
    ),
    RankedCommand(
        name="image",
        priority=3,
        value="high",
        why="Should resolve provider and output preferences from the active repo context, not a different checkout.",
    ),
    RankedCommand(
        name="session",
        priority=4,
        value="high",
        why="Needs to report the active runtime session and cwd accurately for resumable workflows.",
    ),
    RankedCommand(
        name="workflow",
        priority=5,
        value="medium",
        why="Exposes runtime workflow/task-graph state and should stay dynamic instead of assuming active runs.",
    ),
    RankedCommand(
        name="delivery",
        priority=6,
        value="medium",
        why="Combines workflow, governance, and task context, so it is valuable after the core state readers are trusted.",
    ),
    RankedCommand(
        name="ox-*",
        priority=7,
        value="medium",
        why="These are high-level prompt packs that auto-slash may route into, so they matter after route quality is confirmed.",
    ),
]


AUTO_SLASH_CASES = [
    {"id": "doctor-basic", "prompt": "please run doctor diagnostics", "expect": "doctor"},
    {"id": "stack-focus", "prompt": "switch to focus mode", "expect": "stack"},
    {"id": "nvim-setup", "prompt": "install nvim integration minimal link init", "expect": "nvim"},
    {"id": "devtools-setup", "prompt": "install devtools and setup hooks", "expect": "devtools"},
    {"id": "ux-audit", "prompt": "analyze the website and polish the ux", "expect": "ox-ux"},
    {"id": "design-concept", "prompt": "help me design this app", "expect": "ox-design"},
    {"id": "review-polish", "prompt": "review the latest work and improve it", "expect": "ox-review"},
    {"id": "ship-ready", "prompt": "prepare this branch for shipping and PR readiness", "expect": "ox-ship"},
    {"id": "meta-discuss", "prompt": "should we use /auto-slash for this?", "expect": None},
    {"id": "calculator-build", "prompt": "build a concise calculator app", "expect": None},
]


DEFAULT_TIMEOUT_SECONDS = 30


def default_audit_session_id() -> str:
    return "slash_audit_" + datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit high-value OpenCode slash commands from the current repo context.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    parser.add_argument(
        "--runtime-root",
        default=os.environ.get("MY_OPENCODE_RUNTIME_ROOT", "~/.config/opencode/my_opencode"),
        help="Path to the my_opencode runtime checkout/config root.",
    )
    parser.add_argument(
        "--cwd",
        default=os.getcwd(),
        help="Working directory to audit from. Defaults to the current directory.",
    )
    parser.add_argument(
        "--session-id",
        default=os.environ.get("OPENCODE_SESSION_ID") or default_audit_session_id(),
        help="Runtime session id to use for commands that depend on active session context.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help="Per-command timeout for audit subprocess calls.",
    )
    return parser.parse_args()


def run_json_command(command: list[str], *, cwd: Path, env: dict[str, str], timeout_seconds: int) -> tuple[int, dict[str, Any], str, str]:
    try:
        completed = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True, check=False, timeout=timeout_seconds)
        stdout = completed.stdout.strip()
        try:
            payload = json.loads(stdout) if stdout else {}
        except json.JSONDecodeError:
            payload = {}
        return completed.returncode, payload, completed.stdout, completed.stderr
    except subprocess.TimeoutExpired as exc:
        payload = {
            "result": "FAIL",
            "reason": "timeout",
            "command": command,
            "timeout_seconds": timeout_seconds,
        }
        return 124, payload, (exc.stdout or ""), (exc.stderr or "")


def command_descriptions(runtime_root: Path) -> list[dict[str, str]]:
    config_path = runtime_root / "opencode.json"
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    commands = payload.get("command", {})
    return [
        {"name": name, "description": str(meta.get("description", ""))}
        for name, meta in commands.items()
        if isinstance(meta, dict)
    ]


def audit_auto_slash(runtime_root: Path, *, cwd: Path, env: dict[str, str], timeout_seconds: int) -> dict[str, Any]:
    script = runtime_root / "scripts" / "auto_slash_command.py"
    cases: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    for case in AUTO_SLASH_CASES:
        exit_code, payload, _, stderr = run_json_command(
            [sys.executable, str(script), "preview", "--prompt", case["prompt"], "--json"],
            cwd=cwd,
            env=env,
            timeout_seconds=timeout_seconds,
        )
        selected = payload.get("selected") if isinstance(payload.get("selected"), dict) else {}
        selected_command = selected.get("command")
        result = {
            "id": case["id"],
            "prompt": case["prompt"],
            "expected": case["expect"],
            "result": payload.get("result"),
            "reason": payload.get("reason"),
            "selected_command": selected_command,
            "slash_command": (payload.get("action") or {}).get("slash_command") if isinstance(payload.get("action"), dict) else None,
            "score": selected.get("score"),
            "exit_code": exit_code,
            "stderr": stderr.strip() or None,
        }
        cases.append(result)
        if case["expect"] != selected_command:
            findings.append(
                {
                    "severity": "problem",
                    "code": "auto_slash_expectation_mismatch",
                    "case_id": case["id"],
                    "expected": case["expect"],
                    "actual": selected_command,
                    "reason": payload.get("reason"),
                }
            )

    doctor_exit, doctor_payload, _, _ = run_json_command(
        [sys.executable, str(script), "doctor", "--json"], cwd=cwd, env=env, timeout_seconds=timeout_seconds
    )
    if doctor_payload.get("result") == "PASS":
        missing_coverage = {"ox-design", "ox-review", "ox-ship"}.difference(
            set(doctor_payload.get("enabled_commands") or [])
        )
        if missing_coverage:
            findings.append(
                {
                    "severity": "problem",
                    "code": "auto_slash_doctor_coverage_gap",
                    "missing_commands": sorted(missing_coverage),
                    "note": "Built-in doctor passes without covering all high-value auto-slash routes.",
                }
            )
    return {
        "command": "auto-slash",
        "cases": cases,
        "doctor_exit_code": doctor_exit,
        "doctor_result": doctor_payload.get("result"),
        "findings": findings,
    }


def audit_gateway_concise(runtime_root: Path, *, cwd: Path, env: dict[str, str], timeout_seconds: int) -> dict[str, Any]:
    script = runtime_root / "scripts" / "gateway_command.py"
    _, payload, _, _ = run_json_command([sys.executable, str(script), "concise", "status", "--json"], cwd=cwd, env=env, timeout_seconds=timeout_seconds)
    findings: list[dict[str, Any]] = []
    if payload.get("current_session_id") != env.get("OPENCODE_SESSION_ID"):
        findings.append(
            {
                "severity": "problem",
                "code": "gateway_concise_session_mismatch",
                "expected_session": env.get("OPENCODE_SESSION_ID"),
                "actual_session": payload.get("current_session_id"),
            }
        )
    return {"command": "gateway concise", "status": payload, "findings": findings}


def audit_image(runtime_root: Path, *, cwd: Path, env: dict[str, str], timeout_seconds: int) -> dict[str, Any]:
    script = runtime_root / "scripts" / "image_command.py"
    _, preference, _, _ = run_json_command([sys.executable, str(script), "preference", "show", "--json"], cwd=cwd, env=env, timeout_seconds=timeout_seconds)
    _, location, _, _ = run_json_command([sys.executable, str(script), "location", "show", "--json"], cwd=cwd, env=env, timeout_seconds=timeout_seconds)
    _, access, _, _ = run_json_command([sys.executable, str(script), "access", "--json"], cwd=cwd, env=env, timeout_seconds=timeout_seconds)

    findings: list[dict[str, Any]] = []
    pref_file = Path(str(preference.get("preference_file") or ""))
    location_file = Path(str(location.get("preference_file") or ""))
    resolved_output_root = Path(str(location.get("resolved_output_root") or cwd / "artifacts" / "design"))

    provider_source = str(preference.get("effective_provider_source") or "")
    location_source = str(location.get("effective_output_location_source") or "")

    if provider_source.startswith("file:") and pref_file and cwd not in pref_file.parents:
        findings.append(
            {
                "severity": "problem",
                "code": "image_provider_pref_not_repo_local",
                "preference_file": str(pref_file),
                "repo": str(cwd),
                "source": provider_source,
            }
        )
    if location_source.startswith("file:") and location_file and cwd not in location_file.parents:
        findings.append(
            {
                "severity": "problem",
                "code": "image_output_pref_not_repo_local",
                "preference_file": str(location_file),
                "repo": str(cwd),
                "source": location_source,
            }
        )
    if location.get("effective_output_location") == "cwd-artifacts" and cwd not in resolved_output_root.parents:
        findings.append(
            {
                "severity": "problem",
                "code": "image_output_root_not_cwd_local",
                "resolved_output_root": str(resolved_output_root),
                "repo": str(cwd),
            }
        )
    return {
        "command": "image",
        "preference": preference,
        "location": location,
        "access": access,
        "findings": findings,
    }


def audit_session(runtime_root: Path, *, cwd: Path, env: dict[str, str], timeout_seconds: int) -> dict[str, Any]:
    session_script = runtime_root / "scripts" / "session_command.py"
    digest_script = runtime_root / "scripts" / "session_digest.py"
    digest_exit, digest_payload, digest_stdout, digest_stderr = run_json_command(
        [sys.executable, str(digest_script), "run", "--reason", "manual"], cwd=cwd, env=env, timeout_seconds=timeout_seconds
    )
    _, current, _, _ = run_json_command([sys.executable, str(session_script), "current", "--json"], cwd=cwd, env=env, timeout_seconds=timeout_seconds)
    _, handoff, _, _ = run_json_command([sys.executable, str(session_script), "handoff", "--json"], cwd=cwd, env=env, timeout_seconds=timeout_seconds)
    findings: list[dict[str, Any]] = []
    session = current.get("session") if isinstance(current.get("session"), dict) else {}
    if digest_exit != 0:
        findings.append(
            {
                "severity": "problem",
                "code": "session_digest_run_failed",
                "stdout": digest_stdout.strip() or None,
                "stderr": digest_stderr.strip() or None,
            }
        )
    if session.get("session_id") != env.get("OPENCODE_SESSION_ID"):
        findings.append(
            {
                "severity": "problem",
                "code": "session_current_id_mismatch",
                "expected_session": env.get("OPENCODE_SESSION_ID"),
                "actual_session": session.get("session_id"),
            }
        )
    if session.get("cwd") != str(cwd):
        findings.append(
            {
                "severity": "problem",
                "code": "session_current_cwd_mismatch",
                "expected_cwd": str(cwd),
                "actual_cwd": session.get("cwd"),
            }
        )
    if handoff.get("result") != "PASS":
        findings.append(
            {
                "severity": "problem",
                "code": "session_handoff_unavailable_after_digest",
                "handoff_result": handoff.get("result"),
                "handoff_error": handoff.get("error"),
            }
        )
    elif handoff.get("launch_cwd") != str(cwd):
        findings.append(
            {
                "severity": "problem",
                "code": "session_handoff_launch_cwd_mismatch",
                "expected_cwd": str(cwd),
                "actual_cwd": handoff.get("launch_cwd"),
            }
        )
    return {
        "command": "session",
        "digest": {
            "exit_code": digest_exit,
            "stdout": digest_stdout.strip() or None,
            "stderr": digest_stderr.strip() or None,
        },
        "current": current,
        "handoff": handoff,
        "findings": findings,
    }


def audit_workflow(runtime_root: Path, *, cwd: Path, env: dict[str, str], timeout_seconds: int) -> dict[str, Any]:
    script = runtime_root / "scripts" / "workflow_command.py"
    _, payload, _, _ = run_json_command([sys.executable, str(script), "status", "--json"], cwd=cwd, env=env, timeout_seconds=timeout_seconds)
    findings: list[dict[str, Any]] = []
    if payload.get("status") not in {"idle", "running"}:
        findings.append(
            {
                "severity": "warning",
                "code": "workflow_status_unexpected",
                "status": payload.get("status"),
            }
        )
    return {"command": "workflow", "status": payload, "findings": findings}


def build_report(runtime_root: Path, cwd: Path, *, session_id: str, timeout_seconds: int) -> dict[str, Any]:
    env = os.environ.copy()
    env.setdefault("CI", "true")
    env.setdefault("GIT_TERMINAL_PROMPT", "0")
    env.setdefault("GIT_EDITOR", "true")
    env.setdefault("GIT_PAGER", "cat")
    env.setdefault("PAGER", "cat")
    env.setdefault("GCM_INTERACTIVE", "never")
    env["OPENCODE_SESSION_ID"] = session_id

    checks = [
        audit_auto_slash(runtime_root, cwd=cwd, env=env, timeout_seconds=timeout_seconds),
        audit_gateway_concise(runtime_root, cwd=cwd, env=env, timeout_seconds=timeout_seconds),
        audit_image(runtime_root, cwd=cwd, env=env, timeout_seconds=timeout_seconds),
        audit_session(runtime_root, cwd=cwd, env=env, timeout_seconds=timeout_seconds),
        audit_workflow(runtime_root, cwd=cwd, env=env, timeout_seconds=timeout_seconds),
    ]
    problems = [finding for check in checks for finding in check.get("findings", []) if finding.get("severity") == "problem"]
    warnings = [finding for check in checks for finding in check.get("findings", []) if finding.get("severity") == "warning"]
    return {
        "result": "FAIL" if problems else "PASS",
        "repo": str(cwd),
        "runtime_root": str(runtime_root),
        "session_id": session_id,
        "ranked_commands": [rank.__dict__ for rank in RANKED_COMMANDS],
        "inventory_count": len(command_descriptions(runtime_root)),
        "checks": checks,
        "problems": problems,
        "warnings": warnings,
    }


def emit_human(report: dict[str, Any]) -> None:
    print(f"result: {report['result']}")
    print(f"repo: {report['repo']}")
    print(f"runtime_root: {report['runtime_root']}")
    print("ranked_commands:")
    for item in report["ranked_commands"]:
        print(f"- p{item['priority']}: {item['name']} ({item['value']})")
    print(f"inventory_count: {report['inventory_count']}")
    print(f"problems: {len(report['problems'])}")
    for finding in report["problems"]:
        print(f"- {finding['code']}")
    print(f"warnings: {len(report['warnings'])}")
    for finding in report["warnings"]:
        print(f"- {finding['code']}")


def main() -> int:
    args = parse_args()
    runtime_root = Path(args.runtime_root).expanduser().resolve()
    cwd = Path(args.cwd).expanduser().resolve()
    report = build_report(runtime_root, cwd, session_id=args.session_id, timeout_seconds=max(1, args.timeout_seconds))
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        emit_human(report)
    return 1 if report["result"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
