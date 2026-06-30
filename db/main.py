from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from utils.common import get_env_variable_value

mysql_database_url = get_env_variable_value("MYSQL_DATABASE_URL")

BASE_DIR = Path(__file__).resolve().parent.parent
CA_CERT = BASE_DIR / "certs" / "ca.pem"

engine = create_engine(
    mysql_database_url,
    connect_args={
        "ssl": {
            "ca": str(CA_CERT)
        }
    }
)

Sessionlocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db_instance():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()