# init_db.py
from app.db import engine
from app.models import Base

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Done!")