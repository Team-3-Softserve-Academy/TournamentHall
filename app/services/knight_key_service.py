from app.utils.validators import hash_password, has_forbidden_chars
from database.models import Session
from database.repositories.knight_repository import KnightRepository
from datetime import datetime, timezone
import secrets, hmac

def get_spy_key_status(knight_id):
    try:
        with Session() as session:
            knight = KnightRepository(session).get_by_id(knight_id)
            if not knight:
                return None, "Knight not found"

            now = datetime.now(timezone.utc).replace(tzinfo=None)
            can_generate = knight.key_last_updated is None or knight.key_last_updated.date() < now.date()
            has_active_key = bool(knight.key_hash) and (knight.key_last_updated is not None and knight.key_last_updated.date() == now.date())

            return {"has_active_key": has_active_key,
                    "can_generate": can_generate,
                    "key_last_updated": knight.key_last_updated.isoformat() if knight.key_last_updated else None,
                    }, None

    except Exception as ex:
        return None, f"Database error: {ex}"


def generate_spy_key(knight_id):
    try:
        with Session.begin() as session:
            knight = KnightRepository(session).get_by_id(knight_id)
            if not knight:
                return None, "Knight not found"

            now = datetime.now(timezone.utc).replace(tzinfo=None)
            if knight.key_last_updated is not None and knight.key_last_updated.date() == now.date():
                return None, "Spy key can only be generated once per calendar day."

            raw_key = secrets.token_urlsafe(16)
            key_hash = hash_password(raw_key)

            knight = KnightRepository(session).update_key(knight_id, key_hash, now)

            return {"key": raw_key,
                    "key_last_updated": knight.key_last_updated.isoformat() if (knight and knight.key_last_updated) else None,
                    }, None

    except Exception as ex:
        return None, f"Database error: {ex}"


def spy_on_knight(spy_knight_id, target_knight_id, provided_key):
    try:
        with Session.begin() as session:
            if spy_knight_id == target_knight_id:
                return None, "Can't spy on yourself"

            provided_key = (provided_key or "").strip()
            if not provided_key or has_forbidden_chars(provided_key):
                return None, "Provided key is invalid"

            spy_knight = KnightRepository(session).get_by_id(spy_knight_id)
            if not spy_knight:
                return None, "Spy knight not found"

            now = datetime.now(timezone.utc).replace(tzinfo=None)
            if not spy_knight.key_hash:
                return None, "No active spy key"
            if spy_knight.key_last_updated is None or spy_knight.key_last_updated.date() != now.date():
                return None, "Spy key expired"

            if not hmac.compare_digest(hash_password(provided_key), spy_knight.key_hash):
                return None, "Provided key is invalid"

            target_knight = KnightRepository(session).get_by_id(target_knight_id)
            if not target_knight:
                return None, "Target knight not found"

            KnightRepository(session).consume_key(spy_knight_id)

            return {"knight_id": target_knight.id,
                    "full_name": target_knight.full_name,
                    "strength": target_knight.strength,
                    "protection": target_knight.protection,
                    "speed": target_knight.speed,
            }, None

    except Exception as ex:
        return None, f"Database error: {ex}"