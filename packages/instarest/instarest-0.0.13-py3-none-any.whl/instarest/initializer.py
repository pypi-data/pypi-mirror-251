import traceback
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
from instarest.db.base_class import DeclarativeBase
from instarest.db.init_db import init_db, wipe_db
from instarest.core.config import get_environment_settings
from instarest.core.logging import LogConfig
from instarest.db.session import SessionLocal


class Initializer:
    def __init__(self, Base: DeclarativeBase):
        self.logger = LogConfig(LOGGER_NAME=self.__class__.__name__).build_logger()
        self.Base = Base

    def init_db(self):
        init_db(self.Base)

    def wipe_db(self):
        wipe_db(self.Base)

    def init_vector_db(self, db: Session) -> None:
        try:
            db.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))  # for pgvector
            db.commit()
        except Exception as err:
            self.logger.error(err)
            traceback.print_exc()
            db.rollback()
            raise err

    def execute(self, migration_toggle=False, vector_toggle=False) -> None:
        # environment can be one of 'local', 'development, 'test', 'staging', 'production'
        environment = get_environment_settings().environment

        self.logger.info(f"Using initialization environment: {environment}")
        self.logger.info(f"Using migration toggle: {migration_toggle}")

        # clear DB if local or staging as long as not actively testing migrating
        if environment in ["local", "staging"] and migration_toggle is False:
            self.logger.info("Clearing database")
            self.wipe_db()
            self.logger.info("Database cleared")

        # setup vector db if desired
        if vector_toggle:
            self.logger.info("Connecting DB (InstarestInitializer)")
            db = SessionLocal()
            self.logger.info("DB connected (InstarestInitializer)")

            self.logger.info("Ensuring Vector extension is enabled in DB")
            self.init_vector_db(db)
            self.logger.info("Vector extension enabled in DB")

            db.close()

        # all environments need to initialize the database
        # prod only if migration toggle is on
        if environment in ["local", "development", "test", "staging"] or (
            environment == "production" and migration_toggle is True
        ):
            self.logger.info("Creating database schema and tables")
            self.init_db()
            self.logger.info("Initial database schema and tables created.")
        else:
            self.logger.info("Skipping database initialization")
