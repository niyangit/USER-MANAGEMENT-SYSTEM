from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from utils.common import get_env_variable_value

mysql_database_url=get_env_variable_value("MYSQL_DATABASE_URL")


engine = create_engine(mysql_database_url)

Sessionlocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()


def get_db_instance():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()