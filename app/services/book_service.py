from database.models import Session
from database.repositories.knight_repository import KnightRepository
from database.repositories.lord_repository import LordRepository

def get_all_lords():
    try:
        with Session() as session:
            lords = LordRepository(session).get_all()
            return [
                {
                    "id": lord.id,
                    "role": "Lord",
                    "full_name": lord.full_name,
                    "house": lord.house,
                    "photo_url": lord.photo_url,
                }
                for lord in lords
            ], None

    except Exception as ex:
        return None, f"Database Error: {ex}"


def _get_viewer_house(session, role, profile_id):
    if profile_id is None:
        return None

    if role == "Knight":
        viewer = KnightRepository(session).get_by_id(int(profile_id))
        return viewer.house if (viewer and viewer.house) else None

    if role == "Lord":
        viewer = LordRepository(session).get_by_id(int(profile_id))
        return viewer.house if (viewer and viewer.house) else None

    return None

def get_all_knights(current_role, current_profile_id, unlocked_id=None):
    try:
        with Session() as session:
            viewer_house = _get_viewer_house(session, current_role, current_profile_id)
            knights = KnightRepository(session).get_all()

            result = []
            for knight in knights:
                is_owner = (
                    current_role == "Knight"
                    and current_profile_id is not None
                    and knight.id == int(current_profile_id)
                )
                is_same_house = (
                    viewer_house is not None
                    and knight.house is not None
                    and viewer_house == knight.house
                )
                can_view_stats = (
                        is_owner
                        or is_same_house
                        or bool(knight.is_white_knight)
                        or knight.id == unlocked_id
                )

                result.append({
                    "id": knight.id,
                    "role": "Knight",
                    "full_name": knight.full_name,
                    "house": knight.house,
                    "motto": knight.motto,
                    "photo_url": knight.photo_url,
                    "is_white_knight": bool(knight.is_white_knight),
                    "can_view_stats": can_view_stats,
                    "strength": knight.strength if can_view_stats else None,
                    "dexterity": knight.dexterity if can_view_stats else None,
                    "protection": knight.protection if can_view_stats else None,
                })

            return result, None

    except Exception as ex:
        return None, f"Database Error: {ex}"