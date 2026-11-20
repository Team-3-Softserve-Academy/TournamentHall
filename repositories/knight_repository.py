from datetime import datetime
from models import Knight


class KnightRepository:
    def __init__(self, db_session):
        self.session = db_session

    def create_knight(
        self,
        name: str,
        login: str,
        password_hash: str,
        image_url: str = None,
        strength: int = None,
        speed: int = None,
        protection: int = None,
        house: str = None,
        key: str = None,
        key_last_used: datetime = None,
    ):
        knight = Knight(
            name=name,
            login=login,
            password_hash=password_hash,
            image_url=image_url,
            strength=strength,
            speed=speed,
            protection=protection,
            house=house,
            key=key,
            key_last_used=key_last_used,
        )
        self.session.add(knight)
        self.session.commit()
        return knight

    def get_knight_by_id(self, knight_id: int):
        return self.session.query(Knight).filter(Knight.id == knight_id).first()

    def get_knight_by_login(self, login: str):
        return self.session.query(Knight).filter(Knight.login == login).first()

    def update_knight(self, knight_id: int, **kwargs):
        knight = self.get_knight_by_id(knight_id)
        if knight:
            for key, value in kwargs.items():
                if hasattr(knight, key):
                    setattr(knight, key, value)
            self.session.commit()
        return knight

    def delete_knight(self, knight_id: int) -> bool:
        knight = self.get_knight_by_id(knight_id)
        if knight:
            self.session.delete(knight)
            self.session.commit()
            return True
        return False

    def get_all_knights(self):
        return self.session.query(Knight).order_by(Knight.name, Knight.id).all()

    def get_knights_paginated(self, page: int, page_size: int):
        if page < 1 or page_size < 1:
            return None

        offset = (page - 1) * page_size
        return (
            self.session.query(Knight)
            .order_by(Knight.name, Knight.id)
            .limit(page_size)
            .offset(offset)
            .all()
        )
