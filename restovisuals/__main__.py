"""Command line interface: all commands produce data; none apply game settings."""

import argparse
import json
import sys
from pathlib import Path

from .audit import compare_protected, inspect_environment
from .gpu_windows import probe_gpus
from .benchmark import analyze_frame_times, read_frame_csv
from .planning import capabilities_from_audit, make_plan


def main(argv=None):
    parser = argparse.ArgumentParser(prog="restovisuals")
    commands = parser.add_subparsers(dest="command", required=True)
    audit = commands.add_parser("audit", help="Read selected graphics files and hashes")
    audit.add_argument("--game-root", type=Path, required=True)
    audit.add_argument("--user-config", type=Path, required=True)
    audit.add_argument("--cm-executable", type=Path)
    guard = commands.add_parser("guard", help="Compare two audit snapshots")
    guard.add_argument("before", type=Path)
    guard.add_argument("after", type=Path)
    commands.add_parser("gpu", help="Windowless DXGI/D3D11 hardware capability probe")
    capabilities = commands.add_parser("capabilities", help="Convert audit observations to conservative capability claims")
    capabilities.add_argument("audit_snapshot", type=Path)
    plan = commands.add_parser("plan", help="Produce a reviewable plan without changing settings")
    plan.add_argument("--config", type=Path, required=True)
    plan.add_argument("--gpu", type=Path, required=True)
    plan.add_argument("--adapter-index", type=int, required=True)
    plan.add_argument("--capabilities", type=Path, required=True)
    benchmark = commands.add_parser("benchmark", help="Analyze previously captured frame_ms CSV")
    benchmark.add_argument("csv", type=Path)
    benchmark.add_argument("--warmup-frames", type=int, default=0)
    args = parser.parse_args(argv)
    try:
        if args.command == "audit":
            result = inspect_environment(args.game_root, args.user_config, args.cm_executable)
        elif args.command == "gpu":
            result = probe_gpus()
        elif args.command == "capabilities":
            result = capabilities_from_audit(json.loads(args.audit_snapshot.read_text(encoding="utf-8-sig")))
        elif args.command == "plan":
            config = json.loads(args.config.read_text(encoding="utf-8-sig"))
            report = json.loads(args.capabilities.read_text(encoding="utf-8-sig"))
            gpu = json.loads(args.gpu.read_text(encoding="utf-8-sig"))
            adapters = [adapter for adapter in gpu["adapters"] if adapter["adapter_index"] == args.adapter_index]
            if len(adapters) != 1:
                raise ValueError("An explicit unique adapter index is required")
            result = make_plan(config, adapters[0], report)
        elif args.command == "benchmark":
            result = analyze_frame_times(read_frame_csv(args.csv), warmup_frames=args.warmup_frames)
        elif args.command == "guard":
            before = json.loads(args.before.read_text(encoding="utf-8-sig"))
            after = json.loads(args.after.read_text(encoding="utf-8-sig"))
            changes = compare_protected(before, after)
            result = {"protected_files_unchanged": not changes, "changed": changes}
        print(json.dumps(result, indent=2, allow_nan=False))
        return 3 if args.command == "guard" and changes else 0
    except (ValueError, OSError, KeyError, TypeError) as error:
        # Avoid echoing OS exceptions containing private machine paths.
        print(json.dumps({"error": type(error).__name__, "message": "Invalid or unreadable input; see command help and documented input contracts."}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
