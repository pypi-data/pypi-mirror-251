import re

_SPLIT_CAMEL_CASE_PATTERN = re.compile(
    ".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)"
)


def all_lower_to_camel_case(name: str) -> str:
    """
    Converts a string from all_lower_case to camelCase.
    """
    assert name.islower(), name

    if not name:
        return ""

    parts = name.split("_")
    assert parts, (name, parts)

    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def all_upper_to_camel_case(name: str) -> str:
    """
    Converts a string from ALL_UPPER_CASE to camelCase.
    """
    assert name.isupper(), name

    if not name:
        return ""

    parts = name.split("_")
    assert parts, (name, parts)

    return parts[0].lower() + "".join(p.capitalize() for p in parts[1:])


def camel_case_to_all_upper(name: str) -> str:
    """
    Converts a string from camelCase to ALL_UPPER_CASE.
    """
    matches = _SPLIT_CAMEL_CASE_PATTERN.finditer(name)
    groups = [m.group(0).upper() for m in matches]
    return "_".join(groups)


def upper_camel_case_to_camel_case(name: str) -> str:
    """
    Converts a string from UpperCamelCase to camelCase.
    """
    if not name:
        return ""

    return name[0].lower() + name[1:]
