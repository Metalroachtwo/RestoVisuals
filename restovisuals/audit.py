"""Bounded, read-only inspection of explicitly supplied graphics directories."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


def read_ini(path: Path) -> dict[str, dict[str, str]]:
    """Read CSP-style INI, retaining last values and ignoring inline comments.

    These files are data, never evaluated. Only semicolons outside quoted text
    start comments. Duplicate sections/keys are intentional in some CSP files.
    """
    if not path.is_file():
        return {}
    sections: dict[str, dict[str, str]] = {}
    section = ""
    for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        quote = None
        clean = []
        for char in line:
            if char in "\"'" and (quote is None or quote == char):
                quote = char if quote is None else None
            if char == ";" and quote is None:
                break
            clean.append(char)
        text = "".join(clean).strip()
        if not text or text.startswith((";", "#")):
            continue
        if text.startswith("[") and text.endswith("]"):
            section = text[1:-1].strip()
            sections.setdefault(section, {})
        elif "=" in text:
            key, value = text.split("=", 1)
            sections.setdefault(section, {})[key.strip()] = value.strip().strip("\"'")
    return sections


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_environment(game_root: Path, user_config: Path, cm_executable: Path | None = None) -> dict:
    """Return sanitized observations and content hashes, never raw source/config.

    No recursive game scan, executable launch, registry write, download, or
    runtime capability inference. Paths in the result are logical relative IDs.
    """
    if not game_root.is_dir():
        raise ValueError("Game root must be an existing directory")
    if not user_config.is_dir():
        raise ValueError("User configuration must be an existing directory")
    selected = {
        "game/dwrite.dll": game_root / "dwrite.dll",
        "game/extension/config/data_manifest.ini": game_root / "extension/config/data_manifest.ini",
        "game/extension/config/graphics_adjustments.ini": game_root / "extension/config/graphics_adjustments.ini",
        "game/extension/config/extra_fx.ini": game_root / "extension/config/extra_fx.ini",
        "game/extension/weather/pure/manifest.ini": game_root / "extension/weather/pure/manifest.ini",
        "game/extension/weather/Pure LCS/manifest.ini": game_root / "extension/weather/Pure LCS/manifest.ini",
        "user/video.ini": user_config / "video.ini",
        "user/extension/weather_fx.ini": user_config / "extension/weather_fx.ini",
        "user/extension/graphics_adjustments.ini": user_config / "extension/graphics_adjustments.ini",
        "user/extension/extra_fx.ini": user_config / "extension/extra_fx.ini",
    }
    if cm_executable is not None:
        if not cm_executable.is_file():
            raise ValueError("Content Manager executable does not exist")
        selected["content_manager/executable"] = cm_executable
    pp_dir = game_root / "system/cfg/ppfilters"
    pp_names = sorted(path.name for path in pp_dir.glob("*.ini") if path.is_file())
    # Preserve the complete top-level PP filter inventory without ingesting code.
    for name in pp_names:
        selected[f"game/system/cfg/ppfilters/{name}"] = pp_dir / name
    manifest = read_ini(game_root / "extension/config/data_manifest.ini")
    gamma = read_ini(game_root / "extension/weather/pure/manifest.ini")
    lcs = read_ini(game_root / "extension/weather/Pure LCS/manifest.ini")
    video = read_ini(user_config / "video.ini")
    weather = read_ini(user_config / "extension/weather_fx.ini")
    defaults = read_ini(game_root / "extension/config/graphics_adjustments.ini")
    overrides = read_ini(user_config / "extension/graphics_adjustments.ini")
    fsr = dict(defaults.get("FSR", {}))
    fsr.update(overrides.get("FSR", {}))
    extra = dict(read_ini(game_root / "extension/config/extra_fx.ini").get("BASIC", {}))
    extra.update(read_ini(user_config / "extension/extra_fx.ini").get("BASIC", {}))
    methods = {"0": "fsr1", "1": "fsr_legacy_port", "2": "nis", "5": "fsr2", "7": "fsr3"}
    raw_default = (game_root / "extension/config/graphics_adjustments.ini")
    default_text = raw_default.read_text(encoding="utf-8-sig", errors="replace") if raw_default.is_file() else ""
    sdk = game_root / "extension/internal/lua-sdk/ac_pp_filters/lib.lua"
    sdk_text = sdk.read_text(encoding="utf-8-sig", errors="replace") if sdk.is_file() else ""
    names = ("ac.getPatchVersion", "ac.getPatchVersionCode", "ac.getPerformanceCPUAndGPUTime", "render.fullscreenPass", "ui.ExtraCanvas")
    log = game_root / "ReShade.log1"
    header = ""
    if log.is_file():
        with log.open(encoding="utf-8-sig", errors="replace") as stream:
            header = stream.readline(4096)
    version_match = re.search(r"ReShade version '([^']+)'", header)
    return {
        "schema_version": 1,
        "evidence": "observed_locally",
        "runtime_validated": False,
        "csp": {
            "manifest_version": manifest.get("VERSION", {}).get("SHADERS_PATCH"),
            "manifest_build": manifest.get("VERSION", {}).get("SHADERS_PATCH_BUILD"),
            "note": "Manifest is launcher metadata; independently check the binary version.",
        },
        "pure": {
            "gamma_manifest_version": gamma.get("ABOUT", {}).get("VERSION"),
            "lcs_manifest_version": lcs.get("ABOUT", {}).get("VERSION"),
            "configured_weather_implementation": weather.get("BASIC", {}).get("IMPLEMENTATION"),
            "note": "Manifest version does not identify every hotfix or prove runtime mode.",
        },
        "configured": {
            "width": video.get("VIDEO", {}).get("WIDTH"),
            "height": video.get("VIDEO", {}).get("HEIGHT"),
            "msaa_samples": video.get("VIDEO", {}).get("AASAMPLES"),
            "post_processing": video.get("POST_PROCESS", {}).get("ENABLED"),
            "pp_filter": video.get("POST_PROCESS", {}).get("FILTER"),
            "upscaling_active": fsr.get("ACTIVE"),
            "upscaling_method_id": fsr.get("OLD_IMPLEMENTATION"),
            "upscaling_method": methods.get(fsr.get("OLD_IMPLEMENTATION", ""), "unknown"),
            "extra_fx_enabled": extra.get("ENABLED"),
        },
        "interfaces": {
            "pp_sdk_symbols_present": {name: name in sdk_text for name in names},
            "upscaler_labels_present": {name: label in default_text for name, label in {"fsr1": "AMD FSR (v1.0.2", "fsr2": "AMD FSR 2 (v2.2.1", "fsr3": "AMD FSR 3 (v3.1.2"}.items()},
            "note": "Labels and SDK declarations establish file presence only, not callable support.",
        },
        "pp_filters": pp_names,
        "reshade": {
            "historical_log_version": version_match.group(1) if version_match else None,
            "root_loader_present": {name: (game_root / name).is_file() for name in ("dxgi.dll", "d3d11.dll")},
            "runtime_active": "unknown",
        },
        "protected_files": {name: {"exists": path.is_file(), "sha256": file_hash(path) if path.is_file() else None} for name, path in selected.items()},
    }


def compare_protected(before: dict, after: dict) -> list[str]:
    """List additions, removals, and hash changes in the audited set."""
    old, new = before["protected_files"], after["protected_files"]
    return sorted(name for name in old.keys() | new.keys() if old.get(name) != new.get(name))
