from contextlib import contextmanager
from database_access import get_session


@contextmanager
def session_scope():
    session = get_session()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()