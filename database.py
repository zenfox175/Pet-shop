from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "sqlite:///./pet.db"


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})



@event.listens_for(engine, "connect")
def _habilitar_foreign_keys(conexao_dbapi, connection_record):
    cursor = conexao_dbapi.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
