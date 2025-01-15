# The model registration happens automatically when the model classes are imported,
# since they inherit from Base which tracks all model classes.
# Simply importing them is enough to register them with SQLAlchemy's metadata.
from tci.db.models import Company  # Company model
from tci.db.models import Job  # Job model
from tci.db.models import User  # Add any new models here; User model
from tci.db.postgresql import Base, engine


def init_database():
    """Initialize the database by creating all tables"""
    # The models are already registered through inheritance and import
    # This just shows what models were registered
    print("Registered models:", Base.metadata.tables.keys())

    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_database()
