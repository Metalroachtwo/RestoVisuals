"""Strict offline configuration and conservative, reviewable capability plans."""

from __future__ import annotations

import json
import re
from pathlib import Path

from .validation import validate_document


TRACKS = {"0.2.11": "stable_baseline", "0.3.0-preview361": "preview_development"}
TIERS = ("ultra_lite", "optimized", "balanced", "enhanced")
# Proposed incremental effect-surface ceilings, not measured GPU memory usage.
EFFECT_CEILINGS_MIB = (24, 48, 96, 128)
CAPABILITIES = ("fsr1", "fsr2", "fsr3", "frame_generation", "color_transform", "depth", "motion", "jitter", "history_reset")
STATES = {"unknown", "documented", "observed_locally", "tested_validated", "proposed", "unavailable"}


def validate_config(config: dict) -> dict:
    """Validate exactly the flat schema's keywords; reject non-finite numbers.

    The committed schema is the single source of field types, bounds and enums.
    This is deliberately not a general-purpose JSON Schema implementation.
    """
    schema = json.loads((Path(__file__).resolve().parents[1] / "schemas/profile.schema.json").read_text(encoding="utf-8"))
    validate_document(config, schema)
    return dict(config)


def capabilities_from_audit(audit: dict) -> dict:
    """Presence becomes an observation, never a validated runtime capability."""
    pure = audit.get("pure", {}).get("configured_weather_implementation")
    report = {
        "schema_version": 1,
        "context": {"csp_version": audit.get("csp", {}).get("manifest_version"),
                    "pure_mode": {"pure": "gamma", "Pure LCS": "lcs"}.get(pure, "unknown"),
                    "render_mode": "unknown", "width": None, "height": None},
        "capabilities": {key: "unknown" for key in CAPABILITIES},
        "evidence_id": "installed_files_only",
    }
    for key, present in audit.get("interfaces", {}).get("upscaler_labels_present", {}).items():
        if key in report["capabilities"] and present is True:
            report["capabilities"][key] = "observed_locally"
    return report


def validate_capabilities(report: dict) -> dict:
    if not isinstance(report, dict) or set(report) != {"schema_version", "context", "capabilities", "evidence_id"}:
        raise ValueError("Invalid capability report fields")
    if type(report["schema_version"]) is not int or report["schema_version"] != 1:
        raise ValueError("Unsupported capability schema")
    context = report["context"]
    if not isinstance(context, dict) or set(context) != {"csp_version", "pure_mode", "render_mode", "width", "height"}:
        raise ValueError("Invalid capability context")
    if not isinstance(report["capabilities"], dict) or set(report["capabilities"]) - set(CAPABILITIES):
        raise ValueError("Unknown capability name")
    if any(not isinstance(value, str) or value not in STATES for value in report["capabilities"].values()):
        raise ValueError("Unknown capability evidence state")
    if not isinstance(report["evidence_id"], str) or not report["evidence_id"].strip():
        raise ValueError("Capability evidence ID is required")
    return report


def _gpu_tier(adapter: dict):
    if not isinstance(adapter, dict):
        raise ValueError("GPU adapter must be an object")
    software = adapter.get("is_software")
    memory = adapter.get("dedicated_video_memory_bytes")
    level = adapter.get("feature_level")
    if type(software) is not bool or type(memory) is not int or memory < 0:
        raise ValueError("GPU memory and software status must be explicit")
    if software:
        return None, "Software adapter is outside hardware targets"
    if not isinstance(level, str) or not re.fullmatch(r"\d{1,2}_[0-9]", level):
        return None, "Measured feature level is unavailable"
    major, minor = map(int, level.split("_"))
    if (major, minor) < (11, 0):
        return None, "Measured feature level is below 11_0"
    if memory < 1792 * 1024**2:
        return None, "Exposed dedicated memory is below the initial 2 GB class target"
    # Boundaries tolerate driver-reserved memory. They are proposed capacity
    # classes, never performance certification or a marketing-name whitelist.
    tier = sum(memory >= boundary * 1024**3 for boundary in (2.5, 5.5, 7.5))
    if adapter.get("vendor_id") not in (0x1002, 0x10DE):
        return 0, "Vendor is outside the initial AMD/NVIDIA validation matrix"
    return tier, "Capacity class is provisional; bandwidth, driver behavior and frame times need measurement"


def make_plan(config: dict, adapter: dict, report: dict) -> dict:
    config = validate_config(config)
    report = validate_capabilities(report)
    tier, gpu_note = _gpu_tier(adapter)
    requested_tier = config["profile"]
    if tier is not None and requested_tier != "auto":
        tier = min(tier, TIERS.index(requested_tier))
    warnings = [gpu_note]
    context_matches = all(report["context"].get(key) == config[key] for key in ("csp_version", "pure_mode", "render_mode", "width", "height"))

    def proven(name):
        return tier is not None and context_matches and report["capabilities"].get(name, "unknown") == "tested_validated"

    if not context_matches:
        warnings.append("Runtime evidence does not match the requested CSP, Pure mode, render mode and resolution; optional features disabled")
    selected = config["upscaler"]
    if selected != "native":
        requirements = [selected]
        if selected in ("fsr2", "fsr3"):
            requirements += ["depth", "motion", "jitter", "history_reset"]
        if not all(proven(name) for name in requirements):
            warnings.append(f"Requested {selected} lacks validated matching capabilities; falling back to native")
            selected = "native"
    frame_generation = config["frame_generation"] and proven("frame_generation")
    if config["frame_generation"] and not frame_generation:
        warnings.append("Frame generation has no separate validated capability; disabled")
    # FSR does not automatically authorize any extra allocation. Its actual CSP
    # working set is unknown and excluded from this simple effect-surface model.
    surface = config["width"] * config["height"] * 8  # one RGBA16F output, no mips/MSAA
    color = config["color_transform"] and proven("color_transform")
    ceiling = EFFECT_CEILINGS_MIB[tier] * 1024**2 if tier is not None else 0
    if color and surface > ceiling:
        color = False
        warnings.append("Proposed color output surface exceeds this tier's incremental memory ceiling; disabled")
    if config["color_transform"] and not color and surface <= ceiling:
        warnings.append("Color transform needs runtime stage/format and Pure ownership validation; disabled")
    return {
        "schema_version": 1, "status": "candidate_only" if tier is not None else "unsupported_or_unmeasured",
        "applies_settings": False, "gameplay_validated": False,
        "csp_track": TRACKS[config["csp_version"]],
        "pure_calibration": config["pure_mode"], "candidate_profile": TIERS[tier] if tier is not None else None,
        "target_frame_ms": 1000 / config["target_fps"],
        "upscaler": selected, "native_available": True,
        "frame_generation": bool(frame_generation), "color_transform": bool(color),
        "effect_surface_model": {"bytes_per_pixel": 8, "surface_count": 1 if color else 0,
                                 "additional_bytes": surface if color else 0,
                                 "ceiling_bytes": ceiling, "fsr_working_set_bytes": None,
                                 "measured_allocation": False},
        "performance_prediction": None, "warnings": warnings,
    }
