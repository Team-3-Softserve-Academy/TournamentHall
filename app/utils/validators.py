import hashlib

FORBIDDEN_CHARS = ";,'[].{}()<>\\|/&="

def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def has_forbidden_chars(text):
    if not text:
        return False

    return any(char in text for char in FORBIDDEN_CHARS)


def parse_knight_stats(strength_raw, protection_raw, speed_raw):
    try:
        strength = int(strength_raw)
        protection = int(protection_raw)
        speed = int(speed_raw)

        for value in (strength, protection, speed):
            if value < 0 or value > 20:
                return (None, "Stats must be between 0 and 20")

        return (strength, protection, speed), None
    except (ValueError, TypeError):
        return (None, "Stats must be integers between 0 and 20")