"""Command line interface: all commands produce data; none apply game settings."""

import argparse
import json
import sys
from pathlib import Path

from .audit import compare_protected, inspect_environment


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
    args = parser.parse_args(argv)
    try:
        if args.command == "audit":
            result = inspect_environment(args.game_root, args.user_config, args.cm_executable)
        else:
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
