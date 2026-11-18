from models import Lord

class LordRepository:
    def __init__(self, db_session):
        self.session = db_session

    def create_lord(self, name: str, image_url: str = None, house: str = None):
        lord = Lord(name=name, image_url=image_url, house=house)
        self.session.add(lord)
        self.session.commit()
        return lord

    def get_lord_by_id(self, lord_id: int):
        return self.session.query(Lord).filter(Lord.id == lord_id).first()

    def update_lord(self, lord_id: int, **kwargs):
        lord = self.get_lord_by_id(lord_id)
        if lord:
            for key, value in kwargs.items():
                if hasattr(lord, key):
                    setattr(lord, key, value)
            self.session.commit()
        return lord

    def delete_lord(self, lord_id: int) -> bool:
        lord = self.get_lord_by_id(lord_id)
        if lord:
            self.session.delete(lord)
            self.session.commit()
            return True
        return False

    def get_all_lords(self):
        return self.session.query(Lord).order_by(Lord.name, Lord.id).all()

    def get_lords_paginated(self, page: int, page_size: int):
        if(page < 1 or page_size < 1):
            return None

        offset = (page - 1) * page_size
        return self.session.query(Lord).order_by(Lord.name, Lord.id).limit(page_size).offset(offset).all()

