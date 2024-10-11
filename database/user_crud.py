from sqlalchemy.orm import Session
from user_model import User
from sqlalchemy.exc import SQLAlchemyError

def create_user(db: Session, t_id: str, t_fullname: str) -> User | None:
    new_user = User(t_id=t_id, t_fullname=t_fullname)
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error creating user: {e}")
        return None
    return new_user

def get_user_by_t_id(db: Session, t_id: str) -> User | None:
    return db.query(User).filter(User.t_id == t_id).first()

def get_user_stage_by_t_id(db: Session, t_id: str) -> int | None:
    user = db.query(User.user_stage).filter(User.t_id == t_id).first()
    return user.user_stage if user else None

def update_user(db: Session, t_id: str, **kwargs) -> User | None:
    user = db.query(User).filter(User.t_id == t_id).first()
    if not user:
        return None

    allowed_fields = {
        'username', 'password', 'fullname', 'gender', 
        'national_number', 'phone', 'email', 'faculty', 'user_stage'
    }

    for key, value in kwargs.items():
        if key in allowed_fields and value is not None:
            setattr(user, key, value)

    try:
        db.commit()
        db.refresh(user)
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error updating user: {e}")
        return None

    return user

def get_user_credentials(db: Session, t_id: str) -> list[str]:
    user = db.query(User.username, User.password, User.user_stage).filter(User.t_id == t_id).first()
    return user
