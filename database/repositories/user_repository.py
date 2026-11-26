from database.models import Knight, CommonFolk, Lord, User
from sqlalchemy import select

class UserRepository():
    def __init__(self, session):
        self.session=session
        
    def is_user(self, login):
        is_user_exists=False

        result_user=self.session.execute(
            select(User). \
            where(User.login==login)
        )
        if(result_user.scalars().first()):
            is_user_exists=True

        return is_user_exists

    def get_data_by_credentials(self, user_login, user_password_hash):

        role_data=self.session.execute(
            select(Lord, Knight, CommonFolk). \
            select_from(User). \
            outerjoin(Lord, Lord.user_id==User.id). \
            outerjoin(Knight, Knight.user_id==User.id). \
            outerjoin(CommonFolk, CommonFolk.user_id==User.id). \
            where(User.login==user_login, User.password_hash==user_password_hash)
        ).first()

        if(role_data==None):
            return None

        target_data=None
        for data in role_data:
            if data != None:
                target_data=data

        return target_data