from datetime import datetime

from auth.utils import verify_password

from tests.db import InmemorySqlite, init_test_inmemory_sqlite_decorator

import users.crud
from users.models import User
from users.schemas import UserCreate, UserUpdate


db = InmemorySqlite()


@init_test_inmemory_sqlite_decorator(db)
async def test_get_user_by_id():
    session = db.get_session()
    username = 'user'
    email = 'user@example.com'
    password = '123'

    user_data = UserCreate(username=username, email=email, password=password)
    user = await users.crud.create_user(session, user_data)
    user_id = user.id

    user: User = await users.crud.get_user_by_id(session, user_id)

    assert user is not None
    assert user.username == username
    assert user.email == email
    assert verify_password(password, user.password) is True
    assert type(user.is_active) is bool
    assert type(user.create_at) is datetime
    assert type(user.id) is int

    user = await users.crud.get_user_by_id(session, user_id + 1)

    assert user is None

    user2 = await users.crud.get_user_by_id(session, -5)

    assert user2 is None

    await session.close()


@init_test_inmemory_sqlite_decorator(db)
async def test_create_user():
    session = db.get_session()
    username = 'user'
    email = 'user@example.com'
    password = '123'

    user_data = UserCreate(username=username, email=email, password=password)
    user = await users.crud.create_user(session, user_data)

    assert user.username == username
    assert user.email == email
    assert verify_password(password, user.password) is True
    assert user.is_active is True
    assert user.create_at is not None

    user_id = user.id

    assert type(user_id) is int

    user: User = await users.crud.get_user_by_id(session, user_id)

    assert user is not None
    assert user.username == username
    assert user.email == email
    assert verify_password(password, user.password) is True

    await session.close()


@init_test_inmemory_sqlite_decorator(db)
async def test_get_users():
    session = db.get_session()

    user_list = [UserCreate(username=f'user{i}', email=f'user{i}@email.com', password=f'12{i}') for i in range(3)]

    await users.crud.create_user(session, user_list[0])

    res_list = await users.crud.get_users(session)

    assert isinstance(res_list, list)
    assert isinstance(res_list[0], User)

    assert user_list[0].username == res_list[0].username
    assert user_list[0].email == res_list[0].email
    assert verify_password(user_list[0].password, res_list[0].password) is True

    await users.crud.create_user(session, user_list[1])
    await users.crud.create_user(session, user_list[2])

    res_list = await users.crud.get_users(session)

    assert isinstance(res_list, list)

    for i in range(3):
        assert isinstance(res_list[i], User)
        assert user_list[i].username == res_list[i].username
        assert user_list[i].email == res_list[i].email
        assert verify_password(user_list[i].password, res_list[i].password) is True

    await session.close()


@init_test_inmemory_sqlite_decorator(db)
async def test_get_user_by_username():
    session = db.get_session()
    username = 'user'
    email = 'user@example.com'
    password = '123'

    user_data = UserCreate(username=username, email=email, password=password)
    user = await users.crud.create_user(session, user_data)

    user: User = await users.crud.get_user_by_username(session, username)

    assert user is not None
    assert user.username == username
    assert user.email == email
    assert verify_password(password, user.password) is True
    assert type(user.is_active) is bool
    assert type(user.create_at) is datetime
    assert type(user.id) is int

    user = await users.crud.get_user_by_username(session, 'some')

    assert user is None

    user2 = await users.crud.get_user_by_username(session, -5)

    assert user2 is None

    await session.close()


@init_test_inmemory_sqlite_decorator(db)
async def test_get_user_by_email():
    session = db.get_session()
    username = 'user'
    email = 'user@example.com'
    password = '123'

    user_data = UserCreate(username=username, email=email, password=password)
    user = await users.crud.create_user(session, user_data)

    user: User = await users.crud.get_user_by_email(session, email)

    assert user is not None
    assert user.username == username
    assert user.email == email
    assert verify_password(password, user.password) is True
    assert type(user.is_active) is bool
    assert type(user.create_at) is datetime
    assert type(user.id) is int

    user = await users.crud.get_user_by_email(session, 'some')

    assert user is None

    user2 = await users.crud.get_user_by_email(session, -5)

    assert user2 is None

    await session.close()


@init_test_inmemory_sqlite_decorator(db)
async def test_update_user():
    session = db.get_session()
    username = 'user'
    email = 'user@example.com'
    password = '123'

    user_data = UserCreate(username=username, email=email, password=password)
    user = await users.crud.create_user(session, user_data)

    update_data = UserUpdate(username='user2', email='user2@example.com')

    updated_user = await users.crud.update_user(session, user, update_data)

    assert isinstance(updated_user, User)
    assert updated_user.username == update_data.username
    assert updated_user.email == update_data.email
    assert verify_password(password, updated_user.password) is True
    assert user.is_active == updated_user.is_active
    assert user.create_at == updated_user.create_at
    assert user.id == updated_user.id

    await session.close()


@init_test_inmemory_sqlite_decorator(db)
async def test_delete_user():
    session = db.get_session()
    username = 'user'
    email = 'user@example.com'
    password = '123'

    user_data = UserCreate(username=username, email=email, password=password)
    user = await users.crud.create_user(session, user_data)

    res_list = await users.crud.get_users(session)

    assert len(res_list) > 0

    await users.crud.delete_user(session, user)

    res_list = await users.crud.get_users(session)

    assert len(res_list) == 0

    await session.close()
