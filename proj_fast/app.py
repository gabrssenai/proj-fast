from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from proj_fast.database import get_session
from proj_fast.models import User
from proj_fast.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()


database: list[UserDB] = []


@app.post(
    '/users/',
    status_code=HTTPStatus.CREATED,
    response_model=UserPublic,
)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = User(
        username=user.username,
        password=user.password,
        email=user.email,
    )
    try:
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or email already exists',
        )
    return db_user


@app.put(
    '/users/{user_id}',
    response_model=UserPublic,
)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):

    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )
    try:
        db_user.username = user.username
        db_user.email = user.email
        db_user.password = user.password
        session.commit()
        session.refresh(db_user)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )
    return db_user


@app.delete(
    '/users/{user_id}',
    response_model=Message,
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )
    session.delete(db_user)
    session.commit()
    return {'message': 'User deleted'}


@app.get(
    '/users/{user_id}',
    response_model=UserPublic,
)
def read_user(
    user_id: int,
    session: Session = Depends(get_session),
):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )
    return db_user


@app.get(
    '/users/',
    response_model=UserList,
)
def read_users(session: Session = Depends(get_session)):
    users = session.scalars(select(User)).all()
    return {'users': users}


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def read_root():
    return {'message': 'Olá, Mundo!'}
