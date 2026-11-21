from models import CommonFolk
from models import User
from sqlalchemy import select

class CommonFolkRepository:
    def __init__(self, session):
        self.session=session
        
    def create(self, name, login, password_hash):
        commonfolk_user=User(
            login=login, 
            password_hash=password_hash,
            role="CommonFolk"
        )
        self.session.add(commonfolk_user)
        self.session.flush()

        commonfolk_role=CommonFolk(
            name=name, 
            user_id=commonfolk_user.id,
        )

        self.session.add(commonfolk_role)
        self.session.commit()

        return commonfolk_role


    def get_by_id(self, folk_id):
        result_commonfolk=self.session.execute(
            select(CommonFolk). \
            where(CommonFolk.id==folk_id)
        ).scalars().first()

        return result_commonfolk