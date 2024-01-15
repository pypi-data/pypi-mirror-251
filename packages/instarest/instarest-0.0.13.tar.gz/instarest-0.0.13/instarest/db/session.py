from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from instarest.core.config import get_core_settings

if get_core_settings().db_rootcert_path is None:
    connect_args = {}
else:
    connect_args = {
        "sslrootcert": get_core_settings().db_rootcert_path,
        "sslmode": "verify-full",
    }

engine = create_engine(
    get_core_settings().sqlalchemy_database_uri,
    connect_args=connect_args,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
