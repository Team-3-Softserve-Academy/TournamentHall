from database.models import Lord, User
from sqlalchemy import select

class LordRepository:
    def __init__(self, session):
        self.session=session
        
    def create(
            self, 
            full_name, 
            login, 
            password_hash,
            photo_url,
            home
        ):  
        lord_user=User(
            login=login, 
            password_hash=password_hash,
            role="Lord"
        )
        self.session.add(lord_user)
        self.session.flush()

        lord_role=Lord(
            full_name=full_name, 
            photo_url=photo_url,
            home=home,
            
            user_id=lord_user.id,
        )

        self.session.add(lord_role)
        self.session.commit()

        return lord_role

    def get_by_id(self, lord_id):
        result_lord=self.session.execute(
            select(Lord). \
            where(Lord.id==lord_id)
        ).scalars().first()

        return result_lord