from database.models import Knight, User
from sqlalchemy import select

class KnightRepository:
    def __init__(self, session):
        self.session=session
        
    def create(
            self, 
            full_name, 
            login, 
            password_hash,
            photo_url,
            house,
            motto,
            strength,
            protection,
            dexterity,
            is_white_knight
        ):
        knight_user=User(
            login=login, 
            password_hash=password_hash,
            role="Knight"
        )
        self.session.add(knight_user)
        self.session.flush()

        knight_role=Knight(
            full_name=full_name, 
            photo_url=photo_url,
            house=house,
            motto=motto,
            strength=strength,
            protection=protection,
            dexterity=dexterity,
            user_id=knight_user.id,
            is_white_knight=is_white_knight
        )

        self.session.add(knight_role)
        self.session.flush()

        return knight_role

    def get_by_id(self, knight_id):
        result_knight=self.session.execute(
            select(Knight). \
            where(Knight.id==knight_id)
        ).scalars().first()

        return result_knight

    def get_all(self):
        return self.session.execute(
            select(Knight)
        ).scalars().all()

    def update_key(self, knight_id, key_hash, updated_at):
        knight = self.get_by_id(knight_id)
        knight.key_hash=key_hash
        knight.key_last_updated=updated_at

        self.session.flush()

        return knight

    def consume_key(self, knight_id):
        knight = self.get_by_id(knight_id)
        if not knight:
            return None

        knight.key_hash=None
        self.session.flush()

        return knight