from datetime import datetime, timezone
from models import User, UserIP


class UserRepository:
    def __init__(self, db_session):
        self.session = db_session

    def get_by_login(self, login: str):
        return self.session.query(User).filter(User.login == login).first()

    def get_by_id(self, user_id: int):
        return self.session.query(User).filter(User.id == user_id).first()

    def create_user(
        self,
        login: str,
        password_hash: str,
        role: str,
        is_white_knight: bool = False,
        lord_id: int = None,
        knight_id: int = None,
        commonfolk_id: int = None,
    ):
        user = User(
            login=login,
            password_hash=password_hash,
            role=role,
            is_white_knight=is_white_knight,
            lord_id=lord_id,
            knight_id=knight_id,
            commonfolk_id=commonfolk_id,
        )
        self.session.add(user)
        self.session.commit()
        return user

    def record_ip(self, user_id: int, ip_address: str):
        if not ip_address:
            return
        now_utc = datetime.now(timezone.utc).replace(tzinfo=None)
        record = (
            self.session.query(UserIP)
            .filter(UserIP.user_id == user_id, UserIP.ip_address == ip_address)
            .first()
        )
        if record:
            record.last_seen_at = now_utc
        else:
            record = UserIP(user_id=user_id, ip_address=ip_address, last_seen_at=now_utc)
            self.session.add(record)
        self.session.commit()