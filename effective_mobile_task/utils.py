from sqlalchemy.orm import Session

class DBTransaction:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc, tb):
        if exc is None:
            return self.db_session.commit()
        
        self.db_session.rollback()

        raise exc