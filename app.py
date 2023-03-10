import copy
import fastapi
import database
import pydantic_models
import config
from fastapi import Request
fake_datebase = {'users': [
    {
        'id': 1,
        'name': 'anna',
        'nick': 'Anna42',
        'balance': 15300
    },
    {
        'id': 2,
        'name': 'Dima',
        'nick': 'dimon123',
        'balance': 8.01
    },
    {
        'id': 3,
        'name': 'Vladimir',
        'nick': 'Vova777',
        'balance': 200.1
    }], }


api = fastapi.FastAPI()


@api.get('/users/')
def get_users(skip: int = 0, limit: int = 10):
    return fake_datebase['users'][skip: skip + limit]


@api.get('/user/{user_id}')
def read_user(user_id: str, query: str | None = None):
    if query:
        return {'user_id': user_id, 'query': query}
    return {"user_id": user_id}


@api.get('/get_info_by_user_id/{id:int}')
def get_info_about_user(id):
    return fake_datebase['users'][id-1]


@api.get('/get_user_balance_by_id/{id:int}')
def get_user_balance(id):
    return fake_datebase['users'][id-1]['balance']


@api.get('/get_total_balance')
def get_total_balance():
    total_balance: float = 0.0
    for user in fake_datebase['users']:
        total_balance += pydantic_models.User(**user).balance
    return total_balance


@api.post('/user/create')
def index(user: pydantic_models.User):
    fake_datebase['users'].append(user)
    return {'User Created!': user}


@api.put('/user/{user_id}')
def update_user(user_id: int, user: pydantic_models.User = fastapi.Body()):
    for index, u in enumerate(fake_datebase['users']):
        if u['id'] == user_id:
            fake_datebase['users'][index] = user
            return user


@api.delete('/user/{user_id}')
def delete_user(user_id: int = fastapi.Path()):
    for index, u in enumerate(fake_datebase['users']):
        if u['id'] == user_id:
            old_db = copy.deepcopy(fake_datebase)
            del fake_datebase['users'][index]
            return {'old_db': old_db,
                    'new_db': fake_datebase}
