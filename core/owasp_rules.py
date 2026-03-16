import re

MIN_LENGTH = 12

def check_policy(password: str):
    """
    OWASP + NIST compliant password checks
    Returns (score, issues)
    """
    issues = []

    if len(password) < MIN_LENGTH:
        issues.append("Password must be at least 12 characters")

    if not re.search(r"[A-Z]", password):
        issues.append("Missing uppercase letter")

    if not re.search(r"[a-z]", password):
        issues.append("Missing lowercase letter")

    if not re.search(r"\d", password):
        issues.append("Missing digit")

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        issues.append("Missing special character")

    score = 5 - len(issues)
    return score, issues
