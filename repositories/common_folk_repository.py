from models import CommonFolk


class CommonFolkRepository:
    def __init__(self, db_session):
        self.session = db_session

    def create_commonfolk(self, name: str, login: str, password_hash: str):
        folk = CommonFolk(name=name, login=login, password_hash=password_hash)
        self.session.add(folk)
        self.session.commit()
        return folk

    def get_commonfolk_by_id(self, folk_id: int):
        return self.session.query(CommonFolk).filter(CommonFolk.id == folk_id).first()

    def get_commonfolk_by_login(self, login: str):
        return self.session.query(CommonFolk).filter(CommonFolk.login == login).first()

    def update_commonfolk(self, folk_id: int, **kwargs):
        folk = self.get_commonfolk_by_id(folk_id)
        if folk:
            for key, value in kwargs.items():
                if hasattr(folk, key):
                    setattr(folk, key, value)
            self.session.commit()
        return folk

    def delete_commonfolk(self, folk_id: int):
        folk = self.get_commonfolk_by_id(folk_id)
        if folk:
            self.session.delete(folk)
            self.session.commit()
            return True
        return False
