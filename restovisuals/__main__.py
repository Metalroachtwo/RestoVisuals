"""Inspect or produce project data; no command applies game settings."""

import argparse
import json
import sys
from pathlib import Path

from .audit import compare_protected, file_hash, inspect_environment
from .gpu_windows import probe_gpus
from .benchmark import analyze_frame_times, compare_captures, read_frame_csv
from .planning import capabilities_from_audit, make_plan
from .shader_compile import compile_prototype
from .d3d11_validation import validate_gpu_shader
from .gpu_demo import demonstrate_gpu_shader
from .runtime_probe import prepare_observer_probe


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
    shader = commands.add_parser("compile-shader", help="Compile prototype entry points in memory; no GPU dispatch")
    shader.add_argument("source", type=Path)
    gpu_validation = commands.add_parser("gpu-validate", help="Bounded isolated GPU identity/readback validation; no game integration")
    gpu_validation.add_argument("--adapter-index", type=int, required=True)
    gpu_validation.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1] / "shaders/RV_ColorPrototype.hlsl")
    gpu_demo = commands.add_parser("gpu-demo", help="Original full-resolution charts on an isolated GPU device; exports to a new .local directory")
    gpu_demo.add_argument("--adapter-index", type=int, required=True)
    gpu_demo.add_argument("--output", type=Path, required=True)
    gpu_demo.add_argument("--profile", choices=("720p", "1080p", "both"), default="both")
    gpu_demo.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1] / "shaders/RV_ColorPrototype.hlsl")
    probe_package = commands.add_parser("prepare-observer-probe", help="Stage original observer files under a new .local directory; does not install or launch")
    probe_package.add_argument("--output", type=Path, required=True)
    probe_package.add_argument("--diagnostic-only", action="store_true", help="Record API value types without subscriptions or rendering")
    compare = commands.add_parser("compare", help="Compare captured CSVs only when declared context matches")
    for argument in ("baseline_csv", "baseline_metadata", "candidate_csv", "candidate_metadata"):
        compare.add_argument(argument, type=Path)
    args = parser.parse_args(argv)
    try:
        def read_object(path):
            value = json.loads(path.read_text(encoding="utf-8-sig"))
            if not isinstance(value, dict):
                raise ValueError("JSON input must be an object")
            return value

        if args.command == "audit":
            result = inspect_environment(args.game_root, args.user_config, args.cm_executable)
        elif args.command == "gpu":
            result = probe_gpus()
        elif args.command == "capabilities":
            result = capabilities_from_audit(read_object(args.audit_snapshot))
        elif args.command == "plan":
            config = read_object(args.config)
            report = read_object(args.capabilities)
            gpu = read_object(args.gpu)
            adapters = [adapter for adapter in gpu["adapters"] if adapter["adapter_index"] == args.adapter_index]
            if len(adapters) != 1:
                raise ValueError("An explicit unique adapter index is required")
            result = make_plan(config, adapters[0], report)
            result["input_files_sha256"] = {name: file_hash(path) for name, path in (("config", args.config), ("gpu", args.gpu), ("capabilities", args.capabilities))}
            result["input_gpu_source"] = gpu.get("source", "unknown")
            result["capability_evidence_id"] = report["evidence_id"]
        elif args.command == "benchmark":
            result = analyze_frame_times(read_frame_csv(args.csv), warmup_frames=args.warmup_frames)
        elif args.command == "compile-shader":
            result = compile_prototype(args.source)
        elif args.command == "gpu-validate":
            result = validate_gpu_shader(args.adapter_index, args.source)
        elif args.command == "gpu-demo":
            result = demonstrate_gpu_shader(args.adapter_index, args.source, args.output, profile=args.profile)
        elif args.command == "prepare-observer-probe":
            result = prepare_observer_probe(args.output, diagnostic_only=args.diagnostic_only)
        elif args.command == "compare":
            result = compare_captures(read_frame_csv(args.baseline_csv), read_frame_csv(args.candidate_csv),
                                      read_object(args.baseline_metadata), read_object(args.candidate_metadata))
            result["input_files_sha256"] = {name: file_hash(getattr(args, name)) for name in ("baseline_csv", "baseline_metadata", "candidate_csv", "candidate_metadata")}
        elif args.command == "guard":
            before = read_object(args.before)
            after = read_object(args.after)
            changes = compare_protected(before, after)
            result = {"protected_files_unchanged": not changes, "changed": changes}
        print(json.dumps(result, indent=2, allow_nan=False))
        if args.command in ("gpu-validate", "gpu-demo") and result["status"] != "passed":
            return 4
        return 3 if args.command == "guard" and changes else 0
    except (ValueError, OSError, KeyError, TypeError, AttributeError, OverflowError) as error:
        # Avoid echoing OS exceptions containing private machine paths.
        print(json.dumps({"error": type(error).__name__, "message": "Invalid or unreadable input; see command help and documented input contracts."}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
