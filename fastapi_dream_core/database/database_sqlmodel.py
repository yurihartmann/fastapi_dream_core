import traceback
from contextlib import contextmanager

from sqlmodel import create_engine, Session

from fastapi_dream_core.application_dependencies.application_dependencies_abc import ApplicationDependenciesABC
from fastapi_dream_core.utils import logger


class DatabaseSQLModel(ApplicationDependenciesABC):

    def __init__(self, db_url: str, echo_queries: bool = False) -> None:
        self._engine = create_engine(db_url, echo=echo_queries)

    def readiness(self) -> bool:
        with Session(self._engine) as session:
            try:
                database_status = session.connection().connection.is_valid
                logger.debug(f"DatabaseSQLModel.readiness = {database_status}")
                return True

            except Exception:
                traceback.print_exc()
                return False

    @contextmanager
    def session(self) -> Session:
        with Session(self._engine) as session:
            try:
                yield session
            except Exception:
                logger.exception("Session rollback because of exception")
                session.rollback()
                raise
            finally:
                session.close()

    def __str__(self):
        return "DatabaseSQLModel"
