import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tci.db.models import Base
from tci.db.postgresql import Database


@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine"""
    TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost/tci_test"
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="session")
def test_db(test_engine):
    """Create test database instance"""
    TestSessionLocal = sessionmaker(bind=test_engine)

    class TestDatabase(Database):
        def get_session(self):
            db = TestSessionLocal()
            try:
                return db
            finally:
                db.close()

    return TestDatabase()
