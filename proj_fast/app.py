from http import HTTPStatus

from fastapi import FastAPI

from proj_fast.schemas import Message, UserSchema

app = FastAPI()


@app.post(
        '/users',
        status_code=HTTPStatus.CREATED,
)
def create_user(user: UserSchema):
    ...

@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def read_root():
    return {'message': 'Olá, Mundo!'}
