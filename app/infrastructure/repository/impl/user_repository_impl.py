from sqlalchemy.orm import Session
from app.domain.models.user_model import User
from app.infrastructure.repository.interfaces.user_note_interfaces import CRUDRep
from app.utils.security import check_encrypted_password

class UserRepositoryImpl:
    def create_user(self, db: Session, username: str, hashed_password: str) -> User:
        user = User(username=username, password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    def verify_user(self, db: Session, username: str, password: str):
        
        user = db.query(User).filter(User.username == username).first()
        print(username, password)
        if not user:
            raise NameError("Usuario o contraseña incorrectos")

        if not check_encrypted_password(password, user.password):
            
            raise NameError("Usuario o contraseña incorrectos")

        return user

