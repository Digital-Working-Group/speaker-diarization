"""
check_sensitive_patterns.py
Pre-commit hook that scans staged file contents for organization-specific
sensitive data patterns (e.g. participant/subject IDs) that generic secret
scanners such as detect-secrets are not aware of, since these look like
ordinary text rather than credentials.

Run automatically by pre-commit; can also be run manually:
    python scripts/check_sensitive_patterns.py <file> [<file> ...]

EDIT ME: replace PARTICIPANT_ID_PATTERN below with your team's real
participant/subject ID format once it is finalized. The placeholder below
matches a 2-4 letter prefix followed by 3-6 digits (e.g. "hv1023",
"buin00427", uppercased) and exists so the hook has something concrete to enforce
today; tighten or replace it as needed. Add further patterns to
SENSITIVE_PATTERNS the same way for any other org-specific identifiers.
"""
import re
import sys

PARTICIPANT_ID_PATTERN = re.compile(r"\b[A-Z]{2,4}-?\d{3,6}\b")

SENSITIVE_PATTERNS = {
    "participant_id_placeholder": PARTICIPANT_ID_PATTERN,
}

# Sample/ground-truth data shipped with the repo is de-identified and may
# legitimately look like these patterns; skip it to avoid false positives.
EXEMPT_PATHS = (
    "sample_files/",
    "ground_truth_files/",
    "data_dictionary/",
)


def is_exempt(path):
    normalized = path.replace("\\", "/")
    return any(normalized.startswith(prefix) for prefix in EXEMPT_PATHS)


def scan_file(path):
    if is_exempt(path):
        return []
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as infile:
            text = infile.read()
    except OSError:
        return []
    findings = []
    for name, pattern in SENSITIVE_PATTERNS.items():
        for match in pattern.finditer(text):
            findings.append((name, match.group(0)))
    return findings


def main(argv):
    had_findings = False
    for path in argv:
        for name, value in scan_file(path):
            had_findings = True
            print(f"{path}: possible {name} match: {value!r}")
    if had_findings:
        print(
            "\nPossible organization-specific sensitive data detected above. "
            "If this is a real participant identifier, remove it before "
            "committing. If it is a false positive, either adjust "
            "SENSITIVE_PATTERNS in scripts/check_sensitive_patterns.py or "
            "add the path to EXEMPT_PATHS."
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
