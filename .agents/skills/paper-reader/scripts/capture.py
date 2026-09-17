#!/usr/bin/env python3
"""Run a command with fully captured output, written to a file.

Use when the RunCommand tool loses command output ("terminal black hole"):
the command itself executes (side effects are real), but its stdout/stderr
never reach the agent. This wrapper captures everything to .tmp_capture_out.txt
(UTF-8) so the output can be recovered with the Read tool.

Usage (from project root; always invoke via uv per pitfalls.md #18):

  uv run python .agents/skills/paper-reader/scripts/capture.py -- git status --porcelain
  uv run python .agents/skills/paper-reader/scripts/capture.py -- uv run python .agents/skills/paper-reader/scripts/append_log.py --op ingest --title "..." --body "..."

The '--' separates this script's flags from the wrapped command. Output file:
.tmp_capture_out.txt in the current directory (delete it when done).

Completion marker: .tmp_capture_out.txt is only written AFTER the wrapped
command finishes, so during long runs (mkdocs builds take ~2 min) a Read of
it returns the PREVIOUS run's output — indistinguishable from "still running"
vs "done" (pitfalls.md #57). This script therefore deletes .tmp_capture_done
at start and writes it (containing "exit=N") at end. Polling protocol:
Read .tmp_capture_done — "File does not exist" = still running (wait, retry);
file exists = done, then Read .tmp_capture_out.txt for the output.
"""
import argparse
import os
import subprocess

OUT = ".tmp_capture_out.txt"
DONE = ".tmp_capture_done"


def main() -> None:
    p = argparse.ArgumentParser(
        description="Run a command, capture stdout/stderr to a file.",
        epilog="Pass the wrapped command after '--'.",
    )
    p.add_argument("cmd", nargs=argparse.REMAINDER, help="command to run, after '--'")
    args = p.parse_args()
    cmd = args.cmd[1:] if args.cmd and args.cmd[0] == "--" else args.cmd
    if not cmd:
        p.error("no command given (pass it after '--')")

    # Clear the completion marker BEFORE starting so a stale marker from a
    # previous run can't be mistaken for this run's completion.
    try:
        os.remove(DONE)
    except FileNotFoundError:
        pass

    exit_code = None
    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=1800,
        )
        exit_code = r.returncode
        body = (
            f"$ {' '.join(cmd)}\n"
            f"exit={r.returncode}\n"
            f"{r.stdout}\n"
            f"--- stderr ---\n"
            f"{r.stderr}"
        )
    except Exception as e:  # timeout, FileNotFoundError, ...
        body = f"$ {' '.join(cmd)}\nEXCEPTION: {e}"

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(body)
    # Completion marker: exists == output file is final for this invocation.
    with open(DONE, "w", encoding="utf-8") as f:
        f.write(f"exit={exit_code}\n")
    # This print may itself be black-holed; the files are the real channel.
    print(f"captured -> {OUT} (done marker: {DONE})")


if __name__ == "__main__":
    main()
