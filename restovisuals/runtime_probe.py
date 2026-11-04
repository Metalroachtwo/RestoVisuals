"""Prepare original observer files under ignored workspace storage; no install."""

import hashlib
import json
import uuid
from pathlib import Path


CHECKOUT_ROOT = Path(__file__).resolve().parents[1]
TARGET = "extension/config-ext/PureLdrEffects/RestoVisuals_Observer_0D"
FILES = ("RestoVisuals_Observer_0D.lua", "restovisuals_host_probe.lua", "restovisuals_observer.lua")


def prepare_observer_probe(output_dir, *, diagnostic_only=False):
    if type(diagnostic_only) is not bool:
        raise ValueError("Diagnostic-only mode must be boolean")
    root = CHECKOUT_ROOT.resolve()
    local, output = (root / ".local").resolve(), Path(output_dir).resolve()
    if not local.is_relative_to(root) or not output.is_relative_to(local) or output == local or output.exists():
        raise ValueError("Use a new output directory under this checkout's .local directory")
    source = root / "runtime/lua"
    run_id = uuid.uuid4().hex
    source_hashes, prepared = {}, {}
    for name in FILES:
        data = (source / name).read_bytes()
        source_hashes[name] = hashlib.sha256(data).hexdigest()
        if name == FILES[0]:
            token = b"__RESTOVISUALS_RUN_ID__"
            if data.count(token) != 1:
                raise ValueError("Unpackaged entry identifier contract changed")
            data = data.replace(token, run_id.encode("ascii"))
            if diagnostic_only:
                marker = b"local diagnosticOnly = false"
                if data.count(marker) != 1:
                    raise ValueError("Diagnostic entry contract changed")
                data = data.replace(marker, b"local diagnosticOnly = true")
        prepared[name] = data
    manifest = {"schema_version": 1, "intent": "native_api_type_diagnostic_only" if diagnostic_only else "read_only_callback_probe_no_rendering",
                "diagnostic_only": diagnostic_only,
                "run_id": run_id, "target_relative_directory": TARGET,
                "source_sha256": source_hashes,
                "files_sha256": {name: hashlib.sha256(data).hexdigest() for name, data in prepared.items()},
                "owned_runtime_output": "runtime-receipt.json", "reference_files_to_overwrite": [],
                "native_loading_validated": False, "native_unloading_validated": False,
                "neutral_shader_validated": False, "installed": False,
                "requires_collision_and_reparse_checks": True,
                "requires_verified_backups_and_rollback_rehearsal": True,
                "requires_confirmed_no_active_game_session": True}
    destination = output / TARGET
    destination.mkdir(parents=True, exist_ok=False)
    for name, data in prepared.items():
        (destination / name).write_bytes(data)
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest
