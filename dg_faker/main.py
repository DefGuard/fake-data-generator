import secrets
import base64
from datetime import datetime
from faker import Faker
import sqlalchemy
import click
from tqdm import tqdm


fake = Faker()

USER_QUERY = """
INSERT INTO "user" (
    username, password_hash, last_name, first_name, email, phone
) values (
    '{}', '{}', '{}', '{}', '{}', '{}'
)
"""

# pass123
PASSWORD_HASH = "$argon2id$v=19$m=4096,t=3,p=1$XHgZw2qF/ryF1gOtuLLyZg$AF/Z0EIWk4KGetBSANEnkdK+IcoIWQLjYGuBQjas8SY"

def insert_user(connection):
    profile = fake.simple_profile()
    query = USER_QUERY.format(
        profile['username'],
        PASSWORD_HASH,
        fake.last_name(),
        fake.first_name(),
        profile['mail'],
        fake.phone_number(),
    )
    connection.execute(query)

DEVICE_QUERY = """
INSERT INTO "device" (
    name, wireguard_ip, wireguard_pubkey, user_id, created
) values (
    '{}', '{}', '{}', '{}', '{}'
)
"""


def wg_key():
    key_bytes = secrets.token_bytes(32)
    key_base64 = base64.b64encode(key_bytes)
    return key_base64[:44].decode("utf-8")


def insert_device(connection, user_id: int):
    profile = fake.simple_profile()
    query = DEVICE_QUERY.format(
        profile['username'],
        fake.ipv4(),
        wg_key(),
        user_id,
        datetime.now(),
    )
    connection.execute(query)


def connect_db(url):
    engine = sqlalchemy.create_engine(url)
    return engine.connect()


@click.group()
def cli():
    pass


@click.command("insert-users")
@click.argument("database_url")
@click.option("--count", default=1, help="How many users to insert")
def insert_users(database_url: str, count: int):
    connection = connect_db(database_url)
    for _ in tqdm(range(count)):
        insert_user(connection)


@click.command("insert-devices")
@click.argument("database_url")
@click.option("--count", default=1, help="How many devices to insert")
@click.option("--user-id", help="User for whom devices should be created")
def insert_devices(database_url: str, count: int, user_id: int):
    connection = connect_db(database_url)
    for _ in tqdm(range(count)):
        insert_device(connection, user_id)

cli.add_command(insert_users)
cli.add_command(insert_devices)

if __name__ == "__main__":
    cli()
