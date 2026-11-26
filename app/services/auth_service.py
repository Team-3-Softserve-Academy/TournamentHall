from app.utils.validators import has_forbidden_chars, hash_password, parse_knight_stats
from database.models import Session
from database.repositories.common_folk_repository import CommonFolkRepository
from database.repositories.lord_repository import LordRepository
from database.repositories.knight_repository import KnightRepository
from database.repositories.user_repository import UserRepository

#TEMPORARY ADAPTER. REMOVE AFTER FIXING CONSISTENCY BETWEEN FRONT AND BD

ROLE_ALIASES = {
    "Smallfolk": "CommonFolk"
}

def _adapt_register_data(raw_data: dict):
    adapted = dict(raw_data)

    role = (adapted.get("role") or "").strip()
    adapted["role"] = ROLE_ALIASES.get(role, role)

    if not adapted.get("home") and adapted.get("house"):
        adapted["home"] = adapted.get("house")

    if adapted.get("protection") is None and adapted.get("constitution") is not None:
        adapted["protection"] = adapted.get("constitution")
    if adapted.get("speed") is None and adapted.get("dexterity") is not None:
        adapted["speed"] = adapted.get("dexterity")

    login = (adapted.get("login") or "").strip()
    if not adapted.get("full_name"):
        adapted["full_name"] = login
    if not adapted.get("name"):
        adapted["name"] = adapted["full_name"]

    adapted.setdefault("motto", "")
    adapted.setdefault("photo_url", "default_photo_url")

    return adapted

def register_user(data: dict):
    data = _adapt_register_data(data)

    role = (data.get('role') or "").strip()
    login = (data.get('login') or "").strip()
    password = data.get('password') or ""

    if not login or not password:
        return None, "Login and password are required."

    if role not in ("Lord", "Knight", "CommonFolk"):
        return None, "Role must be Lord or Knight or CommonFolk."

    if has_forbidden_chars(login) or has_forbidden_chars(password):
        return None, "Forbidden chars in entry fields."

    try:
        with Session.begin() as session:
            user_repo = UserRepository(session)

            if user_repo.is_user(login):
                return None, "User already exists."

            hashed_password = hash_password(password)

            photo_url = data.get('photo_url') or "default_photo_url"

            if role == "CommonFolk":
                name = (data.get("name") or data.get("full_name") or "").strip()

                if not name:
                    return None, "Name cannot be empty."

                if has_forbidden_chars(name):
                    return None, "Forbidden chars in name."

                profile = CommonFolkRepository(session).create(name=name, login=login, password_hash=hashed_password)

            elif role == "Lord":
                full_name = (data.get("full_name") or "").strip()
                home = (data.get("home") or "").strip()

                if not full_name:
                    return None, "Full name cannot be empty."
                if has_forbidden_chars(full_name):
                    return None, "Forbidden chars in full name."
                if not home:
                    return None, "Home cannot be empty."
                if has_forbidden_chars(home):
                    return None, "Forbidden chars in home."

                profile = LordRepository(session).create(full_name=full_name, home=home, login=login, password_hash=hashed_password, photo_url=photo_url)

            elif role == "Knight":
                full_name = (data.get("full_name") or "").strip()
                home = (data.get("home") or "").strip()
                motto = (data.get("motto") or "").strip()
                is_white_knight = bool(data.get("is_white_knight", False))

                if not full_name:
                    return None, "Full name cannot be empty."
                if has_forbidden_chars(full_name):
                    return None, "Forbidden chars in full name."
                if not home:
                    return None, "Home cannot be empty."
                if has_forbidden_chars(home):
                    return None, "Forbidden chars in home."
                if has_forbidden_chars(motto):
                    return None, "Forbidden chars in motto."

                stats, err = parse_knight_stats(data.get("strength"), data.get("protection"), data.get("speed"))
                if err:
                    return None, err
                strength, protection, speed = stats
                profile = KnightRepository(session).create(
                    full_name=full_name,
                    login=login,
                    strength=strength,
                    protection=protection,
                    speed=speed,
                    home=home,
                    motto=motto,
                    photo_url=photo_url,
                    password_hash=hash_password(password),
                    is_white_knight=is_white_knight,
                )

            return {"user_id": profile.user_id, "profile_id": profile.id, "login": login, "role": role}, None

    except Exception as ex:
        return None, f"Database error: {ex}"


def authenticate_user(login, password):
    login = (login or "").strip()

    if not login or not password:
        return None, "Login and password are required."

    if has_forbidden_chars(login) or has_forbidden_chars(password):
        return None, "Forbidden chars in entry fields."

    try:
        with Session() as session:
            hashed_password = hash_password(password)
            profile = UserRepository(session).get_data_by_credentials(login, hashed_password)

            if not profile:
                return None, "User does not exist."

            return {
                "user_id": profile.user_id,
                "profile_id": profile.id,
                "login": login,
                "role": type(profile).__name__,
            }, None

    except Exception as ex:
        return None, f"Database error: {ex}"
