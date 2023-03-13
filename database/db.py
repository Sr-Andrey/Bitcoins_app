from pony.orm import *

db = Database()


class User(db.Entity):
    user_id = Required(str)
    nick = Required(str)
    age = Required(int)
    wallets = Set('Wallet')


class Wallet(db.Entity):
    address = Required(str)
    private_key = Required(str)
    owner = Required(User)


try:
    db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
except Exception as Ex:
    print(Ex)
db.generate_mapping(create_tables=True)
set_sql_debug(True)
@db_session
def print_user_name(user_id):
    u = User[user_id]
    print(u.nick)
    # кэш сессии базы данных будет очищен автоматически
    # соединение с базой данных будет возвращено в пул

@db_session
def add_wallet(user_id, address, private_key):
    Wallet(address=address, private_key=private_key, owner=User[user_id])
    # commit() будет выполнен автоматически
    # кэш сессии базы данных будет очищен автоматически
    # соединение с базой данных будет возвращено в пул
