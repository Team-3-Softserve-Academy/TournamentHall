from app.utils.validators import has_forbidden_chars, hash_password, parse_knight_stats
from database.models import Session
from database.repositories.common_folk_repository import CommonFolkRepository
from database.repositories.lord_repository import LordRepository
from database.repositories.knight_repository import KnightRepository
from database.repositories.user_repository import UserRepository


def register_user(data: dict):
    role = (data.get('role') or "").strip()
    login = (data.get('login') or "").strip()
    password = data.get('password') or ""
    #TODO ROOT-57: full_name field in registration form
    full_name = (data.get("full_name") or login).strip()

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

            #TODO ROOT-63: Photo upload

            if role == "CommonFolk":
                if not full_name:
                    return None, "Full name cannot be empty."
                if has_forbidden_chars(full_name):
                    return None, "Forbidden chars in full name."

                profile = CommonFolkRepository(session).create(full_name=full_name, login=login, password_hash=hashed_password)

            elif role == "Lord":
                house = (data.get("house") or "").strip()

                if not full_name:
                    return None, "Full name cannot be empty."
                if has_forbidden_chars(full_name):
                    return None, "Forbidden chars in full name."
                if not house:
                    return None, "House cannot be empty."
                if has_forbidden_chars(house):
                    return None, "Forbidden chars in house."

                profile = LordRepository(session).create(full_name=full_name, house=house, login=login, password_hash=hashed_password, photo_url=None)

            elif role == "Knight":
                house = (data.get("house") or "").strip()
                motto = (data.get("motto") or "").strip()
                is_white_knight = bool(data.get("is_white_knight", False))

                if not full_name:
                    return None, "Full name cannot be empty."
                if has_forbidden_chars(full_name):
                    return None, "Forbidden chars in full name."
                if not house:
                    return None, "House cannot be empty."
                if has_forbidden_chars(house):
                    return None, "Forbidden chars in house."
                if has_forbidden_chars(motto):
                    return None, "Forbidden chars in motto."

                stats, err = parse_knight_stats(data.get("strength"), data.get("dexterity"), data.get("protection"))
                if err:
                    return None, err
                strength, dexterity, protection = stats
                profile = KnightRepository(session).create(
                    full_name=full_name,
                    login=login,
                    strength=strength,
                    dexterity=dexterity,
                    protection=protection,
                    house=house,
                    motto=motto,
                    photo_url=None,
                    password_hash=hashed_password,
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
