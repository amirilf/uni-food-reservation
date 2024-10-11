from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from database.user_model import User

async def create_user(db: AsyncSession, t_id: str, t_fullname: str) -> User | None:
    new_user = User(t_id=t_id, t_fullname=t_fullname)
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Error creating user: {e}")
        return None
    return new_user

async def get_user_by_t_id(db: AsyncSession, t_id: str) -> User | None:
    result = await db.execute(select(User).filter(User.t_id == t_id))
    return result.scalars().first()

async def get_user_stage_by_t_id(db: AsyncSession, t_id: str) -> int | None:
    result = await db.execute(select(User.user_stage).filter(User.t_id == t_id))
    user_stage = result.scalars().first()
    return user_stage if user_stage else None

async def update_user(db: AsyncSession, t_id: str, **kwargs) -> User | None:
    result = await db.execute(select(User).filter(User.t_id == t_id))
    user = result.scalars().first()

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
        await db.commit()
        await db.refresh(user)
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Error updating user: {e}")
        return None

    return user

async def get_user_credentials(db: AsyncSession, t_id: str) -> list[str]:
    result = await db.execute(select(User.username, User.password, User.user_stage).filter(User.t_id == t_id))
    user = result.first()
    return user if user else None
