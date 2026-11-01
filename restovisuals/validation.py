"""Small validator for the exact schema keyword subset used by this project."""

import math


def validate_document(value, rule):
    """Reject unsupported schema keywords so future schemas cannot fail open.

    This is a project contract validator, not a general JSON Schema library.
    """
    supported = {"$schema", "title", "type", "additionalProperties", "required", "properties", "const", "enum", "minimum", "maximum", "minLength"}
    if rule.keys() - supported:
        raise ValueError("Unsupported schema keyword")
    types = {"integer": lambda v: type(v) is int,
             "number": lambda v: type(v) is int or (type(v) is float and math.isfinite(v)),
             "string": lambda v: isinstance(v, str), "boolean": lambda v: type(v) is bool,
             "object": lambda v: isinstance(v, dict)}
    kind = rule.get("type")
    if kind not in types or not types[kind](value):
        raise ValueError("Invalid document type")
    if "const" in rule and value != rule["const"]:
        raise ValueError("Invalid document constant")
    if "enum" in rule and value not in rule["enum"]:
        raise ValueError("Unsupported document value")
    if "minimum" in rule and value < rule["minimum"]:
        raise ValueError("Value below document minimum")
    if "maximum" in rule and value > rule["maximum"]:
        raise ValueError("Value above document maximum")
    if "minLength" in rule and len(value.strip()) < rule["minLength"]:
        raise ValueError("Document text is empty")
    if kind == "object":
        properties = rule.get("properties", {})
        if set(rule.get("required", [])) - value.keys():
            raise ValueError("Required document fields are missing")
        if rule.get("additionalProperties") is False and value.keys() - properties.keys():
            raise ValueError("Unknown document fields")
        for key, child in value.items():
            if key in properties:
                validate_document(child, properties[key])
    return value
