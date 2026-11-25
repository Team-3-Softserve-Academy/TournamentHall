from database.models import Session
from database.repositories.knight_repository import KnightRepository
from database.repositories.lord_repository import LordRepository

def get_all_lords():
    session = Session()
    try:
        lords = LordRepository(session).get_all()
        return [
            {
                "id": lord.id,
                "full_name": lord.full_name,
                "home": lord.home,
                "photo_url": lord.photo_url,
            }
            for lord in lords
        ], None

    except Exception as ex:
        session.rollback()
        return None, f"Database Error: {ex}"
    finally:
        session.close()


def _get_viewer_home(session, role, profile_id):
    if profile_id is None:
        return None

    if role == "Knight":
        viewer = KnightRepository(session).get_by_id(int(profile_id))
        return viewer.home if (viewer and viewer.home) else None

    if role == "Lord":
        viewer = LordRepository(session).get_by_id(int(profile_id))
        return viewer.home if (viewer and viewer.home) else None

    return None

def get_all_knights(current_role, current_profile_id, unlocked_id=None):
    session = Session()
    try:
        viewer_home = _get_viewer_home(session, current_role, current_profile_id)
        knights = KnightRepository(session).get_all()

        result = []
        for knight in knights:
            is_owner = (
                current_role == "Knight"
                and current_profile_id is not None
                and knight.id == int(current_profile_id)
            )
            is_same_house = (
                viewer_home is not None
                and knight.home is not None
                and viewer_home == knight.home
            )
            can_see_stats = (
                    is_owner
                    or is_same_house
                    or bool(knight.is_white_knight)
                    or knight.id == unlocked_id
            )

            result.append({
                "id": knight.id,
                "full_name": knight.full_name,
                "home": knight.home,
                "motto": knight.motto,
                "photo_url": knight.photo_url,
                "is_white_knight": bool(knight.is_white_knight),
                "stats_visible": can_see_stats,
                "strength": knight.strength if can_see_stats else None,
                "protection": knight.protection if can_see_stats else None,
                "speed": knight.speed if can_see_stats else None,
            })

        return result, None

    except Exception as ex:
        session.rollback()
        return None, f"Database Error: {ex}"
    finally:
        session.close()