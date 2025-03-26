from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está configurada en el archivo .env")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_admin_user():
    from app.models.user import User
    from app.utils.security import hash_password
    db = SessionLocal()
    existing_user = db.query(User).filter_by(email="admin@cataloniablackballparty.com").first()
    if existing_user:
        print("El usuario administrador ya existe.")
        db.close()
        return
    hashed_password = hash_password("admin_password")
    admin_user = User(
        email="admin@cataloniablackballparty.com",
        first_name="Admin",
        last_name="CBP",
        gender="Male",
        country="ES",
        phone_number="600496070",
        hashed_password=hashed_password,
        role="admin",
        is_active=True,
        is_verified=True,
        is_profile_complete=True
    )
    db.add(admin_user)
    db.commit()
    db.close()
if __name__ == "__main__":
    create_admin_user()
