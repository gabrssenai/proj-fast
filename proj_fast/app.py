from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from proj_fast.database import get_session
from proj_fast.models import User
from proj_fast.schemas import (
    InterestList,
    InterestPublic,
    InterestSchema,
    Interest,
    Message, 
    UserDB, 
    UserList, 
    UserPublic, 
    UserSchema,
)

app = FastAPI()


origins = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['GET', 'POST'],
    allow_headers=['Content-Type'],
)

@app.post(
    '/interests/',
    status_code=HTTPStatus.CREATED,
    response_model=InterestPublic,
)
def create_interest(
    interest: InterestSchema,
    session: Session = Depends(get_session),
):
    db_interest = Interest(
    **interest.model_dump()
    )
    session.add(db_interest)
    session.commit()
    session.refresh(db_interest)
    return db_interest


@app.get(
    '/interests/',
    response_model=InterestList,
)
def read_interests(
    session: Session = Depends(get_session),
):
    interests = session.scalars(
        select(Interest)
    ).all()
    return {'interests': interests}


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
