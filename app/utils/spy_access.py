from datetime import datetime, timedelta, timezone, time
from flask import session

def _end_of_today():
    tomorrow = _now().date() + timedelta(days=1)
    return datetime.combine(tomorrow, time.min, tzinfo=timezone.utc)

def _now():
    return datetime.now(timezone.utc)

def grant_spy_access(spy_knight_id, target_knight_id):
    session["spy_access"] = {
        "owner": spy_knight_id,
        "target": target_knight_id,
        "expires_at": _end_of_today().isoformat(),
    }
    session.permanent = True


def get_active_target(spy_knight_id):
    data = session.get("spy_access")
    if not data or data.get("owner") != spy_knight_id:
        return None

    if datetime.fromisoformat(data["expires_at"]) < _now():
        session.pop("spy_access", None)
        return None

    return data["target"]